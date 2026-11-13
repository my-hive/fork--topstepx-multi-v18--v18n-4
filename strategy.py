import numpy as np
import pandas as pd
FAMILY='crypto-bitcoin-blackfriday-liquidity-continuation'
PARAMS={'observe_ct_sec':25200,'entry_ct_sec':30600,'exit_ct_sec':43200,'risk_dollars':250}
def entry_risk(p): return {s:np.full(len(d),250.,dtype=float) for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='MBT':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();q=pd.to_datetime(d.session.astype(str).str[:10]);w=q.dt.weekday.to_numpy();e=(q.dt.month.eq(11)&q.dt.day.between(22,28)&(w==4)).to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==25200];y=g[t[g]==30600]
    if len(x) and len(y) and e[g[0]]:o[g[(t[g]>=30600)&(t[g]<43200)]]=int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
