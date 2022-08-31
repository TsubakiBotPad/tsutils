#!/usr/bin/env bash

cd "$(dirname "$0")" || exit

rm dist/*
python3 setup.py sdist bdist_wheel
twine upload dist/*
