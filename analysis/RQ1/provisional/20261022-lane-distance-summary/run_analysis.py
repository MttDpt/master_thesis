"""Requested provisional summaries of trial-window mean absolute lane offsets.

Run with Python containing numpy and pandas; paths resolve from this script.
Raw data and earlier analysis packages are never overwritten.
"""
from pathlib import Path
import hashlib
import json
import statistics

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
MANIFEST = ROOT / 'analysis/dataset/simulator-data/simulator-data-provenance/derived-simulator-manifest.csv'
CROSSWALK = ROOT / 'analysis/dataset/trial-data/trial-data-crosswalk/72-trial-map.csv'
PREVIOUS = ROOT / 'analysis/RQ1/provisional/20261008-lane-distance/trial_measures.csv'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
hashes = {str(p.relative_to(ROOT)): sha(p) for p in (MANIFEST, CROSSWALK, PREVIOUS)}
manifest = pd.read_csv(MANIFEST)
crosswalk = pd.read_csv(CROSSWALK)
assert len(manifest) == len(crosswalk) == 72
assert manifest.participant_trial_key.is_unique and crosswalk.participant_trial_key.is_unique
assert set(manifest.participant_trial_key) == set(crosswalk.participant_trial_key)
assert dict(manifest.groupby('condition').size()) == {'NT': 24, 'V1': 16, 'V2': 16, 'V3': 16}
joined = manifest.merge(crosswalk[['participant_trial_key', 'final_condition']].rename(columns={'final_condition': 'condition'}),
                        on=['participant_trial_key', 'condition'], validate='one_to_one')
assert len(joined) == 72 and joined.participant_id.nunique() == 24
windows = [('0–120', 0, 120, True), ('30–90', 30, 90, False), ('90–120', 90, 120, False)]
rows, diagnostics = [], []
for r in joined.itertuples():
    path = ROOT / r.derived_simulator_path
    digest = sha(path)
    assert digest == r.derived_simulator_sha256
    hashes[r.derived_simulator_path] = digest
    data = pd.read_csv(path)
    time = np.round(data.SimTime.to_numpy() - r.simulator_to_ipad_offset_s, 8)
    assert len(data) == r.derived_row_count
    assert np.isclose(data.SimTime.iloc[-1] - 120, r.simulator_to_ipad_offset_s)
    assert np.isclose(time[0], 0) and np.isclose(time[-1], 120)
    assert np.allclose(np.diff(time), .01, atol=1e-7)
    left = data[next(c for c in data if c.endswith('laneOffsetLeft'))].to_numpy()
    right = data[next(c for c in data if c.endswith('laneOffsetRight'))].to_numpy()
    lane = data[next(c for c in data if c.endswith('laneId'))].to_numpy()
    eligible = (lane != 0) & np.isfinite(left) & np.isfinite(right) & (right - left > 0)
    distance = np.abs((left + right) / 2)
    np.testing.assert_allclose(distance[eligible], np.abs(left[eligible] + (right[eligible] - left[eligible]) / 2), atol=1e-10)
    diagnostics.append(dict(participant_trial_key=r.participant_trial_key,
                            hash_verified=True, grid_verified=True,
                            left_negative_n=int((left < 0).sum()), right_positive_n=int((right > 0).sum()),
                            nonpositive_clearance_n=int((eligible & ((left >= 0) | (right <= 0))).sum()),
                            lane_width_min_m=float(np.min((right-left)[eligible])),
                            lane_width_max_m=float(np.max((right-left)[eligible]))))
    for window, start, end, inclusive_end in windows:
        mask = (time >= start) & ((time <= end) if inclusive_end else (time < end))
        values = distance[mask & eligible]
        assert len(values) > 0
        rows.append(dict(participant_trial_key=r.participant_trial_key, participant_id=r.participant_id,
                         condition=r.condition, window_s=window,
                         recorded_n=int(mask.sum()), eligible_n=len(values), excluded_n=int((mask & ~eligible).sum()),
                         mean_distance_m=float(values.mean()), median_distance_m=float(np.median(values)),
                         max_distance_m=float(values.max())))
