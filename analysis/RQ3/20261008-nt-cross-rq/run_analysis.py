"""Reproducible NT/animation cross-RQ supplement; no source or Markdown writes."""
from pathlib import Path
from itertools import combinations
from collections import defaultdict
import hashlib
import json
import math
import platform
import numpy as np
import pandas as pd
import scipy
from scipy.stats import binomtest, fisher_exact, hypergeom, rankdata, spearmanr, permutation_test

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in Path(__file__).resolve().parents if (p / "analysis").is_dir() and (p / "overleaf").is_dir())
OLD = HERE.parent / '20261008-combined-detection-confidence'
CHECKS = []
CFG = json.loads((HERE / 'settings.json').read_text())
MEASURES = CFG['main_measures'] + ['M_full']


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(name, passed):
    CHECKS.append({'check': name, 'passed': bool(passed)})
    if not passed:
        raise AssertionError(name)


def sign(v):
    v = np.where(np.abs(v) < 1e-12, 0., v)
    pos, neg, ties = int((v > 0).sum()), int((v < 0).sum()), int((v == 0).sum())
    n = pos + neg
    p = float(binomtest(pos, n, .5).pvalue) if n else 1.
    manual = min(1., 2 * sum(math.comb(n, k) for k in range(min(pos, neg) + 1)) / 2**n) if n else 1.
    assert abs(p - manual) < 1e-13
    return dict(positive=pos, negative=neg, ties=ties, informative=n, raw_p=p)


def holm(ps):
    idx = np.argsort(ps)
    result = np.empty(len(ps))
    result[idx] = np.minimum(1., np.maximum.accumulate(np.asarray(ps)[idx] * (len(ps) - np.arange(len(ps)))))
    return result


def exact_rank_association(x, y):
    """Exact independent-label permutation; binary x, tied ordinal y, two tails."""
    x, y = np.asarray(x, int), np.asarray(y, float)
    if len(np.unique(x)) < 2 or len(np.unique(y)) < 2:
        return np.nan, 1., 0
    ranks = np.rint(rankdata(y) * 2).astype(int)
    k, obs = int(x.sum()), int(ranks[x == 1].sum())
    counts = [defaultdict(int) for _ in range(k + 1)]
    counts[0][0] = 1
    for i, r in enumerate(ranks):
        for j in range(min(k, i + 1), 0, -1):
            for s, n in list(counts[j - 1].items()):
                counts[j][s + int(r)] += n
    total = math.comb(len(x), k)
    assert sum(counts[k].values()) == total
    lo = sum(n for s, n in counts[k].items() if s <= obs)
    hi = sum(n for s, n in counts[k].items() if s >= obs)
    return float(spearmanr(x, y).statistic), min(1., 2 * min(lo, hi) / total), total


def table_and_fisher(x, y):
    tab = np.zeros((2, 2), int)
    np.add.at(tab, (np.asarray(x, int), np.asarray(y, int)), 1)
    p = float(fisher_exact(tab, alternative='two-sided').pvalue)
    a, b, c, d = tab.ravel()
    support = np.arange(max(0, a + c - c - d), min(a + b, a + c) + 1)
    probs = hypergeom.pmf(support, tab.sum(), a + b, a + c)
    observed = hypergeom.pmf(a, tab.sum(), a + b, a + c)
    manual = min(1., probs[probs <= observed * (1 + 1e-12)].sum())
    assert np.isclose(p, manual)
    rho = float(spearmanr(x, y).statistic) if len(np.unique(x)) > 1 and len(np.unique(y)) > 1 else np.nan
    return tab, p, rho


def rank_corr(t):
    if t.ndim == 2:
        t = t[None, :, :]
    row, col = t.sum(2), t.sum(1)
    n = row.sum(1)
    rx = row.cumsum(1) - row / 2 + .5 - (n[:, None] + 1) / 2
    ry = col.cumsum(1) - col / 2 + .5 - (n[:, None] + 1) / 2
    cov = (t * rx[:, :, None] * ry[:, None, :]).sum((1, 2))
    den = np.sqrt((row * rx**2).sum(1) * (col * ry**2).sum(1))
    return np.divide(cov, den, out=np.full(len(t), np.nan), where=den > 0)


