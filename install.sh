#!/usr/bin/env bash
pwd=`pwd`
cd ${pwd}/beamer && ./install.sh
cd ${pwd}/pandoc && ./install.sh
cd ${pwd}/knit && python3 setup.py install
