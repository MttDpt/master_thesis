"""Preserve byte-identical current coding/validation inputs for the adopted run."""
from pathlib import Path
from hashlib import sha256
import json
import shutil

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
dest=OUT/'inputs'
dest.mkdir(exist_ok=True)
record={}
for name in ['full-corpus-trial-codes.csv','full-corpus-validation.json']:
 source=ROOT/'analysis/RQ3/provisional/coding'/name
 target=dest/name
 shutil.copyfile(source,target)
 assert source.read_bytes()==target.read_bytes(),name
 record[str(source.relative_to(ROOT))]=dict(copy=str(target.relative_to(OUT)),sha256=sha256(source.read_bytes()).hexdigest())
(OUT/'input_snapshot_receipt.json').write_text(json.dumps(dict(status='passed',checks=2,source_snapshots=record),indent=2)+'\n')
print('Two byte-identical coding input snapshots preserved')