def build_input():
    old_receipt = json.loads((OLD / 'receipt.json').read_text())
    paths = list(old_receipt['sources']) + [
        'analysis/dataset/trigger-data/trigger-data-cleaning/trigger_presses.csv',
        str((OLD / 'input.csv').relative_to(ROOT)),
        str((OLD / 'tests.csv').relative_to(ROOT)),
        str((OLD / 'receipt.json').relative_to(ROOT)),
        'analysis/RQ3/20261007-cross-rq/settings.json',
    ]
    hashes = {p: sha(ROOT / p) for p in paths}
    for p, h in old_receipt['sources'].items():
        check('unchanged validated source: ' + p, hashes[p] == h)
    check('unchanged earlier analysis code', sha(OLD / 'run_analysis.py') == old_receipt['code_sha256'])
    cw = pd.read_csv(ROOT / 'analysis/dataset/trial-data/trial-data-crosswalk/72-trial-map.csv', keep_default_na=False)
    tr = pd.read_csv(ROOT / 'analysis/dataset/trigger-data/trigger-data-cleaning/trigger_trials.csv', keep_default_na=False)
    pr = pd.read_csv(ROOT / 'analysis/dataset/trigger-data/trigger-data-cleaning/trigger_presses.csv')
    co = pd.read_csv(ROOT / 'analysis/RQ3/coding/full-corpus-trial-codes.csv', keep_default_na=False)
    qu = pd.read_csv(ROOT / 'analysis/RQ2/statistical-tests/20261006-paired-correctness-binary-confidence/tables/sanitized_input.csv')
    raw = pd.read_excel(ROOT / 'analysis/dataset/originals/questionnaire-data/data-aggregated.xlsx', sheet_name='02_DiscriminationQ')
    key = json.loads((ROOT / 'analysis/RQ3/20261007-cross-rq/settings.json').read_text())['scoring_key']
    for name, z in [('crosswalk', cw), ('triggers', tr), ('coding', co), ('questionnaires', qu)]:
        check(name + ' unique 72 keys', len(z) == 72 and z.participant_trial_key.is_unique)
        check(name + ' complete key set', set(z.participant_trial_key) == set(cw.participant_trial_key))
    tr, co, qu = [z.set_index('participant_trial_key') for z in (tr, co, qu)]
    rows = []
    for r in cw.itertuples():
        pk, pid, condition = r.participant_trial_key, r.participant_id, r.final_condition
        t, c, q = tr.loc[pk], co.loc[pk], qu.loc[pk]
        z = raw[(raw['Participant ID'] == pid) & (raw['Trial number'] == r.trial_number)]
        check(pk + ' workbook unique/condition', len(z) == 1 and z.iloc[0]['condition'] == condition)
        check(pk + ' source identity agreement', all(v.participant_id == pid and v.condition == condition for v in [t, c, q]) and t.trial_number == q.trial_number == r.trial_number and c.trial_sequence == r.trial_sequence)
        check(pk + ' included', r.inclusion_status == c.inclusion_status == 'included' and c.source_available == 'yes')
        times = [float(s) for s in str(r.trigger_times_s).split('|') if s]
        times = sorted(s for s in times if 0 <= s <= 120)
        presses = pr[pr.participant_trial_key == pk].sort_values('press_time_s')
        check(pk + ' retained press reconstruction', times == presses.press_time_s.tolist() and len(times) == t.retained_press_count and bool(times) == t.any_press)
        is_nt = condition == 'NT'
        onset, completion = (np.nan, np.nan) if is_nt else (int(any(30 <= s < 90 for s in times)), int(any(90 <= s < 120 for s in times)))
        check(pk + ' event statuses', (t.onset_status == t.completion_status == 'not_applicable') if is_nt else (onset == int(t.onset_status == 'detected') and completion == int(t.completion_status == 'detected')))
        check(pk + ' boundary/classification', presses.classification.eq('false_alarm').all() if is_nt else presses.loc[presses.press_time_s == 120, 'classification'].eq('trial_end').all())
        check(pk + ' assigned coding', c.success in ['yes', 'no'] and (c.specificity in ['full', 'partial'] if c.success == 'yes' else c.specificity == 'NA'))
        d = dict(participant_trial_key=pk, participant_id=pid, trial_number=r.trial_number, condition=condition,
                 retained_presses=len(times), onset=onset, completion=completion,
                 D=np.nan if is_nt else (onset + completion) / 2,
                 S=int(not times) if is_nt else (onset + completion) / 2,
                 M=int(c.success == 'yes'), M_full=int(c.success == 'yes' and c.specificity == 'full'), specificity=c.specificity)
        for j, name in enumerate(['Q1', 'Q2']):
            ans, conf = z.iloc[0, 4 + 3*j], z.iloc[0, 6 + 3*j]
            check(pk + ' ' + name + ' source/scoring/confidence', pd.notna(ans) and conf in [1, 2, 3, 4] and int(ans == key[condition][j]) == q[name + '_correct'] and conf == q[name + '_confidence'])
            d[name], d[name + '_confidence'] = int(ans == key[condition][j]), int(conf)
        rows.append(d)
    data = pd.DataFrame(rows).sort_values(['participant_id', 'trial_number']).reset_index(drop=True)
    check('24 complete participants', data.participant_id.nunique() == 24 and data.groupby('participant_id').size().eq(3).all())
    check('one NT per participant', data[data.condition == 'NT'].groupby('participant_id').size().eq(1).all() and len(data[data.condition == 'NT']) == 24)
    check('two distinct animations per participant', data[data.condition != 'NT'].groupby('participant_id').condition.nunique().eq(2).all())
    check('condition denominators', data.condition.value_counts().to_dict() == dict(NT=24, V1=16, V2=16, V3=16))
    check('complete valid outcomes', data[MEASURES].notna().all().all() and data.S.isin([0, .5, 1]).all() and data[['Q1', 'Q2', 'M', 'M_full']].isin([0, 1]).all().all())
    check('NT event fields remain inapplicable', data.loc[data.condition == 'NT', ['D', 'onset', 'completion']].isna().all().all())
    check('no excluded participants', not set(data.participant_id) & {'P00', 'P06', 'P07'})
    old = pd.read_csv(OLD / 'input.csv').set_index('participant_trial_key')
    new = data[data.condition != 'NT'].set_index('participant_trial_key').loc[old.index]
    for a, b in [('D','D'), ('onset','onset'), ('completion','completion'), ('Q1','Q1'), ('Q2','Q2'), ('M','meaning'), ('M_full','meaning_full'), ('Q1_confidence','Q1_confidence'), ('Q2_confidence','Q2_confidence')]:
        check('prior animated input reconciled: ' + a, np.array_equal(new[a], old[b]))
    return data, hashes


