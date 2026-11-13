"""Experiment 205: Friday basket flow plus daily close hedge flow.
Mechanism: Friday opening ETF basket imbalance and daily closing dealer hedging are
separate institutional execution windows. MNQ can carry both without simultaneous risk.
Falsifier: primary zero, era loss, risk breach, or inadequate years.
"""
import numpy as np,pandas as pd
FAMILY='index-micro-friday-basket-plus-close-hedge-portfolio'
PARAMS={'open_ct_sec':30600,'open_end_ct_sec':32400,'close_start_ct_sec':48600,'close_entry_ct_sec':50400,'close_exit_ct_sec':54000,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='MNQ':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();f=(pd.to_datetime(d.session.astype(str).str[:10]).dt.weekday==4).to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==30600];y=g[t[g]==32400]
    if len(x)and len(y)and f[g[0]]:o[g[(t[g]>=32400)&(t[g]<50400)]]=int(np.sign(c[y[0]]-c[x[0]]))
    x=g[t[g]==48600];y=g[t[g]==50400]
    if len(x)and len(y):o[g[(t[g]>=50400)&(t[g]<54000)]]=int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
