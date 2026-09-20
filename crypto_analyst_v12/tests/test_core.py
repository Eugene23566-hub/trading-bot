import unittest
from crypto_analyst.indicators import ema,rsi,atr
from crypto_analyst.paper import derive_order,pnl_for
class CoreTests(unittest.TestCase):
    def test_ema(self): self.assertAlmostEqual(ema([1,2,3],2)[-1],2.5555555555555554)
    def test_rsi_up(self): self.assertEqual(rsi(list(range(1,30))),100.0)
    def test_atr(self):
        h=[11+i for i in range(20)]; l=[9+i for i in range(20)]; c=[10+i for i in range(20)]
        self.assertAlmostEqual(atr(h,l,c),2.0)
    def test_risk_sizing_long(self):
        f={"symbol":"TESTUSDT","price":100.0,"atr_15m":2.0,"recent_low_3h":97.0,"recent_high_3h":104.0}; o=derive_order(f,"LONG",10000,0.005,10000)
        self.assertIsNotNone(o); self.assertLessEqual(o["risk_usdt"],50.000001); self.assertAlmostEqual(o["target"]-o["entry"],2*(o["entry"]-o["stop"]),places=8)
    def test_pnl(self):
        pnl,r=pnl_for({"side":"LONG","qty":10,"entry":100,"risk_usdt":50},105); self.assertEqual(pnl,50); self.assertEqual(r,1)
if __name__=="__main__": unittest.main()
