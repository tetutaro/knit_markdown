#!/usr/bin/env bash
pwd=`pwd`
cd ${pwd}/beamer && ./install.sh
cd ${pwd}/pandoc && ./install.sh
cd ${pwd}/knitc && python3 setup.py install
