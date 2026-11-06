"""Rerun the adopted Chapter 4 inferential families without altering prior runs.

uv run --with numpy --with pandas --with scipy --with statsmodels --with openpyxl \
    python analysis/RQ3/20261015-ch4-inference-adoption/run_analysis.py
"""
from pathlib import Path
from itertools import combinations
import hashlib
import importlib.util
import json
import math
import platform
import subprocess
import numpy as np
import pandas as pd
import scipy
from scipy import stats
from statsmodels.stats.multitest import multipletests

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in Path(__file__).resolve().parents if (p / "analysis").is_dir() and (p / "overleaf").is_dir())
OUTS = {1: ROOT/'analysis/RQ1/statistical-tests/20261015-ch4-inference-adoption',
        2: ROOT/'analysis/RQ2/statistical-tests/20261015-ch4-inference-adoption', 3: HERE}
CHECKS = []
THREAD = '01a13f05-e6c5-71e2-93a8-bccf8ecaf9e3'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def ck(name, ok):
    CHECKS.append(dict(check=name, passed=bool(ok)))
    if not ok:
        raise AssertionError(name)


def holm(p):
    return multipletests(np.asarray(p), method='holm')[1]


def test(x, y, method, ident, family, **meta):
    x, y = np.asarray(x, float), np.asarray(y, float)
    v = x-y
    n = len(v)
    ck(ident+' complete pairs', n > 1 and np.isfinite(v).all())
    pos, neg = int((v > 1e-12).sum()), int((v < -1e-12).sum())
    row = dict(test_id=ident, family=family, method=method, n_pairs=n,
               first_mean=float(x.mean()), second_mean=float(y.mean()), gap=float(v.mean()),
               positive=pos, negative=neg, tied=n-pos-neg, **meta)
    if method == 'paired_t':
        sd = v.std(ddof=1)
        p = 1. if sd == 0 and v.mean() == 0 else float(stats.ttest_rel(x,y).pvalue)
        t = float(v.mean()/(sd/np.sqrt(n))) if sd else 0.
        half = stats.t.ppf(.975, n-1)*sd/np.sqrt(n)
        row.update(raw_p=p, statistic=t, df=n-1, ci95_low=float(v.mean()-half), ci95_high=float(v.mean()+half))
        independent_p = float(stats.beta.cdf((n-1)/(n-1+t*t), (n-1)/2, .5))
        ck(ident+' independent beta integral', abs(p-independent_p) < 1e-10)
    else:
        ck(ident+' binary', np.isin(x,[0,1]).all() and np.isin(y,[0,1]).all())
        m = pos+neg
        p = float(stats.binomtest(pos,m,.5).pvalue) if m else 1.
        exact = min(1., 2*sum(math.comb(m,k) for k in range(min(pos,neg)+1))/2**m) if m else 1.
        ck(ident+' independent exact binomial sum', abs(p-exact) < 1e-14)
        row.update(raw_p=p, both=int(((x==1)&(y==1)).sum()), neither=int(((x==0)&(y==0)).sum()))
    return row


def correct(rows):
    d = pd.DataFrame(rows)
    d['holm_p'] = holm(d.raw_p)
    d['supported'] = d.holm_p < .05
    return d


