#!/usr/bin/env python3
"""
Generate a sequence of QR code images suitable for the EMS200, tailored to
the pad size of the device to be etched.
"""

import argparse
import concurrent.futures as cf
import datetime
import functools
import os


##############################################################################
# command line option handler
##############################################################################

def check_version_range(val):
    """
    Check that the schematic version number is within the acceptable range.
    """
    val = float(val)
    if not 0.0 <= val <= 9.9:
        raise argparse.ArgumentTypeError(
            f'{val}: '
            'Schematic version number must be between 0.0 and 9.9')
    return val


def check_arguments():
    """
    Handle command line options.

    --------------------------------------------------------------------------
    args : none
    --------------------------------------------------------------------------
    returns : dict
    --------------------------------------------------------------------------
    """
    parser = argparse.ArgumentParser(
        description='Generate QR-codes for the DarkSide-20k project.\
        This script requires ImageMagick and qrencode to be available on the\
        command line. Support requests to: Alan Taylor, Dept. of Physics,\
        University of Liverpool, avt@hep.ph.liv.ac.uk.')

    parser.add_argument(
        'start_serial',
        nargs=1,
        metavar='start_serial',
        help='Serial number of first device in the sequence.',
        type=int,
    )

    # The user should specify either the end serial number or the number of
    # qrcodes to generate.

    group1 = parser.add_mutually_exclusive_group(required=True)
    group1.add_argument(
        '-e', '--end',
        nargs=1,
        metavar='end_serial',
        help='Serial number of last device in the sequence.',
        type=int,
        default=None,
    )
    group1.add_argument(
        '-n', '--number',
        nargs=1,
        metavar='number',
        help='Number of qrcodes to generate.',
        type=int,
        default=None,
    )

    # Generate QR-codes for one type of device only.

    group2 = parser.add_mutually_exclusive_group(required=True)
    group2.add_argument(
        '--tt', '--tile',
        action='store_true',
        help='Generate QR-code(s) for TPC tile(s).',
    )
    group2.add_argument(
        '--tm', '--motherboard',
        action='store_true',
        help='Generate QR-code(s) for TPC motherboard(s).',
    )
    group2.add_argument(
        '--vt', '--vtile',
        action='store_true',
        help='Generate QR-code(s) for VETO tile(s).',
    )
    group2.add_argument(
        '--vm', '--vmotherboard',
        action='store_true',
        help='Generate QR-code(s) for VETO motherboard(s).',
    )

    parser.add_argument(
        '-v', '--version',
        nargs=1,
        metavar='version',
        help='PCB schematic version number, e.g. 3.0',
        type=check_version_range,
        required=True,
    )

    parser.add_argument(
        '-p', '--production',
        action='store_true',
        help=(
            'Production flag. Use this option if the devices are intended '
            'for production use. Omit this flag for pre-production.'
        ),
    )

    return process_args(parser.parse_args())


def process_args(args):
    """
    Basic processing of command line arguments.
    """
    settings = {}

    end_serial = args.end[0] + 1 if args.end else args.start_serial[0] + args.number[0]
    settings['serial_numbers'] = list(range(args.start_serial[0], end_serial))

    object_type = {
        pcb_type
        for pcb_type, active in vars(args).items()
        if pcb_type in {'tt', 'tm', 'vt', 'vm'} and active
    }
    device_info = {
        'tt': (8, 14, 3, 'tpc_tile'),
        'tm': (12, 20, 4, 'tpc_mb'),
        'vt': (10, 10, 1, 'veto_tile'),
        'vm': (12, 20, 2, 'veto_mb'),
    }

    width, height, part, file_prefix = device_info[next(iter(object_type))]

    settings['min_pad_dimension'] = min(width, height)
    settings['part_number'] = part
    settings['production'] = int(args.production)
    settings['version'] = f'{int(args.version[0] * 10):02}'
    settings['file_prefix'] = file_prefix

    return settings


##############################################################################
# utilities
##############################################################################

def convert_format(prefix, qrcode):
    """
    Convert file: PNG to BMP.
    """
    os.system(f'convert {prefix}_{qrcode}.png {prefix}_{qrcode}.bmp')


##############################################################################
def main():
    """
    Generate a sequence of QR code images suitable for the EMS200, tailored to
    the pad size of the device to be etched.
    """
    settings = check_arguments()

    if not settings['serial_numbers']:
        return

    ##########################################################################
    # QR-code geometry
    ##########################################################################

    pixel_width = 10
    qr_width = 21
    border = 3

    ##########################################################################
    # Compute DPI required to get correct physical size
    ##########################################################################

    target_size_mm = settings['min_pad_dimension']
    qr_dpi = pixel_width * (qr_width + (border * 2)) * (25.4 / target_size_mm)

    print(
        f'pixel_width {pixel_width}, qr_width {qr_width}, '
        f'border {border}, qr_dpi {qr_dpi}'
    )

    ##########################################################################
    # Generate QR code images
    ##########################################################################

    date = f'{datetime.datetime.now(datetime.timezone.utc):%y%m%d}'

    prod = settings['production']
    vers = settings['version']
    partno = settings['part_number']
    # part number size (number of digits)
    pns = 3
    # serial number size (number of digits)
    sns = 5

    start_serial, end_serial = min(settings['serial_numbers']), max(settings['serial_numbers'])

    num_qr = end_serial - start_serial + 1

    print(
        f'start_serial {start_serial}, '
        f'end_serial {end_serial}, '
        f'(quantity {num_qr})',
    )

    qrcodes = [
        f'{date}{prod}{vers}{s:>0{sns}}{partno:>0{pns}}'
        for s in settings['serial_numbers']
    ]

    # Square QR code images will be 270x270, and 270x332 once text has been
    # added. Without changing the resolution, change the physical size of the
    # final image.
    density = int(2700 / target_size_mm)

    prefix = settings['file_prefix']

    commands = (
        (
            # create QR-code
            f'qrencode --dpi={qr_dpi} --margin={border} --size={pixel_width} '
            f'--level=H -o {qrcode}.png {qrcode};'
            # combine QR-code and serial number to form new image
            f'convert {qrcode}.png -background white -font Helvetica '
            f'-pointsize 60 +antialias caption:{int(qrcode[9:14])} '
            '-gravity Center -set units PixelsPerCentimeter '
            f'-set density {density} -append {prefix}_{qrcode}.png'
        )
        for qrcode in qrcodes
    )

    # generate qrcode images as PNG files, then add text
    with cf.ProcessPoolExecutor() as executor:
        executor.map(os.system, commands)

    # convert PNG to BMP which the EMS200 software prefers
    # dependency: ImageMagick
    convert = functools.partial(convert_format, prefix)
    with cf.ProcessPoolExecutor() as executor:
        executor.map(convert, qrcodes)


##############################################################################
if __name__ == '__main__':
    main()
