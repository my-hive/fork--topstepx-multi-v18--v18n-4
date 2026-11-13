"""Experiment 248: three-index FOMC hedging capacity audit.
Mechanism: FOMC shock compels duration-sensitive equity hedging across S&P, Nasdaq and
Dow; same post-statement rule tests risk-limited aggregate execution capacity.
Falsifier: primary zero, era loss, risk breach, or inadequate years.
"""
import numpy as np,pandas as pd
FAMILY='index-micro-threeindex-fomc-hedge-capacity-audit'
PARAMS={'observe_ct_sec':50400,'entry_ct_sec':51000,'exit_ct_sec':54000,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s in ('MES','MNQ','MYM'):
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dt=pd.to_datetime(d.session.astype(str).str[:10]);on=(dt.dt.month.isin([3,6,9,12])&(dt.dt.weekday==2)&dt.dt.day.between(15,21)).to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==50400];y=g[t[g]==51000]
    if len(x)and len(y)and on[g[0]]:o[g[(t[g]>=51000)&(t[g]<54000)]]=int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
