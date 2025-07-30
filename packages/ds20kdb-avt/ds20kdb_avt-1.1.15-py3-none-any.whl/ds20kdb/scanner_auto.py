#!/usr/bin/env python3
r"""
Cross-platform script to manage "vpcb_asic", "vtile", "vmotherboard"
and "vpdu" scanner images. Copies the file to a webserver preserving the
timestamp, and updates the DB with the URL of the image, on the vpdu,
vmotherboard, vtile_test or vpcb_asic_test tables.

This version of the script has been designed to assist with the automation
(bulk submission) of scanned images. To enable this, the filename of
scanned images must be in the following two formats:

<qrcode>_<component>_<side>.png
<qrcode>_<component>_<side>_<info>.png

Only the first three parameters are used, the info parameter is ignored (it is
used locally to indicate incoming/outgoing inspection).

For safety, no uploads will be performed without --write (-w).

Examples showing both forms of authentication (macOS/Linux):

./scanner_auto.py <initials> <institute> -s ~/.ds20kdb_scanner_rc
./scanner_auto.py <initials> <institute> -c <remote_username> ~/.ssh/id_ecdsa

./scanner_auto.py tl liverpool -c tle ~/.ssh/id_ecdsa

or from Windows Anaconda PowerShell Prompt:

python scanner_auto.py tl liverpool -c tle $HOME\.ssh\id_ecdsa

If your files are in a specific directory you can use something like this:

python scanner_auto.py tl liverpool -c tle $HOME\.ssh\id_ecdsa -d $HOME\scans

Based on the original script by P.Franchini - p.franchini@lancaster.ac.uk
Available at:

    https://gitlab.in2p3.fr/darkside/productiondb_software/-/
            blob/master/examples_python/submit_scanner/scanner.py
"""

import argparse
import collections
import contextlib
from datetime import datetime
import glob
import hashlib
import itertools
import json
import logging
import os
import pathlib
import posixpath
import socket
import sys
import tempfile
import time
import types

import paramiko
import PIL
from PIL import Image

from ds20kdb import interface


##############################################################################
# data structures
##############################################################################


class Connect:
    """
    Create a persistent SSH connection for use by a context manager.
    """
    # Nodes running CentOS 7 (EOL 2024 06 30) retired
    # Use this node with AlmaLinux release 9.3 (Shamrock Pampas Cat)
    remote_filestore = 'linappserv6.pp.rhul.ac.uk'

    def __init__(self, args):
        self.ssh = None

        try:
            remote_ipv4 = socket.getaddrinfo(self.remote_filestore, 0)[0][-1][0]
        except (IndexError, socket.gaierror):
            print(f'Could not obtain IP address for {self.remote_filestore}')
        else:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                ssh.connect(
                    remote_ipv4, username=args.user, key_filename=args.key,
                )
            except (FileNotFoundError, TimeoutError, paramiko.ssh_exception.SSHException):
                print('Could not connect to remote image filestore.')
            else:
                self.ssh = ssh

    def __enter__(self):
        return self.ssh

    def __exit__(self, exc_type, exc_value, exc_traceback):
        with contextlib.suppress(AttributeError):
            self.ssh.close()

    def __bool__(self):
        return self.ssh is not None


