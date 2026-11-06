"""Reconcile retained 120 s animated presses with the half-open event window."""
from pathlib import Path
import pandas as pd

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "analysis").is_dir() and (p / "overleaf").is_dir())
CLEAN = Path(__file__).resolve().parent
OVERALL = CLEAN.parent / "trigger-data-overall"
KEYS = {"P02_t1", "P10_t1", "P13_t2", "P19_t3"}


def main():
    trials = pd.read_csv(CLEAN / "trigger_trials.csv")
    presses = pd.read_csv(CLEAN / "trigger_presses.csv")
    crosswalk = pd.read_csv(ROOT / "analysis/dataset/trial-data/trial-data-crosswalk/72-trial-map.csv")
    boundary = presses.condition.ne("NT") & presses.press_time_s.eq(120)
    assert set(presses.loc[boundary, "participant_trial_key"]) == KEYS
    for row in presses.loc[boundary].itertuples():
        source = crosswalk.loc[crosswalk.participant_trial_key.eq(row.participant_trial_key), "trigger_times_s"].iloc[0]
        assert 120 in [float(t) for t in str(source).split("|")]
    presses.loc[boundary, "classification"] = "trial_end"
    trials.loc[trials.participant_trial_key.isin(KEYS), ["completion_status", "completion_press_s", "completion_latency_s"]] = ["miss", float("nan"), float("nan")]
    assert presses.groupby("participant_trial_key").size().reindex(trials.participant_trial_key, fill_value=0).to_numpy().tolist() == trials.retained_press_count.to_numpy().tolist()
    presses.to_csv(CLEAN / "trigger_presses.csv", index=False, float_format="%.3f")
    trials.to_csv(CLEAN / "trigger_trials.csv", index=False, float_format="%.3f")

    diag = pd.read_csv(OVERALL / "trial_diagnostics.csv")
    diag.loc[diag.participant_trial_key.isin(KEYS), ["completion_status", "completion_press_s", "completion_latency_s", "completion_press_count"]] = ["miss", float("nan"), float("nan"), 0]
    diag.to_csv(OVERALL / "trial_diagnostics.csv", index=False)
    participant = pd.read_csv(OVERALL / "participant_event_summary.csv")
    affected = participant.participant_trial_key.isin(KEYS)
    participant.loc[affected, "completion_detected"] = False
    participant.loc[affected, "completion_latency_s"] = float("nan")
    participant.loc[affected, "detected_events"] = participant.loc[affected, "onset_detected"].astype(int)
    participant.to_csv(OVERALL / "participant_event_summary.csv", index=False)
    counts = presses.groupby(["condition", "classification"]).size().to_dict()
    classes = pd.read_csv(OVERALL / "press_classification_by_condition.csv")
    classes.loc[classes.classification.eq("completion") & classes.condition.eq("V3"), "count"] = counts["V3", "completion"]
    classes.loc[classes.classification.eq("completion") & classes.condition.eq("V2"), "count"] = counts["V2", "completion"]
    classes = classes.loc[classes.classification.ne("trial_end")]
    classes = pd.concat([classes, pd.DataFrame([{"condition": c, "classification": "trial_end", "count": counts.get((c, "trial_end"), 0)} for c in ["V1", "V2", "V3"]])], ignore_index=True)
    classes.to_csv(OVERALL / "press_classification_by_condition.csv", index=False)
    summary = pd.read_csv(OVERALL / "participant_press_summary.csv")
    for column, cls in [("completion_presses", "completion"), ("extra_presses", "extra")]:
        mapped = presses.loc[presses.classification.eq(cls)].groupby("participant_id").size()
        summary[column] = summary.participant_id.map(mapped).fillna(0).astype(int)
    summary.to_csv(OVERALL / "participant_press_summary.csv", index=False)
    print("reconciled 4 retained trial-end presses; completion detections 17/48")


def sync_overall_from_rq1():
    """Call after the revised RQ1 bootstrap has been recomputed."""
    out = ROOT / "analysis/RQ1/response-tables"
    detection = pd.read_csv(out / "detection_summary.csv")
    reaction = pd.read_csv(out / "reaction_time_summary.csv")
    detection = detection.loc[detection.condition.ne("pooled")].rename(columns={
        "proportion": "detection_rate", "low": "cluster_boot_ci_low", "high": "cluster_boot_ci_high"})
    detection["missed_n"] = detection.eligible_n - detection.detected_n
    detection = detection[["condition", "event", "eligible_n", "detected_n", "missed_n", "detection_rate", "cluster_boot_ci_low", "cluster_boot_ci_high"]]
    assert int(detection.loc[detection.event.eq("completion"), "detected_n"].sum()) == 17
    detection.to_csv(OVERALL / "event_detection_by_condition.csv", index=False)
    reaction = reaction.loc[reaction.condition.ne("pooled")].rename(columns={
        "n": "detected_n", "median": "median_latency_s", "q1": "q1_latency_s", "q3": "q3_latency_s",
        "min": "min_latency_s", "max": "max_latency_s", "low": "cluster_boot_median_ci_low_s", "high": "cluster_boot_median_ci_high_s"})
    reaction = reaction[["condition", "event", "detected_n", "median_latency_s", "q1_latency_s", "q3_latency_s", "min_latency_s", "max_latency_s", "cluster_boot_median_ci_low_s", "cluster_boot_median_ci_high_s"]]
    reaction.to_csv(OVERALL / "latency_by_condition_event.csv", index=False)


if __name__ == "__main__":
    import sys
    if sys.argv[1:] == ["--sync-overall"]:
        sync_overall_from_rq1()
        raise SystemExit
    main()
