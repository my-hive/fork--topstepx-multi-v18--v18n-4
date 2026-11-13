"""Experiment 338: Thanksgiving-week micro-crude liquidity reversal.
Mechanism: thin holiday liquidity overextends crude opening flow before hedgers return.
Falsifier: primary zero, any era loss, risk breach, or inadequate years.
"""
import numpy as np
import pandas as pd
FAMILY='energy-crude-thanksgiving-week-liquidity-reversal'
PARAMS={'observe_ct_sec':25200,'entry_ct_sec':30600,'exit_ct_sec':39600,'risk_dollars':250}
def entry_risk(p): return {s:np.full(len(d),250.,dtype=float) for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='MCL':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dt=pd.to_datetime(d.session.astype(str).str[:10])
   event=(dt.dt.month.eq(11)&dt.dt.day.between(22,28)).to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==25200];y=g[t[g]==30600]
    if len(x) and len(y) and event[g[0]]:
     o[g[(t[g]>=30600)&(t[g]<39600)]]=-int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