class Component:
    """
    Upload a scanned image to the RHUL remote filestore and POST its
    associated record to the database.
    """
    __slots__ = {
        'comment': 'String that gets written the db table comments field.',
        'component': 'Component that was scanned.',
        'configuration': 'Hardware used to produce the scanned image.',
        'dbi': 'database interface session',
        'file': 'The full path and file of the scanned image.',
        'hash': (
            'Hex digest of the scanned image. This will be used later to '
            'verify that the file was uploaded successfully.'
        ),
        'key': 'Full path and file, local SSH private key.',
        'operator': 'Initials of the person who performed the scan.',
        'optical_inspection': 'URL of uploaded image.',
        'institute': (
            'Search text used to find the institute_id. Used as the end of the '
            'remote path.'
        ),
        'institute_id': 'Numeric value from looking up institute in the database.',
        'institute_text': (
            'Full text institution name that relates to the institute_id.'
        ),
        'qrcode': '17-digit numeric as encoded into the QR-code image.',
        'remote_ipv4': 'IP address of the remote filestore.',
        'remote_path': 'URL of the location scanned images are uploaded to.',
        'side': 'The side of the PCB that was scanned.',
        'ssh': 'Instance of class Connect, persistent ssh connection.',
        'table': 'Table to be written to the database.',
        'timestamp_db': 'Timestamp string.',
        'timestamp_file': 'Timestamp string.',
        'user': 'Username for RHUL SSH/SFTP login, used for image upload.',
        'write': 'Flag used to enable/disable file upload and database writes.',
    }

    def __init__(self, dbi, args, image_details, institute_details, ssh):
        self.file, self.qrcode, self.component, self.side = image_details
        self.institute_id, self.institute_text = institute_details
        self.ssh = ssh
        self.dbi = dbi

        self.operator = args.operator
        self.institute = args.institute
        self.configuration = args.configuration
        self.write = args.write

        self.optical_inspection = None
        self.table = None

        datetime_obj = datetime.fromtimestamp(os.path.getmtime(self.file))
        self.timestamp_db = datetime_obj.strftime('%Y-%m-%dT%H:%M:%S')
        self.timestamp_file = datetime_obj.strftime('%Y%m%dT%H%M%S')

        self.remote_path = posixpath.join('/scratch4/DarkSide/scanner', self.institute)
        self.comment = ', '.join(['visual inspection', self.component, self.side])

        self.hash = None

    def __str__(self):
        items = {
            ' ': '-' * 40,
            'Image': self.file,
            'Image source': self.configuration,
            'Timestamp (database)': self.timestamp_db,
            'Timestamp (remote file)': self.timestamp_file,
            'Operator\'s initials': self.operator,
            'QR-code': self.qrcode,
            'Scanned component': self.component,
            'Scanned side': self.side,
            'Institute (remote suffix)': self.institute,
            'Institute full text': self.institute_text,
            'Institute ID': self.institute_id,
            'Comment field': self.comment,
            'Remote path': self.remote_path,
            'Permission to write': self.write,
            '  ': '-' * 40,
        }
        return '\n'.join(f'{k:<28}{v}' for k, v in items.items())

    def upload_target(self, scanned_image, temp_png_image):
        """
        Return a file-like object that represents the image to be uploaded to
        the remote filestore.

        If the original file is a PNG this will be used. If the file is a
        TIFF, a temporary PNG image file (with lossless compression) is
        created in memory and that will be used. Creating the PNG in memory
        works around non-writable filesystems, and prevents the local
        filestore becomming cluttered with temporary files.

        The ultimate aim is to ensure a PNG file is uploaded, so the remote
        filestore doesn't get filled with huge uncompressed TIFF files from
        the scanner.

        For further details see:

        https://docs.python.org/3/library/tempfile.html#module-tempfile
        https://docs.python.org/3/glossary.html#term-file-like-object

        ===============================
        PNG Conversion
        ===============================

        compress_level=6 is the default, compress_level=4 represents the best
        compromise between file size and compression speed for the large
        (~115MB) uncompressed TIF scans used here.

        Time is given relative to compress_level=9 (105.25s) for a
        representative scan

        compress_level    time    file size (MB)
         0                0.02     114
         1                0.03      49
         2                0.04      48
         3                0.06      47
         4                0.08      42
         5                0.12      42
         6                0.23      42
         7                0.31      41
         8                0.65      41
         9                1.00      41
         optimize=True    0.98      41

        For compression options, see:
        https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html
            #png-saving

        ----------------------------------------------------------------------
        args
            scanned_image : file-like object
                Refers to the original scanned image.
            temp_png_image : file-like object.
                Empty at function start, it may subsequently contain a PNG
                file.
        ----------------------------------------------------------------------
        returns : file-like object
        ----------------------------------------------------------------------
        """
        extension = os.path.splitext(self.file)[-1].lower()

        if extension in {'.tif', '.tiff'}:
            print('converting file from TIFF to PNG')
            with Image.open(scanned_image) as img:
                img.save(temp_png_image, format='png', compress_level=4)

            return temp_png_image

        return scanned_image

    @staticmethod
    def report_upload_size(scan_for_upload):
        """
        Print file size in MB.

        ----------------------------------------------------------------------
        args
            scan_for_upload : file-like object
        ----------------------------------------------------------------------
        returns : none
        ----------------------------------------------------------------------
        """
        scan_for_upload.seek(0, os.SEEK_END)
        image_size_bytes = scan_for_upload.tell()
        scan_for_upload.seek(0)

        print(f'Uploading ~{image_size_bytes // (1024 * 1024)}MiB...')

    def upload_image(self):
        """
        Upload file to remote filestore using the SSH File Transfer Protocol.

        Checking if the file was uploaded and is readable is done via SFTP
        because on linappserv3, there's an unpredictable lag between writing
        the file and it being visible on the webserver. We don't
        particularly care about this delay because we're not going to try to
        view the contents of the file immediately, we're just going to write
        the URL to the db. This constitutes an adequate check.

        If this instance refers to a TIFF file, it will be converted to a
        lossless PNG file before upload.

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns : none
            self.file and self.optical_inspection modified
            A PNG file may be created
        ----------------------------------------------------------------------
        """
        if not self.write:
            print('Use the --write command line option to enable image uploads.')
            return

        with open(self.file, 'rb') as scanned_image_flo, tempfile.TemporaryFile() as temp_png_image_flo:

            # convert to PNG if necessary
            scan_for_upload = self.upload_target(scanned_image_flo, temp_png_image_flo)
            self.report_upload_size(scan_for_upload)

            filename = f'{self.qrcode}-{self.side}-{self.timestamp_file}.png'
            url = f'https://www.pp.rhul.ac.uk/DarkSide/scanner/{self.institute}/{filename}'

            # This temporarily loads the entire image into memory. Scanned
            # images should be a maximum of 60MB in size (PNG), so no
            # problems are expected with memory usage. SHA256 is used instead
            # of blake2b simply because sha256sum is ubiquitous and available
            # at the far end from the command line.
            self.hash = hashlib.sha256(scan_for_upload.read()).hexdigest()
            scan_for_upload.seek(0)

            print(f' local hash: {self.hash}')

            remote_file_readable = False

            with contextlib.closing(self.ssh.open_sftp()) as sftp:

                # create remote directory for the give institute name
                try:
                    sftp.chdir(self.remote_path)  # Test if remote_path exists
                except (FileNotFoundError, IOError):
                    sftp.mkdir(self.remote_path)  # Create remote_path
                    sftp.chdir(self.remote_path)

                # send file, overwriting existing file and preserving the time

                # Get the modification time from the original scanner image
                # which should represent the timestamp at the time of the
                # scan.
                local_file_mtime = os.path.getmtime(self.file)

                remote_file_path = posixpath.join(self.remote_path, filename)
                try:
                    sftp.putfo(scan_for_upload, remote_file_path)
                except OSError:
                    # OSError: size mismatch in put!
                    pass
                except EOFError:
                    # remote host closed connection mid-transfer
                    pass
                else:
                    sftp.utime(remote_file_path, (local_file_mtime, local_file_mtime))

                    # Check if local and remote files are the same.
                    #
                    # This is almost certainly overkill given the checks SFTP
                    # performs. However, in the case where (for some reason)
                    # garbage collection isn't performed at the far end in the
                    # case of an interrupted transfer, this will be caught here.
                    # sha256sum is ubiquitous on Linux systems, including the
                    # remote filestore used here.

                    _stdin, stdout, _stderr = self.ssh.exec_command(f'sha256sum {remote_file_path}')
                    try:
                        remote_hash = stdout.read().split()[0].decode('utf-8')
                    except IndexError:
                        pass
                    else:
                        remote_file_readable = remote_hash == self.hash
                        print(f'remote hash: {remote_hash}')

            if remote_file_readable:
                print(f'Upload verified: {url}')
                self.optical_inspection = url
            else:
                print('File not copied to correctly to RHUL or URL not accessible')
                self.optical_inspection = None

            self.table['optical_inspection'] = self.optical_inspection

    def generate_table_for_db_post(self):
        """
        Creates a table dictionary for the component, omitting any NOT NULL
        fields.

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns : bool True if table created, False otherwise
            self.table modified
        ----------------------------------------------------------------------
        """
        lut = {
            # vmotherboard_test
            'vmotherboard': self.table_vmotherboard,
            # vpcb_asic_test
            'vpcb_asic': self.table_vpcb_asic,
            # vpdu_test
            'vpdu': self.table_vpdu,
            # vtile_test
            'vtile': self.table_vtile,
        }
        table_common = {
            'comment': self.comment,
            'timestamp': self.timestamp_db,
            'operator': self.operator,
            'optical_inspection': self.optical_inspection,
            'configuration': self.configuration,
            'institute_id': self.institute_id,
        }

        self.table = lut[self.component](table_common)

        return self.table is not None

    def table_vtile(self, table_common):
        """
        Build the table to suit measurement: vtile_test.

        ----------------------------------------------------------------------
        args
            table_common : dict
                table fields common to all components.
        ----------------------------------------------------------------------
        returns : dict
            all table fields required for database POST operation
        ----------------------------------------------------------------------
        """
        vtile_id = self.dbi.get_vtile_pid_from_qrcode(self.qrcode).data

        if vtile_id is None:
            print(f'failed to find the vtile_id for QR-code {self.qrcode}')
            return None

        return {**table_common, **{'vtile_id': vtile_id}}

    def table_vpdu(self, table_common):
        """
        Build the table to suit measurement: vpdu_test.

        ----------------------------------------------------------------------
        args
            table_common : dict
                table fields common to all components.
        ----------------------------------------------------------------------
        returns : dict
            all table fields required for database POST operation
        ----------------------------------------------------------------------
        """
        try:
            vmotherboard_id = self.dbi.get(
                'vmotherboard', qrcode=self.qrcode
            ).data.vmotherboard_pid[0]
        except KeyError:
            print('failed to find the vmotherboard_id - probably wrong QR code')
            return None
        vpdu_id = self.dbi.get('vpdu', vmotherboard_id=vmotherboard_id).data.vpdu_pid[0]
        if vpdu_id is None:
            print('failed to find the vpdu_id - probably wrong QR code')
            return None

        return {**table_common, **{'vpdu_id': vpdu_id}}

    def table_vmotherboard(self, table_common):
        """
        Build the table to suit measurement: vmotherboard_test.

        ----------------------------------------------------------------------
        args
            table_common : dict
                table fields common to all components.
        ----------------------------------------------------------------------
        returns : dict
            all table fields required for database POST operation
        ----------------------------------------------------------------------
        """
        try:
            vmotherboard_id = self.dbi.get(
                'vmotherboard', qrcode=self.qrcode
            ).data.vmotherboard_pid[0]
        except KeyError:
            print('failed to find the vmotherboard_id - probably wrong QR code')
            return None

        return {**table_common, **{'vmotherboard_id': vmotherboard_id}}

    def table_vpcb_asic(self, table_common):
        """
        Build the table to suit measurement: vpcb_asic_test.

        ----------------------------------------------------------------------
        args
            table_common : dict
                table fields common to all components.
        ----------------------------------------------------------------------
        returns : dict
            all table fields required for database POST operation
        ----------------------------------------------------------------------
        """
        vpcb_asic_id = self.dbi.get_vpcb_asic_pid_from_qrcode(self.qrcode).data
        if vpcb_asic_id is None:
            print('failed to find the vpcb_asic_id - probably wrong QR code')
            return None

        return {**table_common, **{'vpcb_asic_id': vpcb_asic_id}}

    def post_table(self):
        """
        Post test measurement table to the database.

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns : bool
            True if POST failed, False if successful.
        ----------------------------------------------------------------------
        """
        if not self.write:
            print('Use the --write command line option to enable database writes.')
            return True

        if self.optical_inspection is None:
            print('Problems occurred during image upload, skipping database POST.')
            return True

        print("Table:\t", self.component + '_test')
        print(self.table)

        # Rare transient outages have been observed when accessing the
        # production database (which may be attributed to remote or local
        # issues). Seek to avoid a time-consuming manual fix for the file
        # being uploaded to the filestore without a matching database entry.
        attempts = 3
        for attempt in range(attempts, 0, -1):
            post_successful = self.dbi.post_measurement(self.table, self.component)
            if post_successful:
                break
            if attempt > 1:
                time.sleep(10)
        else:
            print(f'Giving up: {attempts} DB POST attempts failed')

        status = 'succeeded' if post_successful else 'failed'
        print(f'POST {status}')

        return not post_successful


