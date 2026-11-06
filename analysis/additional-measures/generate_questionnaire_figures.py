import csv, html, re, zipfile
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "analysis").is_dir() and (p / "overleaf").is_dir())
OUT = Path(__file__).resolve().parent
OUT.mkdir(parents=True, exist_ok=True)
FIG = OUT/'assets'
FIG.mkdir(parents=True, exist_ok=True)

def read_xlsx_sheet(path, sheet_name):
    import xml.etree.ElementTree as ET
    ns = {'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    with zipfile.ZipFile(path) as z:
        strings=[]
        if 'xl/sharedStrings.xml' in z.namelist():
            root=ET.fromstring(z.read('xl/sharedStrings.xml'))
            strings=[''.join(t.text or '' for t in si.iter('{%s}t'%ns['m'])) for si in root.findall('m:si',ns)]
        wb=ET.fromstring(z.read('xl/workbook.xml'))
        rel=ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
        rels={x.attrib['Id']:x.attrib['Target'] for x in rel}
        target=None
        for s in wb.find('m:sheets',ns):
            if s.attrib['name']==sheet_name:
                target='xl/'+rels[s.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']]
        root=ET.fromstring(z.read(target))
        rows=[]
        for row in root.findall('.//m:sheetData/m:row',ns):
            vals={}
            for c in row.findall('m:c',ns):
                ref=c.attrib['r']; col=re.sub(r'\d','',ref); v=c.find('m:v',ns)
                val='' if v is None else v.text
                if c.attrib.get('t')=='s' and val!='': val=strings[int(val)]
                vals[col]=val
            if vals: rows.append(vals)
        cols=sorted({c for r in rows for c in r}, key=lambda x:(len(x),x))
        return pd.DataFrame([[r.get(c,'') for c in cols] for r in rows[1:]], columns=rows[0].values())

def sd(x):
    return float(np.std(np.asarray(x, dtype=float), ddof=1))

# NASA-TLX: response export has trial number but not condition; the canonical workbook supplies the condition key.
nasa = read_xlsx_sheet(ROOT/'analysis/dataset/originals/questionnaire-data/data-aggregated.xlsx', '03_NASA')
nasa.columns=[str(c).strip() for c in nasa.columns]
nasa = nasa[['Participant ID','Trial number','Condition','Mental Demand','Physical Demand','Temporal  Demand','Performance','Effort','Frustration']]
nasa = nasa[pd.to_numeric(nasa['Trial number'], errors='coerce').notna()].copy()
nasa['Participant ID'] = nasa['Participant ID'].astype(str).str.strip()
nasa['Trial number'] = pd.to_numeric(nasa['Trial number']).astype(int)
trial_map = pd.read_csv(ROOT/'analysis/dataset/trial-data/trial-data-crosswalk/72-trial-map.csv',
                        usecols=['participant_id','trial_number','final_condition','inclusion_status'])
trial_map = trial_map[trial_map['inclusion_status'].eq('included')]
joined = nasa.merge(trial_map, left_on=['Participant ID','Trial number'],
                    right_on=['participant_id','trial_number'], how='outer',
                    validate='one_to_one', indicator=True)
assert len(trial_map) == 72 and (joined['_merge'] == 'right_only').sum() == 0
excluded = joined.loc[joined['_merge'].eq('left_only'), 'Participant ID']
assert excluded.value_counts().to_dict() == {'P06': 3, 'P07': 3}
nasa = joined[joined['_merge'].eq('both')].copy()
assert len(nasa) == 72 and nasa['Condition'].eq(nasa['final_condition']).all()
assert nasa['Condition'].value_counts().to_dict() == {'NT': 24, 'V1': 16, 'V2': 16, 'V3': 16}
dim=['Mental Demand','Physical Demand','Temporal  Demand','Performance','Effort','Frustration']
for c in dim: nasa[c]=pd.to_numeric(nasa[c], errors='coerce')
nasa['overall']=nasa[dim].mean(axis=1)
conditions=['NT','V1','V2','V3']
rows=[]
for cond in conditions:
    sub=nasa[nasa['Condition']==cond]
    for metric in dim+['overall']:
        rows.append({'condition':cond,'metric':metric,'n':sub[metric].notna().sum(),'mean':sub[metric].mean(),'sd':sd(sub[metric].dropna())})
nasa_summary=pd.DataFrame(rows)
nasa_summary.to_csv(OUT/'nasa_tlx_summary.csv',index=False)

plt.rcParams.update({'font.family':'DejaVu Sans','axes.spines.top':False,'axes.spines.right':False,'axes.facecolor':'white','figure.facecolor':'white'})
colors={'NT':'#7f8c8d','V1':'#0072B2','V2':'#009E73','V3':'#D55E00'}
metrics=dim+['overall']; labels=['Mental demand','Physical demand','Temporal demand','Performance','Effort','Frustration','Overall']
fig, ax=plt.subplots(figsize=(11.5,6.5), dpi=180)
x=np.arange(len(metrics)); w=0.19
for j,cond in enumerate(conditions):
    d=nasa_summary[nasa_summary.condition==cond].set_index('metric').loc[metrics]
    ax.bar(x+(j-1.5)*w,d['mean'],w,yerr=d['sd'],capsize=3,label=cond,color=colors[cond],edgecolor='white',linewidth=.6,error_kw={'elinewidth':1,'capthick':1})
ax.set_ylabel('NASA-TLX score (1–10)'); ax.set_xlabel('NASA-TLX dimension')
ax.set_xticks(x,labels,rotation=20,ha='right'); ax.set_ylim(0,10.5); ax.set_yticks(np.arange(0,11,2)); ax.grid(axis='y',color='#d9d9d9',linewidth=.7); ax.set_axisbelow(True)
ax.legend(title='Condition',ncol=4,frameon=False,loc='upper center',bbox_to_anchor=(0.5,1.10)); fig.tight_layout(); fig.savefig(FIG/'nasa_tlx_by_condition.png',bbox_inches='tight'); fig.savefig(FIG/'nasa_tlx_by_condition.svg',bbox_inches='tight'); plt.close(fig)

# UEQ: post-playback original UEQ has no condition field, so only an overall product score is estimable.
ueq=pd.read_csv(ROOT/'tmp/questionnaires/ueq.csv')
ueq=ueq[ueq['Participant ID'].notna() & ~ueq['Participant ID'].astype(str).isin(['?',''])].copy()
items=ueq.columns[2:]
raw=ueq[items].apply(pd.to_numeric, errors='coerce')
# Form order and positive direction verified from the live form labels.
positive_right=[True,True,False,False,False,True,True,True,False,False,False,False,True,True,True,True,False,False,False,True,False,True,False,False,False,True]
scores=pd.DataFrame(index=ueq.index)
for i,c in enumerate(items): scores[f'i{i+1}']=raw[c]-4 if positive_right[i] else 4-raw[c]
scale_items={'Attractiveness':[1,12,14,16,24,25],'Perspicuity':[2,4,13,21],'Efficiency':[9,20,22,23],'Dependability':[8,11,17,19],'Stimulation':[5,6,7,18],'Novelty':[3,10,15,26]}
means=[]
for scale, nums in scale_items.items():
    vals=scores[[f'i{i}' for i in nums]].mean(axis=1)
    means.append({'scale':scale,'n':vals.notna().sum(),'mean':vals.mean(),'sd':sd(vals.dropna())})
ueq_summary=pd.DataFrame(means); ueq_summary.to_csv(OUT/'ueq_summary.csv',index=False)
fig, ax=plt.subplots(figsize=(10,6.2), dpi=180)
x=np.arange(len(ueq_summary)); ax.bar(x,ueq_summary['mean'],yerr=ueq_summary['sd'],capsize=4,color=['#0072B2','#56B4E9','#009E73','#E69F00','#D55E00','#CC79A7'],edgecolor='white',linewidth=.7,error_kw={'elinewidth':1,'capthick':1},label='Overall post-playback')
ax.axhline(0,color='#555555',linewidth=.8); ax.set_ylabel('UEQ scale score (−3 to +3)'); ax.set_xlabel('UEQ scale'); ax.set_xticks(x,ueq_summary['scale']); ax.set_ylim(-3.2,3.2); ax.set_yticks(np.arange(-3,4,1)); ax.grid(axis='y',color='#d9d9d9',linewidth=.7); ax.set_axisbelow(True); ax.legend(frameon=False,loc='upper center',bbox_to_anchor=(0.5,1.10)); fig.tight_layout(); fig.savefig(FIG/'ueq_overall.png',bbox_inches='tight'); fig.savefig(FIG/'ueq_overall.svg',bbox_inches='tight'); plt.close(fig)

print(nasa_summary.to_string(index=False)); print(ueq_summary.to_string(index=False))
