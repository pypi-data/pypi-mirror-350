"""
This file manages a file local to the end-user containing plain-text database
login credentials. This should very much be a TEMPORARY arrangement, since
authentication should - in this context - be handled by SSL certificates as
soon as support is enabled at the endpoint.

https://www.postgresql.org/docs/15/auth-methods.html
"""

import contextlib
import getpass
import json
import logging
import os

import requests

from ds20kdb import constants


##############################################################################
# support functions
##############################################################################

def obtain_credentials_from_user():
    """
    Prompt user for database login credentials without displaying text on
    the screen. No authentication is performed.

    --------------------------------------------------------------------------
    args : none
    --------------------------------------------------------------------------
    returns : dict
        e.g. {'username': 'user123', 'password': 'hsU2-l_85k3a-Ur8'}
    --------------------------------------------------------------------------
    """
    with contextlib.suppress(getpass.GetPassWarning):
        username = getpass.getpass(prompt='username: ')
        password = getpass.getpass(prompt='password: ')

    return {'username': username, 'password': password}


##############################################################################
# data structures
##############################################################################


class Authentication:
    """
    Manage setting, verification and read/write from local storage of database
    login credentials.

    No need to be paranoid about in-memory persistence of credentials in this
    context since they are stored in the user's home directory in plain text.
    """
    _filename = '.ds20kdbrc'
    _home_directory = os.path.expanduser('~')
    file_path = os.path.join(_home_directory, _filename)

    ##########################################################################
    # file i/o
    ##########################################################################

    def read_credentials(self, verbose=True):
        """
        Read credentials dictionary from a file in the user's home directory.

        This file should only be written to by the write_credentials method,
        but perform a few confidence checks just to be sure its contents are
        as expected.

        This method is used in two places, (1) when the user runs the command
        create_credentials_file, and (2) when the database interface tries to
        obtain login credentials. In the former case, we don't wish to see
        file-not-found logging errors produced, as this will just confuse the
        end user.

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns
            dict if the read was successful, or None otherwise
                e.g. {'username': 'user123', 'password': 'hsU2-l_85k3a-Ur8'}
            verbose : bool
                Used to suppress error logs in read_credentials() when the
                user is trying to create a new credentials file.
        ----------------------------------------------------------------------
        """
        # confidence checks phase 1
        try:
            size_bytes = os.path.getsize(self.file_path)
        except IOError:
            if verbose:
                logging.error(
                    'file does not exist or is inaccessible: %s',
                    self.file_path
                )
            return None

        if size_bytes > 512:
            logging.warning(
                'file is suspiciously large (%s bytes): %s',
                size_bytes, self.file_path
            )
            return None

        # read file contents
        with open(self.file_path, 'r', encoding='utf-8') as ds20kdbrc:
            try:
                credentials = json.load(ds20kdbrc)
            except json.JSONDecodeError:
                logging.error('could not read file: %s', self.file_path)
                return None

        # confidence checks phase 2
        if not isinstance(credentials, dict):
            logging.error(
                'file did not contain a dictionary: %s', self.file_path
            )
            return None

        num_keys = len(credentials)
        if num_keys != 2:
            logging.error(
                'file has wrong number of entries (%s): %s', num_keys,
                self.file_path
            )
            return None

        missing = {
            x for x in ['username', 'password']
            if x not in credentials.keys()
        }
        if missing:
            logging.error(
                'file is missing key(s) (%s): %s', ', '.join(missing),
                self.file_path
            )
            return None

        return credentials

    def write_credentials(self, credentials):
        """
        Write a credentials dictionary to a file in the user's home directory.

        ----------------------------------------------------------------------
        args
            credentials : dict
                e.g. {'username': 'user123', 'password': 'hsU2-l_85k3a-Ur8'}
        ----------------------------------------------------------------------
        returns : none
        ----------------------------------------------------------------------
        """
        if isinstance(credentials, dict):
            with open(self.file_path, 'w', encoding='utf-8') as ds20kdbrc:
                json.dump(credentials, ds20kdbrc)
        else:
            logging.error('credentials not in expected format')

    ##########################################################################
    # supplemental methods
    ##########################################################################

    @staticmethod
    def credentials_accepted_by_endpoint(credentials):
        """
        Check if the supplied credentials are found to be acceptable by the
        far end.

        ----------------------------------------------------------------------
        args
            credentials : dict
                e.g. {'username': 'user123', 'password': 'hsU2-l_85k3a-Ur8'}
        ----------------------------------------------------------------------
        returns
            bool
                True if the far end found the credentials acceptable,
                False otherwise.
        ----------------------------------------------------------------------
        """
        username, password = credentials['username'], credentials['password']

        try:
            test_response = requests.get(
                constants.BASE_URL,
                auth=requests.auth.HTTPBasicAuth(username, password),
                timeout=10,
            )
        except requests.exceptions.ConnectTimeout:
            logging.error('timeout')
            return False
        except requests.exceptions.ReadTimeout:
            logging.error('read timeout - check credentials')
            return False
        except requests.exceptions.ConnectionError:
            logging.error('connection error')
            return False

        if test_response.status_code == requests.codes.unauthorized:
            logging.error('authentication failed')
            return False

        return True

    def create_credentials_file(self, force=False, verbose=True):
        """
        Create a local JSON file containing the login credentials for the
        database.

        By default, a check is made to see if a credentials file already
        exists and whether the credentials it contains are acceptable. If
        this check is successful, the user will not be prompted for new
        credentials unless they to force the issue.

        The caller is prompted to interactively enter a username/password. A
        test query is made to the database to check if the supplied details
        were correct. If correct, these details are written to a file called
        .ds20kdbrc in the user's home directory. This local file is then read
        when initialising the Database class, which inherits from this
        class.

        ----------------------------------------------------------------------
        args
            force : bool
                Force the creation of a new credentials file, even if a valid
                file already exists.
            verbose : bool
                Used to suppress error logs in read_credentials() when the
                user is trying to create a new credentials file.
        ----------------------------------------------------------------------
        returns
            bool
                True if the file was successfully created, False otherwise.
        ----------------------------------------------------------------------
        """
        try:
            valid_file_exists = not force and self.credentials_accepted_by_endpoint(
                self.read_credentials(verbose=verbose)
            )
        except TypeError:
            # credentials file didn't exist, or contents were not acceptable
            # proceed to prompt the user to create a new file
            pass
        else:
            if valid_file_exists:
                logging.warning(
                    'a valid credentials file already exists, set force to True to overwrite'
                )
                return True

        credentials = obtain_credentials_from_user()

        if self.credentials_accepted_by_endpoint(credentials):
            self.write_credentials(credentials)
            return True

        logging.error('did not create credentials file')
        return False