##############################################################################
# file i/o
##############################################################################


def check_scanner_image_file(filepath):
    """
    Check that the scanner image filename conforms to the required format.

    --------------------------------------------------------------------------
    args
        filepath : string
            filename, e.g. '23020703000088001_vtile_circuit_in.png'
    --------------------------------------------------------------------------
    returns
        filepath : string
        qrcode : string
        component : string
        side : string
    --------------------------------------------------------------------------
    """
    filename = os.path.basename(filepath)

    try:
        qrcode, component, side, *_ = os.path.splitext(filename)[0].split('_')
    except ValueError:
        print(f'{filename}: filename not in appropriate format.')
        return None

    if not interface.qr_code_valid(qrcode):
        print(f'{filename}: invalid QR-code')
        return None

    if component not in {'vpcb_asic', 'vtile', 'vmotherboard', 'vpdu'}:
        print(f'{filename}: invalid component: {component}')
        return None

    if side not in {'circuit', 'sipm'}:
        print(f'{filename}: invalid side: {side}')
        return None

    return filepath, qrcode, component, side


def check_image_type(image):
    """
    Supported filetypes are PNG and TIFF.

    --------------------------------------------------------------------------
    args
        image : PIL.Image instance
    --------------------------------------------------------------------------
    returns : bool
        True if the image and extension match, and the actual image format is
        supported.
    --------------------------------------------------------------------------
    """
    basename = os.path.basename(image.filename)
    extension_upper = os.path.splitext(basename)[-1][1:].upper()
    imgfmt = image.format

    extension_format_mismatch = image.format[:3] not in extension_upper[:3]
    if extension_format_mismatch:
        print(
            f'WARNING ({basename}): extension does not match '
            f'actual image format ({imgfmt})'
        )

    supform = {'PNG', 'TIFF'}
    unsupported_format = imgfmt not in supform
    if unsupported_format:
        print(f'Please use {", ".join(supform)}')

    # For the moment, just issue the warning, allow users to adjust
    # if extension_format_mismatch or unsupported_format:
    #     return False

    return True


