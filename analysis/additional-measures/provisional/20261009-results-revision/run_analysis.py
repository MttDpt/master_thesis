"""User-requested supplementary workload inference and corrected UEQ scoring.
Run with uv run --with numpy --with pandas --with scipy --with openpyxl --with statsmodels python <this file>.
Writes only this provisional package; preserves approved summaries and all raw data.
"""
from pathlib import Path
import hashlib, json, importlib.util, warnings
from itertools import combinations
import numpy as np
import pandas as pd
import scipy
from scipy.stats import t, ttest_1samp, binomtest
import statsmodels
import statsmodels.formula.api as smf
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CHECKS = []
def check(name, ok):
    CHECKS.append({'check': name, 'passed': bool(ok)})
    if not ok: raise AssertionError(name)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(df, name): df.to_csv(HERE / name, index=False)

paths = [
 'analysis/dataset/originals/questionnaire-data/data-aggregated.xlsx',
 'analysis/dataset/trial-data/trial-data-crosswalk/72-trial-map.csv',
 'analysis/additional-measures/approved/generate_questionnaire_figures.py',
 'analysis/additional-measures/approved/nasa_tlx_summary.csv',
 'analysis/RQ3/provisional/20261008-nt-cross-rq/input.csv',
 'analysis/RQ3/provisional/20261008-nt-cross-rq/run_analysis.py',
 'analysis/RQ3/provisional/coding/full-corpus-trial-codes.csv',
 'analysis/RQ3/provisional/coding/full-corpus-validation.json',
]
hashes = {p:sha(ROOT/p) for p in paths}
# Reuse the source-reconciling builder without rerunning prior statistical analyses.
p=ROOT/paths[5]
spec=importlib.util.spec_from_file_location('prior_cross_rq',p)
prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)
joint, upstream_hashes=prior.build_input()
check('prior source-reconstruction checks', all(c['passed'] for c in prior.CHECKS))
old=pd.read_csv(ROOT/paths[4])
check('joint input matches current upstream reconstruction', np.allclose(joint[['S','Q1','Q2','M','M_full']],old[['S','Q1','Q2','M','M_full']]))

cw=pd.read_csv(ROOT/paths[1])
check('canonical included sample',len(cw)==72 and cw.participant_id.nunique()==24 and cw.inclusion_status.eq('included').all())
book=ROOT/paths[0]
nasa=pd.read_excel(book,sheet_name='03_NASA');nasa.columns=nasa.columns.str.strip()
dims=['Mental Demand','Physical Demand','Temporal  Demand','Performance','Effort','Frustration']
nasa=nasa.loc[pd.to_numeric(nasa['Trial number'],errors='coerce').notna(),['Participant ID','Trial number','Condition']+dims].copy()
nasa=nasa.rename(columns={'Participant ID':'participant_id','Trial number':'trial_number','Condition':'source_condition'})
nasa['trial_number']=nasa.trial_number.astype(int)
nasa['participant_id']=nasa.participant_id.str.strip()
check('unique NASA source keys',not nasa.duplicated(['participant_id','trial_number']).any())
check('excluded NASA records are P06/P07 only',nasa.loc[~nasa.participant_id.isin(cw.participant_id),'participant_id'].value_counts().to_dict()=={'P06':3,'P07':3})
df=joint.merge(nasa,on=['participant_id','trial_number'],how='left',validate='one_to_one')
check('NASA join conditions',len(df)==72 and df.condition.eq(df.source_condition).all())
for c in dims: df[c]=pd.to_numeric(df[c],errors='coerce')
check('complete integer six-dimension scores in 1-10',df[dims].notna().all().all() and df[dims].apply(lambda s:s.between(1,10)&s.eq(s.round())).all().all())
df['RTLX']=df[dims].mean(axis=1,skipna=False)
check('no excluded participants',not set(df.participant_id)&{'P00','P06','P07'})
save(df.drop(columns=['Q1_confidence','Q2_confidence']),'trial_input.csv')
pop={'all':df,'animated':df[df.condition!='NT'],'NT':df[df.condition=='NT']}
pop.update({c:df[df.condition==c] for c in ['V1','V2','V3']})
summary=[]
for name,d in pop.items():
 for metric in dims+['RTLX']:
  s=d[metric]
  summary.append(dict(population=name,metric=metric,n_trials=len(s),n_participants=d.participant_id.nunique(),mean=s.mean(),sd=s.std(),median=s.median(),minimum=s.min(),maximum=s.max()))
summary=pd.DataFrame(summary);save(summary,'nasa_descriptive.csv')
approved=pd.read_csv(ROOT/paths[3])
for r in approved.itertuples():
 metric='RTLX' if r.metric=='overall' else r.metric
 row=summary[(summary.population==r.condition)&(summary.metric==metric)].iloc[0]
 check('approved NASA summary '+r.condition+' '+metric,int(row.n_trials)==r.n and np.isclose(row['mean'],r.mean) and np.isclose(row.sd,r.sd))

