"""Experiment 251: independent FOMC equity and Monday gold inventory portfolio.
Mechanism: FOMC equity-duration hedging and gold inventory replenishment after five down
sessions occur on independent catalysts/days. Diversifies eligible FOMC calendar family.
Falsifier primary zero, era loss, risk breach, or inadequate years.
"""
import numpy as np,pandas as pd
FAMILY='metals-gold-monday-drawdown-reversal-robustness'
PARAMS={'fomc_observe_ct_sec':50400,'fomc_entry_ct_sec':51000,'drawdown_sessions':5,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for sym,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if sym=='GC':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();gs=list(d.groupby('session',sort=False).indices.values());r=np.array([c[g[-1]]-c[g[0]] for g in gs]);dt=pd.to_datetime(d.session.iloc[[g[0] for g in gs]].astype(str).str[:10])
   for k in range(5,len(gs)):
    if dt.iloc[k].weekday()==0 and np.all(r[k-5:k]<0):
     g=gs[k];o[g[(t[g]>=36000)&(t[g]<50400)]]=1
  a[sym]=o
 return a