def specifications(d):
    """Build all prespecified tests; each gap vector has one value per person."""
    nt = d[d.condition == 'NT'].set_index('participant_id').sort_index()
    anim = d[d.condition != 'NT'].groupby('participant_id')[MEASURES].mean().sort_index()
    allmeans = d.groupby('participant_id')[MEASURES].mean().sort_index()
    specs = []
    def gap(scope, a, b, v):
        specs.append(dict(test_id=f'{scope}__{a}__{b}', scope=scope, x=a, y=b, method='sign', vector=v, effect_type='mean_gap_pp'))
    for a, b in CFG['gap_pairs'] + CFG['full_only_pairs']:
        gap('all72', a, b, allmeans[a] - allmeans[b])
    for a, b in CFG['gap_pairs']:
        gap('NT', a, b, nt[a] - nt[b])
    for m in MEASURES:
        gap('NT_minus_animated_mean', m, m, nt[m] - anim[m])
        for condition in ['V1', 'V2', 'V3']:
            z = d[d.condition == condition].set_index('participant_id').sort_index()
            gap('NT_minus_' + condition, m, m, nt.loc[z.index, m] - z[m])
    for a, b in CFG['gap_change_pairs']:
        gap('NT_minus_animated_gap', a, b, (nt[a] - nt[b]) - (anim[a] - anim[b]))
    for a, b in CFG['nt_association_pairs']:
        specs.append(dict(test_id=f'NT_association__{a}__{b}', scope='NT_association', x=a, y=b, method='fisher', data=pd.DataFrame({'x':nt[a], 'y':nt[b]}), effect_type='phi'))
    for m in CFG['same_measure_associations']:
        specs.append(dict(test_id=f'NT_animated_association__{m}', scope='NT_animated_association', x=m, y=m, method='permutation', data=pd.DataFrame({'x':nt[m], 'y':anim[m]}), effect_type='rho'))
    for q in ['Q1', 'Q2']:
        z = d[d.condition != 'NT'].copy()
        z['direction'] = np.sign(z.participant_id.map(nt[q + '_confidence']) - z[q + '_confidence'])
        v = z.groupby('participant_id').direction.mean().sort_index()
        gap('confidence_NT_minus_animated', q, q, v)
        specs[-1]['effect_type'] = 'mean_pairwise_direction'
    gap('confidence_NT_questions', 'Q1', 'Q2', np.sign(nt.Q1_confidence - nt.Q2_confidence))
    specs[-1]['effect_type'] = 'mean_pairwise_direction'
    assert len(specs) == 49 and len({s['test_id'] for s in specs}) == 49
    return specs, nt, anim, allmeans


