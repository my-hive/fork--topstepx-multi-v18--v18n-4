"""Experiment 206: S&P pension-rebalance drawdown hedge reversal.
Mechanism: five consecutive down sessions create pension-rebalance inventory hedge demand;
Monday US physical liquidity reverses pressure. Independent economic audit of peer premise.
Falsifier PnL/era<=0.
"""
import numpy as np,pandas as pd
FAMILY='energy-heatingoil-monday-drawdown-pension-rebalance-reversal'
PARAMS={'lookback_sessions':5,'entry_ct_sec':36000,'exit_ct_sec':50400,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='MES':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();gs=list(d.groupby('session',sort=False).indices.values());r=np.array([c[g[-1]]-c[g[0]] for g in gs]);dt=pd.to_datetime(d.session.iloc[[g[0] for g in gs]].astype(str).str[:10])
   for k in range(5,len(gs)):
    if dt.iloc[k].weekday()==0 and np.all(r[k-5:k]<0):
     g=gs[k];o[g[(t[g]>=36000)&(t[g]<50400)]]=1
  a[s]=o
 return a
