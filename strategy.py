"""Experiment 236: gasoline inventory low-volatility breakout.
Mechanism: a quiet pre-release RB market stores inventory uncertainty; weekly inventory
report resolves it and initial repricing persists. Causal 20-session pre-open range norm.
Falsifier PnL/era<=0.
"""
import numpy as np,pandas as pd
FAMILY='energy-gasoline-inventory-lowvolatility-breakout'
PARAMS={'range_start_ct_sec':25200,'open_ct_sec':30600,'entry_ct_sec':32400,'exit_ct_sec':39600,'lookback_sessions':20,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='RB':
   c,h,l,t=d.close.to_numpy(),d.high.to_numpy(),d.low.to_numpy(),d.ct_sec.to_numpy();gs=list(d.groupby('session',sort=False).indices.values());dt=pd.to_datetime(d.session.iloc[[g[0] for g in gs]].astype(str).str[:10]);r=[]
   for k,g in enumerate(gs):
    q=g[(t[g]>=25200)&(t[g]<30600)];v=h[q].max()-l[q].min() if len(q)else 0.;r.append(v);x=g[t[g]==30600];y=g[t[g]==32400]
    if k>=20 and len(x)and len(y)and dt.iloc[k].weekday()==2 and v<np.median(r[k-20:k]):o[g[(t[g]>=32400)&(t[g]<39600)]]=int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
