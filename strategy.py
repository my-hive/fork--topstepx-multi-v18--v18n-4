"""Experiment 357: BoC CAD policy liquidity reversal.
Mechanism: policy repricing overshoots before exporter hedges absorb liquidity.
Falsifier: primary zero, any era loss, risk breach, or inadequate years.
"""
import numpy as np
import pandas as pd
FAMILY='fx-cad-boc-policy-liquidity-reversal'
PARAMS={'observe_ct_sec':32400,'entry_ct_sec':34200,'exit_ct_sec':39600,'risk_dollars':250}
def entry_risk(p): return {s:np.full(len(d),250.,dtype=float) for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='6C':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dt=pd.to_datetime(d.session.astype(str).str[:10]);wd=dt.dt.weekday.to_numpy();event=(dt.dt.day.between(8,14)&(wd==2)).to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==32400];y=g[t[g]==34200]
    if len(x) and len(y) and event[g[0]]: o[g[(t[g]>=34200)&(t[g]<39600)]]=-int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
