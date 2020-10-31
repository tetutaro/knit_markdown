#!/usr/bin/env bash
pwd=`pwd`
texmf_local=`kpsewhich -var-value=TEXMFLOCAL`
local_theme_path="${pwd}/beamer/themes/theme"
texmf_theme_path="${texmf_local}/tex/latex/beamer/themes/theme"
local_image_path="${pwd}/beamer/themes/images"
texmf_image_path="${texmf_local}/tex/latex/beamer/themes/images"
if [ ! -d ${texmf_theme_path} ]; then
	mkdir -p ${texmf_theme_path}
fi
if [ ! -d ${texmf_image_path} ]; then
	mkdir -p ${texmf_image_path}
fi
cd ${local_theme_path}
for file in *; do
	cp ${local_theme_path}/${file} ${texmf_theme_path}/.
done
cd ${local_image_path}
for file in *; do
	cp ${local_image_path}/${file} ${texmf_image_path}/.
done
sudo mktexlsr
