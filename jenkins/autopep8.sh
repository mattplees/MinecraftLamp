#!/bin/bash

echo "Running yapf"
yapf -i -r code/*.py

echo "Running reindent"
find ./code -type f -name "*.py" | xargs python /usr/share/doc/python2.7/examples/Tools/scripts/reindent.py -r -n

echo "Running autopep8"
autopep8 -i -r -aa ./code/*.py

echo "Running autoflake"
autoflake --remove-all-unused-imports --remove-unused-variables -r -i code/*.py

echo "Running pep8ify"
pep8ify -n -w code/