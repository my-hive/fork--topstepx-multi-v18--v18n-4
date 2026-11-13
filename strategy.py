"""Experiment 266: CME Bitcoin weekend-gap continuation.
Mechanism: weekend spot discovery transfers into CME reopening hedge execution.
Falsifier: primary zero, any era loss, risk breach, or inadequate years.
"""
import numpy as np
import pandas as pd
FAMILY='crypto-bitcoin-cme-weekend-gap-continuation'
PARAMS={'observe_ct_sec':0,'entry_ct_sec':21600,'exit_ct_sec':43200,'risk_dollars':250}
def entry_risk(p): return {s:np.full(len(d),250.,dtype=float) for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='MBT':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dt=pd.to_datetime(d.session.astype(str).str[:10]);wd=dt.dt.weekday.to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==0];y=g[t[g]==21600]
    if len(x) and len(y) and wd[g[0]]==0:
     o[g[(t[g]>=21600)&(t[g]<43200)]]=int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
