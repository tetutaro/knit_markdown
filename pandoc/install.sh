#!/usr/bin/env bash
pwd=`pwd`
pandoc_template_path="${HOME}/.pandoc/templates"
if [ ! -d ${pandoc_template_path} ]; then
	mkdir -p ${pandoc_template_path}
fi
cd ${pwd}/templates
for file in *; do
	cp ${pwd}/templates/${file} ${pandoc_template_path}/.
done
cd ${pwd}/filters && pipx install --force -e .
