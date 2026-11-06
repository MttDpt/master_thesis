"""Render the current LLM_wiki contact-frequency figure; no Overleaf writes."""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.colors import to_rgba

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
SOURCE = ROOT / 'analysis/RQ1/provisional/20261003-ambient-contacts/window_measures.csv'
digest = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
data = pd.read_csv(SOURCE)
data = data[data.window.isin(['fixed_30_90', 'fixed_90_120', 'nt_full_trial'])].copy()
data['contacts_per_minute'] = (60 * data.contact_count / data.window_length_s).where(data.status.eq('evaluable'))
ev = data[data.status.eq('evaluable')]
assert np.allclose(ev.frequency_per_valid_min, 60 * ev.contact_count / ev.valid_duration_s)
assert np.allclose(ev.contacts_per_minute, ev.frequency_per_valid_min * ev.valid_duration_s / ev.window_length_s)
animated = data[data.condition.ne('NT')].copy()
assert len(animated) == 96
assert animated.status.eq('evaluable').sum() == 66
assert animated.window_id.is_unique
assert animated.groupby('window').status.apply(lambda x: x.eq('evaluable').sum()).to_dict() == {'fixed_30_90': 35, 'fixed_90_120': 31}

summaries = []
for condition in ['all', 'V1', 'V2', 'V3', 'NT']:
    group = animated if condition == 'all' else data[data.condition.eq(condition)]
    for (window, outcome), cell in group.groupby(['window', 'detection_status']):
        usable = cell[cell.status.eq('evaluable')]
        row = dict(condition=condition, window=window, outcome=outcome,
                   usable=len(usable), eligible=len(cell))
        for metric in ['frequency_per_valid_min', 'contacts_per_minute']:
            values = usable[metric]
            row.update({metric + '_mean': values.mean(), metric + '_sd': values.std(),
                        metric + '_median': values.median(), metric + '_q1': values.quantile(.25),
                        metric + '_q3': values.quantile(.75)})
        summaries.append(row)
summary = pd.DataFrame(summaries)
summary.to_csv(OUT / 'figure-4-5-comparison.csv', index=False, float_format='%.10g')
# Reconcile the source's old means to the current thesis appendix table.
for window, outcome, expected in [('fixed_30_90', 'missed', 129.9),
                                  ('fixed_30_90', 'detected', 126.9),
                                  ('fixed_90_120', 'missed', 103.5),
                                  ('fixed_90_120', 'detected', 114.9)]:
    row = summary[(summary.condition == 'all') & (summary.window == window) & (summary.outcome == outcome)].iloc[0]
    assert round(row.frequency_per_valid_min_mean, 1) == expected

plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 12,
                     'axes.labelsize': 13, 'xtick.labelsize': 12, 'ytick.labelsize': 12})
fig, ax = plt.subplots(figsize=(15.25, 7.2))
fig.subplots_adjust(left=.075, right=.99, bottom=.13, top=.73)
groups = [('all', 'All animated trials', '#718198', 'D'),
          ('V1', 'Sun-to-moon animation', '#00AD83', 'o'),
          ('V2', 'Buildings animation', '#7654B6', 's'),
          ('V3', 'Red-sphere animation', '#D77AB1', '^')]
rng = np.random.default_rng(45)
count_labels = []
for group_index, (condition, label, color, marker) in enumerate(groups):
    group = animated if condition == 'all' else animated[animated.condition.eq(condition)]
    for phase_index, window in enumerate(['fixed_30_90', 'fixed_90_120']):
        centre = group_index * 4.2 + phase_index * 1.7
        for outcome_index, outcome in enumerate(['missed', 'detected']):
            position = centre + (-.40 if outcome_index == 0 else .40)
            cell = group[group.window.eq(window) & group.detection_status.eq(outcome)]
            values = cell.loc[cell.status.eq('evaluable'), 'contacts_per_minute'].to_numpy()
            count_labels.append((position, f'{len(values)}/{len(cell)}', color))
            if len(values):
                ax.boxplot([values], positions=[position], widths=.46, manage_ticks=False,
                           patch_artist=True, showfliers=False, whis=1.5,
                           boxprops={'facecolor': to_rgba(color,.16 if outcome_index else .035), 'edgecolor': color, 'linewidth':1.2},
                           medianprops={'color':color,'linewidth':1.8},
                           whiskerprops={'color':color,'linewidth':1.2},
                           capprops={'color':color,'linewidth':1.2})
                jitter = rng.uniform(-.15,.15,len(values))
                ax.scatter(position+jitter, values, marker=marker, s=35,
                           facecolors=to_rgba(color,.32) if outcome_index else 'white',
                           edgecolors=color, linewidths=1.1, zorder=3)
            else:
                ax.text(position, 153, 'No missed events', rotation=90,
                        ha='center',va='center',color='#888888',fontsize=10)
    if group_index < 3:
        ax.axvline(group_index * 4.2 + 2.75, color='#dedede',lw=.9,ls=(0,(3,4)))

