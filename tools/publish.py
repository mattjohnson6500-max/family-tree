"""Stamp a new build of the family tree for GitHub Pages.

Usage: python3 tools/publish.py SOURCE.html
Copies SOURCE.html (the Claude artifact HTML) into family-tree-index.html,
adds the standalone page head, stamps a new BUILD id, and writes version.json.
Open pages compare their BUILD with version.json and reload automatically.
"""
import datetime, json, sys, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
build = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d%H%M%S")
head = '<!doctype html><html lang="en"><head><meta name="robots" content="noindex"><style>*,*::before,*::after{box-sizing:border-box}</style>'
if src.startswith("<!doctype html><html><head>"):
    src = src.replace("<!doctype html><html><head>", head, 1)
if 'const BUILD = "' not in src:
    sys.exit("SOURCE has no BUILD constant; add the auto-update block first")
import re
src = re.sub(r'const BUILD = "[^"]*";', f'const BUILD = "{build}";', src, count=1)
(root / "family-tree-index.html").write_text(src, encoding="utf-8")
(root / "version.json").write_text(json.dumps({"build": build}) + "\n", encoding="utf-8")
print("build", build)
