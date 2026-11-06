"""Read-only independent checks of frozen final results."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from scipy import stats
R = next(p for p in Path(__file__).resolve().parents if (p / "analysis").is_dir() and (p / "overleaf").is_dir());checks=[]
def ck(name,ok):
 if not bool(ok):raise AssertionError(name)
 checks.append(name)
def holm(p):
 p=np.asarray(p,float);o=np.argsort(p,kind='stable');q=np.empty(len(p));q[o]=np.minimum(1,np.maximum.accumulate(p[o]*np.arange(len(p),0,-1)));return q
b=R/'analysis/RQ3';d=pd.read_csv(b/'20261015-ch4-inference-adoption/input.csv')
ck('72 trials / 24 participants',len(d)==72 and d.participant_trial_key.is_unique and d.participant_id.nunique()==24 and d.groupby('participant_id').size().eq(3).all());ck('condition exposure',d.condition.value_counts().to_dict()=={'NT':24,'V1':16,'V2':16,'V3':16});ck('excluded IDs absent',not d.participant_id.isin(['P00','P06','P07']).any());a=d[d.condition.ne('NT')];ck('compound score',np.allclose(a.S,(a.onset+a.completion)/2))
t=pd.read_csv(b/'20261016-compound-detection-outcomes/tests.csv');ck('18 tests',len(t)==18);ck('Holm-18',np.allclose(t.holm_p,holm(t.raw_p),atol=1e-13))
for r in t.itertuples():
 z=d if r.scope=='all_trials' else d[d.condition.ne('NT')] if r.scope=='animated_trials' else d[d.condition.eq('NT')];z=z.groupby('participant_id')[[r.x,r.y]].mean();v=(z[r.x]-z[r.y]).to_numpy();ck(str((r.scope,r.x,r.y))+' gap',len(v)==r.n_participants and np.isclose(v.mean(),r.gap));s=v[v!=0];p=stats.ttest_rel(z[r.x],z[r.y]).pvalue if r.method=='paired_t' else stats.binomtest(int((s>0).sum()),len(s),.5).pvalue if len(s) else 1.;ck(str((r.scope,r.x,r.y))+' p',np.isclose(p,r.raw_p,atol=1e-13,rtol=1e-11))
q=R/'analysis/RQ2/statistical-tests/20261015-ch4-inference-adoption';c=pd.read_csv(q/'confidence_family15.csv');ck('complete Holm-15',len(c)==15 and np.allclose(c.holm_p,holm(c.raw_p),atol=1e-13));ck('six confidence contrasts',len(pd.read_csv(q/'mean_confidence_tests.csv'))==6)
w=pd.read_csv(R/'analysis/RQ1/20261022-contact-frequency-update/window_measures.csv');v=w[w.status.eq('evaluable')];ck('168 windows',len(w)==168);ck('full-window rates',np.allclose(v.contacts_per_minute,60*v.contact_count/v.window_length_s,atol=1e-9,rtol=1e-10));a=w[w.condition.ne('NT')];ck('66/96 usable animated windows',len(a)==96 and a.status.eq('evaluable').sum()==66);ck('80% coverage',v.coverage_percent.ge(80).all())
a=R/'analysis/additional-measures/20261009-results-revision';u=pd.read_csv(a/'ueq_summary.csv');ck('24 UEQ participants',len(u)==6 and u.n.eq(24).all());n=pd.read_csv(a/'nasa_descriptive.csv');ck('72 NASA trials',n[(n.population=='all')&(n.metric=='RTLX')].n_trials.tolist()==[72]);book=pd.read_excel(R/'analysis/dataset/originals/questionnaire-data/data-aggregated.xlsx',sheet_name='04a_UEQ').set_index('Participant ID');us=pd.read_csv(a/'ueq_participant_scores.csv').set_index('participant_id');right={1,2,6,7,8,13,14,15,16,20,22,26};scales={'Attractiveness':[1,12,14,16,24,25],'Perspicuity':[2,4,13,21],'Efficiency':[9,20,22,23],'Dependability':[8,11,17,19],'Stimulation':[5,6,7,18],'Novelty':[3,10,15,26]}
for pid in us.index:
 for scale,items in scales.items():ck('UEQ '+pid+' '+scale,np.isclose(np.mean([(float(book.loc[pid].iloc[j])-4)*(1 if j in right else -1) for j in items]),us.loc[pid,scale]))
for r in u.itertuples():ck(r.scale+' mean/SD',np.isclose(us[r.scale].mean(),r.mean) and np.isclose(us[r.scale].std(ddof=1),r.sd))
print(json.dumps({'status':'passed','checks':len(checks),'scope':'independent final score, multiplicity, gaze and UEQ checks'},indent=2))
