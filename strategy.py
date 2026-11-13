"""Experiment 165: inflation-month gold real-rate hedge continuation.
Mechanism: CPI/PCE inflation repricing motivates sustained real-rate hedge demand in gold;
first 08:30 response in monthly inflation-release window continues through US morning.
Proxy known: days 10-16 of month. Falsifier: PnL <=0 or era <=0.
"""
import numpy as np,pandas as pd
FAMILY='metals-gold-inflation-window-realrate-hedge-continuation'
PARAMS={'open_ct_sec':30600,'entry_ct_sec':32400,'exit_ct_sec':39600,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='GC':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();on=pd.to_datetime(d.session.astype(str).str[:10]).dt.day.between(10,16).to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==30600];y=g[t[g]==32400]
    if len(x)and len(y)and on[g[0]]:o[g[(t[g]>=32400)&(t[g]<39600)]]=int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
