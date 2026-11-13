"""Experiment 223: micro copper London-to-US industrial demand handoff.
Mechanism: Asian/London industrial price discovery carries into COMEX when US hedgers
join. MHG reduces execution cost. Falsifier: stressed PnL <=0 or any era <=0.
"""
import numpy as np
FAMILY='metals-microcopper-london-us-industrial-handoff'
PARAMS={'observe_ct_sec':21600,'entry_ct_sec':30600,'exit_ct_sec':37800,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='MHG':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==21600];y=g[t[g]==30600]
    if len(x)and len(y):o[g[(t[g]>=30600)&(t[g]<37800)]]=int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
