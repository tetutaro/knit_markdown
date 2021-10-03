#!/usr/bin/env bash
pwd=`pwd`
cd ${pwd}/pandoc && ./install.sh
cd ${pwd}/knit && pipx install --force -e .
