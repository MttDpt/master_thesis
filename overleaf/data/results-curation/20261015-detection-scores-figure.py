import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
import sys
out=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent
out.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False,'axes.linewidth':.7})
x=np.arange(4); w=.25
fig,ax=plt.subplots(figsize=(10,4.9)); fig.subplots_adjust(left=.085,right=.985,top=.84,bottom=.20)
for vals,offset,edge,fill,marker,label in [([40/48,1,13/16,11/16],-w/2,'#008FE8','#C0DCEA','o','Changes happening (30–90 s)'),([17/48,5/16,5/16,7/16],w/2,'#FF6500','#F7D9C2','D','Changes finished (90–120 s)')]:
 ax.bar(x+offset,vals,w,color=fill,edgecolor=edge,linewidth=.9,zorder=3)
 ax.plot(x+offset,vals,linestyle='None',marker=marker,markersize=4,markerfacecolor=fill,markeredgecolor=edge,markeredgewidth=.75,zorder=4)
 for pos,val in zip(x+offset,vals):
  txt=str(Decimal(str(val)).quantize(Decimal('.001'),rounding=ROUND_HALF_UP))
  ax.text(pos,val+.025,txt,ha='center',va='bottom',fontsize=8,color=edge)
 ax.plot([],[],color=edge,marker=marker,markersize=4,markerfacecolor=fill,markeredgewidth=.75,linewidth=.8,label=label)
for pos,y,stars,p in zip(x,[.965,1.135,.945,.825],['**','**','*',''],['< 0.01','< 0.01','< 0.05','≥ 0.05 (NS)']):
 ax.plot([pos-w/2,pos-w/2,pos+w/2,pos+w/2],[y-.012,y,y,y-.012],color='#666666',linewidth=.8)
 ax.text(pos,y+.009,r'$p_{\mathrm{Holm}}$'+(' '+stars if stars else '')+'\n'+p,ha='center',va='bottom',fontsize=7.5,color='#4F4F4F',linespacing=1.12)
ax.axvline(.5,color='#BDBDBD',lw=.7,ls=':')
ax.set_ylim(0,1.28); ax.set_yticks(np.arange(0,1.01,.2)); ax.set_yticklabels([f'{v:.1f}' for v in np.arange(0,1.01,.2)])
ax.set_xlim(-.55,3.55); ax.set_ylabel('Mean detection score (1 = detected, 0 = missed)',fontsize=9)
ax.set_xticks(x,['All animated trials\n(48 trials)','Sun-to-moon\n(16 trials)','Buildings\n(16 trials)','Red-sphere\n(16 trials)']); ax.tick_params(axis='both',length=2.5,width=.6,labelsize=8)
ax.set_xlabel('Onset versus completion within each group',fontsize=9,labelpad=9)
ax.set_axisbelow(True); ax.grid(axis='y',color='#E5E5E5',linewidth=.65)
ax.legend(loc='lower center',bbox_to_anchor=(.5,1.025),ncol=2,frameon=False,fontsize=8,handlelength=2.2,columnspacing=2)
for ext in ['png','pdf','svg']: fig.savefig(out/f'detection_scores_matched.{ext}',dpi=220,facecolor='white')
print(out/'detection_scores_matched.png')
