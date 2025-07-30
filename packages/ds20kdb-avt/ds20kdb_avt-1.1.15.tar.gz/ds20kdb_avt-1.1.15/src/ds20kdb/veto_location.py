#!/usr/bin/env python3
"""
For the given QR code, this script determines the most manufactured state of
the item identified by the QR code, and updates its location and status with
the date and time the script is run.

Based on the original script by P.Franchini - p.franchini@lancaster.ac.uk
Available at:

    https://gitlab.in2p3.fr/darkside/productiondb_software/-/
            blob/master/examples_python/veto_location/veto_location_GUI.py
"""

import argparse
import datetime
import functools
import sys
import time
import types

from ds20kdb import interface


##############################################################################
# command line option handler
##############################################################################


def check_datetime(value):
    """
    Converts current date/time into a string in UTC to the nearest second.

    e.g. 1668688788.970397 converts to '2022-11-17 12:39:48'

    The DarkSide-20k database requires UTC date/time in this format:

    YYYY-MM-DD hh:mm:ss, e.g. 2022-07-19 07:00:00

    --------------------------------------------------------------------------
    args
        tref : float
            time in seconds since the epoch
    --------------------------------------------------------------------------
    returns : string
    --------------------------------------------------------------------------
    """
    try:
        dti = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f'valid date/time in format YYYY-MM-DD HH:MM:SS required, received ({value})'
        ) from exc

    return dti.strftime('%Y-%m-%d %H:%M:%S')


def check_institute_string(dbi, institute):
    """
    Check if institute search has a match in the database, if so, return its ID
    """
    response = dbi.get_institute_id(institute)
    if response.network_timeout:
        raise argparse.ArgumentTypeError(
            'timeout when trying to obtain institute_id'
        )
    if response.data is None:
        raise argparse.ArgumentTypeError(
            f'search term "{institute}"" not found in database'
        )

    return response.data


def check_qrcode(qrcode):
    """
    Check whether the QR code supplied is formatted correctly. No check is
    made to confirm its existence in the database.
    """
    if not interface.qr_code_valid(qrcode):
        raise argparse.ArgumentTypeError(f'{qrcode}: invalid QR-code')

    return qrcode


def check_qrcodes(filename):
    """
    Check QR codes
    """
    good = set()
    bad = set()

    with open(filename, encoding='utf-8') as file:
        for line in file:
            qrc = line.strip()

            if interface.qr_code_valid(qrc):
                good.add(qrc)
            else:
                bad.add(qrc)

    if bad:
        raise argparse.ArgumentTypeError(
            f'malformed QR code(s) in file: {", ".join(bad)}'
        )

    return good


def check_arguments(dbi):
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
            'For the given QR code, this script determines the most\
            manufactured state of the item identified by the QR code, and\
            updates its location and status with the date and time the script\
            was run. Supported items: vpcb, vpcb_asic, vtile, vmotherboard,\
            vpdu.'
        )
    )
    parser.add_argument(
        'status', nargs=1, metavar='status',
        help=(
            'Status of object:\
            "received";\
            "unbagged", object removed from sealed bags and exposed to atmosphere;\
            "tested", tests and measurements performed and finished;\
            "bagged", object in sealed bags;\
            "shipped", object collected by a courier for shipment;\
            "produced", production terminated on the object;\
            "stored", object in storage;\
            "integrated", object installed (vTile on vPDU, vPDU in the detector);\
            "damaged", object damaged so unusable, waiting for a possible repair;\
            "reworked", object repaired so fully usable;\
            "scrapped", object removed from production, never to be integrated;'
        ),
        choices=[
            'received', 'unbagged', 'tested', 'bagged', 'shipped',
            'produced', 'stored', 'integrated', 'damaged', 'reworked','scrapped'
        ],
        type=str
    )
    parser.add_argument(
        'institute', nargs=1, metavar='institute',
        help=(
            'Searchable name of the institute in lowercase\
            (e.g. genova, ral, liverpool, noa-smu, ...). This will be used to\
            obtain the ID of the institute in the database.'
        ),
        type=functools.partial(check_institute_string, dbi)
    )

    group1 = parser.add_mutually_exclusive_group()
    group1.add_argument(
        '-q', '--qrcode', nargs=1, metavar='qrcode',
        help='17-digit QR code of object', type=check_qrcode
    )
    group1.add_argument(
        '-f', '--file', nargs=1, metavar='file',
        help='File containing one 17-digit QR code per line', type=check_qrcodes
    )

    parser.add_argument(
        '-c', '--comment', nargs=1, metavar='comment',
        help=(
            'Optional comment to document anything notable about the batch.'
        ),
        type=str, default=['']
    )
    parser.add_argument(
        '-d', '--datetime', nargs=1, metavar='datetime',
        help=(
            'Optional UTC date and time of location change. Expects format\
            YYYY-MM-YY HH:MM:SS. If omitted, the current date and time is\
            used.'
        ),
        type=check_datetime,
        default=datetime.datetime.fromtimestamp(
            time.time(),
            datetime.timezone.utc
        ).isoformat().split('.')[0].replace('T', ' ')
    )
    parser.add_argument(
        '-w',
        '--write',
        action='store_true',
        help='By default - for safety - this script will write NOTHING to\
        the database. This option allows data writes to occur.',
    )

    args = parser.parse_args()

    if args.qrcode:
        args.qrcode = args.qrcode
    else:
        args.qrcode = args.file[0]
        del args.file

    args.status = args.status[0]
    args.institute = args.institute[0]
    args.comment = args.comment[0]

    return args


