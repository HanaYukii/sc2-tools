import unittest
from pathlib import Path
from app import parse
class ReplayTests(unittest.TestCase):
 def test_real_replay(self):
  d=parse(next((Path(__file__).parent / 'samples').glob('*.SC2Replay')).read_bytes())
  self.assertEqual(len(d['players']),2)
  self.assertTrue(any(p['race']=='Zerg' for p in d['players']))
  self.assertGreater(len(d['series'][1]),50)
  self.assertTrue(all(0<=s['t']<=d['duration']+1 for rows in d['series'].values() for s in rows))
  self.assertFalse(any(e['label'].startswith(('Spray','Reward')) for e in d['timeline']))
  self.assertTrue(any(e['kind']=='建築完成' for e in d['timeline']))
 def test_invalid_replay(self):
  with self.assertRaises(Exception):parse(b'not a replay')
if __name__=='__main__':unittest.main()
