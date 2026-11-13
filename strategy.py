"""Experiment 256: Thanksgiving-eve S&P dealer de-risking continuation.
Mechanism: pre-holiday institutional de-risking in thin liquidity amplifies opening flow.
Falsifier: primary zero, any era loss, risk breach, or inadequate years.
"""
import numpy as np
import pandas as pd
FAMILY='index-thanksgiving-eve-dealer-derisking-continuation'
PARAMS={'open_ct_sec':30600,'entry_ct_sec':32400,'exit_ct_sec':50400,'risk_dollars':250}
def entry_risk(p): return {s:np.full(len(d),250.,dtype=float) for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='MES':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy(); dt=pd.to_datetime(d.session.astype(str).str[:10])
   # Fourth Thursday in November; Wednesday immediately preceding.
   tomorrow=dt+pd.Timedelta(days=1)
   event=((dt.dt.month==11)&(dt.dt.weekday==2)&(tomorrow.dt.month==11)&(tomorrow.dt.weekday==3)&tomorrow.dt.day.between(22,28)).to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==30600]; y=g[t[g]==32400]
    if len(x) and len(y) and event[g[0]]:
     o[g[(t[g]>=32400)&(t[g]<50400)]]=int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
