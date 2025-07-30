#!/usr/bin/env python3
"""
Tests for class Database in interface.py.

Run with <filename.py> -v.

See:
https://docs.python.org/3/library/unittest.html#assert-methods
"""

import collections
import itertools
import logging
import math
import unittest
import sys

import constants
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
# support
###############################################################################


def nan_to_none(dct):
    """
    Convert any NaN dict values to None. This makes equality tests less
    troublesome.

    ---------------------------------------------------------------------------
    args
        dct : dict
            e.g. {
                'vtile_pid': 64, 'vpcb_asic_id': 74, 'sipm_1': 663,
                ...
                'sipm_24': 843, 'vpdu_id': nan, 'run_number': 2,
                'production_date': '2023-01-12 13:00:00',
                'solder_id': 13, 'institute_id': 5, 'comment': nan,
            }
    ---------------------------------------------------------------------------
    returns
        data : dict
            e.g. {
                'vtile_pid': 64, 'vpcb_asic_id': 74, 'sipm_1': 663,
                ...
                'sipm_24': 843, 'vpdu_id': None, 'run_number': 2,
                'production_date': '2023-01-12 13:00:00',
                'solder_id': 13, 'institute_id': 5, 'comment': None,
            }
    ---------------------------------------------------------------------------
    """
    data = {}

    for field, dval in dct.items():
        try:
            fnan = math.isnan(dval)
        except TypeError:
            # probably a text field
            value = dval
        else:
            # Original value was blank (float('nan') otherwise propagate
            # float value.
            value = None if fnan else dval

        data[field] = value

    return data


###############################################################################
# Enable testing of database-centric methods by intercepting the Requests
# session.
###############################################################################


