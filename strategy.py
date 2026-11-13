"""Experiment 260: Ten-year auction concession reversal.
Mechanism: pre-auction duration concession reverses after demand absorbs dealer inventory.
Falsifier: primary zero, any era loss, risk breach, or inadequate years.
"""
import numpy as np
import pandas as pd
FAMILY='rates-tenyear-auction-concession-reversal'
PARAMS={'observe_ct_sec':30600,'entry_ct_sec':43200,'exit_ct_sec':50400,'risk_dollars':250}
def entry_risk(p): return {s:np.full(len(d),250.,dtype=float) for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='ZN':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dt=pd.to_datetime(d.session.astype(str).str[:10]);wd=dt.dt.weekday.to_numpy()
   event=((wd==2)&dt.dt.day.between(8,14)).to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==30600];y=g[t[g]==43200]
    if len(x) and len(y) and event[g[0]]:
     o[g[(t[g]>=43200)&(t[g]<50400)]]=-int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
