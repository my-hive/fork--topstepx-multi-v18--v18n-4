"""Experiment 183: gold/silver inflation-shock liquidity reversal.
Mechanism: CPI surprises produce first-wave stop orders in precious metals; gold/silver
dealer liquidity mean-reverts the initial move. Calendar proxy days 10-16, 08:30 response.
Falsifier PnL/era <=0 or primary=0.
"""
import numpy as np,pandas as pd
FAMILY='metals-gold-silver-inflation-window-continuation'
PARAMS={'open_ct_sec':30600,'entry_ct_sec':32400,'exit_ct_sec':36000,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s in ('GC','SI'):
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();on=pd.to_datetime(d.session.astype(str).str[:10]).dt.day.between(10,16).to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==30600];y=g[t[g]==32400]
    if len(x)and len(y)and on[g[0]]:o[g[(t[g]>=32400)&(t[g]<36000)]]=int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
