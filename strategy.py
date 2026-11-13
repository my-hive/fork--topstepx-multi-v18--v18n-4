"""Experiment 373: BoE sterling liquidity reversal.
Mechanism: policy repricing overshoots before London interbank hedge absorption.
Falsifier: primary zero, any era loss, risk breach, or inadequate years.
"""
import numpy as np
import pandas as pd
FAMILY='fx-sterling-boe-policy-liquidity-reversal'
PARAMS={'observe_ct_sec':21600,'entry_ct_sec':23400,'exit_ct_sec':32400,'risk_dollars':250}
def entry_risk(p): return {s:np.full(len(d),250.,dtype=float) for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='6B':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dt=pd.to_datetime(d.session.astype(str).str[:10]);wd=dt.dt.weekday.to_numpy();event=(dt.dt.day.between(1,7)&(wd==3)).to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==21600];y=g[t[g]==23400]
    if len(x) and len(y) and event[g[0]]: o[g[(t[g]>=23400)&(t[g]<32400)]]=-int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
