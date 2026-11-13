"""Experiment 203: S&P month-end closing-auction allocation continuation.
Mechanism: pension/index fund allocation and benchmark rebalancing concentrates in the
last session's closing auction; pre-close direction continues through auction execution.
Known month-end calendar. Falsifier PnL/era <=0.
"""
import numpy as np,pandas as pd
FAMILY='index-sp-monthend-closing-auction-allocation-reversal'
PARAMS={'observe_ct_sec':50400,'entry_ct_sec':52200,'exit_ct_sec':54000,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='MES':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dt=pd.to_datetime(d.session.astype(str).str[:10]);nextdt=dt+pd.Timedelta(days=1);last=(nextdt.dt.month!=dt.dt.month).to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==50400];y=g[t[g]==52200]
    if len(x)and len(y)and last[g[0]]:o[g[(t[g]>=52200)&(t[g]<54000)]]=-int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
