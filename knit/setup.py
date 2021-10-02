#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from setuptools import setup, find_packages


def setup_package() -> None:
    metadata = dict()
    metadata['name'] = 'knit_markdown'
    metadata['version'] = '0.2.0'
    metadata['description'] = 'convert from markdown(tex) to PDF'
    metadata['author'] = 'tetutaro'
    metadata['url'] = 'https://github.com/tetutaro/knit_markdown'
    metadata['py_modules'] = ['knit']
    metadata['entry_points'] = {
        'console_scripts': [
            'knit_markdown = knit:main',
        ],
    }
    metadata['packages'] = find_packages()
    metadata['include_package_data'] = False
    setup(**metadata)
    return


if __name__ == "__main__":
    setup_package()
