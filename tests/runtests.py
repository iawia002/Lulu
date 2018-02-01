#!/usr/bin/env python
# coding=utf-8

import unittest


TEST_MODULES = [
    'tests.test_util',
    'tests.test_common',
    'tests.test_extractors',
]


def all():
    return unittest.defaultTestLoader.loadTestsFromNames(TEST_MODULES)


if __name__ == '__main__':
    unittest.main(defaultTest='all')
