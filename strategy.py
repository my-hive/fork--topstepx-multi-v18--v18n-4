"""Experiment 286: RBNZ-proxy NZD liquidity continuation.
Mechanism: policy repricing propagates through NZD carry hedges in Asia liquidity.
Falsifier: primary zero, any era loss, risk breach, or inadequate years.
"""
import numpy as np
import pandas as pd
FAMILY='fx-nzd-rbnz-decision-liquidity-continuation'
PARAMS={'observe_ct_sec':72000,'entry_ct_sec':73800,'exit_ct_sec':82800,'risk_dollars':250}
def entry_risk(p): return {s:np.full(len(d),250.,dtype=float) for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='6N':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dt=pd.to_datetime(d.session.astype(str).str[:10]);wd=dt.dt.weekday.to_numpy()
   event=((wd==2)&dt.dt.day.between(8,14)).to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==72000];y=g[t[g]==73800]
    if len(x) and len(y) and event[g[0]]:
     o[g[(t[g]>=73800)&(t[g]<82800)]]=int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
