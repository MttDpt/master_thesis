"""Descriptive RQ1 contact extension, controlled by current specification section 8.
Run: uv run --with numpy --with pandas --with matplotlib run_analysis.py
No significance tests; outputs are provisional until user approval.
"""
from pathlib import Path
import hashlib, json, sys, platform
import numpy as np
import pandas as pd

RUN = Path(__file__).resolve().parent
ROOT = next(p for p in Path(__file__).resolve().parents if (p / "analysis").is_dir() and (p / "overleaf").is_dir())
NAMES = {'V1':'sun-to-moon animation', 'V2':'buildings animation',
         'V3':'red-sphere animation', 'NT':'no-animation'}
METRICS = ['share_percent','total_ambient_s','median_contact_ms','longest_contact_ms',
           'contact_count','frequency_per_valid_min']
HASHES, CHECKS = {}, []

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def read(p):
    p = ROOT/p
    HASHES[str(p.relative_to(ROOT))] = sha(p)
    return pd.read_csv(p)

def check(name, ok, detail=''):
    CHECKS.append(dict(check=name, passed=bool(ok), detail=str(detail)))
    if not ok:
        raise AssertionError(f'{name}: {detail}')

def save(d, name):
    d.to_csv(RUN/f'{name}.csv',index=False,float_format='%.12g')

def classify(d):
    x,y=d.X.to_numpy(),d.Y.to_numpy()
    usable=(~d.GazeSource.eq('Invalid') & ~d.Status.isin(['Invalid','off-display','off_display'])
            & ~d.spatial_region.isin(['unclassified','off-display','off_display'])).to_numpy()
    inside=np.isfinite(x)&np.isfinite(y)&(x>=0)&(x<3840)&(y>=0)&(y<656)
    return np.where(usable&inside,np.where(x<1280,'driver_axis','ambient_display'),'off_display')

def construct(t, state):
    """Return sample-centred interval halves and ambient run IDs for full stream."""
    dt=np.diff(t); ok=(dt>0)&(dt<=.025); mid=(t[:-1]+t[1:])/2
    starts=np.concatenate([t[:-1][ok],mid[ok]])
    ends=np.concatenate([mid[ok],t[1:][ok]])
    sample_idx=np.concatenate([np.flatnonzero(ok),np.flatnonzero(ok)+1])
    order=np.argsort(starts,kind='stable')
    starts,ends,sample_idx=starts[order],ends[order],sample_idx[order]
    cid=np.full(len(t),-1,dtype=int); runs=[]; current=-1
    for i in range(len(t)):
        if state[i]!='ambient_display':
            continue
        if i==0 or state[i-1]!='ambient_display' or t[i]-t[i-1]>.025:
            current+=1; runs.append([])
        cid[i]=current; runs[current].append(i)
    contacts=[]
    for j,indices in enumerate(runs):
        sel=cid[sample_idx]==j
        first,last=indices[0],indices[-1]
        contacts.append(dict(contact_id=j,first_sample_s=t[first],last_sample_s=t[last],
                             samples=len(indices),isolated=len(indices)==1,
                             support_start_s=min(t[first],starts[sel].min()) if sel.any() else t[first],
                             support_end_s=max(t[last],ends[sel].max()) if sel.any() else t[last],
                             full_duration_ms=1000*(ends[sel]-starts[sel]).sum(),
                             starts_after_long_gap=first>0 and t[first]-t[first-1]>.025,
                             ends_before_long_gap=last<len(t)-1 and t[last+1]-t[last]>.025))
    return starts,ends,sample_idx,cid,contacts

