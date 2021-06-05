#!/usr/bin/env bash
pwd=`pwd`
pandoc_template_path="${HOME}/.pandoc/templates"
cd ${pwd}/templates
for file in *; do
	rm ${pandoc_template_path}/${file}
done
pip uninstall -y kmd-filters
