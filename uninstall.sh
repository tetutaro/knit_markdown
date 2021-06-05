#!/usr/bin/env bash
pwd=`pwd`
cd ${pwd}/beamer && ./uninstall.sh
cd ${pwd}/pandoc && ./uninstall.sh
pip uninstall -y knit-markdown
