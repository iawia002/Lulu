# coding=utf-8

from fabric.api import (
    local,
)


def test(proxy=False):
    cmd = 'PYTHONPATH=./ {} coverage run tests/runtests.py'.format(
        'proxychains4 -q' if proxy else ''
    )
    local(cmd)


def test_download(func):
    '''
    fab test_download:acfun
    '''
    cmd = (
        'PYTHONPATH=./ python tests/test_extractors.py '
        'TestExtractors.test_{}'.format(func)
    )
    local(cmd)


def upload():
    local(
        'python3 setup.py upload'
    )
