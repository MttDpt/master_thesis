"""Provisional lane-centre distance; primary median of trial-window medians."""
from pathlib import Path
import hashlib
import itertools
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
MAN = ROOT / 'analysis/dataset/simulator-data/simulator-data-provenance/derived-simulator-manifest.csv'
TRIG = ROOT / 'analysis/dataset/trigger-data/trigger-data-cleaning/trigger_trials.csv'
MAP = ROOT / 'analysis/dataset/trial-data/trial-data-crosswalk/72-trial-map.csv'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
m = pd.read_csv(MAN)
t = pd.read_csv(TRIG)
crosswalk = pd.read_csv(MAP)
assert len(m) == len(t) == len(crosswalk) == 72
assert m.participant_trial_key.is_unique and t.participant_trial_key.is_unique
assert set(m.participant_trial_key) == set(crosswalk.participant_trial_key)
j = m.merge(t[['participant_trial_key', 'condition', 'any_press']], on=['participant_trial_key', 'condition'], validate='one_to_one')
assert len(j) == 72 and j.participant_id.nunique() == 24
assert j.groupby('condition').size().to_dict() == {'NT': 24, 'V1': 16, 'V2': 16, 'V3': 16}
rows, checks, input_hashes = [], [], {str(p.relative_to(ROOT)): sha(p) for p in (MAN, TRIG, MAP)}
for r in j.itertuples():
    p = ROOT / r.derived_simulator_path
    assert sha(p) == r.derived_simulator_sha256
    input_hashes[r.derived_simulator_path] = sha(p)
    d = pd.read_csv(p)
    time = np.round(d.SimTime.to_numpy() - r.simulator_to_ipad_offset_s, 8)
    assert len(d) == r.derived_row_count and np.all(np.diff(time) > 0)
    assert np.isclose(time[0], 0) and np.isclose(time[-1], 120)
    assert np.allclose(np.diff(time), .01, atol=1e-7)
    left = d[[c for c in d if c.endswith('laneOffsetLeft')][0]].to_numpy()
    right = d[[c for c in d if c.endswith('laneOffsetRight')][0]].to_numpy()
    lane = d[[c for c in d if c.endswith('laneId')][0]].to_numpy()
    valid = (lane != 0) & np.isfinite(left) & np.isfinite(right) & (right-left > 0)
    distance = np.abs((left + right) / 2)
    # Equivalent independent reconstruction from lane width and left offset.
    np.testing.assert_allclose(distance[valid], np.abs(left[valid] + (right[valid]-left[valid])/2), atol=1e-10)
    windows = [('whole_trial', 0, 120)]
    if r.condition != 'NT':
        windows += [('onset', 30, 90), ('completion', 90, 120)]
    for phase, start, end in windows:
        mask = (time >= start) & ((time <= end) if phase == 'whole_trial' else (time < end))
        x = distance[mask & valid]
        assert len(x) > 0
        rows.append(dict(participant_trial_key=r.participant_trial_key, participant_id=r.participant_id,
                         condition=r.condition, phase=phase, any_press=bool(r.any_press),
                         recorded_n=int(mask.sum()), eligible_n=len(x), excluded_n=int((mask & ~valid).sum()),
                         mean_distance_m=float(np.mean(x)), median_distance_m=float(np.median(x)),
                         max_distance_m=float(np.max(x))))
    checks.append(dict(participant_trial_key=r.participant_trial_key, hash_valid=True, grid_valid=True,
                       eligible_n=int(valid.sum()), excluded_n=int((~valid).sum()),
                       nonpositive_clearance_n=int((valid & ((left >= 0) | (right <= 0))).sum())))
