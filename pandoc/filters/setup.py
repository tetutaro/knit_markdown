#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from setuptools import setup, find_packages


def setup_package():
    metadata = dict()
    metadata['name'] = 'kmd-filters'
    metadata['version'] = '0.2.1'
    metadata['description'] = 'pandocfilters for knit-markdown'
    metadata['author'] = 'tetutaro'
    metadata['url'] = 'https://github.com/tetutaro/knit_markdown'
    metadata['py_modules'] = ['crossref', 'latex', 'beamer']
    metadata['entry_points'] = {
        'console_scripts': [
            'kmd-filter-crossref = crossref:main',
            'kmd-filter-latex = latex:main',
            'kmd-filter-beamer = beamer:main',
        ],
    }
    metadata['packages'] = find_packages()
    metadata['include_package_data'] = False
    metadata['install_requires'] = [
        'panflute >= 2.1.0',
    ]
    setup(**metadata)
    return


if __name__ == "__main__":
    setup_package()
