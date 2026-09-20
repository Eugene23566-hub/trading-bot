from statistics import mean
def ema(values, period):
    if not values: return []
    a=2.0/(period+1.0); out=[values[0]]
    for v in values[1:]: out.append(a*v+(1-a)*out[-1])
    return out
def rsi(values, period=14):
    if len(values)<=period: return None
    gains=[]; losses=[]
    for a,b in zip(values[-period-1:-1],values[-period:]):
        d=b-a; gains.append(max(d,0)); losses.append(max(-d,0))
    ag=mean(gains); al=mean(losses)
    if al==0: return 100.0
    rs=ag/al; return 100-(100/(1+rs))
def macd(values):
    if len(values)<35: return None,None,None
    fast=ema(values,12); slow=ema(values,26); line=[f-s for f,s in zip(fast,slow)]; signal=ema(line,9)
    return line[-1],signal[-1],line[-1]-signal[-1]
def atr(highs,lows,closes,period=14):
    if len(closes)<=period: return None
    trs=[max(highs[i]-lows[i],abs(highs[i]-closes[i-1]),abs(lows[i]-closes[i-1])) for i in range(1,len(closes))]
    return mean(trs[-period:])
def volume_ratio(volumes,period=20):
    if len(volumes)<period+1: return None
    baseline=mean(volumes[-period-1:-1]); return volumes[-1]/baseline if baseline else None
