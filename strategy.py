"""Experiment 201: soybean crush-margin opening confirmation.
Mechanism: matched soybean and soybean-oil cash-open moves represent processor margin
hedging; soybean direction continues as crusher orders execute. Falsifier PnL/era <=0.
"""
import numpy as np
FAMILY='grains-soy-crush-margin-opening-confirmation'
PARAMS={'open_ct_sec':30600,'entry_ct_sec':32400,'exit_ct_sec':39600,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={s:np.zeros(len(d),dtype=np.int64)for s,d in p.items()}
 if not all(s in p for s in ('ZS','ZL')):return a
 q={}
 for s in ('ZS','ZL'):
  d=p[s];c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
  for x,g in d.groupby('session',sort=False).indices.items():
   u=g[t[g]==30600];v=g[t[g]==32400]
   if len(u)and len(v):q.setdefault(x,{})[s]=int(np.sign(c[v[0]]-c[u[0]]))
 d=p['ZS'];t=d.ct_sec.to_numpy()
 for x,g in d.groupby('session',sort=False).indices.items():
  z=q.get(x,{})
  if z.get('ZS',0) and z.get('ZS')==z.get('ZL',0):a['ZS'][g[(t[g]>=32400)&(t[g]<39600)]]=z['ZS']
 return a