def calculate(s, omit=None):
    row = {k: v for k, v in s.items() if k not in ['vector', 'data']}
    if s['method'] == 'sign':
        v = s['vector'].drop(index=omit, errors='ignore') if omit else s['vector']
        row.update(sign(v.to_numpy()))
        row.update(n_participants=len(v), estimate=float(v.mean() * (100 if s['effect_type'] == 'mean_gap_pp' else 1)))
    else:
        z = s['data'].drop(index=omit, errors='ignore') if omit else s['data']
        if s['method'] == 'fisher':
            tab, p, rho = table_and_fisher(z.x, z.y)
            row.update({f'n{x}{y}':int(tab[x,y]) for x in [0,1] for y in [0,1]})
            row.update(raw_p=p, estimate=rho)
        else:
            rho, p, total = exact_rank_association(z.x, z.y)
            row.update(raw_p=p, estimate=rho, exact_assignments=total)
        row.update(n_participants=len(z), estimable=bool(np.isfinite(row['estimate'])))
    return row


def boot_intervals(s, weights, people):
    if s['method'] == 'sign':
        if s['effect_type'] != 'mean_gap_pp':
            return {}
        v = s['vector'].reindex(people)
        valid = v.notna().to_numpy()
        den = weights[:, valid].sum(1)
        draws = np.divide(weights @ v.fillna(0).to_numpy(), den, out=np.full(len(weights), np.nan), where=den > 0) * 100
        range_low, range_high = (-200, 200) if s['scope'] == 'NT_minus_animated_gap' else (-100, 100)
        idx = np.repeat(np.arange(len(people)), weights[0])
        check(s['test_id'] + ' bootstrap expansion', np.isclose(np.nanmean(v.to_numpy()[idx]) * 100, draws[0], equal_nan=True))
    else:
        z = s['data'].loc[people]
        catsx, catsy = sorted(z.x.unique()), sorted(z.y.unique())
        cells = np.zeros((len(people), len(catsx), len(catsy)), int)
        xi, yi = pd.Categorical(z.x, categories=catsx).codes, pd.Categorical(z.y, categories=catsy).codes
        cells[np.arange(len(people)), xi, yi] = 1
        draws = rank_corr((weights @ cells.reshape(len(people), -1)).reshape(-1, len(catsx), len(catsy)))
        check(s['test_id'] + ' observed frequency-table correlation', np.isclose(rank_corr(cells.sum(0))[0], spearmanr(z.x,z.y).statistic))
        for j in [0, 999, len(weights) - 1]:
            zz = z.iloc[np.repeat(np.arange(len(people)), weights[j])]
            expected = spearmanr(zz.x, zz.y).statistic if zz.x.nunique() > 1 and zz.y.nunique() > 1 else np.nan
            check(s['test_id'] + ' bootstrap tie-rank expansion ' + str(j), np.isclose(draws[j], expected, equal_nan=True))
        range_low, range_high = -1, 1
    out = {'undefined_bootstrap':int((~np.isfinite(draws)).sum())}
    for name, family in [('point95', 1), ('family49', 49), ('family79', 79)]:
        alpha = .05 / family
        out[name + '_low'] = float(np.quantile(np.where(np.isfinite(draws), draws, range_low), alpha / 2))
        out[name + '_high'] = float(np.quantile(np.where(np.isfinite(draws), draws, range_high), 1 - alpha / 2))
    # Independent seed half-sample endpoint stability is a diagnostic, not another test.
    for name, part in [('half1',draws[:len(draws)//2]), ('half2',draws[len(draws)//2:])]:
        out[name + '_family49_low'] = float(np.quantile(np.where(np.isfinite(part),part,range_low), .05/98))
        out[name + '_family49_high'] = float(np.quantile(np.where(np.isfinite(part),part,range_high), 1-.05/98))
    return out


def descriptive_tables(d, nt, anim, allmeans):
    profiles, overlaps, confidence = [], [], []
    groups = [('all72',d), ('animated',d[d.condition != 'NT'])] + list(d.groupby('condition'))
    for scope, z in groups:
        row = dict(scope=scope, n_trials=len(z), n_participants=z.participant_id.nunique(), response_score_sum=float(z.S.sum()), mean_response_score=float(z.S.mean()), no_press_trials=int((z.retained_presses==0).sum()), retained_presses=int(z.retained_presses.sum()))
        for m in ['Q1', 'Q2', 'M', 'M_full']:
            row[m + '_successes'], row[m + '_rate'] = int(z[m].sum()), float(z[m].mean())
        row['all_four_full_response'] = int(((z.S==1) & z.Q1.eq(1) & z.Q2.eq(1) & z.M.eq(1)).sum())
        row['all_four_full_response_full_only'] = int(((z.S==1) & z.Q1.eq(1) & z.Q2.eq(1) & z.M_full.eq(1)).sum())
        profiles.append(row)
        for a,b in CFG['gap_pairs']:
            for va in sorted(z[a].unique()):
                for vb in sorted(z[b].unique()):
                    n = int((z[a].eq(va) & z[b].eq(vb)).sum())
                    overlaps.append(dict(scope=scope,x=a,y=b,x_value=va,y_value=vb,n=n,denominator=len(z),percent=100*n/len(z)))
        for q in ['Q1','Q2']:
            for level in [1,2,3,4]:
                zz=z[z[q+'_confidence']==level]
                confidence.append(dict(scope=scope,question=q,level=level,n=len(zz),denominator=len(z),correct=int(zz[q].sum())))
    pd.DataFrame(profiles).to_csv(HERE/'profiles.csv',index=False)
    pd.DataFrame(overlaps).to_csv(HERE/'cross_tabs.csv',index=False)
    pd.DataFrame(confidence).to_csv(HERE/'confidence.csv',index=False)
    d.assign(full_response=d.S.eq(1).astype(int)).groupby(['condition','S','Q1','Q2','M','M_full']).size().rename('n').reset_index().to_csv(HERE/'joint_patterns.csv',index=False)
    pd.crosstab(d.condition,d.trial_number).to_csv(HERE/'position_exposure.csv')
    paired = pd.concat({'NT':nt[MEASURES], 'animated':anim, 'all72':allmeans, 'equal_context_weight':(nt[MEASURES]+anim)/2}, axis=1)
    paired.columns = ['__'.join(c) for c in paired.columns]
    paired.to_csv(HERE/'participant_means.csv')
    weighting=[]
    for a,b in CFG['gap_pairs']+CFG['full_only_pairs']:
        original=(allmeans[a]-allmeans[b]).mean()*100
        balanced=(((nt[a]+anim[a])/2)-((nt[b]+anim[b])/2)).mean()*100
        weighting.append(dict(x=a,y=b,observed_2_to_1_gap_pp=original,equal_context_gap_pp=balanced,same_direction=np.sign(original)==np.sign(balanced)))
    pd.DataFrame(weighting).to_csv(HERE/'weighting_sensitivity.csv',index=False)
    # Q1 is retained in descriptive tables but has no variance in NT.
    pd.DataFrame([dict(scope=s,measure='Q1',reason='NT Q1 equals 1 for every participant; association not estimable') for s in ['within_NT','NT_to_animated']]).to_csv(HERE/'nonestimable.csv',index=False)
    return pd.DataFrame(profiles)


def main():
    d, source_hashes = build_input()
    d.to_csv(HERE/'input.csv',index=False)
    specs, nt, anim, allmeans = specifications(d)
    rows = [calculate(s) for s in specs]
    check('49 prespecified tests',len(rows)==49)
    people=allmeans.index
    oldtests=pd.read_csv(OLD/'tests.csv')
    check('earlier family retains 30 tests',len(oldtests)==30)
    ps=np.array([r['raw_p'] for r in rows])
    adj=holm(ps)
    combined=holm(np.r_[oldtests.raw_p.to_numpy(),ps])
    weights=np.random.default_rng(CFG['seed']).multinomial(24,np.full(24,1/24),size=CFG['bootstrap_draws'])
    for i,(s,r) in enumerate(zip(specs,rows)):
        r.update(holm49_p=float(adj[i]),holm79_p=float(combined[30+i]))
        expected=min(1.,max((49-j)*p for j,p in enumerate(sorted(ps)) if p<=r['raw_p']))
        check(r['test_id']+' independent Holm',np.isclose(expected,adj[i]))
        r.update(boot_intervals(s,weights,people))
        if s['method']=='permutation':
            z=s['data']; ranks=rankdata(z.y)
            stat=lambda a,b,axis:np.mean(a,axis=axis)-np.mean(b,axis=axis)
            independent=permutation_test((ranks[z.x.eq(1)],ranks[z.x.eq(0)]),stat,vectorized=True,permutation_type='independent',alternative='two-sided',n_resamples=np.inf,batch=5000)
            check(s['test_id']+' scipy exact permutation',np.isclose(r['raw_p'],independent.pvalue))
    tests=pd.DataFrame(rows)
    tests.to_csv(HERE/'tests.csv',index=False)
    oldtests['holm79_p']=combined[:30]
    oldtests.to_csv(HERE/'earlier_tests_expanded79.csv',index=False)
    vectors=[]
    for s in specs:
        if s['method']=='sign':
            for pid,value in s['vector'].items():
                vectors.append(dict(test_id=s['test_id'],participant_id=pid,value=value))
    pd.DataFrame(vectors).to_csv(HERE/'test_vectors.csv',index=False)
    loo=[]
    for pid in people:
        result=[calculate(s,omit=pid) for s in specs]
        corrected=holm([r['raw_p'] for r in result])
        for r,p in zip(result,corrected):
            loo.append(dict(removed=pid,test_id=r['test_id'],estimate=r['estimate'],raw_p=r['raw_p'],holm49_p=p,bonferroni79_upper_bound=min(1.,79*r['raw_p'])))
    pd.DataFrame(loo).to_csv(HERE/'leave_one_out.csv',index=False)
    profiles=descriptive_tables(d,nt,anim,allmeans)
    check('pooled mean preserves 2:1 trial weighting',np.allclose(allmeans.mean(),(2*anim.mean()+nt[MEASURES].mean())/3))
    check('NT known counts reconciled',nt.S.sum()==16 and nt.Q1.sum()==24 and nt.Q2.sum()==18 and nt.M.sum()==18 and nt.retained_presses.sum()==17)
    check('animated event denominator reconciled',d.D.sum()==28.5 and d.onset.sum()==40 and d.completion.sum()==17)
    check('finite valid p-values',tests[['raw_p','holm49_p','holm79_p']].notna().all().all() and tests[['raw_p','holm49_p','holm79_p']].ge(0).all().all() and tests[['raw_p','holm49_p','holm79_p']].le(1).all().all())
    check('Holm79 at least Holm49',np.all(tests.holm79_p>=tests.holm49_p-1e-12))
    for p,h in source_hashes.items():
        check('source unchanged after run: '+p,sha(ROOT/p)==h)
    pd.DataFrame(CHECKS).to_csv(HERE/'validation_checks.csv',index=False)
    outputs={p.name:sha(p) for p in HERE.glob('*.csv')}
    receipt=dict(status='passed',checks=len(CHECKS),failed=0,analysis_status='provisional_exploratory',draft_integration='user_authorized',final_thesis_publication='not_performed',source_hashes=source_hashes,output_hashes=outputs,code_sha256=sha(Path(__file__)),settings_sha256=sha(HERE/'settings.json'),requirements_sha256=sha(HERE/'requirements.txt'),versions=dict(python=platform.python_version(),numpy=np.__version__,pandas=pd.__version__,scipy=scipy.__version__),bootstrap_draws=CFG['bootstrap_draws'],family_sizes=[49,79],old_outputs_preserved=True)
    (HERE/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(profiles[['scope','n_trials','mean_response_score','Q1_successes','Q2_successes','M_successes','all_four_full_response']].to_string(index=False))
    print(tests[['test_id','estimate','positive','negative','ties','raw_p','holm49_p','holm79_p']].to_string(index=False))
    print(json.dumps(dict(status='passed',checks=len(CHECKS),failed=0)))


if __name__=='__main__':
    main()
