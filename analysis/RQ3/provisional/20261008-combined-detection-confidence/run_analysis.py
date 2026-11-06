"""Combined event detection and ordinal confidence: reproducible exploratory supplement."""
from pathlib import Path
from itertools import combinations
import hashlib
import json
import math
import platform
import numpy as np
import pandas as pd
import scipy
from scipy.stats import binomtest, spearmanr

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE = HERE.parent/'20261008-cross-rq-gaps'
ORIGINAL = HERE.parent/'20261007-cross-rq'
CHECKS = []

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def check(name, passed):
    CHECKS.append(dict(check=name, passed=bool(passed)))
    assert passed, name

def sign(values):
    pos, neg, ties = [int(np.sum(f(values))) for f in [lambda v:v>0, lambda v:v<0, lambda v:v==0]]
    n = pos+neg
    p = binomtest(pos,n,.5).pvalue if n else 1.
    manual = min(1., 2*sum(math.comb(n,k) for k in range(min(pos,neg)+1))/2**n) if n else 1.
    assert abs(p-manual)<1e-14
    return dict(positive=pos,negative=neg,ties=ties,informative=n,raw_p=p)

def holm(ps):
    idx=np.argsort(ps); out=np.empty(len(ps))
    out[idx]=np.minimum(1,np.maximum.accumulate(np.asarray(ps)[idx]*(len(ps)-np.arange(len(ps)))))
    return out

def rank_corr(t):
    """Exact Spearman coefficient of frequency tables; fractional average tie ranks."""
    if t.ndim==2:
        t=t[None,:,:]
    rows,cols=t.sum(2),t.sum(1)
    n=rows.sum(1)
    rx=np.cumsum(rows,axis=1)-rows/2+.5-(n[:,None]+1)/2
    ry=np.cumsum(cols,axis=1)-cols/2+.5-(n[:,None]+1)/2
    cov=(t*rx[:,:,None]*ry[:,None,:]).sum((1,2))
    den=np.sqrt((rows*rx**2).sum(1)*(cols*ry**2).sum(1))
    return np.divide(cov,den,out=np.full(len(t),np.nan),where=den>0)

def bounds(draws, alpha):
    return [float(np.quantile(np.where(np.isfinite(draws),draws,fill),q)) for fill,q in [(-1,alpha/2),(1,1-alpha/2)]]

