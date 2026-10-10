import random,math
def backtest(prices,window=10,cost_bps=10):
    if not isinstance(window,int) or window<2 or window>=len(prices):raise ValueError('Invalid window')
    if not 0<=cost_bps<=1000 or any(not math.isfinite(p) or p<=0 for p in prices):raise ValueError('Invalid price or cost')
    equity=1.;peak=1.;drawdown=0.;previous=0;curve=[1.];trades=0
    for t in range(1,len(prices)):
        # Position for interval t-1 to t uses ONLY data through t-1.
        position=int(t>=window and prices[t-1]>sum(prices[t-window:t])/window)
        turnover=abs(position-previous);trades+=turnover
        equity*=1+position*(prices[t]/prices[t-1]-1)-turnover*cost_bps/10000
        peak=max(peak,equity);drawdown=max(drawdown,1-equity/peak);curve.append(equity);previous=position
    if previous:equity*=1-cost_bps/10000;curve[-1]=equity;trades+=1;drawdown=max(drawdown,1-equity/peak)
    return {'strategy_return':equity-1,'buy_hold_return':prices[-1]/prices[0]-1,'max_drawdown':drawdown,'trades':trades,'curve':curve}
def run(p):
    rng=random.Random(int(p.get('seed',42)));prices=[100.]
    for _ in range(119):prices.append(prices[-1]*math.exp(rng.gauss(.001,.025)))
    result=backtest(prices,int(p.get('window',10)),float(p.get('cost_bps',10)))
    return {**result,'prices':prices,'note':'Synthetic educational backtest, no broker connection or investment recommendation.'}
