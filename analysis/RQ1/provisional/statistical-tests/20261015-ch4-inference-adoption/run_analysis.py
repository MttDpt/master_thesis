"""Entry point for the coordinated RQ1/RQ2/RQ3 Chapter 4 rerun."""
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[5]
runpy.run_path(str(ROOT/'analysis/RQ3/provisional/20261015-ch4-inference-adoption/run_analysis.py'), run_name='__main__')
