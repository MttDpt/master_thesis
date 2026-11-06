"""Adopt contacts per minute of the full window using verified derived counts.

Reproduce: uv run --with pandas --with numpy python run_analysis.py
Preserves raw data, contact construction, coverage, non-frequency measures and
historical packages; frequency_per_valid_min is the sensitivity, not primary.
"""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd

RUN = Path(__file__).resolve().parent
BASE = RUN.parent / '20261003-ambient-contacts'
WHOLE = RUN.parent / '20261008-whole-trial-gaze-response'
METRICS = ['share_percent', 'total_ambient_s', 'median_contact_ms',
           'longest_contact_ms', 'contact_count', 'contacts_per_minute',
           'frequency_per_valid_min']
CHECKS = []
HASHES = {}


def read(path):
    HASHES[str(path.relative_to(RUN.parents[3]))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return pd.read_csv(path)


def check(name, value):
    CHECKS.append(dict(check=name, passed=bool(value)))
    if not value:
        raise AssertionError(name)


def save(data, name):
    data.to_csv(RUN / f'{name}.csv', index=False, float_format='%.12g')


def add_rate(data):
    result = data.copy()
    result['contacts_per_minute'] = (
        60 * result.contact_count / result.window_length_s).where(result.status.eq('evaluable'))
    pd.testing.assert_frame_equal(data, result[data.columns])
    for row in result.itertuples():
        usable = row.status == 'evaluable'
        check(f'{row.participant_trial_key}/{row.start_s}-{row.end_s}: rate and missingness',
              np.isclose(row.contacts_per_minute,
                         60 * row.contact_count / (row.end_s-row.start_s) if usable else np.nan,
                         equal_nan=True))
        if usable:
            check(f'{row.participant_trial_key}/{row.start_s}-{row.end_s}: unchanged eligibility/conversion',
                  row.coverage_percent >= 80 and row.valid_duration_s > 0
                  and np.isclose(row.contacts_per_minute,
                                 row.frequency_per_valid_min * row.valid_duration_s / row.window_length_s))
    return result


def describe(data, **metadata):
    group = data
    usable = group[group.status.eq('evaluable')]
    row = dict(**metadata, eligible=len(group), evaluable=len(usable),
               indeterminate=len(group)-len(usable),
               windows_with_contacts=int(usable.contact_count.gt(0).sum()),
               zero_contact_windows=int(usable.contact_count.eq(0).sum()))
    for metric in METRICS:
        values = usable[metric]
        row[metric+'_mean'] = values.mean()
        row[metric+'_sd'] = values.std(ddof=1)
        row[metric+'_median'] = values.median()
        row[metric+'_q1'] = values.quantile(.25)
        row[metric+'_q3'] = values.quantile(.75)
        row[metric+'_iqr'] = row[metric+'_q3']-row[metric+'_q1']
    # Independent scalar median calculation.
    v = sorted(usable.contacts_per_minute.tolist())
    n = len(v)
    med = (v[n//2] if n % 2 else (v[n//2-1]+v[n//2])/2) if n else np.nan
    check('independent median '+str(metadata), np.isclose(row['contacts_per_minute_median'], med, equal_nan=True))
    return row


def main():
    old = read(BASE/'window_measures.csv')
    windows = add_rate(old[old.window.isin(['fixed_30_90','fixed_90_120','nt_full_trial'])].copy())
    whole = add_rate(read(WHOLE/'trial_measures.csv'))
    check('168 current fixed/context windows and 72 unique whole trials',
          len(windows)==168 and windows.window_id.is_unique
          and len(whole)==72 and whole.participant_trial_key.is_unique)
    check('fixed/context eligibility: 114 usable; 66/96 animated fixed windows',
          windows.status.eq('evaluable').sum()==114
          and windows[windows.condition.ne('NT')].status.eq('evaluable').sum()==66)
    check('whole trials: 43 usable (13 NT, 30 animated)',
          whole.status.eq('evaluable').sum()==43
          and whole[whole.condition.eq('NT')].status.eq('evaluable').sum()==13)
    save(windows,'window_measures')
    save(whole,'whole_trial_measures')
    names={'V1':'sun-to-moon animation','V2':'buildings animation','V3':'red-sphere animation','NT':'no-animation'}
    summaries=[]
    for (window,condition), group in windows.groupby(['window','condition']):
        outcomes=['no_press','any_press'] if condition=='NT' else ['detected','missed']
        for outcome,sub in [('combined',group)]+[(o,group[group.detection_status.eq(o)]) for o in outcomes]:
            summaries.append(describe(sub,window=window,condition=condition,
                                      condition_name=names[condition],outcome_group=outcome))
    for window,group in windows[windows.condition.ne('NT')].groupby('window'):
        for outcome,sub in [('combined',group)]+list(group.groupby('detection_status')):
            summaries.append(describe(sub,window=window,condition='all',
                                      condition_name='all animated trials',outcome_group=outcome))
    summaries=pd.DataFrame(summaries)
    # Reconcile every unchanged measure against the previous condition summaries.
    previous=read(BASE/'condition_summary.csv')
    previous=previous[previous.window.isin(windows.window.unique())]
    merged=previous.merge(summaries,on=['window','condition','outcome_group'],validate='one_to_one',suffixes=('_old','_new'))
    check('all 33 former condition/outcome summaries retained',len(merged)==len(previous))
    for metric in [m for m in METRICS if m!='contacts_per_minute']:
        for stat in ['q1','median','q3']:
            col=metric+'_'+stat
            check('unchanged '+col,np.allclose(merged[col+'_old'],merged[col+'_new'],equal_nan=True))
    save(summaries,'condition_summary')
    nt=whole[whole.condition.eq('NT')]
    anim=whole[whole.condition.ne('NT')]
    groups=[('NT_all',nt),('animations_all',anim),('NT_no_press',nt[nt.retained_press_count.eq(0)]),
            ('NT_press',nt[nt.retained_press_count.gt(0)])]
    for event in ['onset','completion']:
        groups += [(f'animations_{event}_{outcome}',anim[anim[event+'_status'].eq(outcome)])
                   for outcome in ['detected','miss']]
    whole_summary=pd.DataFrame([describe(g,group=name) for name,g in groups])
    save(whole_summary,'whole_trial_group_summary')
    save(pd.DataFrame([describe(g,condition=c) for c,g in whole.groupby('condition')]),'whole_trial_condition_summary')
    fixed=windows[windows.window.ne('nt_full_trial')]
    pair=fixed.pivot(index=['participant_trial_key','condition'],columns='window',values=['contacts_per_minute','frequency_per_valid_min']).dropna()
    paired=pd.DataFrame(index=pair.index)
    for metric in ['contacts_per_minute','frequency_per_valid_min']:
        paired[metric+'_completion_minus_onset']=pair[(metric,'fixed_90_120')]-pair[(metric,'fixed_30_90')]
    paired=paired.reset_index()
    save(paired,'paired_phase_comparison')
    pair_summary=paired.groupby('condition').agg(paired_trials=('participant_trial_key','size'),
                        contacts_per_minute_change_median=('contacts_per_minute_completion_minus_onset','median'))
    save(pair_summary.reset_index(),'paired_phase_summary')
    for relative,digest in HASHES.items():
        check('input preserved '+relative,hashlib.sha256((RUN.parents[3]/relative).read_bytes()).hexdigest()==digest)
    save(pd.DataFrame(CHECKS),'validation_checks')
    receipt=dict(status='adopted_for_reporting',validation='passed',checks=len(CHECKS),
                 metric='Contacts per minute',formula='60 * contact_count / window_length_s',
                 sensitivity='frequency_per_valid_min (same evaluable windows)',
                 source_sha256=HASHES,raw_data_changed=False,non_frequency_measures_changed=False,
                 contact_rules_changed=False,coverage_rules_changed=False,tests_added=False)
    (RUN/'validation_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    cols=['window','condition_name','outcome_group','evaluable','eligible','contacts_per_minute_mean','contacts_per_minute_median','contacts_per_minute_q1','contacts_per_minute_q3']
    report='''<!doctype html><meta charset="utf-8"><title>Contacts per minute — current RQ1 results</title>
<style>body{font:16px system-ui;max-width:1450px;margin:32px auto;padding:0 24px;color:#17202a;line-height:1.5}table{border-collapse:collapse;font-size:13px;width:100%}td,th{padding:8px;border-bottom:1px solid #ddd;text-align:left}img{max-width:100%}</style>
<h1>Contacts per minute</h1><p>Recorded ambient-display contacts divided by the full analysis-window duration in minutes. Fixed onset: [30,90); completion: [90,120); whole trials: [0,120). Existing ≥80% valid-sample coverage and positive valid-duration rules retained; indeterminate windows are not zero. Display share (%) is retired from reporting; retained share fields are audit-only. Contact counts and all non-frequency results are unchanged.</p>
<p>Current descriptive reporting definition, adopted at the user's request. Valid-minute frequency remains explicitly named sensitivity data in the CSVs. Rates summarise individual windows, without pooling counts or time; contacts may be fragmented by recording gaps and are not verified intentional looks.</p>
<h2>Fixed windows and NT whole-trial context</h2>'''
    report+=summaries[cols].to_html(index=False,float_format=lambda x:f'{x:.2f}')
    report+='<h2>Separate whole-trial response groups</h2>'
    report+=whole_summary[['group','evaluable','eligible','contacts_per_minute_mean','contacts_per_minute_median','contacts_per_minute_q1','contacts_per_minute_q3']].to_html(index=False,float_format=lambda x:f'{x:.2f}')
    report+='<p>Whole-trial animated response groups classify the same 0–120 s gaze separately by onset and completion outcome; they are not phase-specific gaze windows. Participants contribute repeated trials; group comparisons are descriptive, without causal interpretation or significance tests.</p>'
    report+=f'<p>{len(CHECKS)} validation checks passed; all input hashes unchanged. <a href="condition_summary.csv">Condition tables</a> · <a href="whole_trial_group_summary.csv">Whole-trial groups</a> · <a href="validation_receipt.json">Validation</a></p>'
    (RUN/'report.html').write_text(report)
    print(json.dumps(receipt,indent=2))
    print(whole_summary[['group','evaluable','eligible','contacts_per_minute_mean','contacts_per_minute_median']].to_string(index=False))


if __name__=='__main__':
    main()
