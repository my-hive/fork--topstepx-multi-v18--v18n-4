"""Experiment 311: Nasdaq June reconstitution close continuation.
Mechanism: Russell reconstitution spills into Nasdaq closing auction execution.
Falsifier: primary zero, any era loss, risk breach, or inadequate years.
"""
import numpy as np
import pandas as pd
FAMILY='index-nasdaq-june-reconstitution-close-continuation'
PARAMS={'observe_ct_sec':50400,'entry_ct_sec':52200,'exit_ct_sec':54000,'risk_dollars':250}
def entry_risk(p): return {s:np.full(len(d),250.,dtype=float) for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='MNQ':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dt=pd.to_datetime(d.session.astype(str).str[:10]);wd=dt.dt.weekday.to_numpy()
   event=(dt.dt.month.eq(6)&dt.dt.day.between(22,28)&(wd==4)).to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==50400];y=g[t[g]==52200]
    if len(x) and len(y) and event[g[0]]:
     o[g[(t[g]>=52200)&(t[g]<54000)]]=int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
