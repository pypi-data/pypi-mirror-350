<h1 align="center">flask-route-checker</h1>
<p align="center">
  <em>CLI to detect ⚠️ and auto-fix 🔧 broken <code>url_for()</code> calls in your Flask templates.</em><br>
  <a href="https://pypi.org/project/flask-route-checker/"><img src="https://badge.fury.io/py/flask-route-checker.svg" /></a>
</p>

---

## Features

* ✅ scans all `.html` templates for `url_for()` usage  
* 🚨 flags endpoints that don’t exist  
* 🔧 **--fix** mode rewrites templates + creates backups  
* 🎨 coloured output, dry-run diff viewer, ignore filters, JSON / MD report  
* 🧹 detects unused routes, optional external link checker  
* 🏗️ supports plain `app = Flask(__name__)` *and* factory pattern

---

## Quick start

```bash
# install
pip install flask-route-checker

# run from your Flask project root
flask-route-checker                       # just report issues
flask-route-checker --fix --backup-dir .backups

# possible erros 
ModuleNotFoundError: No module named 'routes'
two ways to fix 

1. run flask-route-checker from project root + add . to PYTHONPATH
    just run this from the same directory as app.py:
    set PYTHONPATH=.
    flask-route-checker --app app.py # or you main file that runs your flask app 

    if you are on GIT BASH ot UNIX:
    PYTHONPATH=. flask-route-checker --app app.py

2. Turn your routes/ into a proper python package
Make sure the routes/ folder has an __init__.py:

touch routes/__init__.py to make it easier 

| flag                       | purpose                                            |
| -------------------------- | -------------------------------------------------- |
| `--fix`                    | auto-patch broken routes                           |
| `--dry-run`                | show diff, don’t write                             |
| `--backup-dir DIR`         | where fixed templates are backed up                |
| `--ignore-endpoint TEXT`   | skip endpoints containing TEXT (can pass multiple) |
| `--report {json,markdown}` | dump a machine-readable report                     |
| `--unused`                 | list endpoints defined but never used              |
| `--diff`                   | colour diff view (needs **rich**)                  |
| `--factory NAME`           | custom factory instead of `create_app`             |


<h1 align="center">Contributing</h1>
1. Fork 🚀
2. git clone your fork 
3. pip install -e .[dev]
4. Create a branch feat/my-awesome-thing
5. PRs welcome! (Add test if you can)

# ADIOS AMIGO