# map URL (with common prefix removed) to raw text response
RAW_RESPONSES = {
    # hash(dbi.describe_raw()) -8723067029205089134
    'db/describe': (
        '["acs", "amicra_settings", "attribute", "attribute_description", '
        '"cryoprobe_card", "sipm", "sipm_test", "user_test", "vtile", '
        '"detector", "dummy", "dummyload", "dummyload_test", "motherboard", '
        '"wafer", "noa_users", "pcb", "pcb_status", "pdu", "pdu_pulse_test", '
        '"sipm_qc", "tile", "solder", "tile_setup", "tile_status", '
        '"tile_test_offline", "vasic", "vasic_grip_ring", "vasic_test", '
        '"vasic_wafer", "vcable", "vmotherboard", "vmotherboard_test", '
        '"vpcb", "vpcb_asic", "vpcb_asic_test", "vpcb_test", "vpdu", '
        '"vpdu_cold_test", "vpdu_test", "vtile_test", "wafer_defects", '
        '"wafer_status", "vtile_cold_test", "tile2", "tile_test", "tile_qc", '
        '"motherboard_pdu_status", "vtile_qc", "unusable_sipm", "pdu_test", '
        '"pdu_qc", "vmotherboard_pdu_status", "pcb_qc", "pcb_test", '
        '"vdust_test", "vtile_exp"]'
    ),
    # dbi.describe_raw('sipm')
    'db/describe/sipm': (
        '["sipm_pid", "wafer_id", "column", "row", "tile_id", "tile_type"]'
    ),
    # dbi.describe_raw('sipm_test')
    'db/describe/sipm_test': (
        '["id", "timestamp", "institute_id", "operator", "sipm_id", "vbd", '
        '"rq", "i_at_20v", "i_at_35v", "iv_rev", "iv_fwd", "chi2_shape", '
        '"sipm_qc_id", "group", "temperature", "classification", '
        '"quality_flag", "comment", "i_at_25v"]'
    ),
    # hash(dbi.describe_raw('vtile')), 1163532309661987894
    'db/describe/vtile': (
        '["vtile_pid", "vpcb_asic_id", "sipm_1", "sipm_2", "sipm_3", '
        '"sipm_4", "sipm_5", "sipm_6", "sipm_7", "sipm_8", "sipm_9", '
        '"sipm_10", "sipm_11", "sipm_12", "sipm_13", "sipm_14", "sipm_15", '
        '"sipm_16", "sipm_17", "sipm_18", "sipm_19", "sipm_20", "sipm_21", '
        '"sipm_22", "sipm_23", "sipm_24", "vpdu_id", "run_number", '
        '"production_date", "solder_id", "institute_id", "comment"]'
    ),
    # hash(dbi.describe_raw('vtile_test')) -380170252979837445
    'db/describe/vtile_test': (
        '["id", "timestamp", "institute_id", "operator", "vtile_id", '
        '"optical_inspection", "metrology", "capacitance_curve", "iv_curve", '
        '"breakdown_voltage", "noise_curve", "capacitance_1", "resistance_1", '
        '"capacitance_2", "resistance_2", "capacitance_3", "resistance_3", '
        '"capacitance_4", "resistance_4", "configuration", "temperature", '
        '"quality_flag", "comment", "oven_temperature"]'
    ),
    # hash(dbi.get_raw('vtile', vtile_pid=64)) -2619542856731662222
    'item/vtile?w="vtile_pid"=\'64\'': (
        'vtile_pid,vpcb_asic_id,sipm_1,sipm_2,sipm_3,sipm_4,sipm_5,sipm_6,'
        'sipm_7,sipm_8,sipm_9,sipm_10,sipm_11,sipm_12,sipm_13,sipm_14,sipm_15,'
        'sipm_16,sipm_17,sipm_18,sipm_19,sipm_20,sipm_21,sipm_22,sipm_23,'
        'sipm_24,vpdu_id,run_number,production_date,solder_id,institute_id,'
        'comment\n'
        '64,74,663,550,640,765,544,679,612,546,673,646,677,649,653,788,767,'
        '1041,382,412,501,379,522,1063,904,843,,2,2023-01-12 13:00:00,13,5,\n'
    ),
    # Contrived - and shortened - response to dbi.get('vtile_qrcode') as used
    # in dbi.vtile_id_to_qrcode_lut()
    #
    # dbi.get_raw('vtile_qrcode')
    #
    # Note that in this context a custom URL can be formed by adding a
    # `?any_random_text` suffix, and a response from the db obtained with
    # dbi.session.get(URL).text
    'item/vtile_qrcode': (
        'vtile_id,qrcode\n'
        # some old pre-production
        '8,22060103000001001\n10,22060103000015001\n'
        '12,22060103000000001\n11,22060103000016001\n'
        # faked vTile with one repair
        '110,23062903000169001\n'
        '10000,23062903000169001\n'
        # some new production
        '712,24013013001440001\n713,24013013001441001\n'
        '714,24013013001442001\n715,24013013001443001\n'
    ),
    'item/vpcb': (
        'vpcb_pid,manufacturer,run_number,production_date,vpcb_asic_id,qrcode,comment\n'
        # some old pre-production
        '14,3,1,2022-07-18 10:42:31,,22060103000015001,\n'
        '20,3,1,2022-07-18 17:17:33,,22060103000016001,\n'
        # some mid range production, already made into a vTile
        '118,3,4,2023-07-19 15:15:46,,23062903000169001,\n'
        # some new production
        '1936,3,0,2024-05-24 16:27:33,,24013013001441001,\n'
        '1938,3,0,2024-05-24 16:31:06,,24013013001443001,\n'
        '2195,3,0,2024-05-23 17:13:26,,24013013001386001,\n'
        '2196,3,0,2024-05-23 17:15:46,,24013013001387001,\n'
    ),
}