def main():
    for p in OUTS.values():
        p.mkdir(parents=True, exist_ok=True)
    historical_dirs = [
        'analysis/RQ3/20261014-three-scope-outcome-comparisons',
        'analysis/RQ3/20261015-interpretation-binary-score',
        'analysis/RQ2/statistical-tests/20261009-confidence-score-t-ordinal',
        'analysis/RQ2/statistical-tests/20261009-within-animation-confidence',
        'analysis/RQ2/statistical-tests/20261014-accuracy-gap-interactions',
        'analysis/RQ1/statistical-tests/exact-mcnemar']
    preserved = {str(p.relative_to(ROOT)):sha(p) for folder in historical_dirs
                 for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    source = ROOT/'analysis/RQ3/20261008-nt-cross-rq/run_analysis.py'
    spec = importlib.util.spec_from_file_location('verified_source',source)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    d, hashes = m.build_input()
    CHECKS.extend(m.CHECKS)
    d.to_csv(HERE/'input.csv',index=False)
    old = pd.read_csv(ROOT/'analysis/RQ3/20261014-three-scope-outcome-comparisons/input.csv')
    ck('reconstructed inputs equal latest Chapter 4 package', d.fillna('NA').equals(old.fillna('NA')))
    animated = d[d.condition!='NT']
    scopes = {'all_trials':(d,['Q1','S','Q2','M']),
              'animated_trials':(animated,['onset','completion','Q1','Q2','M']),
              'no_animation':(d[d.condition=='NT'],['Q1','S','Q2','M'])}
    rows, means, vectors, loo = [], [], {}, []
    for scope,(z,measures) in scopes.items():
        a = z.groupby('participant_id')[measures].mean().sort_index()
        ck(scope+' 24 participants', len(a)==24)
        for pid,r in a.iterrows():
            means.append(dict(scope=scope,participant_id=pid,**r.to_dict()))
        for x,y in combinations(measures,2):
            ident = scope+'__'+x+'__'+y
            method = 'exact_mcnemar' if scope=='no_animation' else 'paired_t'
            rows.append(test(a[x],a[y],method,ident,'cross_outcome22',scope=scope,first=x,second=y,n_trials=len(z)))
            vectors[ident] = (a[x].to_numpy(),a[y].to_numpy(),method,a.index)
    cross = correct(rows)
    ck('22 cross-outcome tests',len(cross)==22)
    rng = np.random.default_rng(20261014)
    w = rng.multinomial(24,np.full(24,1/24),size=200000)
    for i,r in cross.iterrows():
        x,y,method,ids = vectors[r.test_id]
        low,high = np.quantile(w@(x-y)/24,[.025,.975])
        cross.loc[i,'bootstrap95_low'] = low
        cross.loc[i,'bootstrap95_high'] = high
    for pid in sorted(d.participant_id.unique()):
        local = []
        for ident,(x,y,method,ids) in vectors.items():
            keep = ids != pid
            r = test(x[keep],y[keep],method,ident,'cross_outcome22')
            r['removed_participant'] = pid
            local.append(r)
        loo.extend(correct(local).to_dict('records'))
    cross.to_csv(HERE/'cross_outcome_tests.csv',index=False)
    pd.DataFrame(means).to_csv(HERE/'participant_means.csv',index=False)
    pd.DataFrame(loo).to_csv(HERE/'cross_outcome_leave_one_out.csv',index=False)
    historical = pd.read_csv(ROOT/'analysis/RQ3/20261014-three-scope-outcome-comparisons/tests.csv')
    h = historical.set_index('test_id')
    for r in cross.itertuples():
        ck(r.test_id+' reproduces previous raw and adjusted p',
           np.allclose([r.raw_p,r.holm_p],[h.loc[r.test_id,'raw_p'],h.loc[r.test_id,'holm22_p']],atol=1e-12))
    # RQ1: three within-animation tests; pooled comparison is reused, never added to Holm3.
    rows = []
    for cn,z in animated.groupby('condition'):
        rows.append(test(z.onset,z.completion,'exact_mcnemar',cn+'__onset__completion',
                         'detection3',condition=cn,first='onset',second='completion',n_trials=len(z)))
    detection = correct(rows)
    detection.to_csv(OUTS[1]/'within_animation_detection.csv',index=False)
    cross[cross.test_id=='animated_trials__onset__completion'].to_csv(OUTS[1]/'pooled_detection.csv',index=False)
    d[['participant_trial_key','participant_id','condition','onset','completion','S']].to_csv(OUTS[1]/'input.csv',index=False)
    olddet = pd.read_csv(ROOT/'analysis/RQ1/statistical-tests/exact-mcnemar/tables/results.csv')
    # RQ2: four paired binary question comparisons and six selected numerical confidence tests.
    rows = []
    for cn,z in d.groupby('condition'):
        rows.append(test(z.Q1,z.Q2,'exact_mcnemar',cn+'__Q1__Q2','accuracy4',condition=cn,first='Q1',second='Q2',n_trials=len(z)))
    accuracy = correct(rows)
    accuracy.to_csv(OUTS[2]/'within_condition_accuracy.csv',index=False)
    cross[cross.test_id.isin(['all_trials__Q1__Q2','animated_trials__Q1__Q2'])].to_csv(OUTS[2]/'pooled_accuracy.csv',index=False)
    d[['participant_trial_key','participant_id','trial_number','condition','Q1','Q2','Q1_confidence','Q2_confidence']].to_csv(OUTS[2]/'input.csv',index=False)
    subprocess.run(['Rscript',str(OUTS[2]/'rerun_confidence.R'),str(ROOT)],check=True,cwd=ROOT,
                   stdout=(OUTS[2]/'R_stdout.txt').open('w'),stderr=(OUTS[2]/'R_stderr.txt').open('w'))
    confidence = pd.read_csv(OUTS[2]/'confidence_family15.csv')
    ck('confidence 15 unique tests',len(confidence)==15 and confidence.test_id.is_unique)
    ck('confidence Holm15 recomputed',np.allclose(confidence.holm_p,holm(confidence.raw_p)))
    oldconf = pd.read_csv(ROOT/'analysis/RQ2/statistical-tests/20261009-within-animation-confidence/expanded_family15.csv')
    ck('all confidence raw p reproduced',np.allclose(confidence.raw_p,oldconf.p_raw,rtol=2e-3,atol=1e-7))
    ck('all confidence supported decisions reproduced',np.array_equal(confidence.holm_p<.05,oldconf.p_holm15<.05))
    for r in confidence[confidence.method=='paired_t'].itertuples():
        name = r.test_id.removeprefix('prior_t_').removeprefix('within_t_')
        if name in ['all','animated','NT']:
            z = d if name=='all' else d[d.condition!='NT'] if name=='animated' else d[d.condition=='NT']
            a = z.groupby('participant_id')[['Q1_confidence','Q2_confidence']].mean()
            v = a.Q1_confidence-a.Q2_confidence
        elif '-' in name:
            first,second = name.split('-')
            wgap = d.assign(gap=d.Q1_confidence-d.Q2_confidence).pivot(index='participant_id',columns='condition',values='gap')
            v = (wgap[first]-wgap[second]).dropna()
        else:
            z=d[d.condition==name]
            v=z.Q1_confidence-z.Q2_confidence
        ck(r.test_id+' independent scipy t',np.isclose(r.raw_p,stats.ttest_1samp(v,0).pvalue,rtol=1e-9,atol=1e-12))
    # RQ3: interpretation comparisons restrict each contrast to eight shared participants.
    wide = animated.pivot(index='participant_id',columns='condition',values='M')
    rows,pairs = [],[]
    for first,second in [('V2','V1'),('V2','V3'),('V1','V3')]:
        z = wide[[first,second]].dropna()
        ck(first+second+' eight shared participants',len(z)==8)
        ident=first+'__'+second
        rows.append(test(z[first],z[second],'exact_mcnemar',ident,'interpretation3',first=first,second=second,n_trials=16,
                         first_overall_mean=float(animated[animated.condition==first].M.mean()),
                         second_overall_mean=float(animated[animated.condition==second].M.mean())))
        for pid,r in z.iterrows():
            pairs.append(dict(test_id=ident,participant_id=pid,first_score=r[first],second_score=r[second]))
    interpretation=correct(rows)
    interpretation.to_csv(HERE/'interpretation_tests.csv',index=False)
    pd.DataFrame(pairs).to_csv(HERE/'interpretation_pairs.csv',index=False)
    oldint=pd.read_csv(ROOT/'analysis/RQ3/20261015-interpretation-binary-score/pairwise_tests.csv')
    ck('interpretation exact tests reproduce binary permutation tests',np.allclose(interpretation.raw_p,oldint.p_raw) and np.allclose(interpretation.holm_p,oldint.p_holm))
    d.groupby('condition')[['onset','completion','S','Q1','Q2','M','Q1_confidence','Q2_confidence']].agg(['count','mean','sum']).to_csv(HERE/'condition_summaries.csv')
    for path,hval in {**hashes,**preserved}.items():
        ck('source/historical file preserved '+path,sha(ROOT/path)==hval)
    for rq,out in OUTS.items():
        pd.DataFrame(CHECKS).to_csv(out/'validation_checks.csv',index=False)
        receipt=dict(status='passed',approval='user-adopted inferential methods; provisional single-coder RQ3 outcomes',
                     thread_id=THREAD,date='2026-10-15',rq=rq,source_hashes=hashes,
                     historical_files_checked=len(preserved),checks=len(CHECKS),failed=0,
                     chapter_revision='7405d76',families={'cross_outcome22':22,'detection3':3,'accuracy4':4,'confidence15':15,'interpretation3':3},
                     bootstrap_draws=200000,seed=20261014,
                     limitations=['post hoc selection after inspection of earlier results','incomplete overlapping exposure and possible order/carryover effects',
                                  'unequal onset/completion windows','numerical confidence means assume equal rating steps',
                                  'interpretation contrasts use eight shared participants, not full condition marginals','provisional single-coder interpretation'],
                     versions=dict(python=platform.python_version(),numpy=np.__version__,pandas=pd.__version__,scipy=scipy.__version__))
        receipt['outputs']={p.name:sha(p) for p in out.iterdir() if p.is_file() and p.suffix in ['.csv','.py','.R','.txt']}
        (out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(dict(status='passed',checks=len(CHECKS),cross_supported=int(cross.supported.sum()),
                         detection_supported=int(detection.supported.sum()),accuracy_supported=int(accuracy.supported.sum()),
                         interpretation_supported=int(interpretation.supported.sum()))))


if __name__=='__main__':
    main()
