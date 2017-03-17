# -*- coding: utf-8 -*-

__author__ = """Microsoft Corporation"""
__email__ = 'ptvshelp@microsoft.com'
__version__ = '0.1.0'

from .kudu import KuduSession

if __name__ == '__main__':
    from .cli import main
    main()