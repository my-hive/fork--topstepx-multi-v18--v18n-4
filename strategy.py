"""Experiment 238: independent equity-Friday and gold-Tuesday portfolio.
Mechanism: Friday ETF basket execution in MES and Tuesday bullion safe-haven liquidity
reversal in MGC occur on distinct days and assets, potentially diversify combine paths.
Falsifier: primary zero, era loss, risk breach, or inadequate years.
"""
import numpy as np,pandas as pd
FAMILY='crossasset-friday-equity-plus-tuesday-gold-portfolio'
PARAMS={'open_ct_sec':30600,'entry_ct_sec':32400,'exit_ct_sec':50400,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64);c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dt=pd.to_datetime(d.session.astype(str).str[:10]);wd=dt.dt.weekday.to_numpy()
  if s=='MES':
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==30600];y=g[t[g]==32400]
    if len(x)and len(y) and wd[g[0]]==4:o[g[(t[g]>=32400)&(t[g]<50400)]]=int(np.sign(c[y[0]]-c[x[0]]))
  if s=='MGC':
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==25200];y=g[t[g]==30600]
    if len(x)and len(y) and wd[g[0]]==1:o[g[(t[g]>=30600)&(t[g]<39600)]]=-int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
