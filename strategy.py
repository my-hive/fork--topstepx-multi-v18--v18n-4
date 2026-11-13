"""Experiment 251: independent FOMC equity and Monday gold inventory portfolio.
Mechanism: FOMC equity-duration hedging and gold inventory replenishment after five down
sessions occur on independent catalysts/days. Diversifies eligible FOMC calendar family.
Falsifier primary zero, era loss, risk breach, or inadequate years.
"""
import numpy as np,pandas as pd
FAMILY='crossasset-fomc-equity-plus-gold-drawdown-portfolio'
PARAMS={'fomc_observe_ct_sec':50400,'fomc_entry_ct_sec':51000,'drawdown_sessions':5,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64);c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
  if s=='MES':
   dt=pd.to_datetime(d.session.astype(str).str[:10]);on=(dt.dt.month.isin([3,6,9,12])&(dt.dt.weekday==2)&dt.dt.day.between(15,21)).to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==50400];y=g[t[g]==51000]
    if len(x)and len(y)and on[g[0]]:o[g[(t[g]>=51000)&(t[g]<54000)]]=int(np.sign(c[y[0]]-c[x[0]]))
  if s=='MGC':
   gs=list(d.groupby('session',sort=False).indices.values());r=np.array([c[g[-1]]-c[g[0]] for g in gs]);dt=pd.to_datetime(d.session.iloc[[g[0] for g in gs]].astype(str).str[:10])
   for k in range(5,len(gs)):
    if dt.iloc[k].weekday()==0 and np.all(r[k-5:k]<0):
     g=gs[k];o[g[(t[g]>=36000)&(t[g]<50400)]]=1
  a[s]=o
 return a