def image_dimensions_within_bounds(filepath):
    """
    Is the supplied image small enough for PIL to process without complaint?

    This function should be called early, so huge files are eliminated from
    the set of potential uploads before an ssh connection is established with
    the remote RHUL filestore.

    Image.open is lazy: it opens the file but doesn't read the data into
    memory, but it will trigger the decompression bomb exception if the image
    has a total number of pixels above the bound (Image.MAX_IMAGE_PIXELS * 2).
    We set Image.MAX_IMAGE_PIXELS above the default in main().

    https://pillow.readthedocs.io/en/stable/reference/Image.html

    This function also ensures that there is no mismatch between file
    extension and actual image type.

    --------------------------------------------------------------------------
    args
        filepath : string
            filename, e.g. '23020703000088001_vtile_circuit_in.png'
    --------------------------------------------------------------------------
    returns : bool
        True if file is small enough to process, False if image is huge.
    --------------------------------------------------------------------------
    """
    try:
        img = Image.open(filepath)
    except Image.DecompressionBombError as err:
        print(
            f'{'-' * 80}\n'
            f'{err}\n{filepath} omitted\n'
            f'{'-' * 80}'
        )
        return False
    except PIL.UnidentifiedImageError as err:
        # Catch non-images with image-like file extensions or unsupported
        # image formats with incorrect but allowed file extensions.
        print(err)

    # Catch mismatches between file extension and image type, e.g.
    # JPEG files saved with TIFF or PNG extensions.
    valid_image = check_image_type(img)

    img.close()
    if valid_image:
        return True

    return False