def measure(t,state,built,a,b):
    starts,ends,idx,cid,runs=built
    duration=np.maximum(0,np.minimum(ends,b)-np.maximum(starts,a))
    totals={s:float(duration[state[idx]==s].sum()) for s in ['ambient_display','driver_axis','off_display']}
    rows=[]
    for r in runs:
        j=r['contact_id']; samples=(cid==j)&(t>=a)&(t<b)
        amount=float(duration[cid[idx]==j].sum())
        if not samples.any() and amount<=0:
            continue
        rows.append({**r,'window_duration_ms':amount*1000,'samples_in_window':int(samples.sum()),
                     'carried_in':r['first_sample_s']<a,
                     'clipped_start':r['support_start_s']<a,
                     'clipped_end':r['support_end_s']>b,
                     'zero_allocated_duration':amount==0})
    mask=(t>=a)&(t<b); recorded=int(mask.sum()); valid=int((mask&(state!='off_display')).sum())
    expected=(b-a)*60; denom=totals['ambient_display']+totals['driver_axis']
    coverage=valid/expected if expected>0 else np.nan
    evaluable=expected>0 and coverage>=.8 and denom>0
    status='evaluable' if evaluable else ('indeterminate_zero_window' if expected==0 else
            'indeterminate_low_coverage' if coverage<.8 else 'indeterminate_no_valid_duration')
    contacts=np.array([r['window_duration_ms'] for r in rows]); n=len(rows)
    gaps=np.diff(t); gapmask=(t[:-1]<b)&(t[1:]>a)&(gaps>.025)
    result=dict(start_s=a,end_s=b,window_length_s=b-a,status=status,
                recorded_samples=recorded,valid_samples=valid,expected_samples=expected,
                coverage_percent=100*coverage,off_display_samples=recorded-valid,
                off_display_recorded_percent=100*(recorded-valid)/recorded if recorded else np.nan,
                missing_samples=max(0,expected-recorded),recorded_excess_samples=max(0,recorded-expected),
                valid_duration_s=denom,allocated_ambient_s=totals['ambient_display'],
                driver_duration_s=totals['driver_axis'],off_display_duration_s=totals['off_display'],
                unassigned_duration_s=b-a-sum(totals.values()),gaps_over_25ms=int(gapmask.sum()),
                largest_gap_ms=1000*gaps[gapmask].max() if gapmask.any() else 0,
                observed_contact_count=n,isolated_contacts=sum(r['isolated'] for r in rows),
                zero_duration_contacts=sum(r['zero_allocated_duration'] for r in rows),
                carried_in_contacts=sum(r['carried_in'] for r in rows),
                clipped_start_contacts=sum(r['clipped_start'] for r in rows),
                clipped_end_contacts=sum(r['clipped_end'] for r in rows),
                share_percent=100*totals['ambient_display']/denom if evaluable else np.nan,
                total_ambient_s=totals['ambient_display'] if evaluable else np.nan,
                median_contact_ms=float(np.median(contacts)) if evaluable and n else np.nan,
                longest_contact_ms=float(contacts.max()) if evaluable and n else np.nan,
                contact_count=n if evaluable else np.nan,
                frequency_per_valid_min=n/(denom/60) if evaluable else np.nan)
    return result,rows

def boundary_checks():
    def m(t,s,a,b):
        t=np.array(t);s=np.array(s);return measure(t,s,construct(t,s),a,b)
    A,D='ambient_display','driver_axis'
    r,c=m([0,.02,.04],[A,A,D],.015,.035)
    check('carried in counted once and clipped',len(c)==1 and c[0]['carried_in'] and c[0]['clipped_start'] and np.isclose(r['allocated_ambient_s'],.015))
    r,c=m([0,.026],[A,A],0,.03)
    check('gap splits isolated zero-duration contacts',len(c)==2 and all(x['isolated'] and x['zero_allocated_duration'] for x in c) and r['allocated_ambient_s']==0)
    r,c=m([0,.025],[A,A],0,.025)
    check('25ms included, half-open sample count',len(c)==1 and c[0]['samples_in_window']==1 and np.isclose(c[0]['window_duration_ms'],25))
    r,c=m([0,.02],[A,D],.01,.02)
    check('midpoint boundary assigns later driver sample',len(c)==0 and r['allocated_ambient_s']==0)
    r,c=m([.01,.03],[D,A],.015,.025)
    check('sample outside window can contribute clipped contact',len(c)==1 and c[0]['samples_in_window']==0 and np.isclose(c[0]['window_duration_ms'],5))
    t=np.arange(0,1.001,.01);s=np.repeat(D,len(t));r,c=measure(t,s,construct(t,s),0,1)
    check('adequate no-contact is zero with undefined duration summaries',r['status']=='evaluable' and all(r[k]==0 for k in ['share_percent','total_ambient_s','contact_count','frequency_per_valid_min']) and np.isnan(r['median_contact_ms']))
    r,c=measure(t,s,construct(t,s),0,0)
    check('zero-length event remains indeterminate',r['status']=='indeterminate_zero_window')

