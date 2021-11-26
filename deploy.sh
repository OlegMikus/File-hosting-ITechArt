#!/bin/bash

echo ">>> $(basename ${BASH_SOURCE[0]})"

set -o errexit # exit script when command fails
set -o pipefail # this setting prevents errors in a pipeline from being masked
set -o nounset # exit script when it tries to use undeclared variables


zip -r  proj.zip ./src/ ./srv/ ./docker-compose.yml ./Pipfile ./Pipfile.lock ./manage.py ./.env ./static/ ./entrypoint.sh

ssh root@134.122.78.76 'cd /home/oleg && sudo rm -r ./*'

scp proj.zip root@134.122.78.76:/home/oleg/

ssh root@134.122.78.76 'sudo unzip /home/oleg/proj.zip -d /home/oleg/file-hosting'
