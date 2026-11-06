"""Rebuild C.13--C.15 from frozen fixed-window gaze observations.

Run from any directory. Input records preserve unavailable windows; statistics
use evaluable records only, sample SD and linearly interpolated quartiles.
Whole-trial animated gaze is classified separately by each scheduled event;
no-animation gaze is classified by false-alarm press occurrence.
"""
from pathlib import Path
import csv
import hashlib
import json
import re
import statistics as st

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
INPUT = HERE / '20261018-gaze-outcome-inputs.csv'
METRICS = {
    'total_ambient_s': 'Time looking at the display (s)',
    'frequency_per_valid_min': 'Contact frequency (recorded contacts per valid minute)',
}
SCOPES = [('all animations', None), ('sun-to-moon', 'V1'),
          ('buildings', 'V2'), ('red-sphere', 'V3')]


def stats(records, metric):
    values = [float(r[metric]) for r in records if r['status'] == 'evaluable']
    if not values:
        return dict(usable=0, eligible=len(records), M=None, SD=None, Md=None, IQR=None)
    q = st.quantiles(values, n=4, method='inclusive') if len(values) > 1 else [values[0]] * 3
    return dict(usable=len(values), eligible=len(records), M=st.fmean(values),
                SD=st.stdev(values) if len(values) > 1 else None,
                Md=st.median(values), IQR=q[2] - q[0])


def cells(result):
    return [f"{result['usable']}/{result['eligible']}"] + [
        '--' if result[k] is None else f'{result[k]:.1f}' for k in ['M', 'SD', 'Md', 'IQR']]


