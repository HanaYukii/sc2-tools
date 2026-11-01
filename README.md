# SC2 蟲族對局筆記

給 3600 → 4000 練習用的流程速查與本地 RP 復盤雛形。

- **流程表**：ZvT／ZvP／ZvZ，裸雙到三開、氣礦配工、毒爆巢、攻防與科技銜接。
- **決策提醒**：依對局展開，練習窗口配合偵查調整。
- **RP 復盤**：雙方工兵、資源、人口、軍隊價值，以及建築／科技時間軸。
- **最多三個回看入口**：浮礦、軍隊損失、科技銜接；不直接判成失誤。

## 啟動

需要 Python 3.12。第一次先安裝依賴。

macOS：

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python launch.py
```

Windows（PowerShell）：

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe launch.py
```

之後可雙擊 `開啟蟲族筆記.command`（Mac）或 `開啟蟲族筆記.cmd`（Windows）。
瀏覽器開啟 http://127.0.0.1:8773/ 。服務留在背景；若需直接控制啟停，用同一個 Python 執行 `app.py`，按 Ctrl+C 停止。

## 目前範圍

- 只在本機解析 RP，不上傳、不呼叫 LLM；先支援含 tracker 的 1v1。
- 資源與人口是定期快照；建造開始與科技完成分開顯示。
- 尚未分析注卵效率、完整蟲苔、視野或交戰站位。
- 有 localhost:6119/game 連線探測，但尚未實測 SC2 客戶端；對局種族手動切換，沒有 MMR 查詢。
- 流程時間為研究整理的練習基準，不是每場硬性門檻。來源可在各流程表下方展開。
- RP 解析可能受遊戲版本影響；目前以公開 5.0.15 樣本驗證。單位名稱仍有部分英文。

## 驗證

```sh
python -m unittest -v
```

請使用已安裝依賴的 Python。已在 macOS arm64／Python 3.12 驗證解析；Windows 啟動與實際遊戲連線尚待測試。

公開 RP 樣本來自 [sc2reader](https://github.com/ggtracker/sc2reader)，不是使用者對局，也不是程度比較標準。來源及授權見 [samples/README.md](samples/README.md)。

## 結構

- `app.py`：本地 HTTP API 與 replay parser。
- `index.html`：流程速查與復盤介面。
- `launch.py`：本地啟動器。
- `sample.json`：公開 RP 的預先解析結果。

技術參考：[s2protocol](https://github.com/Blizzard/s2protocol)、[sc2reader](https://github.com/ggtracker/sc2reader)、[s2client-proto](https://github.com/Blizzard/s2client-proto)。
