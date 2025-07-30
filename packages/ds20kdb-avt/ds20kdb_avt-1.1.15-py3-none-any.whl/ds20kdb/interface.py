"""
Data structures to provide low-level interaction with the pre-production
database within Python.

E.g.

macbook:pf_db avt$ python3
Python 3.10.6 (main, Aug  3 2022, 05:37:08) [Clang 13.0.0 (clang-1300.0.29...
Type "help", "copyright", "credits" or "license" for more information.
>>> from ds20kdb import interface
>>> db = interface.Database()
>>> help(db.get)
>>> response = db.get('wafer')
>>> help(response)
>>> response.data
     wafer_pid  manufacturer         lot  ...  spad_size dose   description
0            1             2     9262109  ...         30    3  back... run B
1            2             2     9262109  ...         30    3  back... run A
2            3             2     9262109  ...         30    3  back... run C
3            4             2     9262109  ...         30    3  back... run A
4            5             2     9262109  ...         30    3  back... run B
..         ...           ...         ...  ...        ...  ...  ...
206        207             2     9306869  ...         30    3  ds-run=7
207        208             2     9306869  ...         30    3  ds-run=7
208        209             2     9306869  ...         30    3  ds-run=7
209        210             2     9306869  ...         30    3  ds-run=7
210        211             2     9306869  ...         30    3  ds-run=7

[211 rows x 8 columns]

>>> db.get('wafer', lot=9262109, wafer_number=12).data
   wafer_pid  manufacturer         lot  ...  spad_size dose    description
0          6             2     9262109  ...         30    3  back... run A

[1 rows x 8 columns]
"""

import collections
import contextlib
import csv
import datetime
import functools
import http.client as http_client
import io
import itertools
import json
import logging
import math
import platform
import urllib.parse

try:
    from importlib import metadata
except (ImportError, ModuleNotFoundError):
    try:
        import importlib_metadata as metadata
    except (ImportError, ModuleNotFoundError):
        py_version = platform.python_version()
        if py_version < '3.8':
            logging.warning(
                'Cannot import importlib, version information will NOT be available.'
            )
            logging.warning(
                'Unsupported Python version (%s), upgrade to Python 3.8 or newer.',
                py_version,
            )
        else:
            logging.error('Cannot import importlib')

import numpy as np
import requests
import pandas as pd
import polars as pl

from ds20kdb import constants
from ds20kdb import auth

# read the package version number as originally specified in setup.py
try:
    __version__ = metadata.version('ds20kdb-avt')
except NameError:
    # end-user is probably using a Python version < 3.8
    __version__ = 'unknown'


##############################################################################
# utilities
##############################################################################


def dict_from_qrcode(qr_code_numerals):
    """
    --------------------------------------------------------------------------
    args
        qr_code_numerals : string or int
            e.g. '22061703000032001', where (from left to right):
                220617 - YYMMDD
                0      - PRODUCTION FLAG
                30     - VERSION
                00032  - SERIAL NUMBER
                001    - PART NUMBER
    --------------------------------------------------------------------------
    returns : dict or None
        {
            'timestamp': datetime.datetime, 'production': bool,
            'version': int, 'serial_number': int, 'part_number': int
        }
        e.g.
        dict_from_qrcode('22061703000032001')
        {
            'timestamp': datetime.datetime(2022, 6, 17, 0, 0),
            'production': False,
            'version_string': '3.0',
            'version_major': 3,
            'version_minor': 0,
            'serial_number': 32,
            'part_number': 1
        }

        dict if the received string looks plausible, None otherwise.
    --------------------------------------------------------------------------
    """
    if not qr_code_valid(qr_code_numerals):
        return None

    qr_code_numerals = str(qr_code_numerals)

    yymmdd = qr_code_numerals[:6]
    prod_flag = qr_code_numerals[6]
    version = qr_code_numerals[7:9]
    serial_number = qr_code_numerals[9:14]
    part_number = qr_code_numerals[14:17]

    return {
        'timestamp': datetime.datetime.strptime(yymmdd, '%y%m%d'),
        'production': prod_flag == '1',
        'version_string': f'{version[0]}.{version[1]}',
        'version_major': int(version) // 10,
        'version_minor': int(version) % 10,
        'serial_number': int(serial_number),
        'part_number': int(part_number),
    }


def qr_code_valid(qr_code_numerals):
    """
    Basic validation of string decoded from QR code.

    --------------------------------------------------------------------------
    args
        qr_code_numerals : string or int
            e.g. '22061703000032001', where (from left to right):
                220617 - YYMMDD
                0      - PRODUCTION FLAG
                30     - VERSION
                00032  - SERIAL NUMBER
                001    - PART NUMBER
    --------------------------------------------------------------------------
    returns : bool
        True if the received string looks plausible, False otherwise.
    --------------------------------------------------------------------------
    """
    # numerals only
    try:
        int(qr_code_numerals)
    except (OverflowError, TypeError, ValueError):
        return False

    qr_code_numerals = str(qr_code_numerals)

    # always 17 numerals
    if len(qr_code_numerals) != 17:
        return False

    prod_flag = qr_code_numerals[6]
    if prod_flag not in {'0', '1'}:
        return False

    yymmdd = qr_code_numerals[:6]
    try:
        datetime.datetime.strptime(yymmdd, '%y%m%d')
    except ValueError:
        return False

    # version, serial_number and part_number can be pretty much anything
    # so no further checks at this point

    return True


def removesuffix(table_name, suffix):
    """
    Remove suffix from string.

    Python versions prior to 3.9 do not have <string>.removesuffix().

    --------------------------------------------------------------------------
    args
        string : string
            e.g. 'vpcb_asic_test'
        suffix : string
            e.g. '_test'
    --------------------------------------------------------------------------
    returns : string
        e.g.'vpcb_asic'
    --------------------------------------------------------------------------
    """
    if suffix and table_name.endswith(suffix):
        table_name = table_name[:-len(suffix)]

    return table_name


def sanitise(value):
    """
    Obtain an int value for the value provided if possible. Intended to
    sanitise function arguments that are expected to be int.

    Pass through int values unchanged. Floats are changed to int if they are
    equivalent (e.g. 57.0 == 57), None is returned if not. Strings are
    converted to int if their float representation is equivalent.

    E.g.

    41                    -> 41
    41.0                  -> 41
    4.1e1                 -> 41
    '41'                  -> 41
    '41.0'                -> 41
    '41.0000000000000001' -> 41 (mantissa small enough to be considered 0)
    41.0000000000000001   -> 41 (mantissa small enough to be considered 0)
    4.1e0                 -> None
    4.1                   -> None
    '4.1'                 -> None
    41.00000000000001     -> None

    --------------------------------------------------------------------------
    args
        value : numeric (float, int or string)
    --------------------------------------------------------------------------
    returns : int or None
        True if the received string looks plausible, False otherwise.
    --------------------------------------------------------------------------
    """
    if isinstance(value, int):
        return value

    try:
        value = float(value)
    except TypeError:
        return None

    if value.is_integer():
        retval = int(value)
    else:
        retval = None
        logging.debug('integer expected, received float %s', value)

    return retval


def sanitise_multiple(*values):
    """
    Sanitise multiple numeric values. Return None if any one fails to convert.

    --------------------------------------------------------------------------
    args
        *values : supplied parameters
    --------------------------------------------------------------------------
    returns
        sanval: list
    --------------------------------------------------------------------------
    """
    sanval = [sanitise(value) for value in values]

    if any(value is None for value in sanval):
        return None

    return sanval


def sort_qrcodes_by_serial_number(qrcodes):
    """
    Sort an iterable containing QR codes represented as strings, returning
    a list of sorted unique QR codes.

    --------------------------------------------------------------------------
    args
        qrcodes : iterable of string
            e.g. ['23090713000541001', '23090713000530001', ...]
    --------------------------------------------------------------------------
    returns : list of string
        ['23090713000530001', '23090713000541001', ...]
    --------------------------------------------------------------------------
    """
    return sorted(set(qrcodes), key=lambda q: (int(q[-3:]), int(q[-8:-3])))


def wafer_map_valid_locations(legacy=False):
    """
    Generate all valid SiPM positions on the wafer. ASSUME that this
    layout is generic across all wafers.

    Wafer map geometry:

    columns (x) : 0 - 19
    rows    (y) : 0 - 25

      0,  0 : bottom left
     19, 25 : top right

    Valid SiPM positions within bounds:

    columns (x) : 2 - 17
    rows    (y) : 2 - 23

    HOWEVER...

    SiPMs in columns 2 and 17 cannot be probed at LNGS, therefore these four
    devices should be excluded when picking production wafers:

    column row
    02     12
    02     13
    17     12
    17     13

    In the database, the 'sipm' table itself (for a given wafer_id) contains
    SiPM PIDs for all 268 positions, but there will be no corresponding entry
    for the above four devices in the 'sipm_test' table.

    --------------------------------------------------------------------------
    args
        legacy : bool
            True to consider the original 268 SiPM positions instead of the
            default 264.
    --------------------------------------------------------------------------
    yields : sequence of tuples (int, int)
        (wafer_column, wafer_row)
    --------------------------------------------------------------------------
    """
    # bottom half of wafer
    row_columns = {
        2: range(7, 12 + 1),
        3: range(6, 13 + 1),
        4: range(5, 14 + 1),
        5: range(4, 15 + 1),
        6: range(4, 15 + 1),
        7: range(3, 16 + 1),
        8: range(3, 16 + 1),
        9: range(3, 16 + 1),
        10: range(3, 16 + 1),
        11: range(3, 16 + 1),
        12: range(2, 17 + 1) if legacy else range(3, 16 + 1),
    }

    # column pattern is symmetrical: add top half of wafer
    for row, colrange in row_columns.copy().items():
        row_columns[25 - row] = colrange

    # yield all valid wafer map locations
    for row, colrange in row_columns.items():
        for column in colrange:
            yield column, row


##############################################################################
# Result handling - structured to provide meaningful documentation to the
# caller of member functions of class Database.
##############################################################################


class Result:
    """
    A simple data container to hold results from database operations.
    """

    __slots__ = {
        'network_timeout': (
            'A boolean value indicating whether a network timeout occurred\n'
            'when communicating with the database.'
        ),
        'data': (
            'Data created from the database query response, supplied in an\n'
            'appropriate datatype.'
        ),
    }

    def __init__(self):
        self.network_timeout = False
        self.data = None

    def __str__(self):
        return '\n'.join(
            [
                f'network_timeout={self.network_timeout}',
                f'data={self.data}'
            ]
        )


##############################################################################
# database handling
##############################################################################


