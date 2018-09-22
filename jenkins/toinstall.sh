#!/bin/bash

sudo apt install python-flake8 -y

pip install --upgrade pip
sudo rm -rf ~/.local/lib/python2.7/site-packages/

pip install pep8ify
pip install yapf
pip install pytest
pip install pytest-cov
pip install colorlog
pip install coverage
pip install pyzmq
pip install autoflake
pip install pylint
pip install flake8
pip install autopep8

