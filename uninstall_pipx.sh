#!/usr/bin/env bash
pwd=`pwd`
cd ${pwd}/beamer && ./uninstall.sh
cd ${pwd}/pandoc && ./uninstall.sh
pipx uninstall knit-markdown
pipx uninstall kmd-filters
