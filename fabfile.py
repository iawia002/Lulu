# coding=utf-8

from fabric.api import (
    local,
)


def test(proxy=False):
    cmd = 'PYTHONPATH=./ {} coverage run tests/runtests.py'.format(
        'proxychains4' if proxy else ''
    )
    local(cmd)


def upload():
    local(
        'python3 setup.py upload'
    )
