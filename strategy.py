"""Experiment 255: Quarterly index-option expiry opening imbalance continuation.
Mechanism: quarterly index-option expiry dealer hedging causes opening imbalance to
persist while expiry-related unwind flows execute.
Falsifier: primary zero, any era loss, risk breach, or inadequate years.
"""
import numpy as np
import pandas as pd
FAMILY='index-micro-quarterly-expiry-opening-imbalance-continuation'
PARAMS={'open_ct_sec':30600,'entry_ct_sec':32400,'exit_ct_sec':43200,'risk_dollars':250}
def entry_risk(p): return {s:np.full(len(d),250.,dtype=float) for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='MNQ':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
   dt=pd.to_datetime(d.session.astype(str).str[:10])
   expiry=(dt.dt.month.isin([3,6,9,12])&(dt.dt.weekday==4)&dt.dt.day.between(15,21)).to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==30600]; y=g[t[g]==32400]
    if len(x) and len(y) and expiry[g[0]]:
     o[g[(t[g]>=32400)&(t[g]<43200)]]=int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
