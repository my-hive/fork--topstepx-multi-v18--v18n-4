"""Experiment 166: soybean month-start crush hedge reversal.
Mechanism: month-start processor procurement and elevator hedge rolls make overnight
soybean movement temporary; cash grain liquidity reverses it in first business days.
Known calendar, no same-day close data. Falsifier: PnL <=0 or any era <=0.
"""
import numpy as np,pandas as pd
FAMILY='grains-soy-monthstart-crush-hedge-reversal'
PARAMS={'business_days':3,'observe_ct_sec':7200,'entry_ct_sec':30600,'exit_ct_sec':46800,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='ZS':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dt=pd.to_datetime(d.session.astype(str).str[:10]);first=np.array([np.busday_count(x.replace(day=1).date(),x.date()) for x in dt])
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==7200];y=g[t[g]==30600]
    if len(x)and len(y)and first[g[0]]<3:o[g[(t[g]>=30600)&(t[g]<46800)]]=-int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
