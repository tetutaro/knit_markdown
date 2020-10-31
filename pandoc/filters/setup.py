#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from setuptools import setup, find_packages


def setup_package() -> None:
    metadata = dict()
    metadata['name'] = 'panclarinet'
    metadata['version'] = '0.1.0'
    metadata['description'] = 'filters for pandoc based on panflute'
    metadata['author'] = 'tetutaro'
    metadata['url'] = 'https://github.com/tetutaro/knit_markdown'
    metadata['py_modules'] = ['crossref', 'latex', 'beamer']
    metadata['entry_points'] = {
        'console_scripts': [
            'panclarinet_crossref = crossref:main',
            'panclarinet_latex = latex:main',
            'panclarinet_beamer = beamer:main',
        ],
    }
    metadata['packages'] = find_packages()
    metadata['include_package_data'] = False
    metadata['install_requires'] = [
        'panflute >= 1.12.5',
    ]
    setup(**metadata)
    return


if __name__ == "__main__":
    setup_package()
