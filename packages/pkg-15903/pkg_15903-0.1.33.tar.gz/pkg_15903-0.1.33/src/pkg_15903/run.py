#!/usr/bin/env python

"""
Purpose: run some test package
"""

import click
import requests

from pkg_15903 import __version__


@click.command()
@click.option('--url', required=False, default='https://google.com', help='Enter URL')
@click.version_option(version=__version__)
def main(url):
    response = requests.get(url)
    print(f'URL ({response.url}) result: {response.status_code}')


if __name__ == '__main__':  # pragma: no cover
    main()
