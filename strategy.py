"""Experiment 358: BOJ proxy Nikkei liquidity reversal.
Mechanism: policy repricing overextends initial Nikkei flow before local hedger absorption.
Falsifier: primary zero, any era loss, risk breach, or inadequate years.
"""
import numpy as np
import pandas as pd
FAMILY='index-nikkei-boj-policy-liquidity-reversal'
PARAMS={'observe_ct_sec':68400,'entry_ct_sec':70200,'exit_ct_sec':79200,'risk_dollars':250}
def entry_risk(p): return {s:np.full(len(d),250.,dtype=float) for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='NKD':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dt=pd.to_datetime(d.session.astype(str).str[:10]);wd=dt.dt.weekday.to_numpy();event=(dt.dt.month.isin([3,6,9,12])&dt.dt.day.between(15,21)&(wd==3)).to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==68400];y=g[t[g]==70200]
    if len(x) and len(y) and event[g[0]]: o[g[(t[g]>=70200)&(t[g]<79200)]]=-int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
