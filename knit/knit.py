#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import subprocess
import argparse

parser = argparse.ArgumentParser("convert markdown/tex to PDF")
parser.add_argument(
    'filename', type=str, help='file to convert'
)
parser.add_argument(
    '-c', '--clean', action='store_true', help='clean files'
)


def clean(bname: str) -> None:
    cmd = 'latexmk -CA {bname}.tex'.format(bname=bname)
    subprocess.call(cmd, shell=True)
    if os.path.exists(bname + '.bbl'):
        os.remove(bname + '.bbl')
    if os.path.exists(bname + '.nav'):
        os.remove(bname + '.nav')
    if os.path.exists(bname + '.run.xml'):
        os.remove(bname + '.run.xml')
    if os.path.exists(bname + '.snm'):
        os.remove(bname + '.snm')
    if os.path.exists(bname + '.vrb'):
        os.remove(bname + '.vrb')
    if exit != '.tex' and os.path.exists(bname + '.tex'):
        os.remove(bname + '.tex')
    return


def main() -> None:
    args = parser.parse_args()
    fname = args.filename
    if not os.path.exists(fname):
        raise FileNotFoundError('%s not found' % fname)
    bname, ext = os.path.splitext(fname)
    if args.clean:
        clean(bname=bname)
        return
    if ext == '.tex':
        cmd = 'latexmk -pv {fname}'
    elif ext == '.md':
        if bname.endswith('.beamer'):
            cmd = 'pandoc --template=panclarinet --filter=panclarinet_crossref --filter=panclarinet_beamer -t beamer {fname} -o {bname}.tex && sed -i "" -e "s/fragile/containsverbatim/g" {bname}.tex && sed -i "" -e "s/\\\\\\\\\\\\\\\\label/\\\\\\\\label/g" {bname}.tex && latexmk -pv {bname}.tex'
        elif bname.endswith('.beamer169'):
            cmd = 'pandoc --template=panclarinet169 --filter=panclarinet_crossref --filter=panclarinet_beamer -t beamer {fname} -o {bname}.tex && sed -i "" -e "s/fragile/containsverbatim/g" {bname}.tex && sed -i "" -e "s/\\\\\\\\\\\\\\\\label/\\\\\\\\label/g" {bname}.tex && latexmk -pv {bname}.tex'
        else:
            cmd = 'pandoc -N --template=panclarinet --filter=panclarinet_crossref --filter=panclarinet_latex -t latex {fname} -o {bname}.tex && sed -i "" -e "s/@{{}}//g" {bname}.tex && sed -i "" -e "s/\\\\\\\\\\\\\\\\label/\\\\\\\\label/g" {bname}.tex && latexmk -pv {bname}.tex'
    else:
        return
    cmd = cmd.format(fname=fname, bname=bname)
    subprocess.call(cmd, shell=True)
    return


if __name__ == '__main__':
    main()
