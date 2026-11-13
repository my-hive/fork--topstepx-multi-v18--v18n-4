"""Experiment 232: option-expiry closing auction flow.
Mechanism: monthly option expiry forces dealer delta hedge execution into cash close;
pre-auction ES direction continues through final order imbalance. Falsifier PnL/era<=0.
"""
import numpy as np,pandas as pd
FAMILY='index-sp-options-expiry-closing-auction-continuation'
PARAMS={'observe_ct_sec':50400,'entry_ct_sec':52200,'exit_ct_sec':54000,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='ES':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dt=pd.to_datetime(d.session.astype(str).str[:10]);expiry=((dt.dt.weekday==4)&dt.dt.day.between(15,21)).to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==50400];y=g[t[g]==52200]
    if len(x)and len(y)and expiry[g[0]]:o[g[(t[g]>=52200)&(t[g]<54000)]]=int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