contrasts=[];vectors=[]
for metric in dims+['RTLX']:
 pivot=df.pivot(index='participant_id',columns='condition',values=metric)
 anim=df[df.condition!='NT'].groupby('participant_id')[metric].mean()
 pairs=[('animated-NT',anim-pivot.NT)]+[(a+'-'+b,(pivot[a]-pivot[b]).dropna()) for a,b in combinations(['V1','V2','V3'],2)]
 for name,d in pairs:
  n=len(d);se=d.std()/np.sqrt(n);mean=d.mean();ci=t.ppf(.975,n-1)*se
  pos=int((d>1e-10).sum());neg=int((d< -1e-10).sum())
  contrasts.append(dict(metric=metric,contrast=name,n_pairs=n,mean_difference=mean,sd_difference=d.std(),ci_low=mean-ci,ci_high=mean+ci,raw_p=ttest_1samp(d,0).pvalue,positive=pos,negative=neg,ties=n-pos-neg,sign_raw_p=binomtest(pos,pos+neg).pvalue if pos+neg else 1.))
  vectors.extend(dict(metric=metric,contrast=name,participant_id=pid,difference=x) for pid,x in d.items())
contrasts=pd.DataFrame(contrasts);save(pd.DataFrame(vectors),'paired_differences.csv')

assoc=[];outdesc=[]
for name in ['all','animated','NT']:
 d=pop[name].copy()
 for outcome in ['S','Q1','Q2','M']:
  for val,z in d.groupby(outcome):
   outdesc.append(dict(population=name,outcome=outcome,score=val,n_trials=len(z),n_participants=z.participant_id.nunique(),RTLX_mean=z.RTLX.mean(),RTLX_sd=z.RTLX.std()))
  row=dict(population=name,outcome=outcome,n_trials=len(d),n_participants=d.participant_id.nunique())
  if d[outcome].nunique()<2:
   assoc.append(dict(**row,status='not_estimable_constant_outcome',raw_p=1.));continue
  rhs='C(trial_number)' if name=='NT' else 'C(participant_id) + C(condition) + C(trial_number)'
  model=smf.ols('RTLX ~ '+outcome+' + '+rhs,data=d)
  # The scheduled animation/position terms can be aliased; retain their full
  # nuisance column space in an orthonormal basis, never discard the outcome.
  j=model.exog_names.index(outcome);Z=np.delete(model.exog,j,axis=1);x=model.exog[:,j];y=model.endog
  U,s,_=np.linalg.svd(Z,full_matrices=False);rank=int((s>max(Z.shape)*np.finfo(float).eps*s[0]).sum())
  nuisance=U[:,:rank];rx=x-nuisance@(nuisance.T@x)
  row['redundant_nuisance_columns']=Z.shape[1]-rank
  if np.linalg.norm(rx)<1e-9:
   assoc.append(dict(**row,status='not_estimable_after_covariates',raw_p=1.));continue
  exog=pd.DataFrame(np.column_stack([x,nuisance]),index=d.index,columns=[outcome]+['nuisance_'+str(k) for k in range(rank)])
  model=sm.OLS(y,exog)
  check('full rank reparameterised model '+name+' '+outcome,np.linalg.matrix_rank(model.exog)==model.exog.shape[1])
  if name=='NT': fit=model.fit(cov_type='HC3',use_t=True)
  else: fit=model.fit(cov_type='cluster',cov_kwds={'groups':d.participant_id,'use_correction':True,'df_correction':True},use_t=True)
  ci=fit.conf_int().loc[outcome]
  row.update(status='estimated',coefficient=fit.params[outcome],se=fit.bse[outcome],ci_low=ci.iloc[0],ci_high=ci.iloc[1],raw_p=fit.pvalues[outcome],residual_df=fit.df_resid,reference_df=getattr(fit,'df_resid_inference',fit.df_resid),design_rank=np.linalg.matrix_rank(model.exog),max_leverage=fit.get_influence().hat_matrix_diag.max())
  check('finite estimate '+name+' '+outcome,np.isfinite([row['coefficient'],row['se'],row['raw_p']]).all())
  # Verify the covariate-adjusted coefficient independently by residualising X and Y.
  j=model.exog_names.index(outcome);Z=np.delete(model.exog,j,axis=1);x=model.exog[:,j];y=model.endog
  rx=x-Z@np.linalg.lstsq(Z,x,rcond=None)[0];ry=y-Z@np.linalg.lstsq(Z,y,rcond=None)[0]
  check('independent partial-regression coefficient '+name+' '+outcome,np.isclose(rx@ry/(rx@rx),row['coefficient']))
  assoc.append(row)
