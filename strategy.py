"""Experiment 321: Payroll micro-gold real-rate reversal.
Mechanism: payroll rate shock overextends gold hedge flow before liquidity normalizes.
Falsifier: primary zero, any era loss, risk breach, or inadequate years.
"""
import numpy as np
import pandas as pd
FAMILY='metals-microgold-payroll-realrate-reversal'
PARAMS={'observe_ct_sec':28800,'entry_ct_sec':30600,'exit_ct_sec':39600,'risk_dollars':250}
def entry_risk(p): return {s:np.full(len(d),250.,dtype=float) for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='MGC':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dt=pd.to_datetime(d.session.astype(str).str[:10]);wd=dt.dt.weekday.to_numpy()
   event=((wd==4)&dt.dt.day.between(1,7)).to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==28800];y=g[t[g]==30600]
    if len(x) and len(y) and event[g[0]]:
     o[g[(t[g]>=30600)&(t[g]<39600)]]=-int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
