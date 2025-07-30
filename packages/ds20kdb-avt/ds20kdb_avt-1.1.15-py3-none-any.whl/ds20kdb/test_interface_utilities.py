#!/usr/bin/env python3
"""
Tests for the utility functions in interface.py.

Run with <filename.py> -v.

See:
https://docs.python.org/3/library/unittest.html#assert-methods
"""

import datetime
import itertools
import math
import unittest
import sys

import interface

# required here: <string>.removeprefix()
assert sys.version_info >= (3, 9), 'Python 3.9 or later requried'

# required here: interface.qr_code_valid(): v1.0.26, 12 May 2024
assert tuple(
    # remove alpha/beta suffix from version: 1.1a0 becomes 1.1
    int(''.join(itertools.takewhile(lambda v: v.isdigit(), x)))
    for x in interface.__version__.split('.')
) >= (1, 0, 26), (
    'ds20kdb 1.0.26 or newer required '
    f'(found {interface.__version__})'
)


###############################################################################
# TESTS | interface.py, utility functions
###############################################################################


class TestUtilities(unittest.TestCase):
    """
    interface.py, utilities section
    """

    def test_dict_from_qrcode(self):
        """
        Check dict creation from dbi.dict_from_qrcode(...).
        """
        test_cases = {
            # example from documentation
            '22061703000032001': {
                'timestamp': datetime.datetime(2022, 6, 17, 0, 0),
                'production': False,
                'version_string': '3.0',
                'version_major': 3,
                'version_minor': 0,
                'serial_number': 32,
                'part_number': 1
            }
        }
        for qrcode, response in test_cases.items():
            self.assertEqual(interface.dict_from_qrcode(qrcode), response)

    def test_removesuffix(self):
        """
        The tested function is only present to support old Python
        versions <= 3.8.
        """
        # standard removal
        self.assertEqual(
            interface.removesuffix('vpcb_asic_test', '_test'), 'vpcb_asic',
        )

        # pass through
        self.assertEqual(
            interface.removesuffix('vpcb_asic', '_test'), 'vpcb_asic'
        )
        self.assertEqual(interface.removesuffix('vpcb_asic', ''), 'vpcb_asic')
        self.assertEqual(interface.removesuffix('', '_test'), '')
        self.assertEqual(interface.removesuffix('', ''), '')
        self.assertEqual(interface.removesuffix('', None), '')
        self.assertIsNone(interface.removesuffix(None, None))
        self.assertIsNone(interface.removesuffix(None, ''))

    def test_qr_code_valid(self):
        """
        The QR code should be a string, but a valid int should be tolerated.
        """
        # known good QR code
        self.assertTrue(interface.qr_code_valid('22061703000032001'))
        self.assertTrue(interface.qr_code_valid(22061703000032001))
        # bad QR code
        self.assertFalse(interface.qr_code_valid('1234'))
        self.assertFalse(interface.qr_code_valid(1234))
        self.assertFalse(interface.qr_code_valid(''))
        self.assertFalse(interface.qr_code_valid(None))
        self.assertFalse(interface.qr_code_valid(math.nan))
        self.assertFalse(interface.qr_code_valid(math.inf))
        self.assertFalse(interface.qr_code_valid(0))
        self.assertFalse(interface.qr_code_valid(-0.0))

        # Part No., 0 [min]
        self.assertTrue(interface.qr_code_valid('22061703000032000'))
        # Part No., 999 [max]
        self.assertTrue(interface.qr_code_valid('22061703000032999'))

        # Schematic version, 00 (0.0) [min]
        self.assertTrue(interface.qr_code_valid('22061700000032001'))
        # Schematic version, 99 (9.9) [max]
        self.assertTrue(interface.qr_code_valid('22061709900032001'))

        # Production flag, 0 [min]
        self.assertTrue(interface.qr_code_valid('22061703000032001'))
        # Production flag, 1 [max]
        self.assertTrue(interface.qr_code_valid('22061713000032001'))
        # bad production flag, 2
        self.assertTrue(not interface.qr_code_valid('22061723000032001'))
        # bad production flag, 9
        self.assertTrue(not interface.qr_code_valid('22061793000032001'))

        # # we're really just testing standard library datetime, so keep this
        # minimal

        # Year,  0 (2000) [min]
        self.assertTrue(interface.qr_code_valid('00061703000032001'))
        # Year, 99 (2099) [max]
        self.assertTrue(interface.qr_code_valid('99061703000032001'))

        # Month, 1 (2000) [min]
        self.assertTrue(interface.qr_code_valid('22011703000032001'))
        # Month, 12 (2099) [max]
        self.assertTrue(interface.qr_code_valid('22121703000032001'))
        # Month, 0
        self.assertFalse(interface.qr_code_valid('22001703000032001'))
        # Month, 13
        self.assertFalse(interface.qr_code_valid('22131703000032001'))

        # January 1st
        self.assertTrue(interface.qr_code_valid('22010103000032001'))
        # January 31st
        self.assertTrue(interface.qr_code_valid('22013103000032001'))
        # January 0th
        self.assertFalse(interface.qr_code_valid('22010003000032001'))
        # January 32nd
        self.assertFalse(interface.qr_code_valid('22013203000032001'))

    def test_sanitise(self):
        """
        return int from numeric, if it's close enough to an int.
        """
        self.assertEqual(interface.sanitise(41), 41)
        self.assertEqual(interface.sanitise(41.0), 41)
        self.assertEqual(interface.sanitise(4.1e1), 41)
        self.assertEqual(interface.sanitise('41'), 41)
        self.assertEqual(interface.sanitise('41.0'), 41)
        self.assertEqual(interface.sanitise('41.0000000000000001'), 41)
        self.assertEqual(interface.sanitise(41.0000000000000001), 41)
        self.assertEqual(interface.sanitise(4.1e0), None)
        self.assertEqual(interface.sanitise(4.1), None)
        self.assertEqual(interface.sanitise('4.1'), None)
        self.assertEqual(interface.sanitise(41.00000000000001), None)

    def test_sanitise_multiple(self):
        """
        Basic checks for interface.sanitise_multiple()
        """
        self.assertEqual(interface.sanitise_multiple(), [])
        self.assertIsNone(interface.sanitise_multiple([]))
        self.assertIsNone(interface.sanitise_multiple(None))
        self.assertEqual(interface.sanitise_multiple(1, 2, 3), [1, 2, 3])
        self.assertEqual(interface.sanitise_multiple(1), [1])

    def test_sort_qrcodes_by_serial_number(self):
        """
        QR codes string sort order may not match sort by S. No.
        due to batch processing order.

        index  sorted by string  sorted by S.No.   match
        0228   23062913000281001 23062913000281001 True
        0229   23062913000282001 23062913000282001 True
        0230   23062913000290001 23081413000284001 False
        0231   23062913000291001 23081413000288001 False
        ...
        0249   23081413000288001 23062913000317001 False
        0250   23081413000289001 23062913000319001 False
        0251   23081413000323001 23081413000323001 True
        0252   23081413000324001 23081413000324001 True
        """
        string_sort_order = [
            '23062913000281001', '23062913000282001', '23062913000290001',
            '23062913000291001', '23062913000292001', '23062913000293001',
            '23062913000295001', '23062913000296001', '23062913000301001',
            '23062913000302001', '23062913000303001', '23062913000304001',
            '23062913000307001', '23062913000310001', '23062913000313001',
            '23062913000314001', '23062913000315001', '23062913000316001',
            '23062913000317001', '23062913000319001', '23081413000284001',
            '23081413000288001', '23081413000289001', '23081413000323001',
            '23081413000324001',
        ]
        serno_sort_order = [
            '23062913000281001', '23062913000282001', '23081413000284001',
            '23081413000288001', '23081413000289001', '23062913000290001',
            '23062913000291001', '23062913000292001', '23062913000293001',
            '23062913000295001', '23062913000296001', '23062913000301001',
            '23062913000302001', '23062913000303001', '23062913000304001',
            '23062913000307001', '23062913000310001', '23062913000313001',
            '23062913000314001', '23062913000315001', '23062913000316001',
            '23062913000317001', '23062913000319001', '23081413000323001',
            '23081413000324001',
        ]

        # Not a check of the method, just a quick confidence check that the
        # above lists of QR codes are the same.
        self.assertTrue(set(string_sort_order), set(serno_sort_order))

        self.assertTrue(
            interface.sort_qrcodes_by_serial_number(string_sort_order),
            serno_sort_order,
        )

    def test_wafer_map_valid_locations(self):
        """
        Test wafer map locations.
        """
        # check valid SiPM locations on production wafers
        production_locs_l = list(interface.wafer_map_valid_locations())
        production_locs_s = set(production_locs_l)

        self.assertEqual(len(production_locs_s), len(production_locs_l))
        self.assertEqual(len(production_locs_s), 264)

        # check valid SiPM locations on pre-production wafers
        pre_prod_locs_l = list(
            interface.wafer_map_valid_locations(legacy=True)
        )
        pre_prod_locs_s = set(pre_prod_locs_l)

        self.assertEqual(len(pre_prod_locs_s), len(pre_prod_locs_l))
        self.assertEqual(len(pre_prod_locs_s), 268)

        # Check the difference between production and pre-production
        # (legacy) valid locations. Only the left-most 2 (column 2) and
        # right-most 2 (column 17 )SiPMs are untested, and unsuitable for
        # production.
        self.assertEqual(
            pre_prod_locs_s.difference(production_locs_s),
            {(2, 12), (2, 13), (17, 12), (17, 13)}
        )


###############################################################################
if __name__ == '__main__':
    unittest.main()
