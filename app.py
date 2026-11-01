"""Local-only SC2 replay prototype; no external upload or LLM calls."""
import io,json,time,urllib.request,urllib.error
from pathlib import Path
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
import sc2reader
ROOT=Path(__file__).parent

def parse(blob):
    r=sc2reader.load_replay(io.BytesIO(blob),load_level=4)
    fps=22.4 if r.build>=34784 else 16
    if len(r.players)!=2 or not r.tracker_events:
        raise ValueError('目前支援有 tracker 資料的 1v1 RP')
    players=[dict(id=p.pid,name=p.name,race=p.play_race,result=p.result) for p in r.players]
    series={p.pid:[] for p in r.players}; timeline=[]
    for e in r.tracker_events:
        t=round(e.frame/fps,1);name=e.name
        if name=='PlayerStatsEvent' and e.pid in series:
            series[e.pid].append(dict(t=t,minerals=e.minerals_current,gas=e.vespene_current,workers=e.workers_active_count,supply=e.food_used,cap=e.food_made,mineralIncome=e.minerals_collection_rate,gasIncome=e.vespene_collection_rate,army=e.minerals_used_current_army+e.vespene_used_current_army,lost=e.minerals_lost_army+e.vespene_lost_army))
        elif name=='UpgradeCompleteEvent' and not e.upgrade_type_name.lower().startswith(('spray','reward','skin','emote','banner','taunt')):
            timeline.append(dict(t=t,pid=e.pid,kind='科技完成',label=e.upgrade_type_name))
        elif name in ('UnitInitEvent','UnitDoneEvent','UnitTypeChangeEvent','UnitBornEvent'):
            u=e.unit;pid=getattr(getattr(u,'owner',None),'pid',None)
            pid=getattr(e,'control_pid',pid)
            historical=[typ for frame,typ in getattr(u,'type_history',{}).items() if frame<=e.frame]
            label=getattr(e,'unit_type_name',None) or (historical[-1].name if historical else 'Unknown')
            if (name=='UnitInitEvent' and getattr(u,'is_building',False)) or (name=='UnitDoneEvent' and getattr(u,'is_building',False)) or (name=='UnitTypeChangeEvent' and label in ('Lair','Hive','GreaterSpire')) or (name=='UnitBornEvent' and label in ('Queen','Infestor','Viper','LurkerMP','Ultralisk','BroodLord','Mutalisk','Corruptor')):
                timeline.append(dict(t=t,pid=pid,kind='建造指令／開始' if name=='UnitInitEvent' else ('建築完成' if name=='UnitDoneEvent' else '單位／形態'),label=label))
    return dict(map=r.map_name,version=r.release_string,duration=round(r.frames/fps),players=players,series=series,timeline=timeline,source='真實 RP 解析',limitations=['資源與人口是定期快照，不是逐幀狀態。','建造開始、科技完成分開呈現；不是所有單位都有開始事件。','暫不評分注卵、蟲苔覆蓋、偵查視野或站位；不能靠指令數直接判定失誤。'])

class Handler(BaseHTTPRequestHandler):
    def send(self,status,data,ctype='application/json; charset=utf-8'):
        payload=json.dumps(data,ensure_ascii=False).encode() if isinstance(data,(dict,list)) else data
        self.send_response(status);self.send_header('Content-Type',ctype);self.send_header('Content-Length',str(len(payload)));self.end_headers();self.wfile.write(payload)
    def do_GET(self):
        if self.path=='/api/live':
            try:
                with urllib.request.urlopen('http://127.0.0.1:6119/game',timeout=1) as f:game=json.load(f)
                self.send(200,dict(connected=True,game=game))
            except Exception:self.send(200,dict(connected=False,message='未連接 SC2；可手動選對戰種族，或匯入 RP。'))
        elif self.path=='/api/sample':
            p=ROOT/'sample.json'
            self.send(200,p.read_bytes()) if p.exists() else self.send(404,dict(error='尚無樣本'))
        elif self.path in ('/','/index.html'):
            self.send(200,(ROOT/'index.html').read_bytes(),'text/html; charset=utf-8')
        else:self.send(404,dict(error='Not found'))
    def do_POST(self):
        if self.path!='/api/replay':return self.send(404,dict(error='Not found'))
        if self.headers.get('Origin') not in (None,'http://127.0.0.1:8773','http://localhost:8773'):return self.send(403,dict(error='Local requests only'))
        try:
            n=int(self.headers.get('Content-Length','0'))
            if not 0<n<=50*1024*1024:return self.send(413,dict(error='檔案大小須小於 50 MB'))
            result=parse(self.rfile.read(n));self.send(200,result)
        except Exception as e:self.send(422,dict(error='無法解析這份 RP，可能是版本不支援或檔案不完整。',detail=type(e).__name__))

if __name__=='__main__':
    print('蟲族對局筆記 http://127.0.0.1:8773',flush=True)
    ThreadingHTTPServer(('127.0.0.1',8773),Handler).serve_forever()