PROCESSED_RESPONSES = {
    # dbi.describe().data
    'db/describe': [
        'acs', 'amicra_settings', 'attribute', 'attribute_description',
        'cryoprobe_card', 'sipm', 'sipm_test', 'user_test', 'vtile',
        'detector', 'dummy', 'dummyload', 'dummyload_test', 'motherboard',
        'wafer', 'noa_users', 'pcb', 'pcb_status', 'pdu', 'pdu_pulse_test',
        'sipm_qc', 'tile', 'solder', 'tile_setup', 'tile_status',
        'tile_test_offline', 'vasic', 'vasic_grip_ring', 'vasic_test',
        'vasic_wafer', 'vcable', 'vmotherboard', 'vmotherboard_test', 'vpcb',
        'vpcb_asic', 'vpcb_asic_test', 'vpcb_test', 'vpdu', 'vpdu_cold_test',
        'vpdu_test', 'vtile_test', 'wafer_defects', 'wafer_status',
        'vtile_cold_test', 'tile2', 'tile_test', 'tile_qc',
        'motherboard_pdu_status', 'vtile_qc', 'unusable_sipm', 'pdu_test',
        'pdu_qc', 'vmotherboard_pdu_status', 'pcb_qc', 'pcb_test',
        'vdust_test', 'vtile_exp'
    ],
    # dbi.describe('sipm').data
    'db/describe/sipm': [
        'sipm_pid', 'wafer_id', 'column', 'row', 'tile_id', 'tile_type'
    ],
    # dbi.describe('sipm_test').data
    'db/describe/sipm_test': [
        'id', 'timestamp', 'institute_id', 'operator', 'sipm_id', 'vbd', 'rq',
        'i_at_20v', 'i_at_35v', 'iv_rev', 'iv_fwd', 'chi2_shape',
        'sipm_qc_id', 'group', 'temperature', 'classification',
        'quality_flag', 'comment', 'i_at_25v'
    ],
    # dbi.describe('vtile').data
    'db/describe/vtile': [
        'vtile_pid', 'vpcb_asic_id', 'sipm_1', 'sipm_2', 'sipm_3', 'sipm_4',
        'sipm_5', 'sipm_6', 'sipm_7', 'sipm_8', 'sipm_9', 'sipm_10', 'sipm_11',
        'sipm_12', 'sipm_13', 'sipm_14', 'sipm_15', 'sipm_16', 'sipm_17',
        'sipm_18', 'sipm_19', 'sipm_20', 'sipm_21', 'sipm_22', 'sipm_23',
        'sipm_24', 'vpdu_id', 'run_number', 'production_date', 'solder_id',
        'institute_id', 'comment'
    ],
    # dbi.describe('vtile_test').data
    'db/describe/vtile_test': [
        'id', 'timestamp', 'institute_id', 'operator', 'vtile_id',
        'optical_inspection', 'metrology', 'capacitance_curve', 'iv_curve',
        'breakdown_voltage', 'noise_curve', 'capacitance_1', 'resistance_1',
        'capacitance_2', 'resistance_2', 'capacitance_3', 'resistance_3',
        'capacitance_4', 'resistance_4', 'configuration', 'temperature',
        'quality_flag', 'comment', 'oven_temperature'
    ],
    # dbi.get('vtile', vtile_pid=64).data.to_dict('records')
    'item/vtile?w="vtile_pid"=\'64\'': [
        {
            'vtile_pid': 64, 'vpcb_asic_id': 74, 'sipm_1': 663, 'sipm_2': 550,
            'sipm_3': 640, 'sipm_4': 765, 'sipm_5': 544, 'sipm_6': 679,
            'sipm_7': 612, 'sipm_8': 546, 'sipm_9': 673, 'sipm_10': 646,
            'sipm_11': 677, 'sipm_12': 649, 'sipm_13': 653, 'sipm_14': 788,
            'sipm_15': 767, 'sipm_16': 1041, 'sipm_17': 382, 'sipm_18': 412,
            'sipm_19': 501, 'sipm_20': 379, 'sipm_21': 522, 'sipm_22': 1063,
            'sipm_23': 904, 'sipm_24': 843, 'vpdu_id': None, 'run_number': 2,
            'production_date': '2023-01-12 13:00:00', 'solder_id': 13,
            'institute_id': 5, 'comment': None
        }
    ],
    # dbi.vtile_id_to_qrcode_lut()
    'item/vtile_qrcode': {
        8: '22060103000001001', 10: '22060103000015001',
        12: '22060103000000001', 11: '22060103000016001',
        # repaired vTile
        110: '23062903000169001', 10000: '23062903000169001',
        712: '24013013001440001', 713: '24013013001441001',
        714: '24013013001442001', 715: '24013013001443001',
    },
    # dbi.vtile_id_to_qrcode_lut(reverse=True)
    'item/vtile_qrcode_reversed': {
        '22060103000001001': [8],
        '22060103000015001': [10],
        '22060103000000001': [12],
        '22060103000016001': [11],
        '23062903000169001': [110, 10000],
        '24013013001440001': [712],
        '24013013001441001': [713],
        '24013013001442001': [714],
        '24013013001443001': [715],
    },
    # dbi.get('vpcb').data.to_dict('records')
    'item/vpcb': [
        {
            'vpcb_pid': 14, 'manufacturer': 3, 'run_number': 1,
            'production_date': '2022-07-18 10:42:31', 'vpcb_asic_id': None,
            'qrcode': 22060103000015001, 'comment': None,
        },
        {
            'vpcb_pid': 20, 'manufacturer': 3, 'run_number': 1,
            'production_date': '2022-07-18 17:17:33', 'vpcb_asic_id': None,
            'qrcode': 22060103000016001, 'comment': None,
        },
        {
            'vpcb_pid': 118, 'manufacturer': 3, 'run_number': 4,
            'production_date': '2023-07-19 15:15:46', 'vpcb_asic_id': None,
            'qrcode': 23062903000169001, 'comment': None,
        },
        {
            'vpcb_pid': 1936, 'manufacturer': 3, 'run_number': 0,
            'production_date': '2024-05-24 16:27:33', 'vpcb_asic_id': None,
            'qrcode': 24013013001441001, 'comment': None,
        },
        {
            'vpcb_pid': 1938, 'manufacturer': 3, 'run_number': 0,
            'production_date': '2024-05-24 16:31:06', 'vpcb_asic_id': None,
            'qrcode': 24013013001443001, 'comment': None,
        },
        {
            'vpcb_pid': 2195, 'manufacturer': 3, 'run_number': 0,
            'production_date': '2024-05-23 17:13:26', 'vpcb_asic_id': None,
            'qrcode': 24013013001386001, 'comment': None,
        },
        {
            'vpcb_pid': 2196, 'manufacturer': 3, 'run_number': 0,
            'production_date': '2024-05-23 17:15:46', 'vpcb_asic_id': None,
            'qrcode': 24013013001387001, 'comment': None,
        },
    ],
}