trials = pd.DataFrame(rows)
assert len(trials) == 216
assert not trials.duplicated(['participant_trial_key', 'window_s']).any()
groups = [('all-animated', ['V1', 'V2', 'V3']), ('no-animation', ['NT']),
          ('sun-to-moon', ['V1']), ('buildings', ['V2']), ('red-sphere', ['V3'])]
summary = []
for window, *_ in windows:
    for label, codes in groups:
        cell = trials[(trials.window_s == window) & trials.condition.isin(codes)]
        values = cell.mean_distance_m.to_numpy()
        q1, md, q3 = np.quantile(values, [.25, .5, .75], method='linear')
        expected = 48 if label == 'all-animated' else 24 if label == 'no-animation' else 16
        assert len(values) == expected
        np.testing.assert_allclose([values.mean(), values.std(ddof=1), md],
                                   [statistics.mean(values), statistics.stdev(values), statistics.median(values)], atol=1e-12)
        summary.append(dict(window_s=window, type=label, trials_n=len(values),
                            participants_n=cell.participant_id.nunique(),
                            M_m=float(values.mean()), SD_m=float(values.std(ddof=1)), Md_m=float(md),
                            Q1_m=float(q1), Q3_m=float(q3), IQR_m=float(q3-q1),
                            eligible_samples_n=int(cell.eligible_n.sum()), excluded_samples_n=int(cell.excluded_n.sum())))
summary = pd.DataFrame(summary)
old = pd.read_csv(PREVIOUS)
old['window_s'] = old.phase.map({'whole_trial': '0–120', 'onset': '30–90', 'completion': '90–120'})
paired = old.merge(trials, on=['participant_trial_key', 'condition', 'window_s'], validate='one_to_one', suffixes=('_old', '_new'))
assert len(paired) == len(old) == 168
for field in ['mean_distance_m', 'median_distance_m', 'eligible_n', 'excluded_n']:
    np.testing.assert_allclose(paired[field+'_old'], paired[field+'_new'], atol=1e-12)
trials.to_csv(OUT / 'trial_window_measures.csv', index=False)
summary.to_csv(OUT / 'group_summary.csv', index=False)
pd.DataFrame(diagnostics).to_csv(OUT / 'source_checks.csv', index=False)
receipt = dict(status='validated_provisional', input_hashes=hashes,
               trials_n=72, participants_n=24, trial_windows_n=216, summary_cells_n=15,
               formula='abs((laneOffsetLeft + laneOffsetRight) / 2), applied to each eligible sample',
               aggregation='Mean within trial-window; M, sample SD (ddof=1), median, Q1, Q3 and IQR across trial-window means; equal trial weights',
               quantiles='numpy.quantile(method=linear); IQR = Q3 - Q1',
               windows={'0–120': '[0,120]', '30–90': '[30,90)', '90–120': '[90,120)'},
               eligibility='laneId != 0; finite offsets; right-left > 0; no imputation or extra outlier exclusion',
               prior_reconciliation=dict(matched_trial_windows_n=168, mean_median_and_eligibility_identical=True),
               excluded_sample_counts_by_window=trials.groupby('window_s').excluded_n.sum().to_dict(),
               checks=['72 source hashes match manifest', '72 aligned 100 Hz grids span 0–120 s',
                       '72 unique crosswalk joins, 24 participants, condition counts 24/16/16/16',
                       'Independent algebraic midpoint reconstruction', 'All 15 cell denominators verified',
                       'Group mean, SD and median checked with statistics library',
                       '168 previous trial-window means, medians and sample counts reproduced'],
               limitations=['Descriptive only; trials repeat within participants; all-animated overlaps animation subgroups',
                            'NT shorter windows are clock-matched periods, not animation phases',
                            'Original source exports unavailable; derived hashes verified against provenance manifest',
                            'Manual-stop timing error and clock drift unmeasured; eligible extremes retained'])
(OUT / 'validation_receipt.json').write_text(json.dumps(receipt, indent=2)+'\n')
print(summary[['window_s', 'type', 'trials_n', 'M_m', 'SD_m', 'Md_m', 'IQR_m']].to_string(index=False, float_format=lambda x: f'{x:.3f}'))
print('Validated: 72 trial inputs; 216 trial-windows; 15 summary cells; 168 historical trial-windows reproduced.')
