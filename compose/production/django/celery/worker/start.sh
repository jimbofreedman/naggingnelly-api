#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset


celery -A api2.taskapp worker -l INFO
