#!/bin/bash

echo
echo "WARNING: I'm going to run 'git clean -fdx'. Press [ENTER] to continue..."
read
echo
git clean -fdx &>/dev/null || true

rm -rf .venvtmp dist build || true
python -m venv --copies .venvtmp
source .venvtmp/bin/activate

echo "Generating a regular python package..."
echo

python -m pip install --upgrade build
python -m build

echo 
echo
echo "Done!"
echo
echo "The package is located in the 'dist' directory. You can upload it to PyPI following"
echo "the instructions at https://packaging.python.org/tutorials/packaging-projects/"
echo

rm -rf .venvtmp || true
rm -rf build    || true

