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

#chmod ug+x "./scripts/lint.sh"
#bash ./scripts/lint.sh
#bash ./scripts/tests.sh

zip -r  proj.zip src/ srv/ docker-compose.yml Pipfile Pipfile.lock manage.py .env static/ entrypoint.sh

ssh -i "file-hosting-aws.pem" ubuntu@ec2-18-208-141-90.compute-1.amazonaws.com 'docker-compose down'

ssh -i "file-hosting-aws.pem" ubuntu@ec2-18-208-141-90.compute-1.amazonaws.com 'sudo rm -r ./src/ ./srv/ ./docker-compose.yml ./Pipfile ./Pipfile.lock ./manage.py ./.env ./static/ ./entrypoint.sh'

scp -i "file-hosting-aws.pem" proj.zip ubuntu@ec2-18-208-141-90.compute-1.amazonaws.com:./
#
ssh -i "file-hosting-aws.pem" ubuntu@ec2-18-208-141-90.compute-1.amazonaws.com 'sudo unzip proj.zip -d ./'
#
ssh -i "file-hosting-aws.pem" ubuntu@ec2-18-208-141-90.compute-1.amazonaws.com 'docker-compose up --build'
ssh -i "file-hosting-aws.pem" ubuntu@ec2-18-208-141-90.compute-1.amazonaws.com 'docker rm $(docker ps --filter status=exited -q)'
