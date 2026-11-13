"""Experiment 152: Treasury IMM roll-week liquidity reversion.
Mechanism: quarterly futures roll hedging creates temporary position pressure around third
Wednesday; post-roll cash liquidity reverses preceding US-morning direction. Calendar known.
Falsifier: stressed PnL <=0 or any chronological era PnL <=0.
"""
import numpy as np,pandas as pd
FAMILY='rates-treasury-imm-roll-liquidity-reversion'
PARAMS={'observe_ct_sec':30600,'entry_ct_sec':32400,'exit_ct_sec':39600,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='ZN':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dt=pd.to_datetime(d.session.astype(str).str[:10]);on=(dt.dt.month.isin([3,6,9,12])&(dt.dt.weekday==2)&dt.dt.day.between(15,21)).to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==30600];y=g[t[g]==32400]
    if len(x)and len(y)and on[g[0]]:o[g[(t[g]>=32400)&(t[g]<39600)]]=-int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