def read_credentials(filename):
    """
    Read credentials dictionary from a file from the location specified on the
    command line.

    --------------------------------------------------------------------------
    args
        filename : string
    --------------------------------------------------------------------------
    returns
        dict if the read was successful, or None otherwise
            e.g. {'username': 'user123', 'key': '~/.ssh/id_ecdsa'}
    --------------------------------------------------------------------------
    """
    # confidence checks phase 1
    try:
        size_bytes = os.path.getsize(filename)
    except IOError:
        logging.error(
            'file does not exist or is inaccessible: %s',
            filename
        )
        return None

    if size_bytes > 512:
        logging.warning(
            'file is suspiciously large (%s bytes): %s',
            size_bytes, filename
        )
        return None

    # read file contents
    with open(filename, 'r', encoding='utf-8') as ds20kdb_scanner_rc:
        try:
            credentials = json.load(ds20kdb_scanner_rc)
        except json.JSONDecodeError:
            logging.error('could not read/interpret JSON file: %s', filename)
            return None

    # confidence checks phase 2
    if not isinstance(credentials, dict):
        logging.error(
            'file did not contain a dictionary: %s', filename
        )
        return None

    num_keys = len(credentials)
    if num_keys != 2:
        logging.error(
            'file has wrong number of entries (%s): %s', num_keys,
            filename
        )
        return None

    missing = {
        x for x in ['username', 'key']
        if x not in credentials.keys()
    }
    if missing:
        logging.error(
            'file is missing key(s) (%s): %s', ', '.join(missing),
            filename
        )
        return None

    return credentials


##############################################################################
# command line option handler
##############################################################################


def check_directory_exists(directory):
    """
    Check if directory exists.

    --------------------------------------------------------------------------
    args
        directory : string
    --------------------------------------------------------------------------
    returns
        directory : string
    --------------------------------------------------------------------------
    """
    if not os.path.isdir(directory):
        raise argparse.ArgumentTypeError(
            f'{directory}: directory does not exist'
        )

    return directory


def check_credentials_file(filename):
    """
    Check the specified credentials file: load it and check if the local
    private key file exists.

    --------------------------------------------------------------------------
    args
        filename : string
            filename, e.g. '~/.ds20kdb_scanner_rc'
    --------------------------------------------------------------------------
    returns
        filename : string
    --------------------------------------------------------------------------
    """
    cred = read_credentials(filename)

    if cred is None:
        raise argparse.ArgumentTypeError(f'{filename}: problem with file')

    if not os.path.exists(cred['key']):
        raise argparse.ArgumentTypeError(
            f'{cred["key"]}: private key file does not exist'
        )

    return filename


def check_arguments():
    """
    Handle command line options.

    --------------------------------------------------------------------------
    args : none
    --------------------------------------------------------------------------
    returns
        <class 'argparse.Namespace'>
    --------------------------------------------------------------------------
    """
    parser = argparse.ArgumentParser(
        description=(
            'Uploads scanned images for "vpcb_asic", "vtile", "vmotherboard" '
            'and "vpdu" scanner images. Copies the file(s) to a file/web '
            'server preserving the timestamp, and updates the database with '
            'the URL of the image, on the vpdu, vmotherboard, vtile_test or '
            'vpcb_asic_test tables. Cross-platform. This version of the script '
            'has been designed to assist with the automation (bulk submission) '
            'of scanned images. Acceptable image formats are PNG and TIFF. '
            'TIFF files are converted to lossless PNG files automatically '
            'before being uploaded to the remote filestore.'
        )
    )
    parser.add_argument(
        'operator', nargs=1, metavar='operator', help='Initials of operator.', type=str
    )
    parser.add_argument(
        'institute', nargs=1, metavar='institute',
        help=(
            'Searchable name of the institute in lowercase '
            '(options: birmingham, liverpool, manchester, ral, rhul, warwick). '
            'In addition, the institute name defines the remote URL path, '
            'e.g. "https://www.pp.rhul.ac.uk/DarkSide/scanner/liverpool/"'
        ),
        choices=['birmingham', 'liverpool', 'manchester', 'ral', 'rhul', 'warwick'],
        type=str,
    )
    parser.add_argument(
        '-d', '--directory',
        nargs=1,
        metavar='image-directory',
        help='Directory containing images to be uploaded.',
        type=check_directory_exists, default=[pathlib.Path.cwd()],
    )
    parser.add_argument(
        '--configuration', nargs=1, metavar='configuration',
        help=(
            'Inspection hardware used. '
            'Defaults to the EPSON V850 Pro scanner'
        ),
        type=str, default='Scanner EPSON V850 Pro',
    )

    group1 = parser.add_mutually_exclusive_group(required=True)
    group1.add_argument(
        '-c', '--credentials', nargs=2, metavar=('username', 'keyfile'),
        help=(
            'Royal Holloway Particle Physics (RHUL PP) IT username and local '
            'SSH private key used to set up passwordless login. '
            'Essentially, this option manually specifies the information in '
            'the file used for "-s", e.g. for macOS: '
            '"-c <username> /Users/<username>/.ssh/id_ed25519".'
        ),
        type=str, default=None
    )
    group1.add_argument(
        '-s', '--sftp', nargs=1, metavar='credentials-file',
        help=(
            'File containing RHUL PP IT username and local SSH private key '
            ' used to set up passwordless login, typically '
            '~/.ds20kdb_scanner_rc. The contents of the file (for user '
            '"avt") should look something like '
            '{"username": "avt", "key": "/Users/avt/.ssh/id_ed25519"}. '
            'Note for Windows users: the filename for "key" should be '
            'properly escaped, e.g. '
            r'C:\\Users\\avt\\.ds20kdb_scanner_rc'
            ' or '
            r'C:/Users/avt/.ds20kdb_scanner_rc'
            ' not '
            r'C:\Users\avt\.ds20kdb_scanner_rc'
            '.'
        ),
        type=check_credentials_file, default=None
    )

    parser.add_argument(
        '-u',
        '--unattended',
        action='store_true',
        help='Intended for out-of-hours cron-driven unattended uploads. This\
        option (1) shortlists vTile image files (png, tif) contained in the\
        scan directory for upload, excluding all that are not part of a\
        full set of 3 scans for each QR code: front/back arrival scans, and a\
        front scan at exit. (2) the QR code for each file set is checked\
        in the database, and if scans for that QR code have already been\
        uploaded, then the file set is excluded from upload. This effectively\
        means that only new scans are uploaded. Applicable to the vTile\
        scanning setup at the University of Liverpool. Behaviour in other\
        non-vTile setups is untested/undefined.'
    )
    parser.add_argument(
        '-w',
        '--write',
        action='store_true',
        help='By default - for safety - this script will write NOTHING to\
        the database, and will not transfer any files to the remote\
        filestore. This option allows data writes to occur.',
    )
    parser.add_argument(
        '-o',
        '--overwrite',
        action='store_true',
        help=(
            'DEPRECATED. This option has no effect, and has been left in '
            'place to avoid breaking scripts that depend on its presence. '
            'The original intent was for this to act as a safeguard, where '
            'by default, the uploading of images for the case where a '
            'scanned image already existed in the database for a matching QR '
            'code would be prevented. This has no relevance in the current '
            'production environment.'
        ),
    )
    parser.add_argument(
        '--nodb',
        action='store_true',
        help=(
            'DEBUG: Do NOT write to the database. '
            'Scanned images may still be uploaded.'
        ),
    )

    args = parser.parse_args()

    args.directory = args.directory[0]
    args.operator = args.operator[0]
    args.institute = args.institute[0].lower()
    if args.credentials:
        args.user = args.credentials[0]
        args.key = args.credentials[1]
    else:
        cred = read_credentials(args.sftp[0])
        if not os.path.exists(cred['key']):
            raise argparse.ArgumentTypeError(f'{cred["key"]}: file does not exist')
        args.key = cred['key']
        args.user = cred['username']

    del args.sftp
    del args.credentials

    return args


