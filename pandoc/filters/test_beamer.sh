#!/bin/sh

pandoc -t json ../../samples/sample.beamer.md | crossref.py | beamer.py | jq ".blocks[]"
