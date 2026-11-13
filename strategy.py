import numpy as np
import pandas as pd
FAMILY='rates-ultrabond-fomc-policy-continuation'
PARAMS={'observe_ct_sec':50400,'entry_ct_sec':51000,'exit_ct_sec':54000,'risk_dollars':250}
def entry_risk(p): return {s:np.full(len(d),250.,dtype=float) for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='UB':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();q=pd.to_datetime(d.session.astype(str).str[:10]);w=q.dt.weekday.to_numpy();e=(q.dt.month.isin([3,6,9,12])&q.dt.day.between(15,21)&(w==2)).to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==50400];y=g[t[g]==51000]
    if len(x) and len(y) and e[g[0]]:o[g[(t[g]>=51000)&(t[g]<54000)]]=int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
