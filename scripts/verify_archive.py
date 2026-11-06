"""Read-only source, link, figure and cited-archive checks."""
from pathlib import Path
import hashlib,json,re,zipfile,urllib.parse
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
s=json.loads((R/'provenance/selection.json').read_text())['selected_files']
for n,x in s.items():assert (R/n).is_file() and sha(R/n)==x['sha256'],n
images=set(re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}',(R/'overleaf/examplethesis.tex').read_text()));assert len(images)==34
for n in images:assert (R/'overleaf'/n).is_file(),n
for p in R.rglob('*.md'):
 if '.git' in p.parts or '.build' in p.parts:continue
 for target in re.findall(r'!?\[[^\]]*\]\(([^\n)]+)\)',p.read_text()):
  target=target.split('#',1)[0].strip('<>')
  if target and not re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:',target):assert (p.parent/urllib.parse.unquote(target)).exists(),(str(p),target)
a=R/'references/cited-papers.zip';receipt=json.loads((R/'references/archive-check.json').read_text());assert sha(a)==receipt['sha256']
with zipfile.ZipFile(a) as z:
 assert z.testzip() is None;m=json.loads(z.read('cited-papers/manifest.json'));assert len(m['references'])==48
 for r in m['references']:
  for f in r['files']:assert hashlib.sha256(z.read('cited-papers/'+f['path'])).hexdigest()==f['archive_sha256'],f['path']
 assert sum(n.endswith('.pdf') for n in z.namelist())==45
 assert sum(f.get('zotero_annotations',0) for r in m['references'] for f in r['files'])==453
for p in R.rglob('*'):
 if not p.is_file() or '.git' in p.parts or '.build' in p.parts:continue
 assert p.stat().st_size<100*1024**2,str(p)
 assert not any(x in p.parts for x in ['node_modules','.venv','.python-deps','.worktrees','wiki']),str(p)
print(json.dumps({'status':'passed','source_files':len(s),'figures':len(images),'pdfs':45,'annotations':453,'links_and_zip_hashes':'passed'},indent=2))
