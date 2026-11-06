"""Prepare user-requested exact intervals from validated trial outcomes.

No tests, scoring definitions, source tables or exclusions are changed.
Run: uv run --with pandas --with scipy python <this-file>
"""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd
from scipy.stats import beta, binomtest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
INPUT = HERE.parent / '20261015-ch4-inference-adoption/input.csv'
CODING = HERE.parent / 'coding/full-corpus-trial-codes.csv'
SUMMARY = HERE.parent / '20261016-compound-detection-outcomes/animation_scores.csv'


def main():
    sources = [INPUT, CODING, SUMMARY]
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sources}
    d = pd.read_csv(INPUT)
    coding = pd.read_csv(CODING, keep_default_na=False)
    approved = pd.read_csv(SUMMARY)
    assert len(d) == len(coding) == 72
    assert d.participant_trial_key.is_unique and coding.participant_trial_key.is_unique
    assert d.condition.value_counts().to_dict() == {'NT': 24, 'V1': 16, 'V2': 16, 'V3': 16}
    z = d.drop(columns=['specificity']).merge(coding[['participant_trial_key', 'condition', 'success', 'specificity', 'failure']],
                on=['participant_trial_key', 'condition'], validate='one_to_one')
    assert len(z) == 72 and (z.M == (z.success == 'yes').astype(int)).all()
    assert (z.M_full == ((z.success == 'yes') & (z.specificity == 'full')).astype(int)).all()
    rows, categories = [], []
    for condition in ['V1', 'V2', 'V3', 'NT']:
        g = z[z.condition == condition]
        n = len(g)
        for measure in (['onset', 'completion', 'Q1', 'Q2', 'M'] if condition != 'NT' else ['M']):
            assert g[measure].isin([0, 1]).all()
            k = int(g[measure].sum())
            lo = 0.0 if k == 0 else float(beta.ppf(.025, k, n-k+1))
            hi = 1.0 if k == n else float(beta.ppf(.975, k+1, n-k))
            independent = binomtest(k, n).proportion_ci(.95, method='exact')
            assert np.allclose([lo, hi], independent, atol=1e-10)
            assert 0 <= lo <= k/n <= hi <= 1
            if condition != 'NT' and measure in ['Q1', 'Q2', 'M']:
                a = approved[(approved.condition == condition) & (approved.measure == measure)].iloc[0]
                assert int(a.score_sum) == k and int(a.n_trials) == n
            rows.append(dict(condition=condition, measure=measure, successes=k, trials=n,
                             ci95_low_pct=100*lo, ci95_high_pct=100*hi,
                             formatted=f'{k}/{n} [{100*lo:.1f}–{100*hi:.1f}%]'))
        full = int(((g.success == 'yes') & (g.specificity == 'full')).sum())
        partial = int(((g.success == 'yes') & (g.specificity == 'partial')).sum())
        failures = int((g.success == 'no').sum())
        alternative = int((g.failure == 'alternative').sum())
        unknown = int((g.failure == 'unknown').sum())
        false_change = int((g.failure == 'false-change').sum())
        assert full + partial == int(g.M.sum()) and full + partial + failures == n
        assert alternative + unknown + false_change == failures
        categories.append(dict(condition=condition, responses=n, successes=full+partial,
                               full=full, partial=partial, failures=failures,
                               alternative=alternative, unknown=unknown, false_change=false_change))
        if condition != 'NT':
            assert np.allclose(g.S, (g.onset+g.completion)/2)
            a = approved[(approved.condition == condition) & (approved.measure == 'S')].iloc[0]
            assert g.S.sum() == a.score_sum
    pd.DataFrame(rows).to_csv(HERE/'exact_intervals.csv', index=False)
    pd.DataFrame(categories).to_csv(HERE/'interpretation_categories.csv', index=False)
    for p in sources:
        assert hashes[str(p.relative_to(ROOT))] == hashlib.sha256(p.read_bytes()).hexdigest()
    receipt = dict(status='validated_for_requested_table_update', method='Two-sided exact 95% binomial (Clopper–Pearson)',
                   interval_cells=len(rows), trial_rows=72, source_sha256=hashes,
                   checks=['72 unique trial keys and condition denominators', 'binary outcomes',
                           'recognition and interpretation totals match retained summaries',
                           'full + partial and failure categories reconcile',
                           'beta quantiles match scipy exact binomial intervals',
                           'compound score identity and unchanged source hashes'],
                   limits='Marginal per-condition binary success intervals; no interval for compound scores; no between-animation tests.')
    (HERE/'validation_receipt.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(pd.DataFrame(rows).to_string(index=False))


if __name__ == '__main__':
    main()
