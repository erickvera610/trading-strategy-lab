import unittest
from core import backtest,run
class Tests(unittest.TestCase):
    def test_constant(self):self.assertEqual(backtest([100]*20)['strategy_return'],0)
    def test_cost(self):self.assertLess(backtest(list(range(100,130)),cost_bps=50)['strategy_return'],backtest(list(range(100,130)),cost_bps=0)['strategy_return'])
    def test_no_future_signal(self):self.assertEqual(backtest([100,100,100,200],window=2)['strategy_return'],0)
    def test_invalid(self):
        with self.assertRaises(ValueError):backtest([1,0,2,3],2)
    def test_seed(self):self.assertEqual(run({'seed':9}),run({'seed':9}))