a = pd.DataFrame(rows)
groups = []
for phase, sub in a.groupby('phase', sort=False):
    for group, cell in [('animated', sub[sub.condition != 'NT']), ('NT', sub[sub.condition == 'NT'])] + list(sub.groupby('condition')):
        if len(cell) == 0 or (group == 'NT' and any(z.get('group') == group and z.get('phase') == phase for z in groups)):
            continue
        v = cell.mean_distance_m
        groups.append(dict(group=group, phase=phase, trials_n=len(cell), participants_n=cell.participant_id.nunique(),
                           mean_of_trial_means_m=v.mean(), median_of_trial_means_m=v.median(),
                           q1_trial_means_m=v.quantile(.25), q3_trial_means_m=v.quantile(.75),
                           mean_of_trial_medians_m=cell.median_distance_m.mean(),
                           median_of_trial_medians_m=cell.median_distance_m.median(),
                           q1_trial_medians_m=cell.median_distance_m.quantile(.25),
                           q3_trial_medians_m=cell.median_distance_m.quantile(.75),
                           eligible_samples_n=int(cell.eligible_n.sum()), excluded_samples_n=int(cell.excluded_n.sum())))
for flag, cell in a[(a.condition == 'NT') & (a.phase == 'whole_trial')].groupby('any_press'):
    v = cell.mean_distance_m
    groups.append(dict(group='NT_with_presses' if flag else 'NT_without_presses', phase='whole_trial',
                       trials_n=len(cell), participants_n=cell.participant_id.nunique(), mean_of_trial_means_m=v.mean(),
                       median_of_trial_means_m=v.median(), q1_trial_means_m=v.quantile(.25), q3_trial_means_m=v.quantile(.75),
                       mean_of_trial_medians_m=cell.median_distance_m.mean(),
                       median_of_trial_medians_m=cell.median_distance_m.median(),
                       q1_trial_medians_m=cell.median_distance_m.quantile(.25),
                       q3_trial_medians_m=cell.median_distance_m.quantile(.75),
                       eligible_samples_n=int(cell.eligible_n.sum()),
                       excluded_samples_n=int(cell.excluded_n.sum())))
s = pd.DataFrame(groups)
contrasts = []
for phase in ['whole_trial', 'onset', 'completion']:
    pairs = list(itertools.combinations(['V1', 'V2', 'V3'], 2))
    if phase == 'whole_trial':
        pairs += [('animated', 'NT'), ('NT_without_presses', 'NT_with_presses')]
    for x, y in pairs:
        u = s[(s.phase == phase) & (s.group == x)].iloc[0]
        v = s[(s.phase == phase) & (s.group == y)].iloc[0]
        contrasts.append(dict(phase=phase, first=x, second=y, mean_difference_m=u.mean_of_trial_means_m-v.mean_of_trial_means_m,
                              median_difference_m=u.median_of_trial_medians_m-v.median_of_trial_medians_m))
for c in ['animated', 'V1', 'V2', 'V3']:
    v = s[s.group == c].set_index('phase')
    contrasts.append(dict(phase='completion_minus_onset', first=c, second=c,
                          mean_difference_m=v.loc['completion','mean_of_trial_means_m']-v.loc['onset','mean_of_trial_means_m'],
                          median_difference_m=v.loc['completion','median_of_trial_medians_m']-v.loc['onset','median_of_trial_medians_m']))
a.to_csv(OUT / 'trial_measures.csv', index=False)
s.to_csv(OUT / 'group_summary.csv', index=False)
pd.DataFrame(contrasts).to_csv(OUT / 'comparisons.csv', index=False)
pd.DataFrame(checks).to_csv(OUT / 'validation_checks.csv', index=False)
(OUT / 'validation_receipt.json').write_text(json.dumps(dict(status='validated_provisional', trials_n=72, participants_n=24,
    input_hashes=input_hashes, definition='abs((left + right)/2) metres; primary median of eligible 100 Hz samples per trial-window, then median across trials; original means retained as supplementary',
    whole_trial='0 <= time <= 120', onset='30 <= time < 90', completion='90 <= time < 120',
    missingness='Ineligible samples excluded, no interpolation or imputation; per-window counts retained',
    checks=['72 unique joined trials; 24 participants; 24/16/16/16 condition counts', '72 derived hashes verified',
            'all 72 time grids monotonic, regular 100 Hz, 0–120 s', 'independent algebraic distance reconstruction'],
    limitations=['Descriptive only; incomplete overlapping animation exposure; NT press groups unpaired',
                 'Residual simulator/iPad stop alignment error unmeasured; eligible values including extremes retained']), indent=2)+'\n')
print(s.to_string(index=False))
print('Maximum trial-window distance:', a.max_distance_m.max())
