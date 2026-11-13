"""Experiment 213: CAD crude-inventory shock confirmation reversal.
Mechanism: Wednesday inventory surprise can push both oil and CAD in commodity-risk
alignment; first move may overextend before Canadian exporter hedge liquidity normalizes.
Fade 6C when CL confirms 08:30-09:00 move. Falsifier PnL/era<=0.
"""
import numpy as np,pandas as pd
FAMILY='fx-cad-crude-inventory-confirmed-continuation'
PARAMS={'open_ct_sec':30600,'entry_ct_sec':32400,'exit_ct_sec':39600,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={s:np.zeros(len(d),dtype=np.int64)for s,d in p.items()}
 if not all(s in p for s in ('CL','6C')):return a
 q={}
 for s in ('CL','6C'):
  d=p[s];c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
  for x,g in d.groupby('session',sort=False).indices.items():
   u=g[t[g]==30600];v=g[t[g]==32400]
   if len(u)and len(v):q.setdefault(x,{})[s]=int(np.sign(c[v[0]]-c[u[0]]))
 d=p['6C'];t=d.ct_sec.to_numpy();wd=pd.to_datetime(d.session.astype(str).str[:10]).dt.weekday.to_numpy()
 for x,g in d.groupby('session',sort=False).indices.items():
  z=q.get(x,{})
  if wd[g[0]]==2 and z.get('CL',0)==z.get('6C',0) and z.get('6C',0):a['6C'][g[(t[g]>=32400)&(t[g]<39600)]]=z['6C']
 return a