def derive():
    cross=read('analysis/dataset/trial-data/trial-data-crosswalk/72-trial-map.csv')
    cross=cross[cross.inclusion_status.eq('included')]
    trig=read('analysis/dataset/trigger-data/trigger-data-cleaning/trigger_trials.csv')
    manifest=read('analysis/dataset/gaze-data/gaze-data-cleaning/manifest.csv')
    check('72 unique included trials and 24 participants',len(cross)==72 and cross.participant_trial_key.is_unique and cross.participant_id.nunique()==24)
    check('condition denominators',cross.final_condition.value_counts().to_dict()=={'NT':24,'V1':16,'V2':16,'V3':16})
    check('excluded participants absent',not cross.participant_id.isin(['P00','P06','P07']).any())
    joined=cross.merge(trig,on='participant_trial_key',validate='one_to_one',suffixes=('','_trigger'))
    check('trigger crosswalk mapping',len(joined)==72 and joined.final_condition.eq(joined.condition).all() and joined.participant_id.eq(joined.participant_id_trigger).all())
    windows,clipped,full,provenance=[],[],[],[]
    for r in joined.sort_values('participant_trial_key').itertuples():
        key=r.participant_trial_key; name=f'{key}_gaze.csv';path='analysis/dataset/gaze-data/gaze-data-cleaning/'+name
        d=read(path);entry=manifest[manifest.derived_file.eq(name)]
        check(key+' manifest identity',len(entry)==1 and sha(ROOT/path)==entry.iloc[0].derived_sha256 and len(d)==entry.iloc[0].row_count)
        t=d.Timestamp_ms.to_numpy()/1000; state=classify(d)
        check(key+' labels and ordered timestamps',np.array_equal(state,d.spatial_region.str.replace('-','_')) and np.isfinite(t).all() and (np.diff(t)>0).all())
        keep=(t>=0)&(t<=120);t=t[keep];state=state[keep];built=construct(t,state)
        provenance.append(dict(participant_trial_key=key,gaze_source_id=r.gaze_source_id,derived_file=path,sha256=HASHES[path],retained_samples=len(t),min_s=t.min(),max_s=t.max(),full_contact_count=len(built[4]),long_gap_splits=sum(x['starts_after_long_gap'] for x in built[4])))
        full.extend(dict(participant_trial_key=key,condition=r.condition,**x) for x in built[4])
        if r.condition=='NT':
            press_group='any_press' if int(r.retained_press_count)>0 else 'no_press'
            check(key+' NT press flag',bool(r.any_press)==(press_group=='any_press'))
            early_group=late_group=press_group
        else:
            early_group='missed' if r.onset_status=='miss' else r.onset_status
            late_group='missed' if r.completion_status=='miss' else r.completion_status
            check(key+' fixed outcome labels',early_group in ['detected','missed'] and late_group in ['detected','missed'])
        specs=[('fixed_30_90',30.,90.,early_group),
               ('fixed_90_120',90.,120.,late_group)]
        if r.condition=='NT':
            specs.append(('nt_full_trial',0.,120.,press_group))
        else:
            for event,a,deadline in [('onset',30.,90.),('completion',90.,120.)]:
                raw_status=getattr(r,event+'_status');status='missed' if raw_status=='miss' else raw_status;press=getattr(r,event+'_press_s')
                check(key+' '+event+' valid outcome',status in ['detected','missed'] and (np.isfinite(press) and a<=press<deadline if status=='detected' else pd.isna(press)))
                specs.append((event,a,float(press) if status=='detected' else deadline,status))
        for kind,a,b,outcome in specs:
            row,contacts=measure(t,state,built,a,b)
            meta=dict(window_id=key+'_'+kind,participant_trial_key=key,participant_id=r.participant_id,condition=r.condition,window=kind,detection_status=outcome)
            windows.append({**meta,**row});clipped.extend({**meta,'window_status':row['status'],**x} for x in contacts)
            check(meta['window_id']+' contact duration sum',np.isclose(sum(x['window_duration_ms'] for x in contacts)/1000,row['allocated_ambient_s'],atol=1e-10))
    w=pd.DataFrame(windows);c=pd.DataFrame(clipped)
    check('264 unique windows: 144 fixed, 96 event, 24 NT context',len(w)==264 and w.window_id.is_unique and w.window.value_counts().to_dict()=={'fixed_30_90':72,'fixed_90_120':72,'onset':48,'completion':48,'nt_full_trial':24})
    early=w[w.window=='fixed_30_90']
    check('30–90 fixed endpoints and all eligible trials',early.participant_trial_key.nunique()==72 and early.start_s.eq(30).all() and early.end_s.eq(90).all() and early.condition.value_counts().to_dict()=={'NT':24,'V1':16,'V2':16,'V3':16})
    check('no NT pseudo-events',not ((w.condition=='NT')&w.window.isin(['onset','completion'])).any())
    check('17 completion detections',len(w[(w.window=='completion')&(w.detection_status=='detected')])==17)
    check('window duration partitions',np.allclose(w.valid_duration_s+w.off_display_duration_s+w.unassigned_duration_s,w.window_length_s,atol=1e-9) and (w.unassigned_duration_s>=-1e-9).all())
    ev=w[w.status=='evaluable'];ind=w[w.status!='evaluable']
    check('indeterminate measures are NaN',ind[METRICS].isna().all().all())
    check('share and frequency invariants',np.allclose(ev.share_percent,100*ev.total_ambient_s/ev.valid_duration_s) and np.allclose(ev.frequency_per_valid_min,60*ev.contact_count/ev.valid_duration_s) and ev.share_percent.between(0,100).all())
    check('positive valid duration and >=80% coverage',((ev.valid_duration_s>0)&(ev.coverage_percent>=80)).all())
    count=c.groupby('window_id').size().reindex(w.window_id,fill_value=0).to_numpy()
    check('one row per overlapping full contact',not c.duplicated(['window_id','contact_id']).any() and np.array_equal(count,w.observed_contact_count))
    old=read('analysis/RQ1/20261002-fixed-period-gaze-bootstrap/tables/trial_period_measures.csv')
    old=old[old.period=='90–120']
    comparison=w[w.window=='fixed_90_120'].merge(old,on='participant_trial_key',validate='one_to_one',suffixes=('','_reference'))
    comparison['share_difference_pp']=comparison.share_percent-comparison.share_percent_reference
    comparison['ambient_difference_s']=comparison.allocated_ambient_s-comparison.ambient_duration_s
    check('48 fixed animated windows reproduce previous status/share/duration',len(comparison)==48 and comparison.status.eq(comparison.status_reference).all() and np.allclose(comparison.share_percent,comparison.share_percent_reference,equal_nan=True,atol=1e-8) and np.allclose(comparison.allocated_ambient_s,comparison.ambient_duration_s,atol=1e-8))
    save(comparison[['participant_trial_key','condition','status','share_difference_pp','ambient_difference_s']],'fixed_reconciliation')
    prior=read('analysis/RQ1/20261002-fixed-period-gaze-bootstrap/tables/trial_period_measures.csv')
    prior=prior[prior.period=='30–90']
    early_comparison=early.merge(prior,on='participant_trial_key',validate='one_to_one',suffixes=('','_reference'))
    early_comparison['share_difference_pp']=early_comparison.share_percent-early_comparison.share_percent_reference
    early_comparison['ambient_difference_s']=early_comparison.allocated_ambient_s-early_comparison.ambient_duration_s
    check('48 early fixed animated windows reproduce previous status/share/duration',len(early_comparison)==48 and early_comparison.status.eq(early_comparison.status_reference).all() and np.allclose(early_comparison.share_percent,early_comparison.share_percent_reference,equal_nan=True,atol=1e-8) and np.allclose(early_comparison.allocated_ambient_s,early_comparison.ambient_duration_s,atol=1e-8))
    save(early_comparison[['participant_trial_key','condition','status','share_difference_pp','ambient_difference_s']],'fixed_30_90_reconciliation')
    oldevents=read('analysis/RQ1/response-tables/gaze_events.csv')
    events=w[w.window.isin(['onset','completion'])].merge(oldevents,left_on=['participant_trial_key','window'],right_on=['participant_trial_key','event'],validate='one_to_one',suffixes=('','_historical'))
    events['same_window']=np.isclose(events.start_s,events.anchor_s)&np.isclose(events.end_s,events.end_s_historical)
    events['ambient_difference_s']=events.allocated_ambient_s-events.ambient_duration_s
    events['valid_difference_s']=events.valid_duration_s-events.valid_duration_s_historical
    events['share_difference_pp']=events.share_percent-100*events.ambient_layer_share
    events['outcome_changed']=events.detection_status.eq('detected')!=events.detected
    same=events[events.same_window]
    check('historical event same-window allocations reconcile',len(events)==96 and np.allclose(same.allocated_ambient_s,same.ambient_duration_s,atol=1e-8) and np.allclose(same.valid_duration_s,same.valid_duration_s_historical,atol=1e-8) and np.allclose(same.share_percent,100*same.ambient_layer_share,equal_nan=True,atol=1e-8))
    save(events[['participant_trial_key','window','same_window','outcome_changed','detection_status','detected','end_s','end_s_historical','ambient_difference_s','valid_difference_s','share_difference_pp']],'event_reconciliation')
    save(w,'window_measures');save(c,'window_contacts');save(pd.DataFrame(full),'full_trial_contacts');save(pd.DataFrame(provenance),'provenance')
    return w,c

