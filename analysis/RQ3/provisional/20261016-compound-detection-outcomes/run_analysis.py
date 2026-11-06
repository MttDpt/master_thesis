"""User-approved compound detection presentation and 18-comparison family."""
from pathlib import Path
from itertools import combinations
from decimal import Decimal, ROUND_HALF_UP
import hashlib,json,shutil
import numpy as np
import pandas as pd
from scipy import stats,special
from statsmodels.stats.multitest import multipletests
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb,to_rgba
from matplotlib.lines import Line2D
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'20261015-ch4-inference-adoption/input.csv'
ORDER=['S','Q1','Q2','M']
def fmt(v):return str(Decimal(str(v)).quantize(Decimal('.001'),rounding=ROUND_HALF_UP))
def pv(v):
 if v<.001:return '<.001'
 label=fmt(v).lstrip('0')
 if .01<v<.0105:label=f'{v:.4f}'.lstrip('0')
 return '= '+label
def stars(v):return '***' if v<.001 else '**' if v<.01 else '*' if v<.05 else ''
def main():
 d=pd.read_csv(SOURCE);a=d[d.condition!='NT'];nt=d[d.condition=='NT']
 assert len(d)==72 and d.participant_id.nunique()==24 and len(a)==48 and len(nt)==24
 assert np.allclose(a.S,(a.onset+a.completion)/2)
 assert set(a.S.unique())<={0,.5,1} and set(nt.S.unique())<={0,1}
 assert not d.duplicated(['participant_id','trial_number']).any()
 scopes={'all_trials':d,'animated_trials':a,'no_animation':nt};tests=[];means=[];scores=[]
 for scope,z in scopes.items():
  m=z.groupby('participant_id')[ORDER].mean().sort_index();assert len(m)==24 and m.notna().all().all()
  for pid,r in m.iterrows():means.append(dict(scope=scope,participant_id=pid,**r.to_dict()))
  for measure in ORDER:scores.append(dict(scope=scope,measure=measure,n_trials=len(z),n_participants=24,score_sum=z[measure].sum(),mean_score=m[measure].mean()))
  for x,y in combinations(['Q1','S','Q2','M'],2):
   v=(m[x]-m[y]).to_numpy();gap=v.mean()
   if scope=='no_animation':
    pos=int((v>0).sum());neg=int((v<0).sum());raw=stats.binomtest(pos,pos+neg).pvalue if pos+neg else 1.
    from math import comb
    independent=min(1.,2*sum(comb(pos+neg,i) for i in range(min(pos,neg)+1))/2**(pos+neg))
    method='exact_McNemar'
   else:
    raw=stats.ttest_rel(m[x],m[y]).pvalue;stat=gap/(v.std(ddof=1)/np.sqrt(24));independent=special.betainc(23/2,.5,23/(23+stat**2));method='paired_t'
   assert np.isclose(raw,independent,rtol=1e-10,atol=1e-14)
   tests.append(dict(scope=scope,x=x,y=y,n_participants=24,n_trials=len(z),method=method,x_mean=m[x].mean(),y_mean=m[y].mean(),gap=gap,raw_p=raw))
 t=pd.DataFrame(tests);assert len(t)==18
 t['holm_p']=multipletests(t.raw_p,method='holm')[1]
 order=np.argsort(t.raw_p.to_numpy());manual=np.empty(18);manual[order]=np.minimum(1,np.maximum.accumulate((18-np.arange(18))*t.raw_p.to_numpy()[order]));assert np.allclose(t.holm_p,manual)
 old=pd.read_csv(HERE.parent/'20261014-mean-score-comparisons/within_scope_tests.csv')
 for r in t.itertuples():
  hist=old[(old.scope==r.scope)&(old.x==r.x)&(old.y==r.y)];assert len(hist)==1
  assert np.isclose(r.raw_p,hist.raw_p.iloc[0]) and np.isclose(r.holm_p,hist.holm_p.iloc[0])
 for source,target in [('within_scope_tests.csv','retained_uncertainty.csv'),('within_leave_one_out.csv','retained_deletion_diagnostics.csv')]:shutil.copy2(HERE.parent/'20261014-mean-score-comparisons'/source,HERE/target)
 t.to_csv(HERE/'tests.csv',index=False);pd.DataFrame(means).to_csv(HERE/'participant_means.csv',index=False);pd.DataFrame(scores).to_csv(HERE/'scope_scores.csv',index=False)
 anim=[]
 for c in ['V1','V2','V3']:
  z=a[a.condition==c];assert len(z)==16 and z.participant_id.nunique()==16
  for measure in ORDER:anim.append(dict(condition=c,measure=measure,n_trials=16,score_sum=z[measure].sum(),mean_score=z[measure].mean()))
 pd.DataFrame(anim).to_csv(HERE/'animation_scores.csv',index=False)
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'pdf.fonttype':42})
 def draw(groups,labels,filename,brackets=False):
  fig,ax=plt.subplots(figsize=(15,7.2 if brackets else 6.5));handles=[];texts=[]
  for gi,(key,name,color,marker,data) in enumerate(groups):
   xs=np.arange(4)+gi*5.4;ys=np.array([data[m] for m in ORDER]);fill=tuple(.18*c+.82 for c in to_rgb(color))
   ax.bar(xs,ys,width=.68,color=to_rgba(color,.18),edgecolor=color,linewidth=.9,zorder=2)
   ax.plot(xs,ys,color=color,lw=1.1,zorder=3)
   ax.scatter(xs,ys,marker=marker,s=27,facecolor=fill,edgecolor=color,linewidth=.9,zorder=4,clip_on=False)
   for x,y in zip(xs,ys):texts.append((ax.text(x,y,fmt(y),ha='center',va='bottom',color=color,fontsize=9,zorder=6),x,y))
   handles.append(Line2D([0],[0],marker=marker,color=color,linestyle='None',markerfacecolor=fill,label=name))
   if brackets:
    shown=t[(t.scope==key)&(t.x=='Q1')]
    for level,r in enumerate(shown.itertuples()):
     x1=xs[ORDER.index(r.x)];x2=xs[ORDER.index(r.y)];y=(1.20 if key=="no_animation" else 1.08)+level*.115
     ax.plot([x1,x1,x2,x2],[y-.018,y,y,y-.018],color=color,lw=.7)
     ax.text((x1+x2)/2,y+.015,r'$p_{\mathrm{Holm}}$ '+pv(r.holm_p)+stars(r.holm_p),color=color,ha='center',fontsize=8)
  ax.set_xticks(np.concatenate([np.arange(4)+i*5.4 for i in range(3)]),sum(labels,[]),rotation=43,ha='right',fontsize=9)
  ax.set_ylabel('Mean score (0–1)');ax.set_xlabel('Outcome within each trial set' if brackets else 'Outcome within each animation',labelpad=16)
  ax.set_ylim(0,1.63 if brackets else 1.14);ax.set_xlim(-.6,14.4);ax.set_yticks(np.arange(0,1.01,.25));ax.set_yticklabels([f'{v:.2f}' for v in np.arange(0,1.01,.25)])
  ax.grid(axis='y',color='#DDDDDD',lw=.6);ax.set_axisbelow(True);ax.spines[['top','right']].set_visible(False)
  fig.legend(handles=handles,loc='upper center',ncol=3,frameon=False,bbox_to_anchor=(.51,.99),columnspacing=2.5)
  fig.subplots_adjust(left=.065,right=.99,bottom=.31,top=.87)
  fig.canvas.draw();renderer=fig.canvas.get_renderer();paths=[l.get_path().transformed(l.get_transform()) for l in ax.lines];placed=[]
  for text,x,y in texts:
   origin=ax.transData.transform((x,y))
   for offset in [12,20,28,36,44,52,60]:
    text.set_position(ax.transData.inverted().transform(origin+[0,offset]));box=text.get_window_extent(renderer).expanded(1.15,1.25)
    if not any(path.intersects_bbox(box,filled=False) for path in paths) and not any(box.overlaps(p) for p in placed):placed.append(box);break
   else:raise AssertionError('Label overlap')
  for ext in ['pdf','png']:fig.savefig(HERE/(filename+'.'+ext),dpi=180,facecolor='white')
  plt.close(fig)
 generic=['Detection','Element recognition (Q1)','Change recognition (Q2)','Interpretation']
 group=[]
 for scope,name,color,marker in [('all_trials','All trials (72)','#0072B2','o'),('animated_trials','Animated trials (48)','#D55E00','D'),('no_animation','No-animation (24)','#555555','P')]:
  z=scopes[scope];group.append((scope,name,color,marker,{m:z[m].mean() for m in ORDER}))
 animated_labels=['Detection (onset+completion)']+generic[1:]
 ntlabels=['Detection (no press)','Element recognition (Q1)','Change recognition (Q2)','Interpretation']
 draw(group,[generic,['Detection (onset + completion)']+generic[1:],ntlabels],'cross_outcome_compound',True)
 group=[]
 for c,name,color,marker in [('V1','Sun-to-moon animation (16 trials)','#009E73','o'),('V2','Buildings animation (16 trials)','#6A51A3','s'),('V3','Red-sphere animation (16 trials)','#CC79A7','^')]:
  z=a[a.condition==c];group.append((c,name,color,marker,{m:z[m].mean() for m in ORDER}))
 draw(group,[animated_labels]*3,'animation_mean_scores_compound')
 receipt={'status':'passed','source':str(SOURCE),'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'compound_definition':'Animated S = (onset + completion) / 2; NT S remains binary correct rejection','family':'18 cross-outcome comparisons; 6 pairs per scope','checks':['72/48/24 trials and 24 participants per scope','16 trials per animation','compound identity and missingness','participant-level paired tests','independent beta-tail / binomial arithmetic','manual Holm matches statsmodels','all 18 raw and adjusted results match retained 18-family package','all figure value labels clear of connecting lines'],'separate_phase_tests':'Existing onset/completion inference remains unchanged, outside this replacement cross-outcome family','interpretation':'provisional post hoc operational score comparisons; no common ability scale or temporal trend'}
 (HERE/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(t[['scope','x','y','gap','holm_p']].to_string(index=False));print('PASS')
if __name__=='__main__':main()
