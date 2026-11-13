"""Experiment 200: time-diversified Friday micro-index basket portfolio.
Mechanism: Friday ETF/basket imbalance first moves MNQ during opening constituent execution,
then broader MES flow persists into delayed institutional allocation. Distinct time windows
reduce shared intraday path while retaining same documented weekly flow cause.
Falsifier: primary zero, era loss, risk breach, or inadequate years.
"""
import numpy as np,pandas as pd
FAMILY='index-micro-friday-basket-time-diversified-portfolio'
PARAMS={'open_ct_sec':30600,'signal_end_ct_sec':32400,'mes_entry_ct_sec':36000,'mnq_exit_ct_sec':50400,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64);c,t=d.close.to_numpy(),d.ct_sec.to_numpy();f=(pd.to_datetime(d.session.astype(str).str[:10]).dt.weekday==4).to_numpy()
  if s in ('MES','MNQ'):
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==30600];y=g[t[g]==32400]
    if len(x)and len(y)and f[g[0]]:
     start=36000 if s=='MES' else 32400
     o[g[(t[g]>=start)&(t[g]<50400)]]=int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
