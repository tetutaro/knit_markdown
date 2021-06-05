#!/usr/bin/env bash
pwd=`pwd`
texmf_local=`kpsewhich -var-value=TEXMFLOCAL`
local_theme_path="${pwd}/themes/theme"
texmf_theme_path="${texmf_local}/tex/latex/beamer/themes/theme"
local_image_path="${pwd}/themes/images"
texmf_image_path="${texmf_local}/tex/latex/beamer/themes/images"
cd ${local_theme_path}
for file in *.sty; do
	rm ${texmf_theme_path}/${file}
done
cd ${local_image_path}
for file in *.png; do
	rm ${texmf_image_path}/${file}
done
sudo mktexlsr
