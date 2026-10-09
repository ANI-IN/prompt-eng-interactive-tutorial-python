#!/usr/bin/env bash
# Runs once when the Codespace is created. Installs the course dependencies into
# the container's Python and registers it as a Jupyter kernel.
set -euo pipefail

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m ipykernel install --user --name prompt-eng-python --display-name "Python (prompt-eng)"
