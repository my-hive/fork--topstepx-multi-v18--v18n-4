"""Experiment 249: FOMC S&P and Friday Nasdaq distinct-calendar portfolio.
Mechanism: FOMC equity-duration hedging and weekly Nasdaq ETF basket execution are
separate catalysts on different dates. Same rules frozen from earlier eligible components.
Falsifier: primary zero, era loss, risk breach, or inadequate years.
"""
import numpy as np,pandas as pd
FAMILY='index-fomc-sp-plus-friday-nasdaq-calendar-portfolio'
PARAMS={'fomc_observe_ct_sec':50400,'fomc_entry_ct_sec':51000,'friday_open_ct_sec':30600,'friday_entry_ct_sec':32400,'risk_dollars':250}
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
  if s=='MNQ':
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==30600];y=g[t[g]==32400]
    if len(x)and len(y)and wd[g[0]]==4:o[g[(t[g]>=32400)&(t[g]<50400)]]=int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