def summarize(w):
    rows=[]
    for window in ['fixed_30_90','fixed_90_120','onset','completion','nt_full_trial']:
        for condition in NAMES:
            d=w[(w.window==window)&(w.condition==condition)]
            if window=='nt_full_trial' and condition!='NT':
                continue
            if condition=='NT' and window in ['fixed_30_90','fixed_90_120','nt_full_trial']:
                groups=['combined','no_press','any_press']
            elif condition!='NT' and window in ['fixed_30_90','fixed_90_120','onset','completion']:
                groups=['combined','detected','missed']
            else:
                groups=['combined']
            for group in groups:
                g=d if group=='combined' else d[d.detection_status==group];ev=g[g.status=='evaluable']
                row=dict(window=window,condition=condition,condition_name=NAMES[condition],outcome_group=group,
                         applicability='not_applicable' if condition=='NT' and window in ['onset','completion'] else 'applicable',eligible=len(g),evaluable=len(ev),
                         indeterminate=len(g)-len(ev),zero_contact_windows=int((ev.contact_count==0).sum()),
                         windows_with_contacts=int((ev.contact_count>0).sum()))
                for metric in METRICS+['window_length_s','valid_duration_s','coverage_percent']:
                    vals=ev[metric].dropna()
                    for stat,q in [('q1',.25),('median',.5),('q3',.75)]:
                        row[metric+'_'+stat]=vals.quantile(q,interpolation='linear') if len(vals) else np.nan
                rows.append(row)
    s=pd.DataFrame(rows);save(s,'condition_summary');return s

