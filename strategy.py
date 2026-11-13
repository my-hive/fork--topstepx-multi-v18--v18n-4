"""Experiment 192: MNQ Friday opening-flow clean-room.
Mechanism: weekly ETF and basket rebalancing create Friday cash-open imbalance;
completed first half-hour move continues as constituents execute. Micro cost is compatible.
Falsifier: nonpositive primary, any era loss, inadequate years, or risk breach.
"""
import numpy as np,pandas as pd
FAMILY='equity-micro-index-friday-basket-flow-capacity-audit'
PARAMS={'open_ct_sec':30600,'entry_ct_sec':32400,'exit_ct_sec':50400,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s in ('MNQ','MES'):
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();f=(pd.to_datetime(d.session.astype(str).str[:10]).dt.weekday==4).to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==30600];y=g[t[g]==32400]
    if len(x)and len(y)and f[g[0]]:o[g[(t[g]>=32400)&(t[g]<50400)]]=int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