def main():
    cfg=json.loads((HERE/'settings.json').read_text())
    receipt=json.loads((BASE/'receipt.json').read_text())
    for p,h in receipt['source_hashes'].items():
        check('unchanged source '+p,sha(ROOT/p)==h)
    check('unchanged previous code',sha(BASE/'run_analysis.py')==receipt['code_sha256'])
    check('unchanged input',sha(BASE/'input.csv')==receipt['joined_sha256'])
    d=pd.read_csv(BASE/'input.csv',keep_default_na=False)
    qp=ROOT/'analysis/RQ2/provisional/statistical-tests/20261006-paired-correctness-binary-confidence/tables/sanitized_input.csv'
    q=pd.read_csv(qp)
    check('unique questionnaire keys',q.participant_trial_key.is_unique)
    d=d.merge(q[['participant_trial_key','participant_id','condition','trial_number','Q1_confidence','Q2_confidence']],on=['participant_trial_key','participant_id','condition','trial_number'],how='left',validate='one_to_one')
    check('48 complete trial records',len(d)==48 and d.participant_trial_key.is_unique and d[['Q1_confidence','Q2_confidence']].notna().all().all())
    check('24 participants with two records each',d.participant_id.nunique()==24 and d.groupby('participant_id').size().eq(2).all())
    check('16 trials per animation',d.condition.value_counts().to_dict()==dict(V1=16,V2=16,V3=16))
    check('valid confidence',d[['Q1_confidence','Q2_confidence']].isin([1,2,3,4]).all().all())
    wb=ROOT/'analysis/dataset/originals/questionnaire-data/data-aggregated.xlsx'
    check('unchanged workbook',sha(wb)==receipt['workbook_sha256'])
    raw=pd.read_excel(wb,sheet_name='02_DiscriminationQ')
    key=json.loads((ORIGINAL/'settings.json').read_text())['scoring_key']
    triggers=pd.read_csv(ROOT/'analysis/dataset/trigger-data/trigger-data-cleaning/trigger_trials.csv').set_index('participant_trial_key')
    coding=pd.read_csv(ROOT/'analysis/RQ3/provisional/coding/full-corpus-trial-codes.csv',keep_default_na=False).set_index('participant_trial_key')
    crosswalk=pd.read_csv(ROOT/'analysis/dataset/trial-data/trial-data-crosswalk/72-trial-map.csv').set_index('participant_trial_key')
    for r in d.itertuples():
        c=crosswalk.loc[r.participant_trial_key]
        check(r.participant_trial_key+' crosswalk',c.participant_id==r.participant_id and c.trial_number==r.trial_number and c.final_condition==r.condition)
        z=raw[(raw['Participant ID']==r.participant_id)&(raw['Trial number']==r.trial_number)]
        check(r.participant_trial_key+' workbook match',len(z)==1)
        for j,name in enumerate(['Q1','Q2']):
            check(r.participant_trial_key+' '+name+' original confidence and scoring',z.iloc[0,6+3*j]==getattr(r,name+'_confidence') and int(z.iloc[0,4+3*j]==key[r.condition][j])==getattr(r,name))
        tr=triggers.loc[r.participant_trial_key]; co=coding.loc[r.participant_trial_key]
        check(r.participant_trial_key+' events',r.onset==int(tr.onset_status=='detected') and r.completion==int(tr.completion_status=='detected'))
        check(r.participant_trial_key+' meaning',r.meaning==int(co.success=='yes') and r.meaning_full==int(co.success=='yes' and co.specificity=='full'))
    d['D']=(d.onset+d.completion)/2
    check('D identity and domain',d.D.isin([0,.5,1]).all() and np.array_equal(d.D*2,d.onset+d.completion))
    d=d.sort_values(['participant_id','trial_number']).reset_index(drop=True)
    measures=['onset','completion','Q1','Q2','meaning','meaning_full','D']
    means=d.groupby('participant_id')[measures].mean().sort_index()
    people=means.index.to_numpy()
    nboot=cfg['bootstrap_draws']
    weights=np.random.default_rng(cfg['seed']).multinomial(24,np.full(24,1/24),size=nboot)
    primary=['onset','completion','Q1','Q2','meaning']
    pairs=list(combinations(primary,2))+[(x,'meaning_full') for x in primary if x!='meaning']+cfg['gap_pairs']
    test_vectors=[]; rows=[]
    for a,b in pairs:
        v=(means[a]-means[b]).to_numpy()
        s=sign(v)
        boot=weights@v/24*100
        low,high=np.quantile(boot,[.05/60,1-.05/60])
        lo95,hi95=np.quantile(boot,[.025,.975])
        rows.append(dict(kind='gap',x=a,y=b,**s,gap_pp=v.mean()*100,mean_x=d[a].mean(),mean_y=d[b].mean(),family_low_pp=low,family_high_pp=high,low95_pp=lo95,high95_pp=hi95))
        test_vectors.append(v)
        check(a+b+' bootstrap expansion',np.isclose(np.repeat(v,weights[0]).mean()*100,boot[0]))
    old=pd.read_csv(BASE/'results.csv')
    check('all 14 original p values reproduced',all(np.isclose(r['raw_p'],p) for r,p in zip(rows[:14],old.raw_p)))
    correlations=[]; bycondition=[]; bootstrap_arrays={}
    for a,b in cfg['association_pairs']:
        values=d[[a,b]].to_numpy().reshape(24,2,2)
        v=np.sign(values[:,1,0]-values[:,0,0])*np.sign(values[:,1,1]-values[:,0,1])
        rows.append(dict(kind='concordance',x=a,y=b,**sign(v)))
        test_vectors.append(v)
        nx=len(np.unique(d[a])); ny=len(np.unique(d[b]))
        xi=pd.Categorical(d[a],categories=sorted(d[a].unique())).codes
        yi=pd.Categorical(d[b],categories=sorted(d[b].unique())).codes
        cells=np.zeros((24,nx,ny),dtype=int)
        for i,(xx,yy) in enumerate(zip(xi,yi)):
            cells[i//2,xx,yy]+=1
        point=float(rank_corr(cells.sum(0))[0])
        check(a+b+' Spearman agrees with scipy',np.isclose(point,spearmanr(d[a],d[b]).statistic,equal_nan=True))
        boot=rank_corr((weights@cells.reshape(24,-1)).reshape(nboot,nx,ny))
        low,high=bounds(boot,.05/30);lo95,hi95=bounds(boot,.05)
        for i in [0,999,199999]:
            idx=np.repeat(np.arange(24),weights[i])
            arr=values[idx].reshape(-1,2)
            expected=spearmanr(arr[:,0],arr[:,1]).statistic if len(np.unique(arr[:,0]))>1 and len(np.unique(arr[:,1]))>1 else np.nan
            check(a+b+' correlation bootstrap expansion '+str(i),np.isclose(boot[i],expected,equal_nan=True))
        correlations.append(dict(x=a,y=b,rho=point,family_low=low,family_high=high,low95=lo95,high95=hi95,undefined=int((~np.isfinite(boot)).sum()),bootstrap_draws=nboot))
        bootstrap_arrays[a+'__'+b]=boot
        for condition,z in d.groupby('condition'):
            est=spearmanr(z[a],z[b]).statistic if z[a].nunique()>1 and z[b].nunique()>1 else np.nan
            bycondition.append(dict(condition=condition,x=a,y=b,n=len(z),rho=est,descriptive_only=True))
    check('one family of 30 tests',len(rows)==30)
    for r,p in zip(rows,holm([r['raw_p'] for r in rows])):
        r['holm_p']=p
    # Independent closed-testing calculation for each sorted Holm p.
    ordered=sorted(r['raw_p'] for r in rows)
    for r in rows:
        expected=min(1,max((30-i)*p for i,p in enumerate(ordered) if p<=r['raw_p']))
        check(r['kind']+r['x']+r['y']+' Holm check',np.isclose(expected,r['holm_p']))
    loo=[]
    for i,pid in enumerate(people):
        adj=holm([sign(np.delete(v,i))['raw_p'] for v in test_vectors])
        for r,p in zip(rows,adj):
            loo.append(dict(removed=pid,kind=r['kind'],x=r['x'],y=r['y'],holm_p=p))
    profile=[]
    for condition,z in [('pooled',d),*list(d.groupby('condition'))]:
        profile.append(dict(condition=condition,n_trials=len(z),participants=z.participant_id.nunique(),none=int((z.D==0).sum()),one=int((z.D==.5).sum()),both=int((z.D==1).sum()),detected_events=int(z.onset.sum()+z.completion.sum()),scheduled_events=2*len(z),mean_D=z.D.mean(),Q1_rate=z.Q1.mean(),Q2_rate=z.Q2.mean(),meaning_rate=z.meaning.mean(),meaning_full_rate=z.meaning_full.mean()))
    confidence_cells=[]
    for qname in ['Q1','Q2']:
        for level,z in d.groupby(qname+'_confidence'):
            confidence_cells.append(dict(question=qname,confidence=int(level),n=len(z),correct=int(z[qname].sum()),meaning_success=int(z.meaning.sum()),mean_D=z.D.mean()))
    d.to_csv(HERE/'input.csv',index=False)
    means.to_csv(HERE/'participant_means.csv')
    pd.DataFrame(rows).to_csv(HERE/'tests.csv',index=False)
    pd.DataFrame(correlations).to_csv(HERE/'pooled_correlations.csv',index=False)
    pd.DataFrame(bycondition).to_csv(HERE/'condition_correlations.csv',index=False)
    pd.DataFrame(profile).to_csv(HERE/'observed_profiles.csv',index=False)
    pd.DataFrame(confidence_cells).to_csv(HERE/'confidence_levels.csv',index=False)
    pd.DataFrame(loo).to_csv(HERE/'leave_one_out.csv',index=False)
    pd.DataFrame(CHECKS).to_csv(HERE/'validation_checks.csv',index=False)
    np.savez_compressed(HERE/'correlation_bootstrap.npz',**bootstrap_arrays)
    out=dict(status='passed',checks=len(CHECKS),failed=0,provisional=True,thesis_adoption='pending',sources={**receipt['source_hashes'],str(BASE.relative_to(ROOT) / 'input.csv'):sha(BASE/'input.csv'),str(wb.relative_to(ROOT)):sha(wb)},settings_sha256=sha(HERE/'settings.json'),code_sha256=sha(Path(__file__)),versions=dict(python=platform.python_version(),numpy=np.__version__,pandas=pd.__version__,scipy=scipy.__version__),test_family_size=30,bootstrap_draws=nboot,all_earlier_results_preserved=True)
    (HERE/'receipt.json').write_text(json.dumps(out,indent=2)+'\n')
    print(pd.DataFrame(profile).to_string(index=False))
    print(pd.DataFrame(rows)[['kind','x','y','positive','negative','ties','raw_p','holm_p']].to_string(index=False))
    print(pd.DataFrame(correlations).to_string(index=False))
    print(json.dumps(dict(status='passed',checks=len(CHECKS))))

if __name__=='__main__':
    main()