ticks = [g*4.2+p*1.7 for g in range(4) for p in range(2)]
ax.set_xticks(ticks, ['30–90 s', '90–120 s']*4)
ax.set_xlim(-.92, 3*4.2+1.7+.92)
ax.set_ylim(0,370)
ax.set_yticks(np.arange(0,351,50))
ax.set_xlabel('Fixed trial window', labelpad=11)
ax.set_ylabel('Display contact frequency (contacts/min)',labelpad=12)
ax.grid(axis='y',color='#dedede',lw=.8)
ax.set_axisbelow(True)
for spine in ['top','right']:
    ax.spines[spine].set_visible(False)
ax.spines['left'].set_linewidth(1.2)
ax.spines['bottom'].set_linewidth(1.2)
ax.tick_params(axis='x',length=0,pad=10)
for x,text,color in count_labels:
    ax.text(x,1.018,text,transform=ax.get_xaxis_transform(),ha='center',va='bottom',color=color,fontsize=10.5)
ax.text(1,1.075,'Counts: usable/eligible',transform=ax.transAxes,ha='right',color='#777777',fontsize=10)
handles=[Line2D([],[],marker=marker,color=color,linestyle='none',markersize=7,
                markeredgecolor=color,markeredgewidth=1.2,
                markerfacecolor=to_rgba(color,.12),label=label) for _,label,color,marker in groups]
fig.legend(handles=handles,loc='upper center',bbox_to_anchor=(.53,.98),frameon=False,ncol=4,columnspacing=1.7,handletextpad=.65)
fig.legend(handles=[Line2D([],[],marker='o',color='#666666',markerfacecolor='white',linestyle='none',label='Missed'),
                    Line2D([],[],marker='o',color='#666666',markerfacecolor='#aaaaaa',linestyle='none',label='Detected')],
           loc='upper center',bbox_to_anchor=(.53,.915),frameon=False,ncol=2,columnspacing=2)
for extension in ['png','pdf','svg']:
    fig.savefig(OUT / f'figure_4_5_contacts_per_minute.{extension}',dpi=200,facecolor='white')
plt.close(fig)
caption = '''Figure 4.5 — contacts per minute of the full analysis window. Recorded ambient-display contact frequency in missed and detected animated trials, pooled and by animation. Each point is one usable trial-window; the y-axis is recorded contacts divided by scheduled window length in minutes, and the x-axis separates 30–90 s and 90–120 s fixed periods. Colour and shape identify the animation; hollow markers denote misses and filled markers detections. Box lines show medians, boxes the middle 50%, and whiskers extend to the most extreme points within 1.5 interquartile ranges; all observations are shown. Labels give usable/eligible counts: 66/96 usable animated windows in total (35/48 onset; 31/48 completion), retaining the existing coverage rule. Sun-to-moon has no onset misses. The pooled group repeats the individual-animation observations, and participants contribute repeated trials. These are descriptive distributions, not confidence intervals or significance tests; unrecorded contacts cannot be recovered, and recorded segments may reflect fragmentation rather than intentional looks.'''
(OUT / 'caption.txt').write_text(caption+'\n')
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == digest
(OUT / 'figure_validation.json').write_text(json.dumps({'status':'adopted_for_reporting','validation':'passed',
    'source':str(SOURCE),'source_sha256':digest,'eligible_animated_windows':96,
    'usable_animated_windows':66,'counts_unchanged':True,'old_pooled_means_reconciled_to_thesis':True,
    'overleaf_files_written':False,'units':'Recorded contacts per scheduled minute'},indent=2)+'\n')
print(summary[(summary.condition.eq('all')) | (summary.condition.eq('NT') & summary.window.eq('nt_full_trial'))][['condition','window','outcome','usable','eligible','frequency_per_valid_min_mean','contacts_per_minute_mean','frequency_per_valid_min_median','contacts_per_minute_median']].to_string(index=False))
print(OUT)
