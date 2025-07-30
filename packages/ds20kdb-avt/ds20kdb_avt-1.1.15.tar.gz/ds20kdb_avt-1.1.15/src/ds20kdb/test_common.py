#!/usr/bin/env python3
"""
Tests for common.py.

Run with <filename.py> -v.

See:
https://docs.python.org/3/library/unittest.html#assert-methods
"""

import itertools
import unittest
import sys

import interface
import common

# required here: <string>.removeprefix()
assert sys.version_info >= (3, 9), 'Python 3.9 or later requried'

assert tuple(
    # remove alpha/beta suffix from version: 1.1a0 becomes 1.1
    int(''.join(itertools.takewhile(lambda v: v.isdigit(), x)))
    for x in interface.__version__.split('.')
) >= (1, 1), (
    'ds20kdb 1.1 or newer required '
    f'(found {interface.__version__})'
)


###############################################################################
# TESTS | common.py, general
###############################################################################


class TestPrettyPrint(unittest.TestCase):
    """
    common.py
    """

    def test_compact_expand_integer_sequence(self):
        """
        Test pretty printing of sequences.
        """
        long_form = [
            [],
            [1],
            [1, 2, 3],
            [1, 5, 6, 7, 8],
            [1, 5, 6, 7, 8, 20],
            [1, 5, 6, 7, 8, 14, 15, 16, 20],
            [1, 5, 6, 7, 8, 11, 14, 15, 16, 17, 18, 19, 40],
        ]
        short_form = [
            '',
            '1',
            '1..3',
            '1, 5..8',
            '1, 5..8, 20',
            '1, 5..8, 14..16, 20',
            '1, 5..8, 11, 14..19, 40',
        ]

        for lof, shf in zip(long_form, short_form):
            self.assertEqual(common.compact_integer_sequence(lof), shf)
            self.assertEqual(common.expand_integer_sequence(shf), lof)


###############################################################################
if __name__ == '__main__':
    unittest.main()
