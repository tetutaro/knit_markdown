#!/bin/sh

pandoc -t json ../../samples/sample.md | crossref.py | latex.py | jq ".blocks[]"
