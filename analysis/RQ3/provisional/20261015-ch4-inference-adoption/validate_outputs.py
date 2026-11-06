"""Independent reconstruction from saved trial records; no analysis-helper import."""
from pathlib import Path
from itertools import product
import hashlib
import json
import numpy as np
import pandas as pd
from scipy import stats

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
Q1=ROOT/'analysis/RQ1/provisional/statistical-tests/20261015-ch4-inference-adoption'
Q2=ROOT/'analysis/RQ2/provisional/statistical-tests/20261015-ch4-inference-adoption'
d=pd.read_csv(OUT/'input.csv')
checks=[]
def ck(name,ok):
 checks.append(dict(check=name,passed=bool(ok)))
 if not ok: raise AssertionError(name)
def adjusted(p):
 p=np.asarray(p);o=np.argsort(p,kind='stable');q=np.empty(len(p))
 q[o]=np.minimum(1,np.maximum.accumulate(p[o]*np.arange(len(p),0,-1)))
 return q
ck('72 unique trial keys',len(d)==72 and d.participant_trial_key.is_unique)
ck('24 independent participant bundles',d.participant_id.nunique()==24 and d.groupby('participant_id').size().eq(3).all())
families=[(OUT/'cross_outcome_tests.csv',22),(Q1/'within_animation_detection.csv',3),(Q2/'within_condition_accuracy.csv',4),(Q2/'confidence_family15.csv',15),(OUT/'interpretation_tests.csv',3)]
for path,size in families:
 t=pd.read_csv(path)
 ck(path.name+' family size and unique tests',len(t)==size and t.test_id.is_unique)
 ck(path.name+' independent Holm',np.allclose(t.holm_p,adjusted(t.raw_p),rtol=1e-12,atol=1e-14))
 ck(path.name+' decision labels',np.array_equal(t.supported,t.holm_p<.05))
 if path.name=='confidence_family15.csv':
  for r in pd.read_csv(Q2/'ordinal_contrasts.csv').itertuples():
   ck(r.test_id+' Wald probability',np.isclose(r.raw_p,2*stats.norm.sf(abs(r.log_odds_shift/r.se))))
  continue
 for r in t.itertuples():
  if path.name=='cross_outcome_tests.csv':
   z=d if r.scope=='all_trials' else d[d.condition!='NT'] if r.scope=='animated_trials' else d[d.condition=='NT']
   a=z.groupby('participant_id')[[r.first,r.second]].mean()
  elif path.name=='interpretation_tests.csv':
   a=d[d.condition!='NT'].pivot(index='participant_id',columns='condition',values='M')[[r.first,r.second]].dropna()
  else:
   a=d[d.condition==r.condition][[r.first,r.second]]
  v=(a[r.first]-a[r.second]).to_numpy()
  ck(r.test_id+' pair denominator and gap',len(v)==r.n_pairs and np.isclose(v.mean(),r.gap))
  if r.method=='paired_t':
   p=2*stats.t.sf(abs(v.mean()/(v.std(ddof=1)/np.sqrt(len(v)))),len(v)-1)
  else:
   signs=v[v!=0].astype(int)
   # Exhaustive null sign assignments; independent of scipy binomtest.
   sums=np.array([sum(s) for s in product([-1,1],repeat=len(signs))])
   p=float((np.abs(sums)>=abs(signs.sum())).mean())
  ck(r.test_id+' independent probability',np.isclose(p,r.raw_p,atol=1e-13,rtol=1e-11))
receipt=json.loads((OUT/'receipt.json').read_text())
for path,h in receipt['source_hashes'].items():
 ck('source hash '+path,hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==h)
for folder in [OUT,Q1,Q2]:
 r=json.loads((folder/'receipt.json').read_text())
 for name,h in r['outputs'].items():
  ck(str(folder.relative_to(ROOT))+'/'+name+' hash',hashlib.sha256((folder/name).read_bytes()).hexdigest()==h)
pd.DataFrame(checks).to_csv(OUT/'independent_checks.csv',index=False)
(OUT/'independent_validation.json').write_text(json.dumps(dict(status='passed',checks=len(checks),failed=0,source='saved trial records; independent Holm and exhaustive binary-null enumeration'),indent=2)+'\n')
print(json.dumps(dict(status='passed',checks=len(checks),failed=0)))