##############################################################################
# data structures
##############################################################################


class Object:
    """
    Container for a DarkSide-20k object, and entry of its location in the
    database.
    """
    def __init__(self, dbi, args, qrcode):
        self.dbi = dbi
        self.institute_id = args.institute
        self.timestamp = args.datetime
        self.status = args.status
        self.qrcode = qrcode
        self.comment = args.comment
        self.write = args.write

    def __str__(self):
        items = [
            '-' * 40,
            self.timestamp,
            self.status,
            self.qrcode,
            self.comment,
            self.write,
            '-' * 40
        ]
        return '\n'.join(map(str, items))

    def _get_highest_level_object(self):
        """
        Several objects progress through various stages of assembly throughout
        the production process. Identify the most recent stage of completed
        assembly.

        ----------------------------------------------------------------------
        args
            qrcode : string
                17-digit numeric
        ----------------------------------------------------------------------
        returns
            obj : string
                Object name, database table
            parameter :
                QR code or object ID
        ----------------------------------------------------------------------
        """
        part_number = int(self.qrcode[-3:])

        part_hierarchies = {
            # build progression: vpcb -> vpcb_asic -> vtile
            1: [
                ('vpcb', 'qrcode', 'vpcb_pid'),
                ('vpcb_asic', 'vpcb_id', 'vpcb_asic_pid'),
                ('vtile', 'vpcb_asic_id', 'vtile_pid'),
            ],
            # build progression: vmotherboard -> vpdu
            2: [
                ('vmotherboard', 'qrcode', 'vmotherboard_pid'),
                ('vpdu', 'vmotherboard_id', 'vpdu_pid'),
            ],
        }

        obj = None
        parameter = self.qrcode

        try:
            part_hierarchy = part_hierarchies[part_number]
        except KeyError:
            return obj, parameter

        for test_object, key, select in part_hierarchy:
            try:
                tmp_id = self.dbi.get(
                    test_object, **{key: parameter}
                ).data[select].iloc[-1]
            except (KeyError, IndexError):
                break
            else:
                if not tmp_id:
                    break

                obj = test_object
                parameter = tmp_id

        return obj, parameter

    def submit_command(self):
        """
        Submit information to database.
        """

        # check QR code: identify the most manufactured form of the object
        obj, parameter = self._get_highest_level_object()
        if obj is None:
            print('could not identify object')
            # if status:
            #     print(status)

            return False

        # Post the table
        table = {
            f'{obj}_id': parameter,
            'institute_id': int(self.institute_id),
            'timestamp': self.timestamp,
            'comment': self.comment,
            'state': self.status,
        }

        if not self.write:
            print(
                'Use the --write command line option to enable database '
                'writes.\n'
            )
            return False

        post_successful = self.dbi.post_item(table, f'{obj}_location')

        if post_successful:
            print(f'POST succeeded: {obj} {self.qrcode}')
            return True

        print('POST failed')
        return False


##############################################################################
def main():
    """
    For the given QR code, this script determines the most manufactured state
    of the item identified by the QR code, and updates its location and
    status with the date and time the script is run.
    """
    status = types.SimpleNamespace(success=0, unreserved_error_code=3)
    dbi = interface.Database()

    args = check_arguments(dbi)

    # explicitly create the list so all submissions are processed
    success = all(
        [
            Object(dbi, args, qrcode).submit_command()
            for qrcode in args.qrcode
        ]
    )

    # If any of the database POST operations failed, return a failure code
    return status.success if success else status.unreserved_error_code


##############################################################################
if __name__ == '__main__':
    sys.exit(main())
