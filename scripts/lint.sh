#!/bin/bash

echo ">>> $(basename ${BASH_SOURCE[0]})"

set -o errexit # exit script when command fails
set -o pipefail # this setting prevents errors in a pipeline from being masked
set -o nounset # exit script when it tries to use undeclared variables

# INIT WORKING DIR
# ===================================================
cd "$(dirname "${BASH_SOURCE[0]}")"
FILE_DIR=$(pwd)
cd ..
CWD="$(pwd)"

PY_FILES=$(find ./src -type f -name "*.py" ! -path './.*' -not -path "**/migrations/*" -not -path "**/settings/*")

echo '>>> running pylint'
pylint --max-line-length=120 --disable=E1101,C0116,C0114,R0903,R0401,C0413,C0115,W0613,R1710,W0223,R0801,W0511,R1729,R0201 $PY_FILES

echo '>>> running flake8'
flake8 $PY_FILES

echo '>>> running pycodestyle'
pycodestyle --first $PY_FILES

echo '>>> running mypy'
mypy $PY_FILES --exclude migrations

echo ">>> $(basename ${BASH_SOURCE[0]}) DONE"