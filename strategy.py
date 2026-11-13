"""Experiment 158: Friday closing-auction basket-flow continuation.
Mechanism: weekly ETF creation/redemption and benchmark rebalancing concentrate in Friday
closing auction; pre-auction imbalance direction continues into final execution.
Falsifier: stressed PnL <=0 or any chronological era PnL <=0.
"""
import numpy as np,pandas as pd
FAMILY='index-friday-closing-auction-basket-flow'
PARAMS={'observe_ct_sec':50400,'entry_ct_sec':52200,'exit_ct_sec':54000,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='ES':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();f=(pd.to_datetime(d.session.astype(str).str[:10]).dt.weekday==4).to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==50400];y=g[t[g]==52200]
    if len(x)and len(y)and f[g[0]]:o[g[(t[g]>=52200)&(t[g]<54000)]]=int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
