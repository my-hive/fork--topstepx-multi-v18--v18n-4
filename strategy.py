"""Experiment 163: payroll-week Treasury duration demand.
Mechanism: employment data reprices policy path; rate futures hedge flow builds into first
Friday and carries through US cash session. Follow pre-open ZN impulse on first Friday.
Falsifier: PnL <=0 or any era <=0.
"""
import numpy as np,pandas as pd
FAMILY='rates-payroll-week-duration-continuation'
PARAMS={'observe_ct_sec':28800,'entry_ct_sec':30600,'exit_ct_sec':39600,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='ZN':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dt=pd.to_datetime(d.session.astype(str).str[:10]);on=((dt.dt.weekday==4)&(dt.dt.day<=7)).to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==28800];y=g[t[g]==30600]
    if len(x)and len(y)and on[g[0]]:o[g[(t[g]>=30600)&(t[g]<39600)]]=int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
