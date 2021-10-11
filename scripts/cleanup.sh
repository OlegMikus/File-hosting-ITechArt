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

echo ">>> setup python packages by pipenv"

pipenv install --system --deploy --ignore-pipfile --dev
pipenv update

echo ">>> DONE"

cd "${CWD}"


echo ">>> setup pre-commit hook"

cp -f "${CWD}/hooks/pre-commit.sh" "${CWD}/.git/hooks/pre-commit"
chmod ug+x "${CWD}/.git/hooks/pre-commit"

echo ">>> DONE"


echo ">>> setup pre-push hook"

cp -f "${CWD}/hooks/pre-push.sh" "${CWD}/.git/hooks/pre-push"
chmod ug+x "${CWD}/.git/hooks/pre-push"

echo ">>> DONE"