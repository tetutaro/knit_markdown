#!/usr/bin/env bash
pwd=`pwd`
cd ${pwd}/beamer && ./uninstall.sh
cd ${pwd}/pandoc && ./uninstall_pipx.sh
pipx uninstall knit-markdown