##############################################################################
# Unattended selection and upload for the University of Liverpool scanner
##############################################################################


def scan_set_of_three(fpaths):
    """
    To be valid for uploading to the filestore, there should be a complete set
    of 3 vTile scans. Indicate if this is the case.

    --------------------------------------------------------------------------
    args
        fpaths : set of string
            Each string is expected to contain a path with a properly
            formatted filename as shown below
            (<qrcode>_<component>_<side>_<info>.extension).
            e.g.
            {
                '/Users/avt/scans/23090713000499001_vtile_sipm_out.tif',
                '/Users/avt/scans/23090713000499001_vtile_circuit_in.tif',
                '/Users/avt/scans/23090713000499001_vtile_sipm_in.tif',
            }
    --------------------------------------------------------------------------
    returns : boolean
        True if the complete set of 3 images
    --------------------------------------------------------------------------
    """
    expected_endings = {
        # inspection at arrival (inbound)
        # back-side components populated by BHAM
        'vtile_circuit_in': False,
        # inspection at arrival (inbound), front-side pads bare
        'vtile_sipm_in': False,
        # inspection before despatch (outbound)
        # front-side with SiPMs and wire bonds
        'vtile_sipm_out': False,
    }

    for fpath in fpaths:
        ending = os.path.splitext(os.path.basename(fpath))[0].partition('_')[-1]
        if ending in expected_endings:
            expected_endings[ending] = True

    return all(expected_endings.values())


def scan_incomplete_set_of_three(fpaths):
    """
    Make it easier to track down which QR code has missing scan(s).

    We don't care about the scenario where we have incoming scan(s), and no
    outgoing scan, because it means that a vTile has entered the production
    pipeline, but hasn't been completed yet.

    We do care if we have an outgoing scan (indicating the vTile is ready for
    despatch), but one or both of the incoming scans are missing. This
    function identifies these cases.

    --------------------------------------------------------------------------
    args
        fpaths : set of string
            Each string is expected to contain a path with a properly
            formatted filename as shown below
            (<qrcode>_<component>_<side>_<info>.extension).
            e.g.
            {
                '/Users/avt/scans/23090713000499001_vtile_sipm_out.tif',
                '/Users/avt/scans/23090713000499001_vtile_circuit_in.tif',
                '/Users/avt/scans/23090713000499001_vtile_sipm_in.tif',
            }
    --------------------------------------------------------------------------
    returns : boolean
        True if the complete set of 3 images
    --------------------------------------------------------------------------
    """
    expected_endings = {
        # inspection at arrival (inbound)
        # back-side components populated by BHAM
        'vtile_circuit_in': False,
        # inspection at arrival (inbound), front-side pads bare
        'vtile_sipm_in': False,
        # inspection before despatch (outbound)
        # front-side with SiPMs and wire bonds
        'vtile_sipm_out': False,
    }

    for fpath in fpaths:
        ending = os.path.splitext(os.path.basename(fpath))[0].partition('_')[-1]
        if ending in expected_endings:
            expected_endings[ending] = True

    vci = expected_endings['vtile_circuit_in']
    vsi = expected_endings['vtile_sipm_in']
    vso = expected_endings['vtile_sipm_out']

    return vso and (not vsi or not vci)


