"""Experiment 253: FOMC S&P and Tuesday gold distinct-calendar portfolio.
Mechanism: policy-statement equity hedging and Tuesday bullion safe-haven liquidity
reversal are independent catalysts on distinct days. Falsifier: primary zero or era loss.
"""
import numpy as np,pandas as pd
FAMILY='crossasset-fomc-sp-plus-tuesday-gold-portfolio'
PARAMS={'fomc_observe_ct_sec':50400,'fomc_entry_ct_sec':51000,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64);c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dt=pd.to_datetime(d.session.astype(str).str[:10]);wd=dt.dt.weekday.to_numpy()
  if s=='MES':
   on=(dt.dt.month.isin([3,6,9,12])&(wd==2)&dt.dt.day.between(15,21)).to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==50400];y=g[t[g]==51000]
    if len(x)and len(y)and on[g[0]]:o[g[(t[g]>=51000)&(t[g]<54000)]]=int(np.sign(c[y[0]]-c[x[0]]))
  if s=='MGC':
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==25200];y=g[t[g]==30600]
    if len(x)and len(y)and wd[g[0]]==1:o[g[(t[g]>=30600)&(t[g]<39600)]]=-int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
