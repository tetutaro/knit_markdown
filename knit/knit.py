#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import subprocess
import argparse
import platform

if platform.system() == 'Linux':
    SED_CMND = 'sed -e'
else:
    SED_CMND = 'sed -i "" -e'


def cleanup(bname: str, ext: str) -> None:
    cmd = f'latexmk -CA {bname}.tex'
    subprocess.call(cmd, shell=True)
    if os.path.isfile(bname + '.bbl'):
        os.remove(bname + '.bbl')
    if os.path.isfile(bname + '.nav'):
        os.remove(bname + '.nav')
    if os.path.isfile(bname + '.run.xml'):
        os.remove(bname + '.run.xml')
    if os.path.isfile(bname + '.snm'):
        os.remove(bname + '.snm')
    if os.path.isfile(bname + '.vrb'):
        os.remove(bname + '.vrb')
    if ext != '.tex' and os.path.isfile(bname + '.tex'):
        os.remove(bname + '.tex')
    return


def convert(bname: str, ext: str) -> None:
    fname = bname + ext
    if ext == '.tex':
        cmd = 'latexmk -pv {fname}'
    elif ext == '.md':
        if bname.endswith('.beamer'):
            cmd = ' '.join([
                'pandoc',
                '--template=kmd',
                '--filter=kmd-filter-crossref',
                '--filter=kmd-filter-beamer',
                '-t beamer {fname}',
                '-o {bname}.tex',
                '&&',
                f'{SED_CMND} "s/fragile/containsverbatim/g"',
                '{bname}.tex',
                '&&',
                f'{SED_CMND} "s/\\\\\\\\\\\\\\\\label/\\\\\\\\label/g"',
                '{bname}.tex',
                '&&',
                'latexmk -pv {bname}.tex',
            ])
        elif bname.endswith('.beamer169'):
            cmd = ' '.join([
                'pandoc',
                '--template=kmd169',
                '--filter=kmd-filter-crossref',
                '--filter=kmd-filter-beamer',
                '-t beamer {fname}',
                '-o {bname}.tex',
                '&&',
                f'{SED_CMND} "s/fragile/containsverbatim/g"',
                '{bname}.tex',
                '&&',
                f'{SED_CMND} "s/\\\\\\\\\\\\\\\\label/\\\\\\\\label/g"',
                '{bname}.tex',
                '&&',
                'latexmk -pv {bname}.tex',
            ])
        else:
            cmd = ' '.join([
                'pandoc -N',
                '--template=kmd',
                '--filter=kmd-filter-crossref',
                '--filter=kmd-filter-latex',
                '-t latex {fname}',
                '-o {bname}.tex',
                '&&',
                f'{SED_CMND}',
                '"s/@{{}}//g"',
                '{bname}.tex',
                '&&',
                f'{SED_CMND} "s/\\\\\\\\\\\\\\\\label/\\\\\\\\label/g"',
                '{bname}.tex',
                '&&',
                'latexmk -pv {bname}.tex'
            ])
    else:
        return
    cmd = cmd.format(fname=fname, bname=bname)
    subprocess.call(cmd, shell=True)
    return


def invoke(filename: str, clean: bool) -> None:
    if not os.path.isfile(filename):
        raise FileNotFoundError(f'{filename} not found')
    bname, ext = os.path.splitext(filename)
    if ext not in ['.md', '.tex']:
        raise ValueError('indicate markdown/tex file')
    if clean:
        cleanup(bname=bname, ext=ext)
    else:
        convert(bname=bname, ext=ext)
    return


def main() -> None:
    parser = argparse.ArgumentParser('convert markdown/tex to PDF')
    parser.add_argument(
        'filename', type=str,
        help='file to convert'
    )
    parser.add_argument(
        '-c', '--clean', action='store_true',
        help='remove intermediate files'
    )
    args = parser.parse_args()
    invoke(**vars(args))
    return


if __name__ == '__main__':
    main()
