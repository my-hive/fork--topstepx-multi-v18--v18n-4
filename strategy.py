"""Experiment 250: refined-products winter distillate confirmation.
Mechanism: shared RBOB/HO opening direction reflects refinery throughput and inventory
news, with HO winter hedge demand carrying into US session. Falsifier PnL/era<=0.
"""
import numpy as np,pandas as pd
FAMILY='energy-refinedproducts-winter-opening-confirmation'
PARAMS={'open_ct_sec':30600,'entry_ct_sec':32400,'exit_ct_sec':39600,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={s:np.zeros(len(d),dtype=np.int64)for s,d in p.items()}
 if not all(s in p for s in ('HO','RB')):return a
 q={}
 for s in ('HO','RB'):
  d=p[s];c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
  for x,g in d.groupby('session',sort=False).indices.items():
   u=g[t[g]==30600];v=g[t[g]==32400]
   if len(u)and len(v):q.setdefault(x,{})[s]=int(np.sign(c[v[0]]-c[u[0]]))
 d=p['HO'];t=d.ct_sec.to_numpy();m=pd.to_datetime(d.session.astype(str).str[:10]).dt.month.to_numpy()
 for x,g in d.groupby('session',sort=False).indices.items():
  z=q.get(x,{})
  if m[g[0]] in [11,12,1,2] and z.get('HO',0)==z.get('RB',0) and z.get('HO',0):a['HO'][g[(t[g]>=32400)&(t[g]<39600)]]=z['HO']
 return a
