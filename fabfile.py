# coding=utf-8

from fabric.api import (
    local,
)


def test():
    local(
        'PYTHONPATH=./ coverage run tests/runtests.py'
    )


def upload():
    local(
        'python3 setup.py upload'
    )
