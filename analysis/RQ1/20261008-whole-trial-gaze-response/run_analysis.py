"""User-authorised descriptive full-trial comparisons; no significance tests.

Run: uv run --with numpy --with pandas python run_analysis.py
Uses the existing ambient-contact implementation without executing its main.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import platform

import numpy as np
import pandas as pd

RUN = Path(__file__).resolve().parent
ROOT = next(p for p in Path(__file__).resolve().parents if (p / "analysis").is_dir() and (p / "overleaf").is_dir())
BASE = RUN.parent / '20261003-ambient-contacts'
METRICS = ['share_percent', 'total_ambient_s', 'frequency_per_valid_min']
CHECKS = []
HASHES = {}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source(path):
    HASHES[str(path.relative_to(ROOT))] = digest(path)
    return pd.read_csv(path)


def check(label, passed):
    CHECKS.append({'check': label, 'passed': bool(passed)})
    if not passed:
        raise AssertionError(label)


def main():
    spec = importlib.util.spec_from_file_location('ambient_contacts', BASE / 'run_analysis.py')
    contacts = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(contacts)
    HASHES[str((BASE / 'run_analysis.py').relative_to(ROOT))] = digest(BASE / 'run_analysis.py')
    cross = source(ROOT / 'analysis/dataset/trial-data/trial-data-crosswalk/72-trial-map.csv')
    cross = cross[cross.inclusion_status.eq('included')]
    triggers = source(ROOT / 'analysis/dataset/trigger-data/trigger-data-cleaning/trigger_trials.csv')
    manifest = source(ROOT / 'analysis/dataset/gaze-data/gaze-data-cleaning/manifest.csv')
    check('72 unique included trials from 24 participants',
          len(cross) == 72 and cross.participant_trial_key.is_unique and cross.participant_id.nunique() == 24)
    joined = cross[['participant_trial_key', 'participant_id', 'final_condition']].merge(
        triggers, on='participant_trial_key', validate='one_to_one', suffixes=('', '_trigger'))
    check('crosswalk-trigger participant and condition identity',
          len(joined) == 72 and joined.final_condition.eq(joined.condition).all()
          and joined.participant_id.eq(joined.participant_id_trigger).all())
    check('24 NT and 16 trials per animated condition',
          joined.condition.value_counts().to_dict() == {'NT': 24, 'V1': 16, 'V2': 16, 'V3': 16})
    rows = []
    for trial in joined.sort_values('participant_trial_key').itertuples():
        key = trial.participant_trial_key
        path = ROOT / 'analysis/dataset/gaze-data/gaze-data-cleaning' / f'{key}_gaze.csv'
        gaze = source(path)
        entry = manifest[manifest.derived_file.eq(path.name)]
        check(key + ': manifest hash and row count', len(entry) == 1
              and digest(path) == entry.iloc[0].derived_sha256 and len(gaze) == entry.iloc[0].row_count)
        t = gaze.Timestamp_ms.to_numpy() / 1000
        state = contacts.classify(gaze)
        check(key + ': canonical classifications and ordered timestamps',
              np.array_equal(state, gaze.spatial_region.str.replace('-', '_'))
              and np.isfinite(t).all() and (np.diff(t) > 0).all())
        keep = (t >= 0) & (t <= 120)
        t, state = t[keep], state[keep]
        built = contacts.construct(t, state)
        value, contact_rows = contacts.measure(t, state, built, 0., 120.)
        # Independently reconstruct durations directly from adjacent raw samples.
        dt = np.diff(t)
        ok = (dt > 0) & (dt <= .025)
        mid = (t[:-1] + t[1:]) / 2
        left = np.maximum(0., np.minimum(mid, 120.) - np.maximum(t[:-1], 0.))
        right = np.maximum(0., np.minimum(t[1:], 120.) - np.maximum(mid, 0.))
        totals = {s: float(left[ok & (state[:-1] == s)].sum()
                           + right[ok & (state[1:] == s)].sum())
                  for s in ['ambient_display', 'driver_axis', 'off_display']}
        check(key + ': independent ambient and valid durations',
              np.isclose(totals['ambient_display'], value['allocated_ambient_s'], atol=1e-9)
              and np.isclose(totals['ambient_display'] + totals['driver_axis'],
                             value['valid_duration_s'], atol=1e-9))
        check(key + ': contact durations sum to ambient time',
              np.isclose(sum(c['window_duration_ms'] for c in contact_rows) / 1000,
                         value['allocated_ambient_s'], atol=1e-9))
        expected_valid = int(((t >= 0) & (t < 120) & (state != 'off_display')).sum())
        expected_usable = expected_valid / 7200 >= .8 and value['valid_duration_s'] > 0
        check(key + ': independent full-trial coverage and eligibility',
              value['valid_samples'] == expected_valid and (value['status'] == 'evaluable') == expected_usable)
        if expected_usable:
            check(key + ': share and contact-frequency identities',
                  np.isclose(value['share_percent'], 100 * totals['ambient_display'] / value['valid_duration_s'])
                  and np.isclose(value['frequency_per_valid_min'], 60 * len(contact_rows) / value['valid_duration_s']))
        else:
            check(key + ': unavailable gaze remains missing', all(pd.isna(value[k]) for k in METRICS))
        if trial.condition == 'NT':
            check(key + ': NT press flag', bool(trial.any_press) == (trial.retained_press_count > 0))
        else:
            check(key + ': separate animated event classes',
                  trial.onset_status in ['detected', 'miss'] and trial.completion_status in ['detected', 'miss'])
        rows.append({'participant_trial_key': key, 'participant_id': trial.participant_id,
                     'condition': trial.condition, 'retained_press_count': trial.retained_press_count,
                     'onset_status': trial.onset_status, 'completion_status': trial.completion_status, **value})
    trials = pd.DataFrame(rows)
    previous = source(BASE / 'window_measures.csv')
    old_nt = previous[previous.window.eq('nt_full_trial')].set_index('participant_trial_key').sort_index()
    new_nt = trials[trials.condition.eq('NT')].set_index('participant_trial_key').sort_index()
    check('all 24 NT trial statuses and measurements reconcile',
          len(old_nt) == len(new_nt) == 24 and old_nt.status.eq(new_nt.status).all()
          and all(np.allclose(old_nt[k], new_nt[k], equal_nan=True, atol=1e-8) for k in METRICS))
    nt = trials[trials.condition.eq('NT')]
    animated = trials[trials.condition.ne('NT')]
    check('NT response counts reproduce 16 no-press, 8 press, 17 presses',
          int(nt.retained_press_count.eq(0).sum()) == 16
          and int(nt.retained_press_count.gt(0).sum()) == 8 and int(nt.retained_press_count.sum()) == 17)
    check('animated detection/miss counts reproduce separate events',
          animated.onset_status.value_counts().to_dict() == {'detected': 40, 'miss': 8}
          and animated.completion_status.value_counts().to_dict() == {'miss': 31, 'detected': 17})
    groups = [('NT_all', 'all', nt), ('animations_all', 'all', animated),
              ('NT_no_press', 'correct_rejection', nt[nt.retained_press_count.eq(0)]),
              ('NT_press', 'false_alarm', nt[nt.retained_press_count.gt(0)])]
    for event in ['onset', 'completion']:
        for status in ['detected', 'miss']:
            groups.append((f'animations_{event}_{status}', status,
                           animated[animated[f'{event}_status'].eq(status)]))
    summaries = []
    for name, response, group in groups:
        usable = group[group.status.eq('evaluable')]
        row = {'group': name, 'response': response, 'eligible_trials': len(group),
               'usable_trials': len(usable), 'indeterminate_trials': len(group) - len(usable),
               'usable_participants': usable.participant_id.nunique()}
        for condition in ['NT', 'V1', 'V2', 'V3']:
            row[f'{condition}_usable'] = int(usable.condition.eq(condition).sum())
        for metric in METRICS:
            for label, q in [('q1', .25), ('median', .5), ('q3', .75)]:
                row[f'{metric}_{label}'] = usable[metric].quantile(q)
        summaries.append(row)
        check(name + ': denominator partition', len(group) == len(usable) + row['indeterminate_trials'])
    summary = pd.DataFrame(summaries).set_index('group')
    pairs = [('overall', 'NT_all', 'animations_all')]
    for event in ['onset', 'completion']:
        pairs.extend([(f'{event}_correct', 'NT_no_press', f'animations_{event}_detected'),
                      (f'{event}_incorrect', 'NT_press', f'animations_{event}_miss')])
    comparisons = []
    for label, baseline, target in pairs:
        a, b = summary.loc[baseline], summary.loc[target]
        row = {'comparison': label, 'NT_group': baseline, 'animated_group': target,
               'NT_usable': int(a.usable_trials), 'animated_usable': int(b.usable_trials)}
        for metric in METRICS:
            row[f'{metric}_NT_median'] = a[f'{metric}_median']
            row[f'{metric}_animated_median'] = b[f'{metric}_median']
            row[f'{metric}_animated_minus_NT'] = b[f'{metric}_median'] - a[f'{metric}_median']
        comparisons.append(row)
    condition_rows = []
    for condition, group in trials.groupby('condition'):
        usable = group[group.status.eq('evaluable')]
        condition_rows.append({'condition': condition, 'eligible_trials': len(group),
                               'usable_trials': len(usable),
                               **{f'{k}_median': usable[k].median() for k in METRICS}})
    trials.to_csv(RUN / 'trial_measures.csv', index=False, float_format='%.12g')
    summary.reset_index().to_csv(RUN / 'group_summary.csv', index=False, float_format='%.12g')
    pd.DataFrame(comparisons).to_csv(RUN / 'comparisons.csv', index=False, float_format='%.12g')
    pd.DataFrame(condition_rows).to_csv(RUN / 'condition_summary.csv', index=False, float_format='%.12g')
    pd.DataFrame(CHECKS).to_csv(RUN / 'validation_checks.csv', index=False)
    (RUN / 'validation_receipt.json').write_text(json.dumps({
        'status': 'provisional', 'all_checks_passed': all(c['passed'] for c in CHECKS),
        'checks': len(CHECKS), 'window': '[0,120)', 'coverage_rule': '>=80% valid samples at 60 Hz; positive valid duration',
        'aggregation': 'median across evaluable trial measures; each trial equally weighted',
        'grouping': 'NT correct rejection/false alarm; animated detection/miss separately for onset and completion',
        'inference': 'descriptive only; no p-values; not participant-paired',
        'python': platform.python_version(), 'pandas': pd.__version__, 'numpy': np.__version__,
        'input_sha256': HASHES, 'code_sha256': digest(Path(__file__)),
    }, indent=2) + '\n')
    print(summary[['eligible_trials', 'usable_trials'] + [f'{k}_median' for k in METRICS]].round(3).to_string())
    print(f'Checks passed: {len(CHECKS)}')


if __name__ == '__main__':
    main()
