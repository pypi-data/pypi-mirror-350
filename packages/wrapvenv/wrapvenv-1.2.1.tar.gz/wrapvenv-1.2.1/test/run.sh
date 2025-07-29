#!/bin/bash
#
# This script emulates a simple session where a new frozen requirements file is
# created and then a script run inside of it

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $SCRIPT_DIR

export PYTHONPATH=$SCRIPT_DIR/..


echo
echo "> Converting reqs.txt into reqs-frozen-Linux.txt..."
python -m wrapvenv --freeze reqs.txt

echo 
echo "> Running script inside the custom virtual environment..."
python -m wrapvenv --reqs reqs-frozen-Linux.txt basic_imports.py
