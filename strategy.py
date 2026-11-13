"""Experiment 225: five-year auction concession reversal.
Mechanism: dealer balance-sheet concession before monthly five-year Treasury supply
reverses after auction allocation as short-covering occurs. Third-week Wednesday proxy.
Falsifier: stressed PnL <=0 or any era <=0.
"""
import numpy as np,pandas as pd
FAMILY='rates-fiveyear-auction-concession-continuation'
PARAMS={'observe_ct_sec':34200,'entry_ct_sec':36000,'exit_ct_sec':46800,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='ZF':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dt=pd.to_datetime(d.session.astype(str).str[:10]);on=((dt.dt.weekday==2)&dt.dt.day.between(22,28)).to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==34200];y=g[t[g]==36000]
    if len(x)and len(y)and on[g[0]]:o[g[(t[g]>=36000)&(t[g]<46800)]]=int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
