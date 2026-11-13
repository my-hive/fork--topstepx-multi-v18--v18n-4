"""Exp188: London liquidity reverses thin overnight CHF safe-haven move. Falsifier PnL/era <=0."""
import numpy as np
FAMILY='fx-chf-london-safehaven-liquidity-reversal'
PARAMS={'observe_ct_sec':10800,'entry_ct_sec':14400,'exit_ct_sec':21600,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='6S':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==10800];y=g[t[g]==14400]
    if len(x)and len(y):o[g[(t[g]>=14400)&(t[g]<21600)]]=-int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