def limit_scans_for_upload(dbi, institute_id, image_files):
    """
    Filter the list of image_files to remove files related to any QR code
    already uploaded to the database, and to remove any files that are not in
    a full set of 3 (2 inbound scans, 1 outbound) per QR code.

    --------------------------------------------------------------------------
    args
        dbi : ds20kdb.interface.Database
        image_files : list of strings
            Each string is expected to contain a path with a properly
            formatted filename as shown below
            (<qrcode>_<component>_<side>_<info>.extension).
            e.g.
            [
                '/Users/avt/scans/23090713000499001_vtile_sipm_out.tif',
                '/Users/avt/scans/23090713000499001_vtile_circuit_in.tif',
                '/Users/avt/scans/23090713000499001_vtile_sipm_in.tif',
            ]
    --------------------------------------------------------------------------
    returns
        image_files : list
            no explicit return, mutable type amended in place
    --------------------------------------------------------------------------
    """
    dbi = interface.Database()

    ##########################################################################
    # get local files, and work out which have a full set of 3 images
    ##########################################################################

    files = collections.defaultdict(set)
    for image_file in image_files:
        qrcode = os.path.basename(image_file).partition('_')[0]
        if interface.qr_code_valid(qrcode):
            files[qrcode].add(image_file)

    valid_sets_of_scans = {
        qrc: file_set
        for qrc, file_set in files.items()
        if scan_set_of_three(file_set)
    }

    broken_sets_of_scans = {
        qrc: file_set
        for qrc, file_set in files.items()
        if scan_incomplete_set_of_three(file_set)
    }

    if not valid_sets_of_scans:
        print('No sets of three scans found')
        image_files.clear()
        return

    print(f'{len(valid_sets_of_scans)} sets of three scans per QR code')

    ##########################################################################
    # get records of which qrcodes have images uploaded to the database
    ##########################################################################

    # get liverpool's records
    dfr = dbi.get('vtile_test', institute_id=institute_id).data

    # scanned images will always have a non-null value for optical_inspection
    scan_image_db_records = dfr.dropna(subset=['optical_inspection'])

    vtile_ids_of_scanned_images_in_db = set(scan_image_db_records.vtile_id)

    lut = dbi.vtile_id_to_qrcode_lut()
    qrcodes_of_scanned_images_in_db = {
        lut[vtid]
        for vtid in vtile_ids_of_scanned_images_in_db
    }
    print(f'scans for {len(qrcodes_of_scanned_images_in_db)} QR code(s) found in database')

    qrcodes_to_process = valid_sets_of_scans.keys() - qrcodes_of_scanned_images_in_db
    if not qrcodes_to_process:
        print('No sets of three scans to upload')
        image_files.clear()
        return

    ##########################################################################
    # get records of which vtile_ids have images uploaded to the database
    ##########################################################################

    scans_to_be_uploaded = itertools.chain.from_iterable(
        file_set
        for qrc, file_set in valid_sets_of_scans.items()
        if qrc not in qrcodes_of_scanned_images_in_db
    )

    image_files[:] = list(scans_to_be_uploaded)

    print(f'\n{"#"*80}')
    print('Uploadable scans for QR codes:')
    for i, qrc in enumerate(qrcodes_from_filenames(image_files), start=1):
        print(f'{i:>3} : {qrc}')
    print(f'{"#"*80}\n')

    print(f'\n{"#"*80}')
    print('Sets of three with at least one missing inbound scan:')
    for qrc in broken_sets_of_scans:
        print(qrc)
    print(f'{"#"*80}\n')

    # give the user a chance to review information and/or terminate the script
    time.sleep(8)


def qrcodes_from_filenames(image_files):
    """
    Extract unique QR codes from file path list.

    --------------------------------------------------------------------------
    args
        image_files : list of strings
            Each string is expected to contain a path with a properly
            formatted filename as shown below
            (<qrcode>_<component>_<side>_<info>.extension).
            e.g.
            [
                '/Users/avt/scans/23090713000499001_vtile_sipm_out.tif',
                '/Users/avt/scans/23090713000499001_vtile_circuit_in.tif',
                '/Users/avt/scans/23090713000499001_vtile_sipm_in.tif',
            ]
    --------------------------------------------------------------------------
    returns : list of string
        e.g. ['23090713000530001', '23090713000541001', ...]
    --------------------------------------------------------------------------
    """
    qrcodes = {
        os.path.basename(image_file).partition('_')[0]
        for image_file in image_files
    }

    return interface.sort_qrcodes_by_serial_number(qrcodes)


