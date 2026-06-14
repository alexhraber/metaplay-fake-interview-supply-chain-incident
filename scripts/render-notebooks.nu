#!/usr/bin/env nu

let repo_root = ($env.FILE_PWD | path dirname)
cd $repo_root

python scripts/sanitize-notebooks.py --write notebooks
mkdir docs/notebooks
jupyter nbconvert --to html notebooks/*.ipynb --output-dir docs/notebooks
python scripts/write-notebook-index.py
print "Rendered reviewed notebooks to docs/notebooks/"

