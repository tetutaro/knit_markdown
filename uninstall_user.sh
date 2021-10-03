#!/usr/bin/env bash
pwd=`pwd`
cd ${pwd}/pandoc && ./uninstall.sh
pipx uninstall knit-markdown
