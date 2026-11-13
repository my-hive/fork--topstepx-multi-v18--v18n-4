"""Experiment 215: Treasury weekend duration-gap continuation.
Mechanism: Friday late duration positioning signals unresolved weekend macro/risk demand;
Monday cash bond participation extends it. Prior Friday completed-session direction only.
Falsifier: stressed PnL <=0 or any era <=0.
"""
import numpy as np,pandas as pd
FAMILY='rates-treasury-weekend-duration-gap-continuation'
PARAMS={'entry_ct_sec':30600,'exit_ct_sec':43200,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='ZN':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();gs=list(d.groupby('session',sort=False).indices.values());dt=pd.to_datetime(d.session.iloc[[g[0] for g in gs]].astype(str).str[:10]);r=np.array([c[g[-1]]-c[g[0]] for g in gs])
   for k in range(1,len(gs)):
    if dt.iloc[k].weekday()==0:
     g=gs[k];o[g[(t[g]>=30600)&(t[g]<43200)]]=int(np.sign(r[k-1]))
  a[s]=o
 return a
