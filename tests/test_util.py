#!/usr/bin/env python

import unittest

from lulu.util import fs
from lulu.util import parser


class TestUtil(unittest.TestCase):
    def test_legitimize(self):
        self.assertEqual(fs.legitimize('1*2', os='Linux'), '1*2')
        self.assertEqual(fs.legitimize('1*2', os='Darwin'), '1*2')
        self.assertEqual(fs.legitimize('1*2', os='Windows'), '1-2')

    def test_parser(self):
        p = parser.get_parser('<h1> hello</h1>')
        self.assertEqual(p.h1.string.strip(), 'hello')


if __name__ == '__main__':
    unittest.main()