class FakeResponse:
    """
    Rudimentary fake Requests response data container.
    """
    def __init__(self, url):
        resp = RAW_RESPONSES.get(url.removeprefix(constants.BASE_URL))

        if resp is None:
            # deliberate unofficial response code
            self.status_code = 597
            self.text = 'URL not found in dictionary of known test cases'
        else:
            self.status_code = 200
            self.text = resp


class FakeSession:
    """
    Fake Requests session.
    """
    def get(self, url):
        """
        Fake GET operation.
        """
        return FakeResponse(url)


class FakeDatabase(interface.Database):
    """
    Patch this over the normal database connection.
    """
    def __init__(self):
        self.session = FakeSession()


###############################################################################
# TESTS | interface.py, class Database()
###############################################################################


class TestInterfaceDatabase(unittest.TestCase):
    """
    interface.py, database interface
    """
    def setUp(self):
        self.dbi = FakeDatabase()
        # for debug, in case we need to see all details of a long diff
        # self.maxDiff = None

    # -------------------------------------------------------------------------
    # tests
    # -------------------------------------------------------------------------

    def test_describe(self):
        """
        interface.Database().describe(...)
        """
        response = self.dbi.describe()
        self.assertFalse(response.network_timeout)
        self.assertEqual(response.data, PROCESSED_RESPONSES['db/describe'])

        response = self.dbi.describe('vtile')
        self.assertFalse(response.network_timeout)
        self.assertEqual(
            response.data, PROCESSED_RESPONSES['db/describe/vtile']
        )

        response = self.dbi.describe('vtile_test')
        self.assertFalse(response.network_timeout)
        self.assertEqual(
            response.data, PROCESSED_RESPONSES['db/describe/vtile_test']
        )

    def test_get(self):
        """
        interface.Database().get(...)
        """
        response = self.dbi.get('vtile', vtile_pid=64)
        self.assertFalse(response.network_timeout)

        data = []
        for datum in response.data.to_dict('records'):
            data.append(nan_to_none(datum))

        self.assertEqual(
            data,
            PROCESSED_RESPONSES['item/vtile?w="vtile_pid"=\'64\'']
        )

    def test_get_url(self):
        """
        Verify URL creation for databse GET operations.
        """

        # ---------------------------------------------------------------------
        # table only
        # ---------------------------------------------------------------------

        response = self.dbi.get_url('wafer')
        self.assertEqual(
            response,
            f'{constants.BASE_URL}item/wafer'
        )

        # ---------------------------------------------------------------------
        # table with field value
        # ---------------------------------------------------------------------

        response = self.dbi.get_url('wafer', wafer_id=64)
        self.assertEqual(
            response,
            f'{constants.BASE_URL}item/wafer?w="wafer_id"=\'64\''
        )

        # ---------------------------------------------------------------------
        # limit number of rows in the response
        #
        # refer to feature request:
        # https://gitlab.in2p3.fr/darkside/productiondb_software/-/issues/2
        # ---------------------------------------------------------------------

        # return 4 rows from table sipm, sort by field wafer_id, (d)escending
        qmr = (4, 'wafer_id', 'd')
        response = self.dbi.get_url('sipm', query_max_results=qmr)
        self.assertEqual(
            response,
            f'{constants.BASE_URL}item/sipm?l=4&ob=wafer_id=d'
        )

        # ---------------------------------------------------------------------
        # inner join
        #
        # refer to feature request:
        # https://gitlab.in2p3.fr/darkside/productiondb_software/-/issues/3
        # ---------------------------------------------------------------------

        joins = [
            ('wafer', 'sipm.wafer_id', 'wafer_pid'),
            ('sipm', 'sipm_id', 'sipm.sipm_pid'),
        ]
        response = self.dbi.get_url('sipm_test', joins=joins, wafer_pid=1261)
        self.assertEqual(
            response,
            (
                f'{constants.BASE_URL}item/sipm_test'
                '?ij[0]=wafer&on[0]=sipm.wafer_id=wafer_pid'
                '&ij[1]=sipm&on[1]=sipm_id=sipm.sipm_pid'
                '&w="wafer_pid"=\'1261\''
            )
        )

        # ---------------------------------------------------------------------
        # inner join and row limit together
        # ---------------------------------------------------------------------

        # return 4 rows from table sipm_test, sort by field operator,
        # (a)scending
        qmr = (4, 'operator', 'a')
        response = self.dbi.get_url(
            'sipm_test', joins=joins, wafer_pid=1261, query_max_results=qmr
        )
        self.assertEqual(
            response,
            f'{constants.BASE_URL}item/sipm_test'
            '?ij[0]=wafer&on[0]=sipm.wafer_id=wafer_pid'
            '&ij[1]=sipm&on[1]=sipm_id=sipm.sipm_pid'
            '&l=4&ob=operator=a&w="wafer_pid"=\'1261\''
        )

    def test_vtile_id_to_qrcode_lut(self):
        """
        interface.Database().get('vtile_qrcode') look-up table.

        It is expected that this SQL View derived dict will contain multiple
        keys (IDs) for the same value (QR code) once vTile repairs are
        recorded in the datebase.

        This test obtains a look-up table dict that has multiple keys per
        value.
        """
        response_dict = nan_to_none(self.dbi.vtile_id_to_qrcode_lut())
        self.assertEqual(
            response_dict, PROCESSED_RESPONSES['item/vtile_qrcode']
        )
        self.assertTrue(
            any(
                x == 2
                for x in collections.Counter(response_dict.values()).values()
            )
        )

        response_dict = nan_to_none(self.dbi.vtile_id_to_qrcode_lut(reverse=True))
        self.assertEqual(
            response_dict, PROCESSED_RESPONSES['item/vtile_qrcode_reversed']
        )

    def test_vtile_id_to_qrcode_latest_vtile_only_lut(self):
        """
        Depends on LUT from tile_id_to_qrcode_lut.

        In the case of multiple key/value pairs indicating a repaired vTile,
        vtile_id_to_qrcode_latest_vtile_only_lut() should only leave
        """
        response_dict = nan_to_none(
            self.dbi.vtile_id_to_qrcode_latest_vtile_only_lut()
        )
        # Must only have one row per QR code.
        self.assertEqual(
            max(collections.Counter(response_dict.values()).values()),
            1,
        )

        self.assertTrue(response_dict[10000], '23062903000169001')

        response_dict = self.dbi.vtile_id_to_qrcode_latest_vtile_only_lut(reverse=True)
        self.assertTrue(response_dict['23062903000169001'], 10000)

    def test_get_relevant_qrcodes(self):
        """
        Cross-check get_relevant_qrcodes().
        """
        response_list = self.dbi.get_relevant_qrcodes()

        vpcb_qrcodes = {
            f'{r["qrcode"]}' for r in PROCESSED_RESPONSES['item/vpcb']
        }
        vtile_qrcodes = set(PROCESSED_RESPONSES['item/vtile_qrcode'].values())

        self.assertEqual(
            set(response_list), vpcb_qrcodes.difference(vtile_qrcodes)
        )

    def test_bad_fields(self):
        """
        Verify field checking in user-supplied table dictionaries for POST
        operations.

        Should also check for primary keys, and for log generation using
        assertLogs:
        https://docs.python.org/3/library/unittest.html
            #unittest.TestCase.assertLogs
        """
        # suppress terminal logging.error messages that _bad_fields may
        # generate
        logging.getLogger().disabled = True

        sipm_table = {
            'wafer_id':500,
            'column':10,
            'row':12,
            'tile_type': 'VETO',
        }

        # incorrect table type
        with self.assertRaises(TypeError):
            self.dbi._bad_fields(None, 'sipm', lambda f: f.endswith('_pid'))
        with self.assertRaises(TypeError):
            self.dbi._bad_fields([], 'sipm', lambda f: f.endswith('_pid'))
        with self.assertRaises(TypeError):
            self.dbi._bad_fields('', 'sipm', lambda f: f.endswith('_pid'))

        sipm_table = {
            'wafer_id':500,
            'column':10,
            'row':12,
            'tile_type': 'VETO',
        }
        self.assertFalse(
            self.dbi._bad_fields(
                sipm_table, 'sipm', lambda f: f.endswith('_pid')
            )
        )
        sipm_table = {
            'wafer_id':500,
            'pillar':10,
            'row':12,
            'tile_type': 'VETO',
        }
        self.assertTrue(
            self.dbi._bad_fields(
                sipm_table, 'sipm', lambda f: f.endswith('_pid')
            )
        )
        sipm_table = {
            'wafer_id':500,
            'column':10,
            'row':12,
            'tile_type': 'VETO',
            'something_else': 100,
        }
        self.assertTrue(
            self.dbi._bad_fields(
                sipm_table, 'sipm', lambda f: f.endswith('_pid')
            )
        )

###############################################################################
if __name__ == '__main__':
    unittest.main()
