"""Entry point for the coordinated RQ1/RQ2/RQ3 Chapter 4 rerun."""
from pathlib import Path
import runpy

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "analysis").is_dir() and (p / "overleaf").is_dir())
runpy.run_path(str(ROOT/'analysis/RQ3/20261015-ch4-inference-adoption/run_analysis.py'), run_name='__main__')
