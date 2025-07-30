#!/usr/bin/env python3
"""
Creates a file local to the end-user containing plain-text login credentials
for the DarkSide-20k pre-production database. This is just a convenience
command line tool in case users are uncomfortable with the interactive Python
interface.

You can achieve the same goal like this:

python3
>>> from ds20kdb import auth
>>> aif = auth.Authentication()
>>> aif.create_credentials_file()
"""

import argparse

from ds20kdb import auth


##############################################################################
# command line option handler
##############################################################################

def check_arguments():
    """
    Handle command line options.

    --------------------------------------------------------------------------
    args : none
    --------------------------------------------------------------------------
    returns argparse : argparse.Namespace
    --------------------------------------------------------------------------
    """
    parser = argparse.ArgumentParser(
        description='Creates a file local to the end-user containing\
        plain-text login credentials for the DarkSide-20k pre-production\
        database. The presence of this file is required for the database to\
        be used. Support requests to: Alan Taylor, Particle Physics,\
        University of Liverpool, avt@hep.ph.liv.ac.uk.'
    )
    parser.add_argument(
        '-f',
        '--force',
        action='store_true',
        help='Force the creation of the credentials file, even if a file\
        with valid credentials already exists.',
    )

    return parser.parse_args()


##############################################################################
def main():
    """
    Creates a file local to the end-user containing plain-text database
    login credentials.
    """
    args = check_arguments()

    auth_interface = auth.Authentication()
    auth_interface.create_credentials_file(args.force, verbose=False)


##############################################################################
if __name__ == '__main__':
    main()