def main():
    records = list(csv.DictReader(INPUT.open()))
    assert len(records) == 168
    assert len({(r['participant_trial_key'], r['window']) for r in records}) == 168
    assert sum(r['status'] == 'evaluable' and r['window'] != 'whole_0_120' for r in records) == 66
    assert sum(r['status'] == 'evaluable' and r['window'] == 'whole_0_120' for r in records) == 43
    summaries = []

    def phase_rows(window):
        phase = 'onset' if window == 'fixed_30_90' else 'completion'
        return [(label, [r for r in records if r['window'] == window and
                         (code is None or r['condition'] == code)], phase)
                for label, code in SCOPES]

    animated_whole = [r for r in records if r['window'] == 'whole_0_120' and r['condition'] != 'NT']
    nt_whole = [r for r in records if r['window'] == 'whole_0_120' and r['condition'] == 'NT']
    whole_rows = [
        (r'\shortstack[l]{all animations\\changes happening}', animated_whole, 'onset'),
        (r'\shortstack[l]{all animations\\finished state}', animated_whole, 'completion'),
        ('no-animation', nt_whole, 'press'),
    ]

    def table(label, caption, row_specs, whole=False):
        left = 'Missed / press' if whole else 'Missed'
        right = 'Detected / no press' if whole else 'Detected'
        lines = [r'\begin{table}[!htbp]', r'\centering', r'\scriptsize',
                 '\\caption{' + caption + '}', '\\label{' + label + '}',
                 r'\setlength{\tabcolsep}{2.5pt}', r'\renewcommand{\arraystretch}{1.12}',
                 r'\begin{tabularx}{\textwidth}{@{}>{\raggedright\arraybackslash}X c r r r r c r r r r@{}}',
                 r'\toprule',
                 ' & \\multicolumn{5}{c}{' + left + '} & \\multicolumn{5}{c}{' + right + r'} \\',
                 r'\cmidrule(lr){2-6}\cmidrule(l){7-11}',
                 r'Trials & $n/N$ & \textit{M} & \textit{SD} & \textit{Md} & \textit{IQR} & $n/N$ & \textit{M} & \textit{SD} & \textit{Md} & \textit{IQR} \\',
                 r'\midrule']
        for i, (metric, heading) in enumerate(METRICS.items()):
            if i:
                lines.append(r'\midrule')
            lines.append(r'\multicolumn{11}{@{}l}{\textit{' + heading + r'}} \\')
            for name, group, event in row_specs:
                values = []
                for outcome in ['missed', 'detected']:
                    if event == 'press':
                        subset = [r for r in group if (int(r['retained_press_count']) == 0) == (outcome == 'detected')]
                    else:
                        subset = [r for r in group if r[event + '_status'] == ('detected' if outcome == 'detected' else 'miss')]
                    result = stats(subset, metric)
                    summaries.append(dict(table=label, scope=name, event=event, outcome=(
                        'no press' if outcome == 'detected' else 'press') if event == 'press' else outcome,
                        metric=metric, **result))
                    values.extend(cells(result))
                lines.append(name + ' & ' + ' & '.join(values) + r' \\')
        lines += [r'\bottomrule', r'\end{tabularx}', r'\end{table}']
        return '\n'.join(lines)

    common = ('$n/N$: usable/eligible records in each outcome group; --: no observations. '
              'Statistics use usable records; SD is the sample standard deviation and IQR is $Q_3-Q_1$.')
    replacements = {
        'tab:gaze-onset-summaries': table('tab:gaze-onset-summaries',
            'Gaze descriptors during changes (30--90 s), grouped by detection outcome. ' + common,
            phase_rows('fixed_30_90')),
        'tab:gaze-whole-trial-summaries': table('tab:gaze-whole-trial-summaries',
            'Whole-trial gaze descriptors (0--120 s), grouped by response. Animated trials are grouped separately '
            'by detection of changes happening and of the finished state; the same whole-trial records are reused. '
            'No-animation groups denote press (false alarm) versus no press. ' + common,
            whole_rows, whole=True),
        'tab:gaze-fixed-summaries': table('tab:gaze-fixed-summaries',
            'Gaze descriptors after changes finished (90--120 s), grouped by detection outcome. ' + common,
            phase_rows('fixed_90_120')),
    }
    # Phase medians and usable/eligible counts must reproduce the plotted groups.
    reference_path = HERE / '20261018-gaze-figure-reference.csv'
    reference = list(csv.DictReader(reference_path.open()))
    names = {'All animated trials': 'all animations', 'Sun-to-moon animation': 'sun-to-moon',
             'Buildings animation': 'buildings', 'Red-sphere animation': 'red-sphere'}
    for ref in reference:
        matches = [r for r in summaries if r['event'] == ref['phase'] and
                   r['table'] != 'tab:gaze-whole-trial-summaries' and
                   r['scope'] == names[ref['scope']] and r['metric'] == ref['metric'] and r['outcome'] == ref['outcome']]
        assert len(matches) == 1
        actual = matches[0]
        assert (actual['usable'], actual['eligible']) == (int(ref['usable']), int(ref['eligible']))
        assert actual['Md'] is None if not ref['median'] else abs(actual['Md'] - float(ref['median'])) < 1e-9
    source = ROOT / 'examplethesis.tex'
    text = source.read_text()
    pattern = re.compile(r'\\begin\{table\}(?:\[[^\]]*\])?.*?\\end\{table\}', re.S)
    for label, replacement in replacements.items():
        found = [m.group() for m in pattern.finditer(text) if '\\label{' + label + '}' in m.group()]
        assert len(found) == 1, label
        text = text.replace(found[0], replacement, 1)
    source.write_text(text)
    with (HERE / '20261018-gaze-outcome-summaries.csv').open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summaries[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(summaries)
    receipt = {'input_sha256': hashlib.sha256(INPUT.read_bytes()).hexdigest(),
               'input_records': len(records), 'summary_rows': len(summaries),
               'figure_group_count_median_checks': len(reference),
               'fixed_window_usable': 66, 'fixed_window_eligible': 96,
               'whole_trial_usable': 43, 'whole_trial_eligible': 72,
               'SD': 'sample (n-1)', 'quartiles': 'linear interpolation',
               'sources': ['LLM_wiki/analysis/RQ1/provisional/20261003-ambient-contacts/window_measures.csv',
                           'LLM_wiki/analysis/RQ1/provisional/20261008-whole-trial-gaze-response/trial_measures.csv',
                           'LLM_wiki/analysis/dataset/trigger-data/trigger-data-cleaning/trigger_trials.csv'],
               'scope': 'descriptive presentation only; fixed windows include post-press gaze; no new tests'}
    (HERE / '20261018-gaze-outcome-receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
