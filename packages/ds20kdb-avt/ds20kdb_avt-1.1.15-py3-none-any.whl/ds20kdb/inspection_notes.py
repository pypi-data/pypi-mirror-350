#!/usr/bin/env python3
"""
Supply SiPM inspection notes for a given vTile QR code.
"""

import argparse
import os
import pathlib
import sys
import types
import urllib
from urllib.parse import urlparse
from urllib.request import urlopen

import requests

from ds20kdb import common
from ds20kdb import interface
from ds20kdb import tray


##############################################################################
# command line option handler
##############################################################################

def check_qr(value):
    """
    Check if the QR code complies with the DarkSide-20k format.
    """
    if interface.qr_code_valid(value):
        return value
    else:
        raise argparse.ArgumentTypeError(f'invalid QR code ({value})')

def check_resource(value):
    """
    This could be a local directory or a URL.
    """
    try:
        reply = requests.head(value, allow_redirects=True)
    except requests.exceptions.MissingSchema:
        # probably not a URL, perhaps a directory
        directory = pathlib.Path(value)
        if directory.is_dir():
            return directory
        else:
            raise argparse.ArgumentTypeError(f'unknown resource 1 ({value})')
    else:
        if reply.status_code == 200:
            return urlparse(value)
        else:
            raise argparse.ArgumentTypeError(f'unknown resource 2 ({value})')

def check_arguments():
    """
    handle command line options

    --------------------------------------------------------------------------
    args : none
    --------------------------------------------------------------------------
    returns : none
    --------------------------------------------------------------------------
    """
    parser = argparse.ArgumentParser(
        description='Supply SiPM inspection notes for a given vTile QR code.'
    )
    parser.add_argument(
        'qrcode',
        nargs=1,
        metavar='qrcode',
        help='vTile QR code.',
        type=check_qr,
    )

    parser.add_argument(
        '-r', '--repository', nargs='+', metavar='repository',
        help=(
            'One or more repositories from which to fetch tray files. E.g. '
            '"https://gitlab.ph.liv.ac.uk/avt/ds20k/-/blob/main/wafers/". '
            'Beyond that link, a particular directory structure is expected '
            '<wafer_lot_numnber>/<wafer_number> where the wafer_number is '
            'zero-padded, E.g. "9346469/22/". In those directories, the '
            'script will expect to find "tray files" with .txt extensions.'
            'These tray files describe the content of a 24-capacity tray of '
            'SiPMs. Other files will be ignored.' 
        ),
        type=check_resource,
        default=['https://gitlab.ph.liv.ac.uk/avt/ds20k/-/blob/main/wafers/'],
    )
 
    args = parser.parse_args()
    args.repository = set(args.repository)

    return args


##############################################################################
# main
##############################################################################

def main():
    """
    Generate a wafer map suitable for picking good SiPMs from a wafer using a
    die ejector, such that they may be transferred to trays and later
    installed onto vTiles.
    """
    args = check_arguments()
    print(args)

    status = types.SimpleNamespace(success=0, unreserved_error_code=3)

    # dbi = interface.Database()

    return status.success


##############################################################################
if __name__ == '__main__':
    sys.exit(main())
