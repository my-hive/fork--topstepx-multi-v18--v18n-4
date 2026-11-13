"""Experiment 194: Nasdaq Friday overnight-gap institutional flow.
Mechanism: weekly fund positioning and option hedges accumulated overnight create Friday
cash-open gap; broad-index basket execution continues initial direction into morning.
Different information window from opening-imbalance flow. Falsifier PnL/era/primary<=0.
"""
import numpy as np,pandas as pd
FAMILY='equity-micro-nasdaq-friday-overnight-gap-flow'
PARAMS={'observe_ct_sec':7200,'entry_ct_sec':30600,'exit_ct_sec':46800,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='MNQ':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();f=(pd.to_datetime(d.session.astype(str).str[:10]).dt.weekday==4).to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==7200];y=g[t[g]==30600]
    if len(x)and len(y)and f[g[0]]:o[g[(t[g]>=30600)&(t[g]<46800)]]=int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