class Database(auth.Authentication):
    """
    Low-level database interaction.
    """

    base_url = constants.BASE_URL

    def __init__(self, connection=None, max_io_workers=1):
        """
        requests configuration

        Database login credentials are obtained from a local configuration
        file. A check of credentials is made once at time of initialisation.
        """
        if connection is None:
            _credentials = self.read_credentials()
            if _credentials is None:
                logging.error('could not read local authentication credentials')
                logging.error('see documentation for method: create_credentials_file()')
                assert _credentials is not None, 'no valid credentials, exiting'

            # In the case where a user's credentials have expired, without
            # this check, all they will see are silently failing queries. This
            # will show 'ERROR:root:authentication failed' in the terminal
            # at initialisation, providing some guidance.
            self.credentials_accepted_by_endpoint(_credentials)
        else:
            uuser, upass, self.base_url = connection
            _credentials = {'username': uuser, 'password': upass}
            self.credentials_accepted_by_endpoint(_credentials)

        self.session = requests.Session()
        self.session.auth = (_credentials['username'], _credentials['password'])

        # set the requests pool size to something appropriate for the computer
        # this script is running on
        #
        # Random remote disconnections were experienced with the pre-production
        # database when writing with more than one thread, even if data writes
        # were independent. The initial value of _max_io_workers was set to
        # min(32, os.cpu_count() * 4), and decremented to 2. Even at 2 problems
        # were seen. Threaded reads worked perfectly.
        #
        # Can show the current pool size with:
        # self.session.get_adapter(self.base_url).poolmanager.connection_pool_kw['maxsize']
        self._max_io_workers = max_io_workers
        self.session.mount(
            'https://',
            requests.adapters.HTTPAdapter(
                pool_connections=1, pool_maxsize=self._max_io_workers
            ),
        )

    ##########################################################################
    # requests GET
    ##########################################################################

    ##########################################################################
    # generic

    def describe_url(self, table_name=''):
        """
        Generate the URL for the database DESCRIBE operation.
        """
        return urllib.parse.urljoin(
            self.base_url,
            '/'.join(filter(bool, ['db/describe', table_name]))
        )

    def describe(self, table_name=''):
        """
        Describe database. With no argument, this returns a list containing
        the table names of the database. With a table name specified this
        returns a list of the fields of the specified table.

        Usage:

            response = describe()
            response = describe('vtile')

            Read details of response with:

            response.list
            response.network_timeout

            Use help(response) for more information.

        ----------------------------------------------------------------------
        args
            table_name : string
        ----------------------------------------------------------------------
        returns : class Result
        ----------------------------------------------------------------------
        """
        result = Result()

        try:
            response = self.session.get(self.describe_url(table_name))
        except requests.ConnectionError:
            result.network_timeout = True
            return result

        if response.status_code != requests.codes.ok:
            return result

        tables = [
            table.strip()
            for table in response.text.replace('"', '').strip('[]').split(',')
        ]
        result.data = tables

        return result

    def describe_raw(self, table_name=''):
        """
        Describe database, returns raw text only, or None.

        See describe() for more information.
        """
        try:
            response = self.session.get(self.describe_url(table_name))
        except requests.ConnectionError:
            return None

        if response.status_code != requests.codes.ok:
            return None

        return response.text

    def _row_limit_prefix(self, table_name, query_max_results):
        """
        Generate partial URL query string for limiting the number of returned
        rows. Perform some rudimentary validity checking.

        Initial tests indicate there's no need to compensate for SQL reserved
        words for the column name here.

        ----------------------------------------------------------------------
        args
            table_name : string
            query_max_results : iterable (max_rows, sort_by_column, direction)
                where:
                    max_rows : int, value >= 1
                        maximum number of rows to be returned in the response
                    sort_by_column : string, table field/column name
                    direction : string, 'a' or 'd'
                        e.g. (4, 'operator', 'a')
        ----------------------------------------------------------------------
        returns
            prefix : string
                e.g. '?l=4&ob=operator=a'
        ----------------------------------------------------------------------
        """
        prefix = ''

        try:
            max_rows, sort_by_column, direction = query_max_results
        except (ValueError, TypeError):
            logging.error('_row_limit_prefix: query_max_results malformed')
        else:
            # Do not generate a filtered query that will return nothing.
            try:
                num_rows = int(max_rows)
            except (TypeError, ValueError):
                logging.error('_row_limit_prefix: bad number of rows')
                return prefix

            if num_rows < 1:
                logging.error(
                    (
                        '_row_limit_prefix: bad number of rows (%s), '
                        'value should be > 0'
                    ),
                    num_rows
                )
                return prefix

            # Sort order: (a)scending, (d)ecending
            try:
                direction = direction.lower()
            except AttributeError:
                logging.error(
                    '_row_limit_prefix: unrecognised direction, '
                    'use "a" (ascending) or "d" (descending).',
                )
                return prefix

            if direction not in {'a', 'd'}:
                logging.error(
                    '_row_limit_prefix: unrecognised direction, '
                    'use "a" (ascending) or "d" (descending).',
                )
                return prefix

            # At the cost of an additional database lookup, check that the
            # field exists in the table.
            response = self.describe(table_name)
            if response.network_timeout or sort_by_column not in response.data:
                logging.error(
                    '_row_limit_prefix: unrecognised field "%s" for table "%s"',
                    sort_by_column,
                    table_name,
                )
                return prefix

            prefix = f'l={max_rows}&ob={sort_by_column}={direction}'

        return prefix

    @staticmethod
    def _join_subexpression(args):
        """
        Create database inner join subexpression. No error checking.

        ----------------------------------------------------------------------
        args
            args : tuple (int, (string, string, string))
                e.g. (0, ('wafer', 'sipm.wafer_id', 'wafer_pid'))
        ----------------------------------------------------------------------
        returns : string
            e.g. 'ij[0]=wafer&on[0]=sipm.wafer_id=wafer_pid'
        ----------------------------------------------------------------------
        """
        index, ref = args
        return f'ij[{index}]={ref[0]}&on[{index}]={ref[1]}={ref[2]}'

    def get_url(self, table_name, joins=None, **columns):
        """
        Generate the URL for the database GET operation.

        ----------------------------------------------------------------------
        args
            table_name : string
            joins : dict
            columns : dict
        ----------------------------------------------------------------------
        returns : string
        ----------------------------------------------------------------------
        """
        url_suffix = f'item/{table_name}'
        query_max_results = columns.pop('query_max_results', None)

        # modify the URL so the database returns a subset of the table
        try:
            select_subset = '&'.join(
                f'w="{k}"=\'{v}\'' for k, v in columns.items()
            )
        except AttributeError:
            return None

        # limit number of rows returned if required
        if query_max_results is not None:
            prefix = self._row_limit_prefix(table_name, query_max_results)
            if prefix:
                select_subset = '&'.join(filter(bool, [prefix, select_subset]))
            else:
                # Attempt to limit number of rows failed, so do NOT
                # forward the unlimited GET operation to the database.
                return None

        # implement inner join
        if joins is None:
            prefix = ''
        else:
            prefix = '&'.join(map(self._join_subexpression, enumerate(joins)))
        select_subset = '&'.join(filter(bool, [prefix, select_subset]))

        # build query string
        url_suffix = '?'.join(filter(bool, [url_suffix, select_subset]))

        return urllib.parse.urljoin(self.base_url, url_suffix)

    def get(self, table_name, joins=None, **columns):
        """
        Generic GET operation.

        When supplied with just the table name, this function will return all
        rows of the table. If the 'columns' argument is supplied, a subset of
        the table will be returned, unless the dictionary is empty in which
        case this will yield the entire table. The joins argument allows the
        use of a rudimentary database inner join lookup.

        If the request for a subset of the table is obviously broken
        ('columns' is malformed, for example) it's better that we fail the
        whole request, rather than return the entire contents of the table.

        Note that when fully populated, the 'sipm' and 'sipm_test' tables
        could each contain ~60000 rows which may result in a >10MB response
        from the remote database. The query_max_results key in the columns
        argument may be used to specify the number of responses received.

        Usage:

            (1) response = get('wafer')
            (2) response = get('wafer', lot=9262109)
            (3) response = get('wafer', lot=9262109, wafer_number=12)

            (4) columns = {'lot': 9262109, 'wafer_number': 12}
                response = get('wafer', **columns)

            (5) response = get('wafer', query_max_results=(4, 'operator', 'a'))
                (special case to limit the query response to the given number
                 of rows. This request isn't processed by this interface, it's
                 simply passed on to the database to handle.)

            (6) joins = [
                    ('wafer', 'sipm.wafer_id', 'wafer_pid'),
                    ('sipm', 'sipm_id', 'sipm.sipm_pid'),
                ]
                response = get('wafer', joins=joins, wafer_pid=1261)
                (database inner join)

            (7) joins = [
                    ('wafer', 'sipm.wafer_id', 'wafer_pid'),
                    ('sipm', 'sipm_id', 'sipm.sipm_pid'),
                ]
                response = get(
                    'sipm_test', joins=joins, wafer_pid=1261,
                    query_max_results=(4, 'operator', 'a')
                )
                (can combine 5 and 6)

            Read details of response with:

            response.data
            response.network_timeout

            Use help(response) for more information.

        If the user has made a request to limit the number of rows they
        receive in the response, extract the key/value pair specifying this
        from the columns dict, so it doesn't get prepended with the table
        name as part of the existing column-based filtering. A long and
        unwieldy key (query_max_results) has been chosen to reduce the
        probability of intersection with future additions to the set of all
        database field names. Developers can check this with a call to
        get_unique_field_names().

        ----------------------------------------------------------------------
        args
            table_name : string
            joins : iterable
                [(table, field, field), ...]
                e.g.
                    [
                        ('wafer', 'sipm.wafer_id', 'wafer_pid'),
                        ('sipm', 'sipm_id', 'sipm.sipm_pid'),
                    ]
            columns : <class 'dict'>
                e.g. {'lot': 9262109, 'wafer_number': 12}

                special case:

                columns may contain key 'query_max_results'. If so, its value
                should be an iterable (max_rows, sort_by_column, direction)
                where:
                    max_rows : int, value >= 1
                        maximum number of rows to be returned in the response
                    sort_by_column : string, table field/column name
                    direction : string, 'a' or 'd'
                        e.g. (4, 'operator', 'a')
        ----------------------------------------------------------------------
        returns : class Result
        ----------------------------------------------------------------------
        """
        result = Result()

        full_url = self.get_url(table_name, joins, **columns)
        if full_url is None:
            return result

        try:
            response = self.session.get(full_url)
        except (requests.ConnectionError, requests.exceptions.ChunkedEncodingError):
            result.network_timeout = True
            return result

        if response.status_code != requests.codes.ok:
            return result

        result.data = pd.read_csv(
            io.StringIO(response.text), sep=',', encoding='utf-8',
            low_memory=False,
        )

        return result

    def get_polars(self, table_name, joins=None, **columns):
        """
        Generic get operation, return Polars DataFrame, or None.

        See get() for more information.
        """
        result = Result()

        full_url = self.get_url(table_name, joins, **columns)
        if full_url is None:
            return result

        try:
            response = self.session.get(full_url)
        except (requests.ConnectionError, requests.exceptions.ChunkedEncodingError):
            result.network_timeout = True
            return result

        if response.status_code != requests.codes.ok:
            return result

        with contextlib.suppress(pl.exceptions.NoDataError):
            result.data = pl.read_csv(io.StringIO(response.text))

        return result

    def get_raw(self, table_name, joins=None, **columns):
        """
        Generic GET operation, returns raw text only, or None.

        See get() for more information.
        """
        full_url = self.get_url(table_name, joins, **columns)
        if full_url is None:
            return None

        try:
            response = self.session.get(full_url)
        except (requests.ConnectionError, requests.exceptions.ChunkedEncodingError):
            return None

        if response.status_code != requests.codes.ok:
            return None

        return response.text

    ##########################################################################
    # query database structure

    def get_db_structure(self):
        """
        Get database table/fields structure.

        Dictionary ordering by insertion order is only guaranteed for
        Python 3.7 onwards.

        If you only need the top level tables, just call describe() with no
        arguments.

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns : dict or None (no response from db, no network connection)
            e.g. {<table_name>: <list of fields>, ...}
        ----------------------------------------------------------------------
        """
        try:
            return {
                table: self.describe(table).data
                for table in sorted(self.describe().data)
            }
        except TypeError:
            return None

    def get_unique_field_names(self):
        """
        Get all unique database field names.

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns : list or None (no response from db, no network connection)
            e.g. [
                'a', 'acs_pid', 'afterpulsing', 'amplitude_1pe', ...
                'wafer_number', 'wafer_pid', 'wafer_status_pid'
            ]
        ----------------------------------------------------------------------
        """
        try:
            fields = itertools.chain.from_iterable(
                self.get_db_structure().values()
            )
        except AttributeError:
            return None

        return sorted(set(fields))

    def get_table_names_for_field(self, field):
        """
        Get names of all tables that contain the given field.

        ----------------------------------------------------------------------
        args
            field : string
                e.g. 'qrcode'
        ----------------------------------------------------------------------
        returns : list or None (no response from db, no network connection)
            e.g. [
                'a', 'acs_pid', 'afterpulsing', 'amplitude_1pe', ...
                'wafer_number', 'wafer_pid', 'wafer_status_pid'
            ]
        ----------------------------------------------------------------------
        """
        try:
            tables = {
                table
                for table, fields in self.get_db_structure().items()
                if field in fields
            }
        except AttributeError:
            return None

        return sorted(tables)

    ##########################################################################
    # interaction with views

    @staticmethod
    def _process_sql_view_response(response, object_id, reverse):
        """
        SQL view database response to dict lookup table.

        ----------------------------------------------------------------------
        args
            response : <class 'interface.Result'>
            object_id : string
            reverse : boolean
        ----------------------------------------------------------------------
        returns : dict {int: string, ...}, {string: [int, ...], ...} or None
            e.g.
                {
                    4: '22061703000024001',
                    ...
                    191: '23090713000415001',
                }
                or
                {
                    ...
                    '24020513001920001': [768],
                    '24020513001922001': [769, 1083],
                    '24020513001923001': [770, 1085],
                    '24020513001925001': [771, 1120],
                    '24020513001948001': [772],
                    ...
                }
        ----------------------------------------------------------------------
        """
        if response.network_timeout:
            return None

        if response.data is None:
            return None

        id_to_qr = dict(
            zip(
                response.data[object_id].astype(int),
                response.data['qrcode'].astype(str)
            )
        )
        if reverse:
            q2id_initial = collections.defaultdict(set)
            for vtid, qrc in id_to_qr.items():
                q2id_initial[qrc].add(vtid)
            outval = {
                qrc: sorted(vtid_list)
                for qrc, vtid_list in q2id_initial.items()
            }
        else:
            outval = id_to_qr

        return outval

    def vtile_id_to_qrcode_lut(self, reverse=False):
        """
        Seeing as this SQL view is intended for use as a cache for
        script-writers, it's better to return this data to the user as a
        dictionary. By doing this, the lookup is faster and easier for the
        end user.

        See issue:

        https://gitlab.in2p3.fr/darkside/productiondb_software/-/issues/4

        With vTile repairs active, this method may return more than row with
        the same QR code but different IDs.

        When the lookup table is reversed, the IDs in the list are sorted
        low-to-high.

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns : dict {int: string, ...}, {string: [int, ...], ...} or None
            e.g.
                {
                    4: '22061703000024001',
                    ...
                    191: '23090713000415001',
                }
                or
                {
                    ...
                    '24020513001920001': [768],
                    '24020513001922001': [769, 1083],
                    '24020513001923001': [770, 1085],
                    '24020513001925001': [771, 1120],
                    '24020513001948001': [772],
                    ...
                }
        ----------------------------------------------------------------------
        """
        return self._process_sql_view_response(
            self.get('vtile_qrcode'), 'vtile_id', reverse
        )

    def vpcb_asic_id_to_qrcode_lut(self, reverse=False):
        """
        Seeing as this SQL view is intended for use as a cache for
        script-writers, it's better to return this data to the user as a
        dictionary. By doing this, the lookup is faster and easier for the
        end user.

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns : dict {int: string, ...}, {string: [int, ...], ...} or None
            e.g.
                {
                    4: '22061703000024001',
                    ...
                    191: '23090713000415001',
                }
                or
                {
                    ...
                    '24020513001920001': [768],
                    '24020513001922001': [769, 1083],
                    '24020513001923001': [770, 1085],
                    '24020513001925001': [771, 1120],
                    '24020513001948001': [772],
                    ...
                }
        ----------------------------------------------------------------------
        """
        return self._process_sql_view_response(
            self.get('vpcb_asic_qrcode'), 'vpcb_asic_id', reverse
        )

    def vpcb_id_to_qrcode_lut(self, reverse=False):
        """
        Seeing as this SQL view is intended for use as a cache for
        script-writers, it's better to return this data to the user as a
        dictionary. By doing this, the lookup is faster and easier for the
        end user.

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns : dict {int: string, ...}, {string: [int, ...], ...} or None
            e.g.
                {
                    4: '22061703000024001',
                    ...
                    191: '23090713000415001',
                }
                or
                {
                    ...
                    '24020513001920001': [768],
                    '24020513001922001': [769, 1083],
                    '24020513001923001': [770, 1085],
                    '24020513001925001': [771, 1120],
                    '24020513001948001': [772],
                    ...
                }
        ----------------------------------------------------------------------
        """
        return self._process_sql_view_response(
            self.get('vpcb_qrcode'), 'vpcb_id', reverse
        )

    def vtile_id_to_qrcode_latest_vtile_only_lut(self, reverse=False):
        """
        Return a dict of qrcodes to their highest vTile IDs (should more than
        one vTile ID exist).

        The latest vTile is ASSUMED to be the one with the largest vtile_id.

        In this context, it's safe to reverse the mapping since we only have
        one ID per QR code.

        ----------------------------------------------------------------------
        args
            reverse : bool
                False : return ID to QR code mapping
                True  : return QR code to ID mapping
        ----------------------------------------------------------------------
        returns : dict {int: string, ...}, {string: int, ...}, or None
            e.g.
                {
                    4: '22061703000024001',
                    ...
                    191: '23090713000415001',
                }
                or
                {
                    '22061703000024001': 4,
                    ...
                    '23090713000415001': 191,
                }
        ----------------------------------------------------------------------
        """
        lut = self.vtile_id_to_qrcode_lut()
        qr_to_all_ids = collections.defaultdict(set)

        # qr_to_all_ids = {'23090713000415001': [191, 1045], ...}
        try:
            for pid, qrcode in lut.items():
                qr_to_all_ids[qrcode].add(pid)
        except AttributeError:
            # self.vtile_id_to_qrcode_lut() returned None
            return None

        # latest = {'23090713000415001': 1045, ...}
        latest_vtile_id_to_qrcode = {
            max(pids): qrcode
            for qrcode, pids in qr_to_all_ids.copy().items()
        }
        if reverse:
            return {
                qrcode: pid
                for pid, qrcode in latest_vtile_id_to_qrcode.items()
            }

        return latest_vtile_id_to_qrcode

    def vtile_qrcodes(self):
        """
        Return the set of unique vTile QR code strings.

        See issue:

        https://gitlab.in2p3.fr/darkside/productiondb_software/-/issues/4

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns : set or None
            e.g.
                {'22061703000024001', '23090713000415001', ...}
        ----------------------------------------------------------------------
        """
        response = self.get('vtile_qrcode')

        if response.network_timeout:
            return None

        if response.data is None:
            return None

        return set(response.data['qrcode'].astype(str))

    def get_vtile_qrcode_from_serial_number(self, serial_number):
        """
        Obtain a vTile PID and QR code string from a vTile's serial number.

        Note that this will only give responses for vtile, not vpcb or
        vpcb_asic.

        With vTile repairs active, vtile_id_to_qrcode_lut() may plausibly
        return more than row with the same QR code but different IDs. This
        does not matter in this context where the first row with a QR code
        matching the supplied serial number, will suffice.

        2024/08/26 : no script in examples_python/ uses this call.
        2024/08/26 : therefore, breaking API change since return type changed

        ----------------------------------------------------------------------
        args
            serial_number : int or string equivalent
                e.g. 42 or '42'
        ----------------------------------------------------------------------
        returns : string or None
            e.g. '23090713000515001'
        ----------------------------------------------------------------------
        """
        # ensure False/True do not become 0/1
        if isinstance(serial_number, bool):
            return None

        try:
            value = float(serial_number)
        except TypeError:
            return None

        if not value.is_integer():
            return None

        try:
            value = int(serial_number)
        except ValueError:
            pass
        else:
            if not 0 <= value <= 99999:
                return None

            qrcodes = self.vtile_qrcodes()
            try:
                return next(
                    filter(lambda q: q.endswith(f'{value:05}001'), qrcodes)
                )
            except TypeError:
                # self.vtile_qrcodes() returned None
                pass
            except StopIteration:
                # Serial number not found in the set of QR codes
                pass

        return None

    ##########################################################################
    # tailored enquiries

    def get_institute_id(self, text_ident):
        """
        Get the Institution ID for the given case-insensitive sub-string.

        Note that if the sub-string is common to more than one institute,
        such as '', ' ', 'the' or 'university' only one response will be
        returned.

        ----------------------------------------------------------------------
        args
            text_ident : string
                e.g. liverpool, ral
        ----------------------------------------------------------------------
        returns
            result : class Result
                result.data int
        ----------------------------------------------------------------------
        """
        result = Result()

        # get all institutes
        response = self.get('institute')

        try:
            mask = response.data.name.str.contains(
                text_ident, case=False, na=False, regex=False
            )
        except AttributeError:
            pass
        else:
            try:
                response.data = int(response.data[mask].head().id.values[-1])
            except (AttributeError, IndexError):
                pass
            else:
                result = response

        return result

    def get_institute_details(self, text_ident):
        """
        Get institute ID and text of full institute name from a sub-string
        that can be found in the full institute text.

        Note that if the sub-string is common to more than one institute,
        such as '', ' ', 'the' or 'university' only one response will be
        returned.

        >>> dbi.get_institute_details('liverpool').data
        (5, 'University of Liverpool')

        >>> dbi.get_institute_details('manch').data
        (8, 'The University of Manchester')

        >>> dbi.get_institute_details('vinewood').data
        None

        ----------------------------------------------------------------------
        args
            text_ident : string
                e.g. liverpool, ral
        ----------------------------------------------------------------------
        returns
            result : class Result
                result.data (int, string), e.g. (5, 'University of Liverpool')
        ----------------------------------------------------------------------
        """
        result = Result()

        response = self.get_institute_id(text_ident)
        if response.network_timeout:
            return result

        institute_id = response.data
        try:
            institute_text = self.get(
                'institute', id=institute_id
            ).data.name.iloc[-1]
        except AttributeError:
            return result

        result.data = (institute_id, institute_text)

        return result

    def get_sipm_good(self, sipm_pid):
        """
        Get the status of the SiPM test result. This result indicates the
        pass/fail status of the initial wafer probe test.

        It's possible for there to be more than one test result for a given
        sipm_pid. Taking the minimum of 'good' and 'bad' will return 'bad'
        ensuring that in any pair of results any bad result, will result in
        a bad response.

        ----------------------------------------------------------------------
        args
            sipm_pid : int
        ----------------------------------------------------------------------
        returns
            result : class Result
        ----------------------------------------------------------------------
        """
        result = Result()

        sipm_pid = sanitise(sipm_pid)
        if sipm_pid is None:
            return result

        response = self.get('sipm_test', sipm_id=sipm_pid)

        try:
            response.data = min(response.data.classification.values) == 'good'
        except (AttributeError, IndexError, TypeError, ValueError):
            pass
        else:
            result = response

        return result

    def get_sipm_pid(self, wafer_id, column, row):
        """
        Get the SiPM PID from the database.

        Work around a problem with the database for the sipm table, where
        using the column field results in a "Bad request" response. This
        means that we can't use the database query to obtain the definitive
        response. So instead request SiPMs that match the wafer_id and row,
        obtain the sipm_id and column, then process the response in this
        function to obtain the sipm_id.

        ----------------------------------------------------------------------
        args
            wafer_id : int
            column : int
            row : int
        ----------------------------------------------------------------------
        returns
            rdat : int or None
        ----------------------------------------------------------------------
        """
        sanitised = sanitise_multiple(wafer_id, column, row)
        if sanitised is None:
            return sanitised
        wafer_id, column, row = sanitised

        response = self.get('sipm', wafer_id=wafer_id, row=row)

        # response will contain a DataFrame something like:
        #
        #     sipm_pid  wafer_id  column  row  tile_id tile_type
        # 0         12         1      12    9      NaN      VETO
        # 1         34         1      10    9      NaN      VETO
        # ...
        # 12       251         1       6    9      NaN      VETO
        # 13       254         1      13    9      NaN      VETO

        # Filter by column, then isolate sipm_pid.

        rdat = response.data
        try:
            rdat = int(rdat.loc[rdat.column == column].sipm_pid.values[-1])
        except (AttributeError, IndexError):
            rdat = None

        return rdat

    def get_sipm_test_id(self, sipm_pid):
        """
        Get the SiPM test_id given the sipm_pid. This serves as a check that
        the row was written successfully.

        It's plausible that more than one record may exist in the database for
        the same id, if corrections were made by submitting subsequent
        tables. So the value from the last record returned from the GET
        operation will be returned from this function.

        Example command line query:

        curl -u <USERNAME>:<PASSWORD> "<BASE_URL>item/sipm_test?w=sipm_id=29&c=id"
        id
        29

        ----------------------------------------------------------------------
        args
            sipm_pid : int
        ----------------------------------------------------------------------
        returns
            result : class Result
        ----------------------------------------------------------------------
        """
        result = Result()

        sipm_pid = sanitise(sipm_pid)
        if sipm_pid is None:
            return result

        response = self.get('sipm_test', sipm_id=sipm_pid)

        try:
            response.data = int(response.data.id.values[-1])
        except (AttributeError, IndexError):
            pass
        else:
            result = response

        return result

    def get_vpcb_asic_pid(self, vpcb_pid):
        """
        Get the vPCB ASIC PID from the database, given the vPCB PID.

        ----------------------------------------------------------------------
        args
            vpcb_pid : int
        ----------------------------------------------------------------------
        returns
            result : class Result
        ----------------------------------------------------------------------
        """
        result = Result()

        vpcb_pid = sanitise(vpcb_pid)
        if vpcb_pid is None:
            return result

        response = self.get('vpcb_asic', vpcb_id=vpcb_pid)

        try:
            response.data = int(response.data.vpcb_asic_pid.values[-1])
        except (AttributeError, IndexError):
            pass
        else:
            result = response

        return result

    def get_vpcb_asic_pid_from_qrcode(self, qrcode):
        """
        Get vPCB ASIC PID given the QR-code.

        The call to get_vpcb_asic_pid() will get the most recent value, so in
        the testing scenario, where an ASIC has been replaced on a vpcb_asic,
        this method is sufficient.

        ----------------------------------------------------------------------
        args
            qrcode : string or int
                e.g. 22061703000024001
        ----------------------------------------------------------------------
        returns
            vpcb_asic_pid : class Result
        ----------------------------------------------------------------------
        """
        vpcb_asic_pid = Result()

        if not qr_code_valid(qrcode):
            return vpcb_asic_pid

        try:
            vpcb_pid = self.get_vpcb_pid(f'{qrcode}').data
        except AttributeError:
            pass
        else:
            with contextlib.suppress(AttributeError, IndexError):
                vpcb_asic_pid.data = self.get_vpcb_asic_pid(vpcb_pid).data

        return vpcb_asic_pid

    def get_vpcb_pid(self, qrcode):
        """
        Get the vPCB PID from the database, given the QR-code.

        ----------------------------------------------------------------------
        args
            qrcode : string or int
                e.g. 22061703000024001
        ----------------------------------------------------------------------
        returns
            result : class Result
        ----------------------------------------------------------------------
        """
        result = Result()

        if not qr_code_valid(qrcode):
            return result

        # this returns a dataframe or None
        response = self.get('vpcb', qrcode=f'{qrcode}')

        try:
            response.data = int(response.data.vpcb_pid.values[-1])
        except (AttributeError, IndexError):
            pass
        else:
            result = response

        return result

    def get_tile_pid_from_qrcode(self, qrcode):
        """
        Get the TPC Tile PID given the QR-code.

        ----------------------------------------------------------------------
        args
            qrcode : string or int
                e.g. 23060803000179003
        ----------------------------------------------------------------------
        returns
            result : class Result
        ----------------------------------------------------------------------
        """
        result = Result()

        if not qr_code_valid(qrcode):
            return result

        try:
            pcb_pid = self.get('pcb', qrcode=f'{qrcode}').data.pcb_pid.values[-1]
        except (AttributeError, IndexError):
            return None

        try:
            response = self.get('tile', pcb_id=pcb_pid)
        except AttributeError:
            return None

        try:
            response.data = int(response.data.tile_pid[-1])
        except (AttributeError, IndexError, KeyError):
            pass
        else:
            result = response

        return result

    def get_vtile_pid_from_qrcode(self, qrcode):
        """
        Get the most recent vTile PID given the QR-code.

        Once a vTile table has been written, this method can be used to
        obtain the vTile ID from the QR-code.

        ----------------------------------------------------------------------
        args
            qrcode : string or int
                e.g. 22061703000024001
        ----------------------------------------------------------------------
        returns
            result : class Result
        ----------------------------------------------------------------------
        """
        result = Result()

        if not qr_code_valid(qrcode):
            return result

        qrcode_to_id = self.vtile_id_to_qrcode_latest_vtile_only_lut(reverse=True)

        if qrcode_to_id is None:
            return result

        vtile_id = qrcode_to_id.get(f'{qrcode}')

        if vtile_id is None:
            return result

        result.network_timeout = False
        result.data = vtile_id

        return result

    def get_wafer_pid(self, lot, wafer_number):
        """
        Get the wafer PID from the database, given the lot and wafer numbers.

        ----------------------------------------------------------------------
        args
            lot : int
            wafer_number : int
        ----------------------------------------------------------------------
        returns
            result : class Result
        ----------------------------------------------------------------------
        """
        result = Result()

        sanitised = sanitise_multiple(lot, wafer_number)
        if sanitised is None:
            return result
        lot, wafer_number = sanitised

        # this returns a dataframe or None
        response = self.get(
            'wafer', lot=lot, wafer_number=wafer_number
        )

        try:
            response.data = int(response.data.wafer_pid.values[-1])
        except (AttributeError, IndexError):
            pass
        else:
            result = response

        return result

    def get_wafer_lot_number_from_wafer_pid(self, wafer_pid):
        """
        Get the wafer lot and number given the wafer PID.

        ----------------------------------------------------------------------
        args
            wafer_pid : int
        ----------------------------------------------------------------------
        returns
            result : class Result
                result.data (int, int), e.g. (9324019, 18)
        ----------------------------------------------------------------------
        """
        result = Result()
        columns = ['lot', 'wafer_number']

        with contextlib.suppress(AttributeError, IndexError):
            result.data = tuple(
                self.get(
                    'wafer', wafer_pid=wafer_pid
                ).data.iloc[-1][columns].values
            )

        return result

    ##########################################################################
    # tailored enquiries/processing

    def get_qrcode_from_vpcb_asic_pid(self, vpcb_asic_pid):
        """
        Get the QR-code for the given the vpcb_asic PID.

        In a repair scenario, we may plausibly have:

            * Replacement of SiPM(s) on a vTile
                which leads to
                    in table vtile: multiple rows with the same vpcb_asic_pid

                This does not affect this method.

            * Replacement of an ASIC on a vpcb_asic
                which leads to
                    in table vpcb_asic: multiple rows with different
                    vpcb_asic_pids all referencing the same vpcb (and
                    therefore, the same QR code)

                This is tolerable here, since the most recent row is selected
                from vpcb_asic, which is safer than choosing the highest
                vpcb_asic_pid since a replacement ASIC could plausibly have an
                ID from anywhere in the available range.

        ----------------------------------------------------------------------
        args
            vpcb_asic_pid : int
        ----------------------------------------------------------------------
        returns
            qrcode : str
                Always 17 digits: e.g. '22060103000010001'
        ----------------------------------------------------------------------
        """
        vpcb_asic_pid = sanitise(vpcb_asic_pid)
        if vpcb_asic_pid is None:
            return vpcb_asic_pid

        try:
            vpcb_id = self.get('vpcb_asic', vpcb_asic_pid=vpcb_asic_pid).data.vpcb_id.values[-1]
        except IndexError:
            return None

        try:
            qrcode = int(self.get('vpcb', vpcb_pid=vpcb_id).data.qrcode.values[-1])
        except IndexError:
            return None

        return f'{qrcode}'

    def get_qrcode_from_vtile_pid(self, vtile_pid):
        """
        Get the QR-code for the given the vTile PID.

        ----------------------------------------------------------------------
        args
            vtile_pid : int
        ----------------------------------------------------------------------
        returns
            qrcode : str or None
                Always 17 digits: e.g. '22060103000010001'
        ----------------------------------------------------------------------
        """
        vtile_pid = sanitise(vtile_pid)

        # avoid the database query if the argument will certainly result in a
        # failed lookup
        if not isinstance(vtile_pid, int):
            return None

        lut = self.vtile_id_to_qrcode_lut()

        try:
            return lut[vtile_pid]
        except (KeyError, TypeError):
            return None

    def get_relevant_qrcodes(self):
        """
        Intended to be used by submit_vtile.py to display only QR-codes that
        have not already been allocated to a vTile.

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns
            unallocated_qrcodes : list or None
                e.g. [
                    '22060103000008001',
                    '22060103000009001',
                    ...
                    '23110613001054001',
                    '23110613001054001',
                ]
        ----------------------------------------------------------------------
        """
        # get all qrcodes
        response = self.get('vpcb')
        if response.network_timeout or response.data is None:
            return None

        # It seems vpcb may contain some broken QR codes hence the need for the
        # validity check.
        all_qrcodes = {f'{q}' for q in response.data.qrcode if qr_code_valid(q)}

        # get QR codes allocated to vTiles
        qrcodes_allocated_to_vtile = self.vtile_qrcodes()

        # all QR codes unallocated to vTiles
        # first sort by Part No., then by Serial No.
        try:
            return sort_qrcodes_by_serial_number(
                all_qrcodes - qrcodes_allocated_to_vtile
            )
        except TypeError:
            # qrcodes_allocated_to_vtile is None
            return None

    def get_relevant_solder_ids(self, institute_id, strict=True):
        """
        Intended to be used by submit_vtile.py to display only the in-date
        solder syringes. This is wise, since vTile database entry is
        performed before die attach, so the user can benefit from the
        additional checks that submit_vtile.py provides. This means that any
        solder being used must be in date at time of database entry.

        The date the syringe was brought up to room temperature is now taken
        into consideration, since sites are no longer ordering the larger 25g
        syringes which some sites chose to decant into multiple smaller
        containers before moving them to cold storage.

        ----------------------------------------------------------------------
        args
            institute_id : int
            strict : bool
                Strict solder syringe checking is enabled by default. STFC
                have commented that they perform database entry some time
                after die-attach, so allow them to disable checking.
        ----------------------------------------------------------------------
        returns : list of int, or None (timeout or bad institute_id)
            E.g. [17, 18]
        ----------------------------------------------------------------------
        """
        institute_id = sanitise(institute_id)
        if institute_id is None:
            return institute_id

        # Get the whole table, the size should be fairly small even when the
        # db is fully populated.
        response = self.get('solder', institute_id=institute_id)
        if response.network_timeout:
            return None

        # list of dicts
        # [
        #     {
        #         'solder_pid': 33, 'manufacturer': 4,
        #         'solder_type': 'Indium Paste NC-SMQ80...',
        #         'production_date': '2023-12-14 00:00:00',
        #         'room_temperature_date': '2024-03-12 14:35:58',
        #         'expiry_date': '2024-06-14 00:00:00',
        #         'syringe_id': 19, 'lot': 'PS11134508',
        #         'mass': 10, 'institute_id': 5,
        #     }
        # }
        retval = response.data.to_dict('records')

        def ss_valid(sold, dt_now, strict_ssc):
            """
            Return whether solder syringe is in-date based on expiry date and
            duration at room temperature.
            """
            dt_exp = datetime.datetime.strptime(
                sold['expiry_date'], '%Y-%m-%d %H:%M:%S'
            )
            dt_rtd = datetime.datetime.strptime(
                sold['room_temperature_date'],
                '%Y-%m-%d %H:%M:%S'
            )
            dt_rtd_p30 = dt_rtd + datetime.timedelta(days=30)

            return dt_now <= dt_exp and dt_now <= dt_rtd_p30 if strict_ssc else True

        valid = functools.partial(
            ss_valid, dt_now=datetime.datetime.now(), strict_ssc=strict
        )

        # This list will be ordered as per the database response, with the
        # most recently added item last, hence may be non-sequential.
        return [sold['solder_pid'] for sold in retval if valid(sold)]

    def get_sipms_allocated(self, sipm_pids, unchanged=None):
        """
        Indicate if the given sipm_pid(s) have been allocated to vTile(s).

        There are two ways of approaching this operation, (1) obtain the
        whole vtile table with a single GET operation and perform the search
        locally (as done in this method) or (2) make 24 targeted GET
        operations - one for each SiPM column - letting the db perform the
        search operation.

        The latter should perform better when the database fully populated,
        but in pre-production this is an order of magnitude slower, e.g.

        return any(
            not self.get('vtile', **{c: sipm_pid}).data.empty
            for c in sipm_columns
        )

        Column names can also be obtained from the database if required:

        sipm_columns = (
            c for c in self.describe('vtile').data if c.startswith('sipm_')
        )

        WARNING: This method will become expensive to run once the database
        becomes more populated.

        ----------------------------------------------------------------------
        args
            sipm_pids : iterable (containing int(s))
            unchanged : set or None
        ----------------------------------------------------------------------
        returns : dict (or None if the caller supplied a non-iterable)
            {sipm_pid: True if allocated}
                E.g. {19: True, 33: True, 1000000: False}
        ----------------------------------------------------------------------
        """
        if unchanged is None:
            unchanged = set()

        vtile_table = self.get(constants.TABLE_VTILE).data

        sipm_columns = (f'sipm_{x}' for x in range(1, 24+1))
        all_sipms = set(itertools.chain(*vtile_table[sipm_columns].values))

        try:
            return {
                s: False if s in unchanged else s in all_sipms
                for s in sipm_pids
            }
        except TypeError:
            return None

    def get_table_row_and_modify(self, table_name, select, replacements=None, omit_pid=True):
        """
        Generic method that reads a row from a remote database table,
        replaces values of given fields, then returns the result as a dict
        (which may then be POSTed to the database later).

        Given that this function is generic in nature, it won't complain too
        loudly if more than one row was returned from the GET operation, it
        simply returns the last row. This behaviour is not particularly
        desirable now, but may be so at some stage in the future when the
        database may support multiple table rows with the same PID field
        value; database housekeeping may then consolidate them later into a
        single row. This behaviour may be problematic in the case where the
        caller's selection of rows is too broad.

        Fields (which map to DataFrame columns) that contain NaN/NaT values
        are removed.

        E.g. to add a new indium solder syringe to the database - given that
        many fields will be similar between syringes - it may be helpful to
        get an existing row and modify it. In this instance, adding a syringe
        from the same lot and the same institute, we can just change the
        local syringe PID to get a dict suitable for POSTing it to the
        database:

        get_table_row_and_modify(
            'solder', {'solder_pid': 1}, {'syringe_id': 12}
        )

        Which would return:

        {
            'manufacturer': 4,
            'solder_type': 'Indium Paste NC-SMQ80 Ind#1E 52In48Sn Type 4 ...',
            'production_date': '2022-06-02 00:00:00',
            'room_temperature_date': '2022-07-18 16:00:00',
            'expiry_date': '2022-12-02 00:00:00',
            'syringe_id': 12, 'lot': 'PS11120734', 'mass': 25
        }

        ----------------------------------------------------------------------
        args
            table_name : string
                The caller should ensure the table name is correct, since no
                check is made.
            select : dict
                sufficient {field: value, ...} pairs to obtain the desired row
                from the table. This will probably just contain the _pid field
                for the given table.
            replacements : dict
                Replacement values for fields {field: value, ...}. If this
                argument is not supplied it defaults to None, which is later
                transformed into an empty dict.
            omit_pid : bool
                The principal objective of this method is to return a dict
                that can be POSTed to the database. Since the database doesn't
                currently support POSTing tables with an existing primary key,
                there's little point returning a dict containing one; this
                behaviour may change in the future. Any field ending with _pid
                (and there should be only one such field) is a primary key and
                will be removed by default.
        ----------------------------------------------------------------------
        returns
            table : dict
        ----------------------------------------------------------------------
        """
        # Perform some sanity checks on the supplied table and field names.
        # Calls to describe() are cached, so the cost for these checks is
        # minimal.

        # check table name exists in the db
        db_table_names = self.describe().data
        if table_name not in db_table_names:
            logging.warning(
                'get_table_row_and_modify: unrecognised table "%s"', table_name
            )
            return {}

        # check field names contained in method arguments are valid
        db_field_names = self.describe(table_name).data
        if replacements is None:
            replacements = {}
        categories = {'select': select, 'replacements': replacements}
        select_fail = False

        for category, fields in categories.items():
            for field in fields:
                if field not in db_field_names:
                    logging.warning(
                        (
                            'get_table_row_and_modify: '
                            'table "%s", unrecognised field "%s" (%s)'
                        ),
                        table_name, field, category
                    )
                    select_fail = True

        if select_fail:
            return {}

        # checks complete: process enquiry

        # get the Pandas DataFrame for a subset of this table
        pdf_original = self.get(table_name, **select).data

        # drop all columns with Na{N/T} values
        pdf = pdf_original.dropna(axis=1)

        # convert to dict
        rows = pdf.to_dict('records')

        # if the result is empty, exit early
        if not rows:
            return {}

        num_rows = len(rows)
        if num_rows > 1:
            logging.warning(
                'get_table_row_and_modify: query returned %s rows (expected 1)', num_rows
            )
        table = rows[-1]

        for field, value in replacements.items():
            table[field] = value

        # remove PID field
        if omit_pid:
            table = {
                k: v for k, v in table.items()
                if not k.lower().endswith('_pid')
            }

        return table

    def get_vtile_info(self, qrcode):
        """
        Collate comprehensive information about a vTile given its QR-code.
        Amongst other information, the original wafer position of each SiPM is
        obtained.

        This is an EXPENSIVE method to call with many sequential database
        lookups. It may take a minute to complete.

        ----------------------------------------------------------------------
        args
            qrcode : int
        ----------------------------------------------------------------------
        returns : dict or None
            None is returned if any required datum could not be obtained.
            e.g.
                {
                    'qrcode': 23010603000083001,
                    'vpcb_pid': 58,
                    'vpcb_asic_pid': 75,
                    'vtile_pid': 63,
                    'sipm_1': {
                        'sipm_id': 691,
                        'lot': 9262109,
                        'wafer_number': 15,
                        'column': 4,
                        'row': 6
                    },
                    ...
                    'sipm_24': {
                        'sipm_id': 726,
                        'lot': 9262109,
                        'wafer_number': 15,
                        'column': 10,
                        'row': 4
                    },
                    'vpdu_id': nan,
                    'run_number': 2,
                    'production_date': '2023-01-12 13:00:00',
                    'solder_id': 13,
                    'institute_id': 5,
                    'institute_text': 'University of Liverpool',
                    'solder': {
                        'solder_pid': 13,
                        'manufacturer': 4,
                        'solder_type': 'Indium Paste NC-SMQ80 Ind#1E 52In48Sn...',
                        'production_date': '2022-11-10 00:00:00',
                        'room_temperature_date': '2022-12-12 15:00:00',
                        'expiry_date': '2023-05-10 00:00:00',
                        'syringe_id': 9,
                        'lot': 'PS11124740',
                        'mass': 25,
                        'institute_id': 5
                    },
                    'unique_wafers': {(9262109, 15), (9262109, 13)}
                }
        ----------------------------------------------------------------------
        """
        if not qr_code_valid(qrcode):
            return None

        summary = {'qrcode': qrcode}

        ##########################################################################
        response = self.get('vpcb', qrcode=f'{qrcode}')
        if response.network_timeout:
            return None

        try:
            vpcb_pid = int(response.data.vpcb_pid.values)
        except TypeError:
            return None

        summary['vpcb_pid'] = vpcb_pid

        ##########################################################################
        response = self.get('vpcb_asic', vpcb_id=vpcb_pid)
        if response.network_timeout:
            return None
        try:
            vpcb_asic_pid = int(response.data.vpcb_asic_pid.values)
        except TypeError:
            # some vpcbs never became vpcb_asic
            return None

        summary['vpcb_asic_pid'] = vpcb_asic_pid

        ##########################################################################
        response = self.get(constants.TABLE_VTILE, vpcb_asic_id=vpcb_asic_pid)
        if response.network_timeout:
            return None
        try:
            vtile_table = response.data.to_dict('records')[-1]
        except IndexError:
            # some early vPCB entries never became vTiles
            return None

        summary.update(vtile_table)
        del summary['vpcb_asic_id']

        ##########################################################################
        response = self.get('institute', id=vtile_table['institute_id'])
        if response.network_timeout:
            return None
        institute_text = response.data.name.values[-1]
        summary['institute_text'] = institute_text

        ##########################################################################
        response = self.get('solder', solder_pid=vtile_table['solder_id'])
        if response.network_timeout:
            return None
        solder = response.data.to_dict('records')[-1]
        summary['solder'] = solder

        ##########################################################################
        # compute original wafer locations for SiPMs
        #
        # It seems safest to assume that requests.Session is not thread-safe.
        # Let's do this sequentially for the moment, and implement proper use of
        # the connection pool later.
        sipms = {k: v for k, v in summary.items() if k.startswith('sipm_')}

        for sipm_name, sipm_id in sipms.items():
            location = self.get_wafer_location_from_sipm_pid(sipm_id)
            if location is None:
                continue

            summary[sipm_name] = {**{'sipm_id': sipm_id}, **location}

        ##########################################################################
        # get unique wafers
        summary['unique_wafers'] = {
            (v['lot'], v['wafer_number'])
            for k, v in summary.items()
            if k.startswith('sipm_')
        }

        return summary

    def get_vtile_pids_from_sipm_pids(self, sipm_pids):
        """
        Find out which vTile(s) SiPMs have been allocated to.

        Since a SiPM can only be attached to one vTile, the purpose of this
        method is to help track down problematic data entry.

        WARNING: This method will become expensive to run once the database
        becomes more populated.

        ----------------------------------------------------------------------
        args
            sipm_pids : iterable (containing int(s))
        ----------------------------------------------------------------------
        returns : dict (or None if the caller supplied a non-iterable)
            {sipm_pid: [vtile_pid, ...], ...}
                E.g. {19: [6, 12], 33: [12, 46]}
        ----------------------------------------------------------------------
        """
        def spid_to_vpids(vt_tab, colnames, sipm_pid):
            """sipm_pid -> [vtile_pid, vtile_pid, ...]"""
            return [
                int(x)
                for x in vt_tab.loc[
                    np.where(vt_tab[colnames].isin([sipm_pid]))[0]
                ].vtile_pid.values
            ]

        vtile_table = self.get(constants.TABLE_VTILE).data
        column_names = [f'sipm_{x}' for x in range(1, 24 + 1)]

        try:
            return {
                sipm_pid: spid_to_vpids(vtile_table, column_names, sipm_pid)
                for sipm_pid in sipm_pids
            }
        except TypeError:
            return None

    def get_wafer_location_from_sipm_pid(self, sipm_pid):
        """
        Identify a SiPM's original wafer location based on its PID.

        ----------------------------------------------------------------------
        args
            sipm_pid : int
        ----------------------------------------------------------------------
        returns : dict or None
            E.g. {'lot': 9262109, 'wafer_number': 13, 'column': 12, 'row': 13}
        ----------------------------------------------------------------------
        """
        response = self.get('sipm', sipm_pid=sipm_pid)
        if response.network_timeout or response.data is None:
            return None
        sipm = response.data.to_dict('records')[-1]

        response = self.get('wafer', wafer_pid=sipm['wafer_id'])
        if response.network_timeout or response.data is None:
            return None
        wafer = response.data.to_dict('records')[-1]

        return {
            'lot': wafer['lot'],
            'wafer_number': wafer['wafer_number'],
            'column': sipm['column'],
            'row': sipm['row'],
        }

    def get_vtile_qc(self, qrcode, grade=None):
        """
        Returns the QC assessment of a vTile given a QR code.

        If the argument 'grade' is passed, will return a bool indicating if
        the vTile belongs or not to that grade.

        If the argument grade is not passed:
        - if the vTile has not been cold tested will return 'unknown'.
        - if the vTile cold test attempted but failed, or any other further
        test has failed (e.g. after a vPDU integration), will return
        'scrapped' (given this was manually flagged in the vtile_location
        table).
        - if the vTile cold test has been successfully completed will return
        the Grade as either 'grade_a' or 'grade_b', or the status 'bad',
        according to the vtile_qc table.

        Note that main reason for having a QR code as the argument instead of
        a vTile ID, is that this helps guarantee that we receive the status
        pertaining to the current status of the vTile if it has been
        repaired.

        ----------------------------------------------------------------------
        args
            qrcode : string or int
                e.g. 22061703000024001
            grade : string
                Either 'a' or 'b'
        ----------------------------------------------------------------------
        return : bool or string
              e.g. grade_a
        ----------------------------------------------------------------------
        """

        def check_grade(tgrade):
            """
            From the outer scope's vtile_id, and the given grade 'a'/'b'
            returns True/False.
            """

            # check if QR code is not used in a vTile
            if vtile_id is None:
                return False

            # gets the latest QA/QC from vtile_qc for the given Grade
            limits = json.loads(self.get('vtile_qc', grade=tgrade).data.qc.iloc[-1])

            # True until False
            quality = True

            for variable in variables:
                # Check the limits for this variable
                if f'{variable}_min' not in limits or f'{variable}_max' not in limits:
                    # Limits are not present for this variable, so no need to
                    # check any further for the passport value
                    continue

                # Passport value for this specific variable
                v = df[(df['bias_voltage']==bias_voltage) & (df['vtile_id']==vtile_id)].tail(1)[variable]
                if v.empty:
                    # variable not present in the passport entry so could not
                    # have the asked grade
                    quality = False
                    break

                # Variable is present
                v = v.values[-1]

                # Compare with the limits
                if v < limits[f'{variable}_min'] or v > limits[f'{variable}_max'] or math.isnan(v):
                    # variable already out of the limits or NaN, so could
                    # not have the asked grade
                    quality = False
                    break

            return quality

        # --------------------------------------------------------------------

        # QA/QC are evaluated for 69V
        bias_voltage = 69

        # Full list of QA/QC variables
        variables = [
            'snr', 'amplitude_1pe', 'charge_1pe', 'dark_noise', 'cda',
            'cross_talk', 'rms', 'breakdown', 'apa',
        ]

        # vtile passport
        df = self.get('vtile_cold_test').data

        vtile_id = self.get_vtile_pid_from_qrcode(qrcode).data

        if grade is not None:
            # check for the given specific grade to return True/False
            return check_grade(grade)

        # check if QR code is not used in a vTile
        if vtile_id is None:
            return 'unknown'

        # check if scrapped
        state = self.get('vtile_location', vtile_id=vtile_id).data.state
        if not state.empty:
            if state.iloc[-1] == 'scrapped':
                return 'scrapped'

        # check if it has the passport
        if df[(df['bias_voltage']==bias_voltage) & (df['vtile_id']==vtile_id)].tail(1).empty:
            return 'unknown'

        if check_grade('a'):
            return 'grade_a'

        if check_grade('b'):
            # if not grade A could be grade B
            return 'grade_b'

        # if not grade A or B must be bad
        return 'bad'

    ##########################################################################
    # requests HEAD
    ##########################################################################

    def remote_file_exists(self, url):
        """
        Check if a remote file exists at the given URL. It's only necessary to
        fetch the headers.
        """
        result = False

        try:
            response = self.session.head(url, timeout=46)
        except (requests.ConnectionError, requests.exceptions.ConnectTimeout):
            return result

        if response.status_code != requests.codes.ok:
            return result

        return True

    ##########################################################################
    # requests POST
    ##########################################################################

    ##########################################################################
    # generic

    @staticmethod
    def _dict_to_csv_string(table):
        """
        Convert a dictionary into a CSV-formatted string that requests.post
        will accept as a file.

        Support function for _post_generic().

        ----------------------------------------------------------------------
        args
            table : dict
                e.g.
                    {
                        'manufacturer': 2,
                        'lot': 3,
                        'wafer_number': 6,
                        'spad_size': 30,
                        'dose': 3,
                        'production_date': '2022-09-06 15:30:14',
                        'description': 5,
                    }
        ----------------------------------------------------------------------
        returns : string
            e.g.
                (
                    'manufacturer,lot,wafer_number,spad_size,dose,'
                    'production_date,description\n'
                    '2,3,6,30,3,2022-09-06 15:30:14,5\n'
                )
        ----------------------------------------------------------------------
        """
        sio = io.StringIO()

        # match line terminator used by pandas.DataFrame.from_dict
        csvw = csv.writer(sio, lineterminator='\n')

        csvw.writerow(table.keys())
        csvw.writerow(table.values())

        return sio.getvalue()

    def _post_generic(self, table, url_suffix):
        """
        Generic internal member function to POST a table to the database.

        ----------------------------------------------------------------------
        args
            table : dict
                e.g.
                    {
                        'manufacturer': 2,
                        'lot': 3,
                        'wafer_number': 6,
                        'spad_size': 30,
                        'dose': 3,
                        'production_date': '2022-09-06 15:30:14',
                        'description': 5,
                    }
            url_suffix : string
        ----------------------------------------------------------------------
        returns : bool
        ----------------------------------------------------------------------
        exceptions : may raise TypeError
        ----------------------------------------------------------------------
        """
        if not isinstance(table, dict):
            raise TypeError('Expected argument <table> to be a dictionary.')

        full_url = urllib.parse.urljoin(self.base_url, f'{url_suffix}?d=,&f=csv')

        try:
            response = self.session.post(
                full_url,
                files={'file': ('table.csv', self._dict_to_csv_string(table))}
            )
        except http_client.RemoteDisconnected:
            status = False
            logging.error('remote disconnected')
        else:
            status = response.status_code == requests.codes.ok

        return status

    ##########################################################################
    # categorical

    def _bad_fields(self, table, table_name, comp_fn):
        """
        Try and help the POST operation caller by identifying any announcing
        any incorrect fields, rather than getting a 400 bad request and leaving
        the caller with a return value of False.

        It's highly likely the caller will get the order of the arguments
        wrong at some stage when calling a POST operation. Try and avoid
        support issues by providing helpful feedback when that happens.

        Attempting to write a table with an explicitly specified primary key
        is unsupported by the database, so announce this to the user.

        comp_fn is a lambda expression used to detect user-submitted primary
        keys, such that this method can be used for checking fields for items
        and measurements.

        Discovering a primary key should result in a True return value, but
        not keen to change behaviour at this point.

        ----------------------------------------------------------------------
        args
            table : dict
                e.g.
                    {
                        'manufacturer': 2,
                        'lot': 3,
                        'wafer_number': 6,
                        'spad_size': 30,
                        'dose': 3,
                        'production_date': '2022-09-06 15:30:14',
                        'description': 5,
                    }
            table_name : string
            comp_fn : lambda function
        ----------------------------------------------------------------------
        returns : bool
        ----------------------------------------------------------------------
        exceptions : may raise TypeError
        ----------------------------------------------------------------------
        """
        if not isinstance(table, dict):
            raise TypeError(
                'Expected argument <table> to be a dictionary. '
                'Check argument order in function call.'
            )

        try:
            response = self.describe(table_name)
        except TypeError:
            logging.error(
                'Argument order supplied to function may be incorrect.'
            )
            return True

        if response.network_timeout:
            logging.error('Network timeout')
            return True

        if response.data is None:
            logging.error(
                'db_field is empty for table %s', table_name
            )
            return True

        db_fields = response.data
        unrecognised_fields = set(table).difference(db_fields)

        for field in unrecognised_fields:
            logging.error(
                'table %s, unrecognised field: %s', table_name, field
            )

        # additional check for primary keys
        primary_keys = {user_field for user_field in table if comp_fn(user_field)}
        for primary_key in primary_keys:
            logging.error(
                'explicitly specified primary keys are unsupported: %s', primary_key
            )

        # check for (potentially) missing fields
        # This will generate false positive warnings for non-user-supplied
        # fields that are optional (not specified as non-NULL).
        for db_field in db_fields:
            if comp_fn(db_field):
                continue

            if db_field not in table:
                logging.warning('missing field: %s', db_field)

        return bool(unrecognised_fields)

    def post_item(self, table, table_name):
        """
        POST a table for a "physical" item to the database.

        ----------------------------------------------------------------------
        args
            table : dict
                e.g.
                    {
                        'manufacturer': 2,
                        'lot': 3,
                        'wafer_number': 6,
                        'spad_size': 30,
                        'dose': 3,
                        'production_date': '2022-09-06 15:30:14',
                        'description': 5,
                    }
            table_name : string
                e.g. 'wafer'
        ----------------------------------------------------------------------
        returns : bool
            Success of POST operation.
        ----------------------------------------------------------------------
        """
        # skip the POST operation if it will certainly fail
        if self._bad_fields(table, table_name, lambda f: f.endswith('_pid')):
            return False

        return self._post_generic(table, f'item/{table_name}')

    def post_measurement(self, table, table_name):
        """
        POST a table for a test result to the database.

        ----------------------------------------------------------------------
        args
            table : dict
                e.g.
                    {
                        'manufacturer': 2,
                        'lot': 3,
                        'wafer_number': 6,
                        'spad_size': 30,
                        'dose': 3,
                        'production_date': '2022-09-06 15:30:14',
                        'description': 5,
                    }
            table_name : string
        ----------------------------------------------------------------------
        returns : bool
            Success of POST operation.
        ----------------------------------------------------------------------
        """
        if not table_name.endswith('_test'):
            table_name += '_test'

        # skip the POST operation if it will certainly fail
        if self._bad_fields(table, table_name, lambda f: f == 'id'):
            return False

        return self._post_generic(
            table, f'measure/{removesuffix(table_name, "_test")}'
        )

    ##########################################################################
    # specific physical items
    #
    # These methods are simply wrappers for the generic post_item call.
    #
    # They are only defined to give an interactive user a chance to get the
    # database submission right by referring to the method documentation
    # using the Python interpreter's 'help()' command.
    #

    def post_pcb(self, table):
        """
        POST table: pcb
        """
        # return self.post_item(table, 'pcb')
        raise NotImplementedError

    def post_pdu(self, table):
        """
        POST table: pdu
        """
        # return self.post_item(table, 'pdu')
        raise NotImplementedError

    def post_manufacturer(self, table):
        """
        POST table: manufacturer

        The database consistently responds with "bad response" to this POST
        operation for some reason. The similar curl operation on the command
        line also fails. Tested 2022 09 09.
        """
        # return self.post_item(table, 'manufacturer')
        raise NotImplementedError

    def post_sipm(self, table):
        """
        POST table: sipm

        ----------------------------------------------------------------------
        args
            table : dict
                e.g.
                    {
                        # the wafer this device was picked from
                        'wafer_id': 2,
                        'sipm_grip_ring_id': 1,
                        'column, 12,
                        'row': 6,
                        'tile_type': 'VETO',
                        # the tile this SiPM is mounted on, if any
                        'tile_id: 12,
                    }
        ----------------------------------------------------------------------
        returns : bool
            Success of POST operation.
        ----------------------------------------------------------------------
        """
        return self.post_item(table, 'sipm')

    def post_solder(self, table):
        """
        POST table: solder

        Add solder paste syringe to the database.

        Example syringe label:

        INDIUM CORPORATION

        IPN: PASTEIN-83752-C001        ENGLISH
        FLUX: NC-SMQ80                 MADE IN THE USA
        COMP: 52IN 48SN                INDALLOY:1E
        MESH: -400+635                 LOT: PS11120734
        METAL: 83%                     QUAN (Gms): 25
                                       MFG: 02Jun2022
                                       USE BY: 02Dec2022
                                       STORE: -20°C to 5°C

        ----------------------------------------------------------------------
        args
            table : dict
                e.g.
                    {# Almost certainly Indium Corp.
                     'manufacturer': 4,
                     'solder_type': 'Indium Paste NC-SMQ80 Ind#1E 52In48Sn...',
                     # From the syringe label ("MFG").
                     'production_date': '2022-06-02 00:00:00',
                     # The date the syringe was taken from cold storage and
                     # brought up to room temperature.
                     'room_temperature_date': '2022-07-18 16:00:00',
                     # From the syringe label ("USE BY").
                     'expiry_date': '2022-12-02 00:00:00',
                     # The site's internal reference number for the syringe
                     'syringe_id': 7,
                     # From the syringe label ("LOT").
                     'lot': 'PS11120734',
                     # Mass of solder paste contained in the syringe (grams)
                     'mass': 25}
        ----------------------------------------------------------------------
        returns : bool
            Success of POST operation.
        ----------------------------------------------------------------------
        """
        return self.post_item(table, 'solder')

    def post_tile(self, table):
        """
        POST table: tile
        """
        # return self.post_item(table, 'tile')
        raise NotImplementedError

    def post_vasic(self, table):
        """
        POST table: vasic

        This is for a Veto ASIC.

        ----------------------------------------------------------------------
        args
            table : dict
                e.g.
                    {
                        'vasic_grip_ring_id: 1,
                        'vasic_wafer_id': 2,
                        'column': 6,
                        'row': 5,
                        'vpcb_asic_id': 5,
                    }
        ----------------------------------------------------------------------
        returns : bool
            Success of POST operation.
        ----------------------------------------------------------------------
        """
        return self.post_item(table, 'vasic')

    def post_vasic_grip_ring(self, table):
        """
        POST table: vasic_grip_ring

        ----------------------------------------------------------------------
        args
            table : dict
                e.g. {'serial: '1234'}
        ----------------------------------------------------------------------
        returns : bool
            Success of POST operation.
        ----------------------------------------------------------------------
        """
        return self.post_item(table, 'vasic_grip_ring')

    def post_vasic_wafer(self, table):
        """
        POST table: vasic_wafer

        ----------------------------------------------------------------------
        args
            table : dict
                e.g.
                    {
                        'production_date': '2022-09-06 15:30:14',
                        'manufacturer': 2,
                        'run_number', 123,
                        'serial': '123',
                    }
        ----------------------------------------------------------------------
        returns : bool
            Success of POST operation.
        ----------------------------------------------------------------------
        """
        return self.post_item(table, 'vasic_wafer')

    def post_vcable(self, table):
        """
        POST table: vcable

        ----------------------------------------------------------------------
        args
            table : dict
                e.g.
                    {
                        'production_date': '2022-09-06 15:30:14',
                        'manufacturer': 6,
                        'run_number', 123,
                        'serial': '123',
                        'type': '1234',
                        'length': 1.6,
                    }
        ----------------------------------------------------------------------
        returns : bool
            Success of POST operation.
        ----------------------------------------------------------------------
        """
        return self.post_item(table, 'vcable')

    def post_vmotherboard(self, table):
        """
        POST table: vmotherboard

        This is for a Veto motherboard with a vpdu installed.

        ----------------------------------------------------------------------
        args
            table : dict
                e.g.
                    {
                        'production_date': '2022-09-06 15:30:14',
                        'manufacturer': 6,
                        'run_number', 123,
                        'qrcode': '22060101112345123',
                        'vpdu_id': 6,
                    }
        ----------------------------------------------------------------------
        returns : bool
            Success of POST operation.
        ----------------------------------------------------------------------
        """
        return self.post_item(table, 'vmotherboard')

    def post_vpcb(self, table):
        """
        POST table: vpcb

        This is for a bare Veto PCB.

        ----------------------------------------------------------------------
        args
            table : dict
                e.g.
                    {
                        'production_date': '2022-09-06 15:30:14',
                        'manufacturer': 5,
                        'run_number', 12,
                        'qrcode': '22060101112345789',
                        # Omit this field if submitting the blank PCB for the
                        # first time. When this PCB has an ASIC added later
                        # and becomes a vpcb_asic, this ID can be added to
                        # point to that.
                        'vpcb_asic_id': 3,
                    }
        ----------------------------------------------------------------------
        returns : bool
            Success of POST operation.
        ----------------------------------------------------------------------
        """
        return self.post_item(table, 'vpcb')

    def post_vpcb_asic(self, table):
        """
        POST table: vpcb_asic

        This is for a Veto PCB with back-side components and an ASIC installed.

        ----------------------------------------------------------------------
        args
            table : dict
                e.g.
                    {
                        'production_date': '2022-09-06 15:30:14',
                        'vpcb_id': 5,
                        'vasic_id', 12,
                        'solder_mass': 18.1,
                        # this refers to the original bare vTile PCB's ID.
                        'vtile_id': 3,
                    }
        ----------------------------------------------------------------------
        returns : bool
            Success of POST operation.
        ----------------------------------------------------------------------
        """
        return self.post_item(table, 'vpcb_asic')

    def post_vpdu(self, table):
        """
        POST table: vpdu

        This is for a Veto PDU with 16 vtiles installed.

        ----------------------------------------------------------------------
        args
            table : dict
                e.g.
                    {
                        'production_date': '2022-09-06 15:30:14',
                        'manufacturer': 7,
                        'run_number': 234,
                        'serial': '1234567A'
                        'vmotherboard_id': 5,
                        # 16x vtile_pid
                        'vtile_1': 17,
                        'vtile_2': 18,
                        'vtile_3': 19,
                        'vtile_4': 20,
                        'vtile_5': 21,
                        'vtile_6': 22,
                        'vtile_7': 23,
                        'vtile_8': 24,
                        'vtile_9': 25,
                        'vtile_10': 26,
                        'vtile_11': 27,
                        'vtile_12': 28,
                        'vtile_13': 29,
                        'vtile_14': 30,
                        'vtile_15': 31,
                        'vtile_16': 32,
                        'detector_id': 3,
                    }
        ----------------------------------------------------------------------
        returns : bool
            Success of POST operation.
        ----------------------------------------------------------------------
        """
        return self.post_item(table, 'vpdu')

    def post_vtile(self, table):
        """
        POST table: vtile

        This is for a Veto PCB with back-side components, ASIC and SiPMs
        installed.

        The SiPM numbering is shown looking at the PCB with SiPMs visible and
        towards the viewer, and the backside components
        (resistors, capacitors, ASIC etc.) facing away from the viewer. The
        location of the QR code and ASIC on the back-side of the PCB are also
        shown to provide orientation.

        +----+----+----+----+
        | 19 | 13 |  7 |  1 |
        +----+---QR----+----+
        | 20 | 14 |  8 |  2 |
        +----+----+----+----+
        | 21 | 15 |  9 |  3 |
        +----+----+----+----+
        | 22 | 16 | 10 |  4 |
        +----+---ASIC--+----+
        | 23 | 17 | 11 |  5 |
        +----+----+----+----+
        | 24 | 18 | 12 |  6 |
        +----+----+----+----+

        ----------------------------------------------------------------------
        args
            table : dict
                e.g.
                    {
                        'production_date': '2022-09-06 15:30:14',
                        'manufacturer': 7,
                        'run_number': 234,
                        'serial': '1234567A'
                        'vpcb_asic_id': 5,
                        'solder_id': 2,
                        # 24x sipm_pid
                        'sipm_1': 17,
                        'sipm_2': 18,
                        'sipm_3': 19,
                        'sipm_4': 20,
                        'sipm_5': 21,
                        'sipm_6': 22,
                        'sipm_7': 23,
                        'sipm_8': 24,
                        'sipm_9': 25,
                        'sipm_10': 26,
                        'sipm_11': 27,
                        'sipm_12': 28,
                        'sipm_13': 29,
                        'sipm_14': 30,
                        'sipm_15': 31,
                        'sipm_16': 32,
                        'sipm_17': 33,
                        'sipm_18': 34,
                        'sipm_19': 35,
                        'sipm_20': 36,
                        'sipm_21': 37,
                        'sipm_22': 38,
                        'sipm_23': 39,
                        'sipm_24': 40,
                        # Omit this field if submitting the tile for the
                        # first time. When this tile is assembled onto a vPDU
                        # later, this ID can be added to point to that.
                        'vpdu_id': 3,
                    }
        ----------------------------------------------------------------------
        returns : bool
            Success of POST operation.
        ----------------------------------------------------------------------
        """
        return self.post_item(table, constants.TABLE_VTILE)

    def post_wafer(self, table):
        """
        POST table: wafer

        Add a SiPM wafer table to the database.

        ----------------------------------------------------------------------
        args
            table : dict
                e.g.
                    {
                        'manufacturer': 2,
                        'lot': 3,
                        'wafer_number': 6,
                        'spad_size': 30,
                        'dose': 3,
                        'production_date': '2022-09-06 15:30:14',
                        'description': 5,
                    }
        ----------------------------------------------------------------------
        returns : bool
            Success of POST operation.
        ----------------------------------------------------------------------
        """
        return self.post_item(table, 'wafer')

    def post_wafer_defects(self, table):
        """
        POST table: wafer_defects
        """
        # return self.post_item(table, 'wafer_defects')
        raise NotImplementedError

    def post_wafer_status(self, table):
        """
        POST table: wafer_status
        """
        # return self.post_item(table, 'wafer_status')
        raise NotImplementedError

    ##########################################################################
    # specific test results
    #
    # These methods are simply wrappers for the generic post_measurement call.
    #
    # They are only defined to give an interactive user a chance to get the
    # database submission right by referring to the method documentation
    # using the Python interpreter's 'help()' command.
    #

    def post_dummyload_test(self, table):
        """
        POST table: dummyload_test
        """
        # return self.post_measurement(table, 'dummyload_test')
        raise NotImplementedError

    def post_pdu_pulse_test(self, table):
        """
        POST table: pdu_pulse_test
        """
        # return self.post_measurement(table, 'pdu_pulse_test')
        raise NotImplementedError

    def post_tile_cold_test(self, table):
        """
        POST table: tile_cold_test
        """
        # return self.post_measurement(table, 'tile_cold_test')
        raise NotImplementedError

    def post_tile_warm_test(self, table):
        """
        POST table: tile_warm_test
        """
        # return self.post_measurement(table, 'tile_warm_test')
        raise NotImplementedError

    def post_user_test(self, table):
        """
        POST table: user_test
        """
        # return self.post_measurement(table, 'user_test')
        raise NotImplementedError

    def post_vasic_test(self, table):
        """
        POST table: vasic_test
        """
        # return self.post_measurement(table, 'vasic_test')
        raise NotImplementedError

    def post_sipm_test(self, table):
        """
        POST table: sipm_test

        Add a test result for a SiPM that exists in the database.

        ----------------------------------------------------------------------
        args
            table : dict
                e.g.
                    {
                        'timestamp': '2022-09-06 15:30:14',
                        # initials of person adding this test result
                        'operator': 'ap',
                        'sipm_id': 137,
                        # 1=pass, 0=fail
                        'good': 1,
                        'comment': 'good/bad status based solely on wafer...',
                    }
        ----------------------------------------------------------------------
        returns : bool
            Success of POST operation.
        ----------------------------------------------------------------------
        """
        return self.post_measurement(table, 'sipm')

    def post_vpcb_asic_test(self, table):
        """
        POST table: vpcb_asic_test

        ----------------------------------------------------------------------
        args
            table : dict
        ----------------------------------------------------------------------
        returns : bool
            Success of POST operation.
        ----------------------------------------------------------------------
        """
        return self.post_measurement(table, 'vpcb_asic')

    def post_vpcb_test(self, table):
        """
        POST table: vpcb_test

        ----------------------------------------------------------------------
        args
            table : dict
        ----------------------------------------------------------------------
        returns : bool
            Success of POST operation.
        ----------------------------------------------------------------------
        """
        return self.post_measurement(table, 'vpcb')

    def post_vpdu_cold_test(self, table):
        """
        POST table: vpdu_cold_test

        ----------------------------------------------------------------------
        args
            table : dict
        ----------------------------------------------------------------------
        returns : bool
            Success of POST operation.
        ----------------------------------------------------------------------
        """
        return self.post_measurement(table, 'vpdu_cold_test')

    def post_vpdu_test(self, table):
        """
        POST table: vpdu_test

        ----------------------------------------------------------------------
        args
            table : dict
        ----------------------------------------------------------------------
        returns : bool
            Success of POST operation.
        ----------------------------------------------------------------------
        """
        return self.post_measurement(table, 'vpdu_test')

    def post_vmotherboard_test(self, table):
        """
        POST table: vmotherboard_test

        ----------------------------------------------------------------------
        args
            table : dict
        ----------------------------------------------------------------------
        returns : bool
            Success of POST operation.
        ----------------------------------------------------------------------
        """
        return self.post_measurement(table, 'vmotherboard')

    def post_vtile_test(self, table):
        """
        POST table: vtile_test

        ----------------------------------------------------------------------
        args
            table : dict
        ----------------------------------------------------------------------
        returns : bool
            Success of POST operation.
        ----------------------------------------------------------------------
        """
        return self.post_measurement(table, 'vtile')

    def post_vtile_cold_test(self, table):
        """
        POST table: vtile_cold_test
        """
        # return self.post_measurement(table, 'vtile_cold_test')
        raise NotImplementedError