assoc=pd.DataFrame(assoc)
primary=contrasts.metric.eq('RTLX')
ps=contrasts.loc[primary,'raw_p'].tolist()+assoc.raw_p.tolist()
adj=multipletests(ps,method='holm')[1]
contrasts.loc[primary,'holm_p']=adj[:4];assoc['holm_p']=adj[4:]
contrasts.loc[~primary,'holm_p']=multipletests(contrasts.loc[~primary,'raw_p'],method='holm')[1]
contrasts.loc[primary,'sign_holm_p']=multipletests(contrasts.loc[primary,'sign_raw_p'],method='holm')[1]
contrasts['conclusive']=contrasts.holm_p<.05
assoc['conclusive']=(assoc.status=='estimated')&(assoc.holm_p<.05)
save(contrasts,'nasa_contrasts.csv');save(assoc,'nasa_associations.csv');save(pd.DataFrame(outdesc),'nasa_by_outcome.csv')

ueq=pd.read_excel(book,sheet_name='04a_UEQ')
check('unique aggregate UEQ participants',ueq['Participant ID'].is_unique)
ueq=ueq[ueq['Participant ID'].isin(cw.participant_id)].copy()
check('UEQ 24 included participants',len(ueq)==24 and set(ueq['Participant ID'])==set(cw.participant_id))
raw=ueq.iloc[:,2:28].apply(pd.to_numeric,errors='coerce')
check('UEQ all 624 item scores valid',raw.shape==(24,26) and raw.notna().all().all() and raw.apply(lambda s:s.between(1,7)&s.eq(s.round())).all().all())
right=[True,True,False,False,False,True,True,True,False,False,False,False,True,True,True,True,False,False,False,True,False,True,False,False,False,True]
scores=np.where(np.asarray(right)[None,:],raw.to_numpy()-4,4-raw.to_numpy())
scales={'Attractiveness':[1,12,14,16,24,25],'Perspicuity':[2,4,13,21],'Efficiency':[9,20,22,23],'Dependability':[8,11,17,19],'Stimulation':[5,6,7,18],'Novelty':[3,10,15,26]}
check('UEQ mapping partitions 26 items',sorted(sum(scales.values(),[]))==list(range(1,27)))
uout=pd.DataFrame({'participant_id':ueq['Participant ID'].to_numpy()});us=[]
for scale,idx in scales.items():
 vals=scores[:,np.asarray(idx)-1].mean(axis=1);uout[scale]=vals
 us.append(dict(scale=scale,n=24,mean=vals.mean(),sd=vals.std(ddof=1),classification='positive' if vals.mean()>.8 else ('negative' if vals.mean()<-.8 else 'neutral')))
save(uout,'ueq_participant_scores.csv');save(pd.DataFrame(us),'ueq_summary.csv')
check('inputs unchanged',all(sha(ROOT/p)==h for p,h in hashes.items()))
save(pd.DataFrame(CHECKS),'validation_checks.csv')
receipt={'status':'validated provisional','checks_passed':len(CHECKS),'upstream_source_checks_passed':len(prior.CHECKS),'sources':hashes,'upstream_sources':upstream_hashes,'code_sha256':sha(Path(__file__)),'settings_sha256':sha(HERE/'settings.json'),'versions':{'numpy':np.__version__,'pandas':pd.__version__,'scipy':scipy.__version__,'statsmodels':statsmodels.__version__},'primary_conclusive_count':int(contrasts.loc[primary,'conclusive'].sum()+assoc.conclusive.sum()),'primary_tests':16,'estimated_primary_tests':15,'secondary_dimension_conclusive_count':int(contrasts.loc[~primary,'conclusive'].sum()),'warnings':['Exploratory tests do not establish equivalence when inconclusive.','Animation pairs have only eight shared participants each.','Q3 remains provisional single-coder evidence.','UEQ uses the canonical aggregate ID mapping, including P23 whose raw standalone export ID is blank.','Existing approved UEQ summary is preserved but uses an ineligible n=25 sample; use this n=24 output for the requested draft.']}
(HERE/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(summary[summary.metric=='RTLX'].to_string(index=False))
print(contrasts.loc[primary,['contrast','n_pairs','mean_difference','ci_low','ci_high','raw_p','holm_p','sign_holm_p']].to_string(index=False))
print(assoc[['population','outcome','status','coefficient','ci_low','ci_high','raw_p','holm_p']].to_string(index=False))
print(pd.DataFrame(us).to_string(index=False))
print('Checks:',len(CHECKS),'upstream:',len(prior.CHECKS),'primary conclusive:',receipt['primary_conclusive_count'],'secondary:',receipt['secondary_dimension_conclusive_count'])
