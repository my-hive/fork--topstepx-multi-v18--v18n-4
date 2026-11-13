"""Experiment 308: Month-end JPY fixing-liquidity reversal.
Mechanism: corporate fixing hedges overextend JPY liquidity before normal flow.
Falsifier: primary zero, any era loss, risk breach, or inadequate years.
"""
import numpy as np
import pandas as pd
FAMILY='fx-yen-monthend-fixing-liquidity-reversal'
PARAMS={'observe_ct_sec':7200,'entry_ct_sec':9000,'exit_ct_sec':18000,'risk_dollars':250}
def entry_risk(p): return {s:np.full(len(d),250.,dtype=float) for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='6J':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dt=pd.to_datetime(d.session.astype(str).str[:10])
   event=dt.dt.day.between(28,31).to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==7200];y=g[t[g]==9000]
    if len(x) and len(y) and event[g[0]]:
     o[g[(t[g]>=9000)&(t[g]<18000)]]=-int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
