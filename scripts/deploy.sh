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


zip -r  proj.zip ./src/ ./srv/ ./docker-compose.yml ./Pipfile ./Pipfile.lock ./manage.py ./.env ./static/ ./entrypoint.sh

ssh root@134.122.78.76 'cd /home/oleg/file-hosting && sudo rm -r ./src/ ./srv/ ./docker-compose.yml ./Pipfile ./Pipfile.lock ./manage.py ./.env ./static/ ./entrypoint.sh'

scp proj.zip root@134.122.78.76:/home/oleg/

ssh root@134.122.78.76 'sudo unzip /home/oleg/proj.zip -d /home/oleg/file-hosting'

ssh oleg@134.122.78.76 'cd file-hosting/ && docker-compose down'
ssh oleg@134.122.78.76 'cd file-hosting/ && docker-compose up'