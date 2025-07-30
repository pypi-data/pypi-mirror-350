"""
Primitive read-only cache for database GET operations for testing purposes
(use for refining complex plots/analysis with many db lookups etc.).

Mode of operation:

Assuming a clean start, a typical GET operation such as
dbi.get('solder', institute_id=5) will look in the local cache for table
'solder', will find it's missing, and will then fetch the whole 'solder' table
from the database and write it to the disk cache and load it into memory. A
second GET operation on this table such as dbi.get('solder', institute_id=6)
will not connect to the database, it will read from the cache instead.

In other words, the first GET operation for a table will be slow, but all
subsequent GET operations to the same table will be fast.

DESCRIBE operations are passed through to the database without caching.

CAVEATS:

(1) inner joins are not implemented
(2) limiting numbers of rows returned from the db is not implemented
(3) WARNING: results of any POST operations are NOT cached

To use, change your code from:

from ds20kdb import interface; dbi = interface.Database()

to:

from ds20kdb import interface_cache; dbi = interface_cache.CachedDatabase()
"""

import datetime
import glob
import logging
import os
import time

import pandas as pd

from ds20kdb import interface


###############################################################################
# Constants
###############################################################################


CACHE_DIRECTORY = '.ds20kdb_cache'
CACHE_EXPIRATION_HOURS = 24


###############################################################################
# Data structures
###############################################################################


class CachedDatabase(interface.Database):
    """
    Patch this over the normal database class.
    """
    def __init__(self):
        super().__init__()

        self.cache_hit = 0
        self.cache_miss = 0
        self.cache_reload = 0

        # {'table_name': <Pandas DataFrame>, ...}
        self.cached_table = {}

        # Pandas DataFrames for entire database tables are stored in this
        # directory.
        self.cache_directory = os.path.join(
            os.path.expanduser('~'),
            CACHE_DIRECTORY
        )
        os.makedirs(self.cache_directory, exist_ok=True)

    def _local_query(self, table_name, joins=None, **columns):
        """
        Create a query string to suit a cached Pandas DataFrame, and return
        the response.

        -----------------------------------------------------------------------
        args : Refer to documentation for Class Database get() (interface.py).
        -----------------------------------------------------------------------
        returns : Pandas DataFrame
        -----------------------------------------------------------------------
        """
        query_string = '&'.join(f'{k}=={v}' for k, v in columns.items())
        if query_string:
            try:
                return self.cached_table[table_name].query(query_string)
            except (KeyError, pd.errors.UndefinedVariableError):
                return None
        else:
            return self.cached_table[table_name]

    def _db_fetch_and_cache(self, table_name, joins=None, **columns):
        """
        Fetch table from the database, cache it on the local filestore, and
        load it into memory.

        -----------------------------------------------------------------------
        args : Refer to documentation for Class Database get() (interface.py).
        -----------------------------------------------------------------------
        returns : bool
        -----------------------------------------------------------------------
        """
        path = os.path.join(self.cache_directory, table_name)
        response = super().get(table_name, joins=None, **columns)

        # refresh filestore
        dfr = response.data
        if dfr is None:
            return False

        dfr.to_pickle(path)
        self.cached_table[table_name] = pd.read_pickle(path)

        return True

    def get(self, table_name, joins=None, **columns):
        """
        Replace standard GET operation. Refer to documentation in interface.py.
        """
        result = interface.Result()

        table_cached_in_memory = table_name in self.cached_table
        table_cached_in_filestore, valid = self._table_in_filestore(table_name)
        path = os.path.join(self.cache_directory, table_name)

        if table_cached_in_memory:
            self.cache_hit += 1
            result.data = self._local_query(table_name, joins=None, **columns)

        elif table_cached_in_filestore:
            if valid:
                # files exists in filestore and is valid, load into memory, run query
                self.cache_hit += 1

                self.cached_table[table_name] = pd.read_pickle(path)
                result.data = self._local_query(table_name, joins=None, **columns)
            else:
                # file exists but has expired, refresh from database
                self.cache_miss += 1

                logging.info('version on disk expired, fetch from db')
                success = self._db_fetch_and_cache(table_name, joins=None, **columns)
                if success:
                    self.cache_reload += 1
                    result.data = self._local_query(table_name, joins=None, **columns)
        else:
            # not available locally
            self.cache_miss += 1

            self._db_fetch_and_cache(table_name, joins=None, **columns)
            result.data = self._local_query(table_name, joins=None, **columns)

        return result

    def _table_in_filestore(self, table_name):
        """
        Check if the database table exists in the disk cache, and whether it is
        still valid.

        This style of validity checking may not work on macOS.

        -----------------------------------------------------------------------
        args
            table_name : string
                the name of the database table
        -----------------------------------------------------------------------
        returns
            table_exists : bool
                does the table exist in disk cache
            valid : bool
                is the file's creation date is within the valid expiry period
        -----------------------------------------------------------------------
        """
        now_utc = datetime.datetime.fromtimestamp(
            time.time(), datetime.timezone.utc
        )

        path = os.path.join(self.cache_directory, table_name)
        try:
            timestamp = os.path.getctime(path)
        except FileNotFoundError:
            table_exists = False
            valid = False
        else:
            table_exists = True
            table_creation_timestamp_utc = datetime.datetime.fromtimestamp(
                timestamp, datetime.timezone.utc
            )
            diff = now_utc - table_creation_timestamp_utc
            expiry_period = datetime.timedelta(hours=CACHE_EXPIRATION_HOURS)
            valid = diff < expiry_period

        return table_exists, valid

    ###########################################################################
    # clear cache entries
    ###########################################################################

    def _clear_memory_cache(self):
        """
        Clear tables stored in memory.

        -----------------------------------------------------------------------
        args : none
        -----------------------------------------------------------------------
        returns : none
        -----------------------------------------------------------------------
        """
        self.cached_table.clear()

    def _clear_disk_cache(self):
        """
        Clear tables stored in the disk cache.

        This script only creates plain files in the cache directory. If the
        user has created dotfiles, subdirectories or links, leave them
        alone.

        -----------------------------------------------------------------------
        args : none
        -----------------------------------------------------------------------
        returns : none
        -----------------------------------------------------------------------
        """
        files = filter(
            os.path.isfile,
            glob.glob(os.path.join(self.cache_directory, '*'))
        )

        for file in files:
            os.remove(file)

    def clear_cache(self):
        """
        Clear cache items from memory and disk.

        -----------------------------------------------------------------------
        args : none
        -----------------------------------------------------------------------
        returns : none
        -----------------------------------------------------------------------
        """
        self._clear_memory_cache()
        self._clear_disk_cache()

    ###########################################################################
    # cache stats
    ###########################################################################

    def cache_info(self):
        """
        Supply some basic cache statistics.
        """
        try:
            hit_rate = self.cache_hit / (self.cache_hit + self.cache_miss)
        except ZeroDivisionError:
            hit_rate_suffix = ''
        else:
            hit_rate_suffix = f' ({hit_rate:.2%})'

        return (
            f'cache hits {self.cache_hit}, misses {self.cache_miss}:'
            f'{hit_rate_suffix}\n'
            f'{len(self.cached_table)} table(s) cached: '
            f'{", ".join(sorted(self.cached_table))}\n'
            f'expired tables reloaded from database: {self.cache_reload}'
        )
