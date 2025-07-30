#!/usr/bin/env python3
"""
Generate a wafer map suitable for picking good SiPMs from a wafer, such that
they may be transferred to trays and later installed onto vTiles.
"""

import argparse
import sys
import types

try:
    from ds20kdb import visual
except ModuleNotFoundError:
    print('Please install ds20kdb-avt')
    sys.exit(3)
except ImportError:
    print('Please upgrade to the latest ds20kdb-avt version')
    sys.exit(3)
else:
    from ds20kdb import interface

from ds20kdb import common


##############################################################################
# command line option handler
##############################################################################


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
        description='Generate a wafer map suitable for picking good SiPMs\
        from a wafer using a die ejector, such that they may be transferred\
        to trays and later installed onto tiles. The default behaviour when\
        identifying good/bad SiPMs is to perform a comprehensive check for\
        sipm_test.classification==\'good\' and sipm_test.quality_flag==0,\
        where only the row with the largest value of sipm_test.sipm_qc_id is\
        considered. Colour key: green, good device; red, do not use for\
        production; yellow, functional device with acceptable but borderline\
        performance. Support requests to: Alan Taylor, Dept. of Physics,\
        University of Liverpool, avt@hep.ph.liv.ac.uk.')
    parser.add_argument(
        'lot', nargs=1, metavar='lot',
        help='Wafer lot number, e.g. 9346509',
        type=int)
    parser.add_argument(
        'wafer_number', nargs=1, metavar='wafer_number',
        help='Wafer number.',
        type=int)

    parser.add_argument(
        '-s', '--sequential',
        action='store_true',
        help='DEBUG OPTION. Access the database sequentially when performing\
        a comprehensive check for SiPM good/bad status, this may take\
        approximately one minute to complete. This option may be useful if the\
        database is under considerable load.'
    )

    parser.add_argument(
        '-b', '--nobgradecheck',
        action='store_true',
        help='Do not generate wafer maps that indicate notionally B-grade\
        SiPMs (those at the margins of acceptable performance). This option\
        only applies for non-classification checks.'
    )
    parser.add_argument(
        '-n', '--nounusablesipmcheck',
        action='store_true',
        help='DEBUG OPTION. Ignore unusable_sipm table when generating wafer map.'
    )
    parser.add_argument(
        '-q', '--qcid', nargs=1, metavar='qcid',
        help='DEBUG OPTION. Specify sipm_qc_id to use. The default is to use\
        the most recent for the given sipm_pid from table sipm_test.',
        type=int, default=None,
    )

    args = parser.parse_args()

    try:
        qcid = args.qcid[0]
    except TypeError:
        qcid = args.qcid

    return args.lot[0], args.wafer_number[0], args.sequential, args.nobgradecheck, qcid, args.nounusablesipmcheck


##############################################################################
# main
##############################################################################

def main():
    """
    Generate a wafer map suitable for picking good SiPMs from a wafer using a
    die ejector, such that they may be transferred to trays and later
    installed onto vTiles.
    """
    lot, wafer_number, sequential, no_b_grade, qcid, nounusablesipmcheck = check_arguments()

    status = types.SimpleNamespace(success=0, unreserved_error_code=3)

    dbi = interface.Database()

    print(f'looking up {lot}.{wafer_number:02}')
    try:
        wafer_pid = int(
            dbi.get('wafer', lot=lot, wafer_number=wafer_number).data.wafer_pid.values[0]
        )
    except AttributeError:
        print('Check Internet connection')
        return status.unreserved_error_code
    except IndexError:
        print('Wafer may not exist in the database')
        return status.unreserved_error_code
    except TypeError:
        print(f'No response from the database for {lot}.{wafer_number:02}')
        return status.unreserved_error_code

    print(f'PID {wafer_pid}')

    ##########################################################################
    # obtain (col, row) locations for good/bad SiPMs

    print('Obtaining SiPMs for this wafer')
    try:
        wafer_map_good, wafer_map_b_grade, wafer_map_bad = common.identify_sipm_status(
            dbi, wafer_pid, sequential, no_b_grade, qcid, nounusablesipmcheck
        )
    except TypeError:
        print('Unable to create wafer map')
        return status.unreserved_error_code

    lgreen = len(wafer_map_good)
    lyellow = len(wafer_map_b_grade)
    lred = len(wafer_map_bad)
    print(
        f'green {lgreen}, yellow {lyellow}, red {lred}, '
        f'all {lgreen + lyellow + lred}'
    )

    ##########################################################################
    # draw wafer

    print('Saving wafer map')
    sipm_groups = [
        {
            'name': 'good',
            'locations': wafer_map_good,
            'sipm_colour': 'green',
            'text_colour': 'black',
        },
        {
            'name': 'bad_lfoundry-visual_noa-cryoprobe',
            'locations': wafer_map_bad,
            'sipm_colour': 'darkred',
            'text_colour': 'lightgrey',
        },
        {
            'name': 'bad_noa-test-stats',
            'locations': wafer_map_b_grade,
            'sipm_colour': 'darkgoldenrod',
            'text_colour': 'black',
        },
    ]

    visual.DrawWafer(
        wafer_lot=lot,
        wafer_number=wafer_number,
        sipm_groups=sipm_groups
    ).save()

    return status.success


##############################################################################
if __name__ == '__main__':
    sys.exit(main())
