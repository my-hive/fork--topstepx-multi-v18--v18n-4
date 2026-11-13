"""Experiment 196: M2K Friday basket-flow delayed entry.
Mechanism: weekly basket opening imbalance remains while component orders complete, but
entry after first-hour auction noise may avoid stop churn. Same causal first half-hour sign.
Falsifier: nonpositive primary, era loss, years/risk failure.
"""
import numpy as np,pandas as pd
FAMILY='equity-micro-russell-friday-basket-flow-delayed-entry'
PARAMS={'open_ct_sec':30600,'signal_end_ct_sec':32400,'entry_ct_sec':36000,'exit_ct_sec':50400,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='M2K':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();f=(pd.to_datetime(d.session.astype(str).str[:10]).dt.weekday==4).to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==30600];y=g[t[g]==32400]
    if len(x)and len(y)and f[g[0]]:o[g[(t[g]>=36000)&(t[g]<50400)]]=int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
