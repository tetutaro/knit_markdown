#!/usr/bin/env bash
pwd=`pwd`
cd ${pwd}/beamer && ./install.sh
cd ${pwd}/pandoc && ./install_pipx.sh
cd ${pwd}/knit && pipx install --force -e .