def main():
    boundary_checks();w,c=derive();s=summarize(w)
    for p,h in HASHES.items():
        check('input unchanged '+p,sha(ROOT/p)==h)
    for p in ['analysis/contract_RQ1.md','analysis/rules_preprocessing.md']:
        HASHES[p]=sha(ROOT/p)
    save(pd.DataFrame(CHECKS),'validation_checks')
    (RUN/'source_hashes.json').write_text(json.dumps(HASHES,indent=2)+'\n')
    receipt=dict(status='provisional',validation='passed',checks=len(CHECKS),eligible_trials=72,participants=24,
                 fixed_windows=144,fixed_windows_per_period=72,event_windows=96,nt_context_windows=24,
                 evaluable_by_window=w[w.status=='evaluable'].window.value_counts().to_dict(),
                 full_contact_count=int(pd.read_csv(RUN/'full_trial_contacts.csv').shape[0]),
                 window_contact_rows=len(c),isolated_window_contacts=int(c.isolated.sum()),
                 zero_duration_window_contacts=int(c.zero_allocated_duration.sum()),
                 clipped_start_rows=int(c.clipped_start.sum()),clipped_end_rows=int(c.clipped_end.sum()),
                 maximum_fixed_share_difference_pp=float(pd.read_csv(RUN/'fixed_reconciliation.csv').share_difference_pp.abs().max()),
                 python=sys.version,numpy=np.__version__,pandas=pd.__version__,platform=platform.platform(),
                 code_sha256=sha(Path(__file__)),thread_id='01a1025b-463b-7fd0-910d-691fb08050af',
                 aggregation='Linear quartiles of evaluable window measures, no pooled contacts; individual-duration summaries use windows with contacts.',
                 boundary='Recorded ambient contacts, not verified fixations or intentional glances; no significance tests or causal/outcome modelling.')
    (RUN/'validation_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(s[['window','condition','outcome_group','eligible','evaluable','indeterminate','zero_contact_windows','share_percent_median','total_ambient_s_median','frequency_per_valid_min_median']].to_string(index=False))
    print(f'Passed {len(CHECKS)} checks')

if __name__=='__main__':
    main()
