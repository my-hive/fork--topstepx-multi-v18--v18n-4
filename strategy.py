"""Exp220: new-month allocations reinforce established equity trend. Falsifier PnL/era <=0."""
import numpy as np,pandas as pd
FAMILY='index-smallcap-monthstart-established-trend-allocation'
PARAMS={'trend_sessions':10,'business_days':3,'entry_ct_sec':30600,'exit_ct_sec':43200,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='M2K':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();gs=list(d.groupby('session',sort=False).indices.values());r=np.array([c[g[-1]]-c[g[0]] for g in gs]);dt=pd.to_datetime(d.session.iloc[[g[0] for g in gs]].astype(str).str[:10]);first=np.array([np.busday_count(x.replace(day=1).date(),x.date()) for x in dt])
   for k in range(10,len(gs)):
    if first[k]<3:
     g=gs[k];o[g[(t[g]>=30600)&(t[g]<43200)]]=int(np.sign(r[k-10:k].sum()))
  a[s]=o
 return a