def prefer_png_to_tiff(image_files):
    """
    Remove duplicate scans from the list of file, based solely on their
    filenames, preferring PNG to TIFF.

    This is done to ensure that more than one version of the same scan is not
    uploaded to the database, and PNG files are preferred since the script
    doesn't need to the convert TIFF to PNG before uploading. This is
    operation is performed since we may plausibly encounter an original TIFF
    scan and the PNG it was converted to in the same directory, by a previous
    run of the script.
    """
    def fnwe(filename):
        """ from a path, return its filename without the extension """
        return os.path.splitext(os.path.basename(filename))[0]

    def select_tiffs(filename_list):
        """
        Return every path that doesn't contain a PNG file.

        [
            '/Volumes/Untitled/23090713000480001_vtile_circuit_in.png',
            '/Volumes/Untitled/23090713000480001_vtile_circuit_in.tif',
        ]
        """
        # do we have a PNG file in the list?
        png_file_present = any(
            os.path.splitext(f)[-1].lower() == '.png' for f in filename_list
        )

        if png_file_present:
            return [
                f for f in filename_list
                if os.path.splitext(f)[-1].lower() != '.png'
            ]

        return []

    print(f'{len(image_files)} scans in directory')
    dupe_check = collections.defaultdict(list)

    for image_file in image_files:
        dupe_check[fnwe(image_file)].append(image_file)

    dupes = {k for k, v in dupe_check.items() if len(v) > 1}

    for d in dupes:
        a = select_tiffs(dupe_check[d])
        print(f'ignoring scan(s): {", ".join(a)}')
        for file in select_tiffs(dupe_check[d]):
            image_files.remove(file)

    print(f'{len(image_files)} scans after duplicate removal (prefer PNG to TIFF)')


##############################################################################
def main():
    """
    Uploads scanned images to the RHUL fileserver and creates matching
    database entries. Tested for vtile, but should also work for vpcb_asic,
    vmotherboard and vpdu.
    """
    # avoid warning messages from missing fields
    logging.getLogger().setLevel(logging.ERROR)

    # Handle large images from Manchester (14000 x 14000)
    Image.MAX_IMAGE_PIXELS = 196000000

    args = check_arguments()

    image_files = sorted(
        itertools.chain.from_iterable(
            glob.glob(os.path.join(args.directory, f'*.{extension}'))
            for extension in ['png', 'tif', 'tiff']
        )
    )

    # Avoid time-consuming image format conversions if the user has already
    # converted a TIFF to a PNG, and both TIFF and PNG files coexist.
    prefer_png_to_tiff(image_files)

    # prevent users uploading unsuitable files that were scanned incorrectly
    image_files = [
        f for f in image_files if image_dimensions_within_bounds(f)
    ]

    status = types.SimpleNamespace(success=0, unreserved_error_code=3)
    if not image_files:
        return status.unreserved_error_code

    dbi = interface.Database()

    try:
        response = dbi.get_institute_details(args.institute)
    except TypeError:
        return status.unreserved_error_code

    institute_details = response.data

    try:
        institute_id, _institute_text = institute_details
    except TypeError:
        return status.unreserved_error_code

    if args.unattended:
        limit_scans_for_upload(dbi, institute_id, image_files)

    if not image_files:
        return status.unreserved_error_code

    # ------------------------------------------------------------------------

    broken = collections.defaultdict(set)
    failure = []
    scan_count = 0
    with Connect(args) as ssh:
        if not ssh:
            image_files.clear()
            failure.append(True)

        for file in image_files:
            image_details = check_scanner_image_file(file)

            # Ignore this file if its filename is improperly formatted.
            if image_details is None:
                continue

            comp = Component(dbi, args, image_details, institute_details, ssh)

            print(comp)

            # Ideally, we would generate the table first, which lets us know
            # whether the device has reached the required level of assembly
            # according to the database. That way, it's possible to avoid
            # uploading an image or adding a database entry. For example,
            # this may fail if a vTile has been received at an assembly
            # institution but has not been entered on the database using
            # ds20k_submit_vtile.
            #
            # For the moment, we need to upload the image first to get the
            # optical inspection URL needed to generate the table.

            if comp.generate_table_for_db_post():
                comp.upload_image()
                if comp.optical_inspection is not None:
                    scan_count += 1
                else:
                    broken[file].add('filestore')

                if args.nodb:
                    print('database POST skipped')
                    failure.append(False)
                else:
                    post_failed = comp.post_table()
                    failure.append(post_failed)
                    if post_failed:
                        broken[file].add('database')
            else:
                print(f'Cannot upload {file}')
                broken[file].add('filestore')

    print('\n')
    print('-' * 80)
    print(f'    scans uploaded: {scan_count:>5}')
    print(f'db records created: {collections.Counter(failure)[False]:>5}')
    print('-' * 80)
    if broken:
        print('files with filestore/database issues:')
        for filename, reasons in broken.items():
            print(f'{filename}: {", ".join(sorted(reasons))}')
        print('-' * 80)

    # ------------------------------------------------------------------------

    if any(failure):
        return status.unreserved_error_code

    return status.success


##############################################################################
if __name__ == '__main__':
    sys.exit(main())
