#!/bin/sh
set -eu
echo "ENTRYPOINT: starting validate.py"
python -u /action/validate.py
