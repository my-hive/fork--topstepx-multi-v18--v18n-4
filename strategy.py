"""Exp233: CME Bitcoin weekend gap overextends then institutional futures liquidity reverses Monday. Falsifier PnL/era<=0."""
import numpy as np,pandas as pd
FAMILY='crypto-bitcoin-weekend-gap-institutional-continuation'
PARAMS={'observe_ct_sec':7200,'entry_ct_sec':30600,'exit_ct_sec':43200,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='MBT':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();wd=pd.to_datetime(d.session.astype(str).str[:10]).dt.weekday.to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==7200];y=g[t[g]==30600]
    if len(x)and len(y) and wd[g[0]]==0:o[g[(t[g]>=30600)&(t[g]<43200)]]=int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
