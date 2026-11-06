#!/usr/bin/env python3
"""Build and validate the provisional RQ3 two-layer full-corpus package.

Manual annotations are intentionally embedded below. Raw DOCX sources and the
canonical 72-trial crosswalk are read-only inputs. Historical RQ3 coding files
are not inputs.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "analysis/RQ3/provisional/coding"
DOCX_DIR = ROOT / "analysis/dataset/originals/transcripts/trials"
MAP = ROOT / "analysis/dataset/trial-data/trial-data-crosswalk/72-trial-map.csv"
RULES = ROOT / "analysis/RQ3/provisional/coding/coding-rules.md"
PREPROCESSING = ROOT / "analysis/rules_preprocessing.md"
CONTRACT = ROOT / "analysis/contract_RQ3.md"

OBJECTS = {"sun", "moon", "stars", "sky", "hills", "buildings", "city", "sphere", "landscape", "other", "none"}
TRANSFORMATIONS = {"movement", "appearance", "disappearance", "growth", "zoom", "colour", "transition", "none"}
STAGES = {"start", "process", "end", "unclear"}
INTERPRETATIONS = {"time", "location", "destination", "warning", "weather", "fatigue", "entertainment", "notification", "assistant", "other", "none"}
CERTAINTY = {"sure", "unsure", "unknown"}
REACTIONS = {"distracting", "calming", "decorative", "confusing", "glitch", "useful"}
ACCURACY = {"full", "partial", "incorrect", "NA"}


def d(family, value, paragraph, accuracy="NA", note=""):
    return (family, value, accuracy, paragraph, note)


# Layer 1: success, specificity, failure, evidence paragraph, optional exact span.
L1 = {
    "P01_t1": ("no", "NA", "false-change", 8, None),
    "P01_t2": ("no", "NA", "alternative", 8, None),
    "P01_t3": ("no", "NA", "alternative", 4, None),
    "P02_t1": ("no", "NA", "alternative", 8, None),
    "P02_t2": ("yes", "full", "NA", 2, "I didn't notice anything."),
    "P02_t3": ("yes", "full", "NA", 8, None),
    "P03_t1": ("yes", "full", "NA", 4, None),
    "P03_t2": ("no", "NA", "unknown", 4, None),
    "P03_t3": ("yes", "partial", "NA", 4, None),
    "P04_t1": ("no", "NA", "unknown", 4, None),
    "P04_t2": ("yes", "full", "NA", 6, None),
    "P04_t3": ("yes", "full", "NA", 4, None),
    "P05_t1": ("no", "NA", "alternative", 16, None),
    "P05_t2": ("yes", "full", "NA", 24, None),
    "P05_t3": ("yes", "full", "NA", 4, "I didn't pursue anything. I thought that will be something, change might be as like before, but I didn't reach my expectation. It doesn't change anything."),
    "P08_t1": ("no", "NA", "unknown", 16, None),
    "P08_t2": ("yes", "full", "NA", 4, None),
    "P08_t3": ("yes", "full", "NA", 12, None),
    "P09_t1": ("yes", "full", "NA", 4, None),
    "P09_t2": ("no", "NA", "unknown", 4, None),
    "P09_t3": ("yes", "full", "NA", 12, None),
    "P10_t1": ("no", "NA", "alternative", 20, None),
    "P10_t2": ("yes", "full", "NA", 6, None),
    "P10_t3": ("no", "NA", "alternative", 8, None),
    "P11_t1": ("yes", "full", "NA", 8, None),
    "P11_t2": ("yes", "full", "NA", 8, None),
    "P11_t3": ("yes", "full", "NA", 4, None),
    "P12_t1": ("yes", "full", "NA", 8, None),
    "P12_t2": ("yes", "full", "NA", 4, None),
    "P12_t3": ("yes", "full", "NA", 2, "I didn't see anything this time."),
    "P13_t1": ("yes", "full", "NA", 4, None),
    "P13_t2": ("no", "NA", "alternative", 12, None),
    "P13_t3": ("yes", "full", "NA", 8, None),
    "P14_t1": ("no", "NA", "alternative", 8, None),
    "P14_t2": ("yes", "full", "NA", 3, None),
    "P14_t3": ("yes", "full", "NA", 4, None),
    "P15_t1": ("yes", "full", "NA", 2, "No, I didn't see anything."),
    "P15_t2": ("no", "NA", "unknown", 8, None),
    "P15_t3": ("no", "NA", "alternative", 8, None),
    "P16_t1": ("no", "NA", "alternative", 4, None),
    "P16_t2": ("yes", "full", "NA", 4, None),
    "P16_t3": ("yes", "full", "NA", 10, None),
    "P17_t1": ("no", "NA", "alternative", 16, None),
    "P17_t2": ("yes", "full", "NA", 4, None),
    "P17_t3": ("yes", "full", "NA", 4, None),
    "P18_t1": ("yes", "partial", "NA", 12, None),
    "P18_t2": ("yes", "partial", "NA", 16, None),
    "P18_t3": ("yes", "full", "NA", 4, None),
    "P19_t1": ("no", "NA", "false-change", 4, None),
    "P19_t2": ("no", "NA", "unknown", 12, None),
    "P19_t3": ("yes", "full", "NA", 8, None),
    "P20_t1": ("no", "NA", "alternative", 12, None),
    "P20_t2": ("no", "NA", "false-change", 8, None),
    "P20_t3": ("yes", "full", "NA", 8, None),
    "P21_t1": ("no", "NA", "false-change", 4, None),
    "P21_t2": ("no", "NA", "alternative", 16, None),
    "P21_t3": ("no", "NA", "alternative", 16, None),
    "P22_t1": ("no", "NA", "alternative", 16, None),
    "P22_t2": ("yes", "full", "NA", 4, None),
    "P22_t3": ("yes", "full", "NA", 8, None),
    "P23_t1": ("no", "NA", "alternative", 8, None),
    "P23_t2": ("no", "NA", "unknown", 8, None),
    "P23_t3": ("no", "NA", "false-change", 16, None),
    "P24_t1": ("yes", "full", "NA", 16, None),
    "P24_t2": ("yes", "partial", "NA", 12, None),
    "P24_t3": ("yes", "full", "NA", 4, None),
    "P25_t1": ("yes", "full", "NA", 12, None),
    "P25_t2": ("yes", "full", "NA", 8, None),
    "P25_t3": ("no", "NA", "false-change", 12, None),
    "P26_t1": ("yes", "full", "NA", 4, None),
    "P26_t2": ("no", "NA", "alternative", 8, None),
    "P26_t3": ("yes", "full", "NA", 20, None),
}


# Each detail row: family, value, accuracy, evidence paragraph, decision note.
# A full participant paragraph is retained as verbatim evidence unless a span is
# supplied in SPANS below. Interviewer suggestions are never used as evidence.
D = {
"P01_t1":[d("object","hills",8,"incorrect"),d("object","landscape",8,"full"),d("transformation","appearance",8,"incorrect"),d("transformation","movement",8,"incorrect"),d("stage","start",8),d("stage","process",8),d("stage","end",8),d("interpretation","none",8),d("certainty","unknown",8),d("reaction","unmentioned",8)],
"P01_t2":[d("object","hills",4,"incorrect"),d("object","landscape",4,"full"),d("transformation","zoom",4,"incorrect"),d("transformation","colour",4,"incorrect"),d("stage","process",4),d("stage","end",4),d("interpretation","other",8,note="altitude"),d("certainty","unsure",8),d("reason","object:hills -> interpretation:other(altitude)",8),d("reaction","unmentioned",8)],
"P01_t3":[d("object","sphere",4,"incorrect"),d("object","sun",4,"incorrect"),d("transformation","appearance",4,"incorrect"),d("transformation","movement",4,"incorrect"),d("stage","start",4),d("stage","process",4),d("interpretation","time",4),d("certainty","unsure",4),d("reason","object:sphere or object:sun -> interpretation:time",4,note="Participant alternatives retained"),d("reaction","unmentioned",4)],
"P02_t1":[d("object","sphere",4,"partial",note="Generic red bulb"),d("object","sun",8,"incorrect"),d("transformation","none",4),d("stage","end",4),d("interpretation","time",8),d("certainty","unsure",8),d("reason","object:sun -> interpretation:time",8),d("reaction","unmentioned",8)],
"P02_t2":[d("object","none",2),d("transformation","none",2),d("interpretation","none",2),d("certainty","sure",2),d("reaction","unmentioned",2)],
"P02_t3":[d("object","buildings",8,"full"),d("interpretation","location",8),d("certainty","sure",8),d("reason","object:buildings -> interpretation:location",8),d("reaction","unmentioned",8)],
"P03_t1":[d("object","none",4),d("transformation","none",4),d("interpretation","none",4),d("certainty","sure",4),d("reaction","unmentioned",4)],
"P03_t2":[d("object","sphere",4,"full"),d("transformation","none",4),d("interpretation","none",4),d("certainty","unknown",4),d("reaction","unmentioned",4)],
"P03_t3":[d("object","sphere",4,"partial",note="Generic yellow sphere"),d("object","stars",4,"full"),d("transformation","movement",4,"full"),d("stage","process",4),d("interpretation","time",4),d("certainty","unsure",4),d("reason","object:sphere + object:stars -> interpretation:time",4),d("reaction","unmentioned",4)],
"P04_t1":[d("object","none",4),d("transformation","colour",8,"incorrect",note="Tentative and later rejected"),d("interpretation","time",4,note="Tentative hypothesis later rejected"),d("certainty","unsure",8),d("reason","transformation:colour -> interpretation:time",4,note="Rejected by participant"),d("reaction","unmentioned",4)],
"P04_t2":[d("object","landscape",6,"full"),d("object","hills",6,"full"),d("transformation","colour",6,"full",note="Valid subtle NT background-colour animation"),d("stage","unclear",6),d("interpretation","none",6),d("certainty","unknown",6),d("reaction","unmentioned",6)],
"P04_t3":[d("object","sun",4,"full"),d("object","moon",4,"full"),d("transformation","transition",4,"full"),d("stage","process",4),d("stage","end",4),d("interpretation","time",4),d("certainty","sure",4),d("reason","object:sun + object:moon + transformation:transition -> interpretation:time",4),d("reaction","unmentioned",4)],
"P05_t1":[d("object","stars",4,"full"),d("object","moon",4,"full"),d("object","sphere",8,"partial"),d("transformation","appearance",4,"partial"),d("stage","process",4),d("interpretation","weather",16),d("certainty","unsure",16),d("reason","object:sphere -> interpretation:weather",16,note="Participant calls it sunny"),d("reaction","unmentioned",16)],
"P05_t2":[d("object","buildings",20,"full"),d("transformation","colour",20,"full",note="Orange/red report matches confirmed orange V2 buildings"),d("stage","end",20),d("interpretation","location",24),d("certainty","unsure",24),d("reason","object:buildings -> interpretation:location",24),d("reaction","unmentioned",24)],
"P05_t3":[d("object","none",4),d("transformation","none",4),d("interpretation","none",4),d("certainty","sure",4),d("reaction","unmentioned",4)],
"P08_t1":[d("object","sphere",4,"full"),d("transformation","appearance",4,"partial",note="Generic animation"),d("transformation","movement",4,"partial",note="Generic animation"),d("stage","unclear",4),d("interpretation","none",16),d("certainty","unknown",16),d("reaction","unmentioned",16)],
"P08_t2":[d("object","none",4),d("transformation","none",4),d("interpretation","none",4),d("certainty","sure",4),d("reaction","unmentioned",4)],
"P08_t3":[d("object","city",4,"full"),d("object","buildings",4,"full"),d("transformation","transition",8,"partial"),d("stage","process",8),d("interpretation","location",12),d("certainty","unsure",12),d("reason","object:city + object:buildings -> interpretation:location",12),d("reaction","unmentioned",12)],
"P09_t1":[d("object","none",4),d("transformation","none",8),d("interpretation","none",8),d("certainty","sure",8),d("reaction","unmentioned",8)],
"P09_t2":[d("object","sphere",4,"partial",note="Generic red blob"),d("transformation","movement",4,"partial"),d("transformation","disappearance",4,"partial",note="HUD shutdown described without calling it a glitch"),d("stage","process",4),d("stage","end",4),d("interpretation","none",4),d("certainty","unknown",4),d("reaction","unmentioned",4)],
"P09_t3":[d("object","sun",8,"full"),d("object","stars",12,"full"),d("transformation","movement",8,"full"),d("transformation","disappearance",4,"full"),d("transformation","appearance",12,"full"),d("stage","start",4),d("stage","process",8),d("stage","end",12),d("interpretation","time",12),d("certainty","unsure",12),d("reason","object:sun + object:stars -> interpretation:time",12),d("reaction","unmentioned",12)],
"P10_t1":[d("object","sphere",4,"full"),d("transformation","appearance",4,"full"),d("transformation","growth",4,"partial",note="Pulsating"),d("stage","process",4),d("stage","end",8),d("interpretation","other",20,note="Driving mode"),d("certainty","unsure",20),d("reason","object:sphere + colour:red -> interpretation:other(driving mode)",20),d("reaction","unmentioned",20)],
"P10_t2":[d("object","none",6),d("transformation","none",6),d("interpretation","none",6),d("certainty","sure",6),d("reaction","unmentioned",6)],
"P10_t3":[d("object","sun",4,"partial"),d("object","moon",4,"partial"),d("object","stars",4,"partial",note="Sparkling things"),d("transformation","movement",4,"full"),d("transformation","appearance",4,"partial"),d("transformation","colour",4,"full"),d("stage","start",4),d("stage","process",4),d("interpretation","fatigue",8),d("certainty","unsure",8),d("reason","interpretation:time inferred from colour transition -> interpretation:fatigue",8,note="Creative answer, participant wording retained"),d("reaction","unmentioned",8)],
"P11_t1":[d("object","sun",4,"full"),d("object","moon",4,"full"),d("object","stars",4,"full"),d("transformation","movement",4,"full"),d("transformation","appearance",4,"full"),d("stage","start",4),d("stage","process",4),d("stage","end",4),d("interpretation","time",8),d("certainty","unsure",8),d("reason","object:sun + object:moon + object:stars -> interpretation:time",8),d("reaction","unmentioned",8)],
"P11_t2":[d("object","buildings",4,"full"),d("transformation","appearance",4,"full"),d("transformation","growth",4,"full"),d("transformation","colour",4,"full",note="Grey and yellow/orange building forms"),d("stage","start",4),d("stage","process",4),d("interpretation","location",8),d("certainty","sure",8),d("reason","object:buildings -> interpretation:location",8),d("reaction","unmentioned",8)],
"P11_t3":[d("object","none",4),d("transformation","colour",4,"full",note="Valid subtle NT background-colour animation"),d("stage","start",12),d("stage","end",12),d("interpretation","none",4),d("certainty","sure",4),d("reaction","unmentioned",4)],
"P12_t1":[d("object","hills",4,"full"),d("object","buildings",4,"full"),d("object","city",8,"full"),d("transformation","appearance",4,"full"),d("transformation","growth",4,"full"),d("transformation","zoom",8,"full"),d("transformation","colour",8,"full",note="Orange buildings"),d("transformation","colour",8,"incorrect",note="Blue buildings"),d("transformation","transition",8,"full"),d("stage","start",4),d("stage","process",8),d("interpretation","location",8),d("certainty","unsure",8),d("reason","object:buildings + transformation:transition -> interpretation:location",8),d("reaction","unmentioned",8)],
"P12_t2":[d("object","sun",4,"full"),d("object","moon",4,"full"),d("object","stars",4,"full"),d("transformation","movement",4,"full"),d("transformation","appearance",4,"full"),d("transformation","transition",4,"full"),d("stage","start",4),d("stage","process",4),d("stage","end",4),d("interpretation","time",4),d("certainty","sure",4),d("reason","object:sun + object:moon + object:stars + transformation:transition -> interpretation:time",4),d("reaction","unmentioned",4)],
"P12_t3":[d("object","none",2),d("transformation","none",2),d("interpretation","none",2),d("certainty","sure",2),d("reaction","unmentioned",2)],
"P13_t1":[d("object","none",4),d("transformation","none",4),d("interpretation","none",4),d("certainty","sure",4),d("reaction","unmentioned",4)],
"P13_t2":[d("object","sphere",4,"partial"),d("object","sun",4,"incorrect"),d("transformation","movement",4,"partial"),d("stage","process",4),d("interpretation","warning",12),d("certainty","unsure",12),d("reason","colour:orange -> interpretation:warning",12),d("reaction","unmentioned",12)],
"P13_t3":[d("object","buildings",4,"full"),d("object","city",4,"full"),d("transformation","growth",4,"full"),d("transformation","zoom",4,"full"),d("stage","process",4),d("interpretation","location",8),d("certainty","unsure",8),d("reason","object:buildings + object:city -> interpretation:location",8),d("reaction","unmentioned",8)],
"P14_t1":[d("object","sphere",4,"full"),d("transformation","movement",4,"partial"),d("stage","process",4),d("stage","end",4),d("interpretation","warning",8),d("interpretation","weather",8),d("certainty","unsure",8),d("reason","object:sphere + colour:orange -> interpretation:warning or interpretation:weather",8,note="Alternatives retained"),d("reaction","unmentioned",8)],
"P14_t2":[d("object","none",3),d("transformation","none",3),d("interpretation","none",3),d("certainty","sure",3),d("reaction","unmentioned",3)],
"P14_t3":[d("object","buildings",4,"full"),d("transformation","appearance",4,"full"),d("transformation","growth",4,"full"),d("transformation","colour",4,"full"),d("stage","start",4),d("stage","process",4),d("interpretation","location",4),d("interpretation","warning",4),d("certainty","unsure",4),d("reason","object:buildings -> interpretation:location; entering city -> interpretation:warning",4),d("reaction","unmentioned",4)],
"P15_t1":[d("object","none",2),d("transformation","none",2),d("interpretation","none",2),d("certainty","sure",2),d("reaction","unmentioned",2)],
"P15_t2":[d("object","sphere",4,"partial",note="Generic orange ball"),d("transformation","appearance",4,"full"),d("transformation","growth",4,"partial"),d("stage","start",4),d("stage","process",4),d("interpretation","none",8),d("certainty","unknown",8),d("reaction","distracting",4)],
"P15_t3":[d("object","sun",4,"full"),d("object","moon",4,"full"),d("object","stars",4,"full"),d("transformation","movement",4,"full"),d("transformation","appearance",4,"full"),d("stage","process",4),d("stage","end",4),d("interpretation","fatigue",8),d("certainty","unsure",8),d("reaction","unmentioned",8)],
"P16_t1":[d("object","sphere",4,"partial",note="Generic red ball"),d("transformation","movement",4,"partial"),d("transformation","colour",4,"full"),d("stage","process",4),d("interpretation","warning",4),d("certainty","unsure",4),d("reason","colour:red/orange -> interpretation:warning",4),d("reaction","unmentioned",4)],
"P16_t2":[d("object","none",4),d("transformation","none",4),d("interpretation","none",4),d("certainty","sure",4),d("reaction","unmentioned",4)],
"P16_t3":[d("object","sun",4,"partial"),d("object","moon",6,"full"),d("object","stars",6,"partial",note="Little dots"),d("transformation","movement",6,"full"),d("transformation","colour",6,"full"),d("transformation","appearance",6,"full"),d("transformation","transition",10,"full"),d("stage","process",6),d("stage","end",10),d("interpretation","time",10),d("interpretation","weather",6),d("certainty","unsure",10),d("reason","object:sun + object:moon + transformation:transition -> interpretation:time",10),d("reason","object:stars -> interpretation:weather",6,note="Participant alternative"),d("reaction","unmentioned",10)],
"P17_t1":[d("object","sun",4,"full"),d("object","moon",4,"full"),d("transformation","movement",4,"full"),d("transformation","transition",4,"full"),d("stage","start",4),d("stage","process",4),d("stage","end",4),d("interpretation","entertainment",16),d("certainty","unsure",20),d("reason","random appearance -> interpretation:entertainment",20),d("reaction","unmentioned",20)],
"P17_t2":[d("object","landscape",4,"full"),d("object","buildings",4,"full"),d("transformation","transition",4,"partial"),d("stage","process",4),d("interpretation","location",4),d("certainty","unsure",4),d("reason","object:buildings -> interpretation:location",4),d("reaction","unmentioned",4)],
"P17_t3":[d("object","none",4),d("transformation","none",4),d("interpretation","none",4),d("certainty","sure",4),d("reaction","unmentioned",4)],
"P18_t1":[d("object","buildings",4,"full"),d("transformation","appearance",4,"full"),d("transformation","growth",4,"full"),d("transformation","colour",4,"full"),d("stage","start",4),d("stage","process",4),d("stage","end",4),d("interpretation","location",12),d("certainty","unsure",12),d("reason","object:buildings -> interpretation:location",12,note="Questionnaire-influenced tentative meaning"),d("reaction","confusing",4,note="Difficulty noticing when animation stops")],
"P18_t2":[d("object","sun",4,"partial",note="Generic ball inferred as sunset"),d("object","moon",12,"full"),d("object","stars",12,"full"),d("transformation","appearance",4,"partial"),d("transformation","movement",12,"full"),d("transformation","colour",4,"full"),d("transformation","transition",12,"partial",note="Inferred after missed transition"),d("stage","start",4),d("stage","process",12),d("stage","end",12),d("interpretation","time",16),d("certainty","unsure",4),d("reason","inferred sunset + later moon/stars -> interpretation:time",4),d("reaction","glitch",8),d("reaction","confusing",12)],
"P18_t3":[d("object","none",4),d("transformation","none",4),d("interpretation","none",4),d("certainty","unsure",4),d("reaction","unmentioned",4)],
"P19_t1":[d("object","none",4),d("stage","unclear",4,note="Generic peripheral change retained without inferring colour or a V1-V3 transition"),d("interpretation","none",4),d("certainty","unknown",4),d("reaction","unmentioned",4)],
"P19_t2":[d("object","sphere",8,"full"),d("transformation","appearance",8,"full"),d("transformation","colour",4,"incorrect"),d("stage","process",8),d("stage","end",8),d("interpretation","none",12),d("certainty","unknown",12),d("reaction","unmentioned",12)],
"P19_t3":[d("object","buildings",4,"full"),d("transformation","appearance",4,"full"),d("transformation","growth",4,"full"),d("transformation","colour",4,"full"),d("stage","process",4),d("interpretation","location",8),d("certainty","unsure",8),d("reason","object:buildings -> interpretation:location",8),d("reaction","unmentioned",8)],
"P20_t1":[d("object","sphere",4,"full"),d("transformation","appearance",4,"full"),d("transformation","disappearance",4,"partial",note="Peeling particles"),d("transformation","transition",8,"incorrect",note="Uncertain landscape change"),d("stage","process",4),d("interpretation","warning",12),d("certainty","unsure",12),d("reason","object:sphere + colour:red -> interpretation:warning",12),d("reaction","unmentioned",12)],
"P20_t2":[d("object","none",4),d("transformation","colour",4,"full",note="Valid subtle NT background-colour animation"),d("stage","unclear",4),d("interpretation","warning",8,note="Slow down"),d("certainty","unsure",8),d("reason","transformation:colour -> interpretation:warning",8),d("reaction","unmentioned",8)],
"P20_t3":[d("object","buildings",4,"full"),d("transformation","appearance",4,"full"),d("stage","unclear",4),d("interpretation","location",8),d("interpretation","warning",8),d("certainty","unsure",8),d("reason","object:buildings -> interpretation:location or interpretation:warning",8),d("reaction","unmentioned",8)],
"P21_t1":[d("object","other",4,"incorrect",note="Background colour only; no separate object identified"),d("transformation","colour",4,"full",note="Valid subtle NT background-colour animation"),d("stage","unclear",4),d("interpretation","none",4),d("certainty","unknown",4),d("reaction","unmentioned",4)],
"P21_t2":[d("object","sphere",8,"full"),d("transformation","colour",8,"partial"),d("stage","process",8),d("interpretation","notification",16),d("certainty","unsure",16),d("reason","object:sphere + changing colours -> interpretation:notification",16),d("reaction","unmentioned",16)],
"P21_t3":[d("object","sun",8,"full"),d("object","stars",8,"partial",note="Little shiny things"),d("transformation","movement",12,"full"),d("transformation","appearance",8,"full"),d("transformation","disappearance",12,"full"),d("stage","start",12),d("stage","process",12),d("stage","end",12),d("interpretation","other",16,note="Background"),d("certainty","sure",16),d("reaction","distracting",8)],
"P22_t1":[d("object","sphere",12,"partial"),d("object","sun",12,"incorrect"),d("transformation","growth",12,"full"),d("stage","process",12),d("interpretation","time",16),d("certainty","unsure",16),d("reason","object:sun -> interpretation:time",16),d("reaction","unmentioned",16)],
"P22_t2":[d("object","none",4),d("transformation","none",4),d("interpretation","none",4),d("certainty","sure",4),d("reaction","unmentioned",4)],
"P22_t3":[d("object","sun",4,"full"),d("object","stars",4,"full"),d("transformation","movement",4,"full"),d("transformation","appearance",4,"full"),d("transformation","transition",4,"full"),d("stage","start",4),d("stage","process",4),d("stage","end",4),d("interpretation","time",8),d("certainty","sure",8),d("reason","object:sun + object:stars + transformation:transition -> interpretation:time",8),d("reaction","unmentioned",8)],
"P23_t1":[d("object","sun",4,"partial",note="Generic red dot"),d("object","stars",4,"partial",note="White dots"),d("transformation","movement",4,"full"),d("transformation","disappearance",4,"full"),d("transformation","appearance",4,"full"),d("stage","start",4),d("stage","process",4),d("stage","end",4),d("interpretation","assistant",8),d("certainty","unsure",8),d("reason","moving dot + white dots -> interpretation:assistant",8),d("reaction","unmentioned",8)],
"P23_t2":[d("object","buildings",4,"partial"),d("transformation","colour",4,"full"),d("stage","process",4),d("interpretation","none",8),d("certainty","unknown",8),d("reaction","unmentioned",8)],
"P23_t3":[d("object","other",8,"incorrect"),d("transformation","colour",4,"partial",note="Blue change may reflect NT background colour, but participant was unsure whether it was an object"),d("stage","unclear",4),d("interpretation","assistant",16),d("interpretation","other",16,note="Real-world object"),d("certainty","unsure",20),d("reason","object:other -> interpretation:assistant or interpretation:other(real world)",16,note="Alternatives retained"),d("reaction","unmentioned",20)],
"P24_t1":[d("object","buildings",8,"full"),d("transformation","appearance",8,"partial",note="Final state noticed, onset missed"),d("transformation","growth",12,"full"),d("stage","process",12),d("stage","end",8),d("interpretation","location",16),d("certainty","sure",16),d("reason","object:buildings -> interpretation:location",16),d("reaction","unmentioned",16)],
"P24_t2":[d("object","sun",4,"full"),d("object","moon",4,"full"),d("object","stars",4,"full"),d("transformation","movement",4,"full"),d("transformation","colour",4,"full"),d("transformation","appearance",4,"full"),d("transformation","transition",4,"full"),d("stage","process",4),d("stage","end",4),d("interpretation","time",12),d("certainty","sure",12),d("reason","object:sun + object:moon + object:stars + transformation:transition -> interpretation:time",12),d("reaction","confusing",4,note="Could not identify animation start and stop")],
"P24_t3":[d("object","none",4),d("transformation","none",4),d("interpretation","none",4),d("certainty","sure",4),d("reaction","unmentioned",4)],
"P25_t1":[d("object","landscape",4,"full"),d("object","buildings",8,"full"),d("transformation","colour",4,"full",note="Yellow/orange and grey forms"),d("transformation","appearance",8,"full"),d("transformation","growth",8,"full"),d("transformation","transition",4,"full"),d("stage","process",8),d("stage","end",4),d("interpretation","location",12),d("certainty","unsure",12),d("reason","object:buildings + transformation:transition -> interpretation:location",12),d("reaction","unmentioned",12)],
"P25_t2":[d("object","sun",4,"partial"),d("object","moon",4,"partial"),d("transformation","colour",4,"full"),d("transformation","movement",4,"full"),d("transformation","transition",8,"partial",note="Inferred after participant says details were missed"),d("stage","start",4),d("stage","process",4),d("interpretation","time",8),d("certainty","unsure",8),d("reason","object:sun or object:moon + transformation:transition -> interpretation:time",8,note="Alternatives retained"),d("reaction","unmentioned",8)],
"P25_t3":[d("object","landscape",4,"full"),d("transformation","zoom",8,"incorrect"),d("stage","process",8),d("interpretation","entertainment",12),d("certainty","unsure",12),d("reason","transformation:zoom -> interpretation:entertainment",12),d("reaction","unmentioned",12)],
"P26_t1":[d("object","landscape",4,"full"),d("transformation","movement",8,"full",note="Correct description of the continuous NT landscape colour shift flowing from left to right"),d("stage","process",8),d("interpretation","none",4),d("certainty","unknown",4),d("reaction","unmentioned",4,note="Not distracting is not coded as calming")],
"P26_t2":[d("object","sun",4,"incorrect"),d("transformation","appearance",4,"partial",note="Particles shooting out"),d("stage","start",4),d("interpretation","time",8),d("certainty","unsure",8),d("reason","object:sun -> interpretation:time",8),d("reaction","distracting",4)],
"P26_t3":[d("object","city",4,"full"),d("object","buildings",8,"full"),d("object","landscape",4,"full"),d("transformation","transition",4,"full"),d("transformation","appearance",8,"full"),d("transformation","zoom",8,"partial"),d("transformation","movement",8,"partial"),d("transformation","colour",12,"incorrect",note="Blue/green report does not match confirmed orange/grey V2 buildings"),d("stage","start",4),d("stage","process",8),d("interpretation","location",20),d("certainty","unsure",20),d("reason","object:buildings + object:city -> interpretation:location",20),d("reaction","unmentioned",20,note="Not distracting/harmonic is not coded as calming")],
}


SPANS = {
    ("P02_t1", 4): "I only noticed this red bulb look like a song to me in that part of the Pi Hu, but I only noticed it at the end of the trial.",
    ("P02_t2", 2): "I didn't notice anything.",
    ("P04_t2", 6): "To be honest, nothing I would say I saw what I see now, so this landscape, I would say some, I dunno, mountains or whatever it is, and just colour changing. Nothing else. Totally. I was unsure for a moment because it's research. I was super confused because it has to be something. So that's why I also said my frustration is 10 because I cannot believe that I cannot notice anything and that's why ah, and exactly why I pressed also the trigger because I thought that this animation, the basic one, the colour changing to dark, bluish, whatever, I thought that this also counts, but not.",
    ("P05_t3", 4): "I didn't pursue anything. I thought that will be something, change might be as like before, but I didn't reach my expectation. It doesn't change anything.",
    ("P08_t1", 16): "Then I have no,",
    ("P12_t3", 2): "I didn't see anything this time.",
    ("P15_t1", 2): "No, I didn't see anything.",
    ("P26_t1", 8): "No. No. It was like flowing away from left to right",
}


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_docx(path):
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    with ZipFile(path) as zf:
        root = ET.fromstring(zf.read("word/document.xml"))
    paragraphs = {}
    timestamps = {}
    current = "timestamp-unavailable"
    for i, paragraph in enumerate(root.findall(".//w:body/w:p", ns), 1):
        text = "".join(t.text or "" for t in paragraph.findall(".//w:t", ns)).strip()
        if not text:
            continue
        paragraphs[i] = text
        match = re.search(r"\((\d{2}:\d{2})\):", text)
        if match:
            current = match.group(1)
        timestamps[i] = current
    return paragraphs, timestamps


def evidence_for(key, paragraph, paragraphs, timestamps, span=None):
    full = paragraphs[key][paragraph]
    selected = span or SPANS.get((key, paragraph)) or full
    if selected not in full:
        raise ValueError(f"Evidence is not exact for {key} p{paragraph}: {selected!r}")
    return selected, f"{key} {timestamps[key][paragraph]} p{paragraph}"


def write_csv(path, rows, fields):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main():
    with MAP.open(newline="", encoding="utf-8-sig") as f:
        crosswalk = list(csv.DictReader(f))
    keys = [row["participant_trial_key"] for row in crosswalk]
    condition = {row["participant_trial_key"]: row["final_condition"] for row in crosswalk}
    inclusion = {row["participant_trial_key"]: row["inclusion_status"] for row in crosswalk}
    paragraphs, timestamps = {}, {}
    source_rows = []
    for key in keys:
        path = DOCX_DIR / f"{key}.docx"
        if path.exists():
            paragraphs[key], timestamps[key] = read_docx(path)
            source_rows.append({"participant_trial_key": key, "condition": condition[key], "inclusion_status": inclusion[key], "source_path": str(path.relative_to(ROOT)), "source_available": "yes", "source_sha256": sha256(path)})
        else:
            paragraphs[key], timestamps[key] = {}, {}
            source_rows.append({"participant_trial_key": key, "condition": condition[key], "inclusion_status": inclusion[key], "source_path": str(path.relative_to(ROOT)), "source_available": "no", "source_sha256": "NA"})

    errors, warnings = [], []
    if len(keys) != 72 or len(set(keys)) != 72:
        errors.append("Canonical map must contain 72 unique participant-trial keys")
    if set(L1) != set(keys):
        errors.append(f"Layer 1 key mismatch: missing={sorted(set(keys)-set(L1))}; extra={sorted(set(L1)-set(keys))}")
    if set(D) != set(keys):
        errors.append(f"Layer 2 key mismatch: missing={sorted(set(keys)-set(D))}; extra={sorted(set(D)-set(keys))}")
    missing_sources = [row["participant_trial_key"] for row in source_rows if row["source_available"] == "no"]
    if missing_sources:
        errors.append(f"Missing eligible sources: {missing_sources}")

    long_rows, trial_rows = [], []
    for key in keys:
        success, specificity, failure, pno, span = L1[key]
        try:
            l1_evidence, l1_locator = evidence_for(key, pno, paragraphs, timestamps, span)
        except Exception as exc:
            errors.append(str(exc)); l1_evidence, l1_locator = "", ""
        if success not in {"yes", "no"} or (success == "yes" and (specificity not in {"full", "partial"} or failure != "NA")) or (success == "no" and (specificity != "NA" or failure not in {"alternative", "unknown", "false-change"})):
            errors.append(f"Invalid Layer 1 branch for {key}: {L1[key]}")
        for family, value, accuracy, detail_pno, note in D[key]:
            if family == "reaction" and value == "unmentioned":
                continue
            allowed = {"object": OBJECTS, "transformation": TRANSFORMATIONS, "stage": STAGES, "interpretation": INTERPRETATIONS, "certainty": CERTAINTY, "reaction": REACTIONS}
            if family in allowed and value not in allowed[family]:
                errors.append(f"Invalid {family} value for {key}: {value}")
            if family in {"object", "transformation"}:
                expected_accuracy = "NA" if value == "none" else None
                if expected_accuracy == "NA" and accuracy != "NA":
                    errors.append(f"Accuracy must be NA for {key} {family}:none")
                if value != "none" and accuracy not in {"full", "partial", "incorrect"}:
                    errors.append(f"Missing accuracy for {key} {family}:{value}")
            elif accuracy != "NA":
                errors.append(f"Accuracy must be NA outside object/transformation for {key} {family}:{value}")
            try:
                ev, loc = evidence_for(key, detail_pno, paragraphs, timestamps)
            except Exception as exc:
                errors.append(str(exc)); ev, loc = "", ""
            long_rows.append({"participant_trial_key": key, "condition": condition[key], "code_family": family, "code_value": value, "accuracy": accuracy, "evidence": ev, "locator": loc, "source_path": f"analysis/dataset/originals/transcripts/trials/{key}.docx", "speaker": "participant", "decision_note": note})
        by_family = defaultdict(list)
        for row in long_rows:
            if row["participant_trial_key"] == key:
                rendered = row["code_value"] if row["accuracy"] == "NA" else f'{row["code_value"]} [{row["accuracy"]}]'
                by_family[row["code_family"]].append(rendered)
        trial_rows.append({"participant_trial_key": key, "participant_id": key.split("_")[0], "trial_sequence": key.split("_")[1], "condition": condition[key], "inclusion_status": inclusion[key], "source_available": "yes" if paragraphs[key] else "no", "success": success, "specificity": specificity, "failure": failure, "layer1_evidence": l1_evidence, "layer1_locator": l1_locator, "object_codes": " | ".join(by_family["object"]), "transformation_codes": " | ".join(by_family["transformation"]), "stage_codes": " | ".join(by_family["stage"]), "interpretation_codes": " | ".join(by_family["interpretation"]), "certainty_codes": " | ".join(by_family["certainty"]), "reaction_codes": " | ".join(by_family["reaction"]), "reason_links": " | ".join(by_family["reason"])})

    if len(trial_rows) != 72 or len({r["participant_trial_key"] for r in trial_rows}) != 72:
        errors.append("Trial output must contain 72 unique keys")
    condition_counts = Counter(r["condition"] for r in trial_rows)
    expected_counts = {"NT": 24, "V1": 16, "V2": 16, "V3": 16}
    if dict(condition_counts) != expected_counts:
        errors.append(f"Condition denominators differ: {dict(condition_counts)}")
    if condition["P01_t3"] != "V2":
        errors.append("P01_t3 must remain V2")
    if any(not r["evidence"] or not re.fullmatch(r"P\d{2}_t[123] (?:\d{2}:\d{2}|timestamp-unavailable) p\d+", r["locator"]) for r in long_rows):
        errors.append("Every Layer 2 row must have evidence and a resolvable key/timestamp/paragraph locator")
    duplicate_detail_rows = [item for item, n in Counter((r["participant_trial_key"],r["code_family"],r["code_value"],r["accuracy"],r["locator"],r["decision_note"]) for r in long_rows).items() if n > 1]
    if duplicate_detail_rows:
        errors.append(f"Duplicate detail rows: {duplicate_detail_rows}")

    expected_meaning = {"V1": "time", "V2": "location", "V3": "destination"}
    animated_success_semantic_match = all(
        expected_meaning[row["condition"]] in row["interpretation_codes"].split(" | ")
        for row in trial_rows
        if row["condition"] in expected_meaning and row["success"] == "yes"
    )
    if not animated_success_semantic_match:
        errors.append("Every animated success must contain the condition's intended meaning code")

    reviewed_nt_success = {"P02_t2", "P03_t1", "P04_t2", "P05_t3", "P08_t2", "P09_t1", "P10_t2", "P11_t3", "P12_t3", "P13_t1", "P14_t2", "P15_t1", "P16_t2", "P17_t3", "P18_t3", "P22_t2", "P24_t3", "P26_t1"}
    reviewed_nt_failure = {"P01_t1", "P19_t1", "P20_t2", "P21_t1", "P23_t3", "P25_t3"}
    observed_nt_success = {row["participant_trial_key"] for row in trial_rows if row["condition"] == "NT" and row["success"] == "yes"}
    observed_nt_failure = {row["participant_trial_key"] for row in trial_rows if row["condition"] == "NT" and row["success"] == "no"}
    nt_reviewed_assignments = observed_nt_success == reviewed_nt_success and observed_nt_failure == reviewed_nt_failure
    if not nt_reviewed_assignments:
        errors.append("NT success/failure assignments differ from the reviewed 18/6 transcript classification")
    v1_literal_meanings_partial = all(
        next(row for row in trial_rows if row["participant_trial_key"] == key)["specificity"] == "partial"
        for key in ("P18_t2", "P24_t2")
    )
    if not v1_literal_meanings_partial:
        errors.append("P18_t2 and P24_t2 must remain partial literal-state meaning matches")

    unresolved = [
        "Explicit NT background-colour reports are coded full; imprecise colour-motion accounts may be partial, while generic unspecified changes are not forced into colour or V1-V3 transition codes.",
        "Generic animation language is split into partial appearance and movement only where the rules explicitly require that treatment.",
        "Reaction is left unassigned when no reaction is explicitly stated; absence is not interpreted as neutrality.",
        "Single-coder detail assignments remain provisional; no consensus or inter-rater reliability claim is made.",
    ]
    warnings.extend(unresolved)

    write_csv(OUT / "full-corpus-trial-codes.csv", trial_rows, list(trial_rows[0]))
    write_csv(OUT / "full-corpus-code-evidence.csv", long_rows, list(long_rows[0]))
    write_csv(OUT / "full-corpus-source-manifest.csv", source_rows, list(source_rows[0]))

    success_by_condition = {}
    specificity_by_condition = {}
    failure_by_condition = {}
    for cond in expected_counts:
        subset = [r for r in trial_rows if r["condition"] == cond]
        success_by_condition[cond] = dict(Counter(r["success"] for r in subset))
        specificity_by_condition[cond] = dict(Counter(r["specificity"] for r in subset if r["specificity"] != "NA"))
        failure_by_condition[cond] = dict(Counter(r["failure"] for r in subset if r["failure"] != "NA"))
    summary = {
        "status": "provisional-single-coder",
        "trial_count": len(trial_rows),
        "condition_denominators": dict(sorted(condition_counts.items())),
        "success_by_condition": success_by_condition,
        "specificity_by_condition": specificity_by_condition,
        "failure_by_condition": failure_by_condition,
        "detail_row_count": len(long_rows),
        "detail_counts": {family: dict(Counter(r["code_value"] for r in long_rows if r["code_family"] == family)) for family in ["object","transformation","stage","interpretation","certainty","reaction"]},
    }
    (OUT / "full-corpus-summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    report_values = {
        "condition_denominators": summary["condition_denominators"],
        "success_by_condition": summary["success_by_condition"],
        "specificity_by_condition": summary["specificity_by_condition"],
        "failure_by_condition": summary["failure_by_condition"],
        "trial_count": summary["trial_count"],
        "detail_row_count": summary["detail_row_count"],
    }
    (OUT / "full-corpus-report-values.json").write_text(json.dumps(report_values, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    receipt = {
        "status": "validated" if not errors else "failed",
        "generated_on": "2026-10-01",
        "population_rule": "All 72 included participant-trials in the canonical crosswalk; P07 is excluded upstream and P07_t3 is not substituted.",
        "condition_denominators": dict(sorted(condition_counts.items())),
        "available_sources": 72 - len(missing_sources),
        "missing_sources": missing_sources,
        "p01_t3_condition": condition.get("P01_t3"),
        "checks": {
            "unique_trial_keys": len({r["participant_trial_key"] for r in trial_rows}) == 72,
            "expected_coverage": len(trial_rows) == 72 and not missing_sources,
            "condition_join": dict(condition_counts) == expected_counts,
            "valid_layer1_branches": not any("Layer 1 branch" in e for e in errors),
            "valid_labels_and_accuracy": not any(e.startswith("Invalid ") or "accuracy" in e.lower() for e in errors),
            "exact_evidence_and_locators": not any("evidence" in e.lower() or "locator" in e.lower() for e in errors),
            "animated_success_semantic_match": animated_success_semantic_match,
            "nt_reviewed_assignments": nt_reviewed_assignments,
            "v1_literal_meanings_partial": v1_literal_meanings_partial,
            "p01_t3_v2": condition.get("P01_t3") == "V2",
            "report_values_match_summary": report_values["success_by_condition"] == summary["success_by_condition"] and report_values["specificity_by_condition"] == summary["specificity_by_condition"] and report_values["condition_denominators"] == summary["condition_denominators"],
        },
        "errors": errors,
        "warnings": warnings,
        "hashes": {
            "canonical_map_sha256": sha256(MAP),
            "coding_rules_sha256": sha256(RULES),
            "preprocessing_rules_sha256": sha256(PREPROCESSING),
            "rq3_contract_sha256": sha256(CONTRACT),
            "build_script_sha256": sha256(Path(__file__)),
        },
        "outputs": ["full-corpus-trial-codes.csv", "full-corpus-code-evidence.csv", "full-corpus-source-manifest.csv", "full-corpus-summary.json", "full-corpus-report-values.json", "full-corpus-inclusion-receipt.json", "full-corpus-validation.json", "coding-report.md"],
    }
    inclusion_receipt = {k: receipt[k] for k in ["status","population_rule","condition_denominators","available_sources","missing_sources","p01_t3_condition"]}
    inclusion_receipt["canonical_map_sha256"] = receipt["hashes"]["canonical_map_sha256"]
    (OUT / "full-corpus-inclusion-receipt.json").write_text(json.dumps(inclusion_receipt, indent=2) + "\n", encoding="utf-8")
    (OUT / "full-corpus-validation.json").write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": receipt["status"], "trials": len(trial_rows), "details": len(long_rows), "denominators": dict(condition_counts), "errors": errors}, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
