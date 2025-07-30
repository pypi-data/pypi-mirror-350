#!/usr/bin/env python3
"""
GUI for POSTing new/repaired DarkSide-20k vTiles to the production database.

FIXME: some dicts use key 'lot' others use 'lot_number': unify these instances
FIXME: unify ordering to (column, row, lot, wafer_number)
FIXME: class Gui should maintain a list of SiPMs, also add __slots__
"""

import collections
import contextlib
import datetime
from enum import IntEnum
import functools
import itertools
import json
import logging
import math
import os
import platform
import re
import sys
import time
import webbrowser
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import font

from dateutil.parser import parse

from ds20kdb import interface
from ds20kdb import common
from ds20kdb import constants

# Python 3.6 EOL 2023-06-27
# Python 3.7 EOL 2021-12-23
# https://devguide.python.org/versions/
#
# required here: = functools.cached_property decorator
assert sys.version_info >= (3, 8), 'Python 3.8 or later requried'

# required here: interface.sort_qrcodes_by_serial_number()
# v1.0.26, 12 May 2024
assert tuple(
    # remove alpha/beta suffix from version: 1.1a0 becomes 1.1
    int(''.join(itertools.takewhile(lambda v: v.isdigit(), x)))
    for x in interface.__version__.split('.')
) >= (1, 0, 26), (
    'ds20kdb 1.0.26 or newer required '
    f'(found {interface.__version__})'
)

##############################################################################
# data structures
#
# Since users may request the validity of their data to be checked against the
# database more than once per vTile submission, these database enquiries
# are cached. This reduces database traffic and provide a more responsive
# experience for the user.
#
# Caching is performed outside the class definition to allow it to occur
# across all SiPMs.
##############################################################################


# Disable database writes with DEBUG = True
DEBUG = False


# Do not allow field 'version' to be used in table 'vtile'
# if VTILE_REPAIR = False. Internally, class Gui will still keep track of
# vtile versions.
VTILE_REPAIR = True


@functools.lru_cache(maxsize=64)
def get_wafer_pid_wrapper(dbi, lot_number, wafer_number):
    """ Cache wrapper """
    return dbi.get_wafer_pid(lot_number, wafer_number).data


@functools.lru_cache(maxsize=128)
def get_sipm_pid_wrapper(dbi, wafer_pid, column, row):
    """ Cache wrapper """
    return dbi.get_sipm_pid(wafer_pid, column, row)


class SiPM:
    """
    Basic data container used for SiPMs.

    This requires network access.
    """
    __slots__ = {
        'dbi': 'ds20kdb.interface.Database instance, used for db interaction',
        'lot_number': 'Wafer lot number, 7-digits, e.g. 9306869',
        'wafer_number': 'Wafer number, 1-2 digits in the range 1-25',
        'column': 'Physical location of this SiPM on the wafer',
        'row': 'Physical location of this SiPM on the wafer',
        'wafer_pid': 'Database PID of the wafer this SiPM came from',
        'sipm_pid': 'Database PID of this SiPM',
    }

    def __init__(self, dbi, column, row, lot_number, wafer_number):
        self.dbi = dbi
        self.lot_number = lot_number
        self.wafer_number = wafer_number
        self.column = column
        self.row = row
        self.wafer_pid = get_wafer_pid_wrapper(
            dbi, lot_number, wafer_number
        )
        self.sipm_pid = get_sipm_pid_wrapper(
            dbi, self.wafer_pid, column, row
        )

    def __repr__(self):
        return (
            'SiPM('
            f'dbi={self.dbi}, '
            f'lot_number={self.lot_number}, '
            f'wafer_number={self.wafer_number}, '
            f'column={self.column}, '
            f'row={self.row})'
        )

    def __str__(self):
        contents = {
            'lot number': self.lot_number,
            'wafer number': self.wafer_number,
            'SiPM column': self.column,
            'SiPM row': self.row,
            'wafer PID': self.wafer_pid,
            'SiPM PID': self.sipm_pid,
        }
        return ', '.join(f'{k}={v:>3}' for k, v in contents.items())


##############################################################################
# GUI data structures
#
# Principally used for setting of default conditions
##############################################################################


class ButtonSubmit(tk.Button):
    """ Button: only used for the submit button """

    def set_default(self):
        """ Set default state """
        self.configure(state=tk.DISABLED)


class ColourLabel(ttk.Label):
    """ Label: used for all labels """

    def set_default(self):
        """ Set default state """
        self.configure(foreground='black')


class SipmLotNum(ttk.Combobox):
    """ Drop-down menu: used for the wafer's lot number only """

    def set_default(self):
        """ Set default state """
        self.set('lot')


class SipmWaferNum(ttk.Combobox):
    """ Drop-down menu: used for the wafer number only """

    def set_default(self):
        """ Set default state """
        self.set('wafer')


class SipmColumn(ttk.Combobox):
    """ Drop-down menu: used for SiPM column numbers """

    def set_default(self):
        """ Set default state """
        self.set('col')


class SipmRow(ttk.Combobox):
    """ Drop-down menu: used for SiPM row numbers """

    def set_default(self):
        """ Set default state """
        self.set('row')


class Solder(ttk.Combobox):
    """
    Drop-down menu: used for the 4 supplemental items:

    Institute, solder syringe PID, QR code, production run number
    """
    def set_default(self):
        """ Set default state """
        self.set('')
        self.configure(values=[])


class Supplemental(ttk.Combobox):
    """
    Drop-down menu: used for the 4 supplemental items:

    Institute, solder syringe PID, QR code, production run number
    """
    def set_default(self):
        """ Set default state """
        self.set('')


# Widget type
Itype = IntEnum('Itype', ['BUTTON', 'COMBOBOX', 'LABEL', 'TEXT'])

# Cluster type
Cluster = IntEnum(
    'Cluster',
    [
        'COMMENT',
        'CONSOLE',
        'INSTITUTE',
        'PRODUCTION_DATE',
        'QRCODE',
        'RUN_NUMBER',
        'SOLDER_ID',
        'SUBMIT',
        'SIPM_01',
        'SIPM_02',
        'SIPM_03',
        'SIPM_04',
        'SIPM_05',
        'SIPM_06',
        'SIPM_07',
        'SIPM_08',
        'SIPM_09',
        'SIPM_10',
        'SIPM_11',
        'SIPM_12',
        'SIPM_13',
        'SIPM_14',
        'SIPM_15',
        'SIPM_16',
        'SIPM_17',
        'SIPM_18',
        'SIPM_19',
        'SIPM_20',
        'SIPM_21',
        'SIPM_22',
        'SIPM_23',
        'SIPM_24',
    ]
)


class Widget:
    """
    Generic container for tkinter widgets.
    """
    __slots__ = {
        'instance': 'Instance of the tkinter widget.',
        'itype': (
            'This is the widget type, which may be one of these four: '
            'button, combobox (drop-down menu), label (text label), and '
            'text (console area). Integer values from IntEnum.'
        ),
        'cluster': (
            'The cluster represents an umbrella under which a group of '
            'categories may be placed. The cluster names are: console, '
            'institute, production_date, qrcode, run_number, sipm_N (where N '
            'is a value between 1 and 24 inclusive), and solder_id. '
            'Only production_date and sipm_N have multiple categories. '
            'production_date has categories of year, month, day, hour and '
            'minute. sipm_N has categories of lot_number, wafer_number, '
            'column, and row.'
        ),
        'category': 'E.g. lot, label',
    }

    def __init__(self, instance, itype, cluster, category):
        self.instance = instance
        self.itype = itype
        self.cluster = cluster
        self.category = category


class Gui:
    """
    Construct/operate GUI.
    """
    # window extents
    # main
    root_w = 1024
    root_h = 584
    # about pop-up
    about_w = 320
    about_h = 200
    # solder syringe pop-up
    solder_w = 640
    solder_h = 576
    # import vTile from database pop-up
    import_w = 320
    import_h = 128

    outer_split = 8
    base_title_text = 'DarkSide-20k POST vTile'

    # values for GUI drop-down boxes
    dt_range = {
        'years': list(range(2022, 2033)),
        'months': list(range(1, 13)),
        'days': list(range(1, 32)),
        'hours': list(range(0, 24)),
        'minutes': list(range(0, 60, 15)),
    }

    try:
        dbi = interface.Database()
    except AssertionError:
        sys.exit()

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry(f'{self.root_w}x{self.root_h}+0+0')
        self.root.title(self.base_title_text)
        self.root.resizable(False, False)

        self.frame = {}
        self.table_json = {}
        self.widgets = []
        self.table_json_string = None
        self.version = 1

        self.session_timestamp = timestamp_to_utc(time.time())
        self.wafer_table_dataframe = self.database_alive()

        self.valid_locations = set(interface.wafer_map_valid_locations())

        self.strict_solder_syringe_checking = tk.BooleanVar()
        self.strict_solder_syringe_checking.set(True)

        self.repair_mode = tk.BooleanVar()
        self.repair_mode.set(False)
        self.repair_row_sipms = {}
        self.repair_sipm_location_to_id_lut = {}

        # QR code combobox from the Import vTile from database popup
        self.qrcode_combobox_repair = None

        ######################################################################
        # platform specific items related to detecting paste, font handling
        ######################################################################

        self.system = platform.system()

        default_fonts = [
            # labelframe, label
            font.nametofont('TkDefaultFont'),
            # combobox
            font.nametofont('TkTextFont'),
            # entry (console)
            font.nametofont('TkFixedFont'),
            # menu bar
            font.nametofont('TkMenuFont'),
        ]

        for dfont in default_fonts:
            self.amend_font(dfont)

        ######################################################################
        # Location of file from which to load/save GUI combobox default values
        # on application start.
        ######################################################################

        self.defaults_filename = '.ds20kdb_defaults'
        self.defaults_tray_filename = '.ds20kdb_tray_defaults'
        self.home_directory = os.path.expanduser('~')
        self.defaults_file_path = os.path.join(
            self.home_directory, self.defaults_filename
        )
        self.defaults_tray_file_path = os.path.join(
            self.home_directory, self.defaults_tray_filename
        )
        self.tray_file_directory = self.home_directory

        # build GUI

        self.populate_window_with_frames()

        self.populate_console_frame()
        self.populate_menu_bar()
        self.populate_sipm_frame()
        self.populate_supplemental_frame()
        self.populate_production_date_frame()
        self.populate_action_button_frame()

        self.load_defaults()

        self.root.focus_force()

    def run(self):
        """
        Run GUI.

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns : none
        ----------------------------------------------------------------------
        """
        self.root.mainloop()

    ##########################################################################
    # Platform-specific font handling
    ##########################################################################

    @staticmethod
    def amend_font(tkf):
        """
        Amend font size if it will limit visibility.

        Windows 10:
            {'family': 'Segoe UI', 'size': 9, ...}
            {'family': 'Courier New', 'size': 10, ...}

        Ubuntu 22.04, Pop!_OS 22.04, CentOS 7 (size=0):
            {'family': 'DejaVu Sans', 'size': 10, ...}
            {'family': 'DejaVu Sans Mono', 'size': 10, ...}

        Raspberry Pi OS (RPi4, bullseye):
            {'family': 'Bitstream Vera Sans', 'size': 10, ...}
            {'family': 'Liberation Mono', 'size': 10, ...}

        Raspberry Pi OS (RPi5, bookworm):
            {'family': 'Noto Sans', 'size': 10, ...}
            {'family': 'Liberation Mono', 'size': 10, ...}

        macOS Ventura:
            {'family': 'Verdana', 'size': 9, ...}
            {'family': 'Andale Mono', 'size': 9, ...}

        macOS Sequoia:
            {'family': '.AppleSystemUIFont', 'size': 13, ...}
            # no need to change the scaling for Menlo
            {'family': 'Menlo', 'size': 11, ...}

        ----------------------------------------------------------------------
        args
            tkf : <class 'tkinter.font.Font'>
        ----------------------------------------------------------------------
        returns : none
            GUI state changed
        ----------------------------------------------------------------------
        """
        font_list = {
            'Noto Sans': 9,
            'Liberation Mono': 9,
            'Courier New': 9,
            'DejaVu Sans Mono': 9,
            'Menlo': 11,
            '.AppleSystemUIFont': 10,
        }
        details = tkf.actual()
        try:
            fsize = font_list[details['family']]
        except KeyError:
            pass
        else:
            if details['family'] in font_list and details['size'] > fsize:
                tkf.configure(size=fsize)

    ##########################################################################
    # Build the GUI interface (main window areas)
    ##########################################################################

    def populate_window_with_frames(self):
        """
        Populate the main GUI window with labelled frames.

        --------------------------------------------------------------------------
        args
            root : tk.Tk
                The top-level Tk widget for the main GUI window
            frame : dict
                {<frame_name>: <tk.LabelFrame>, ...}
        --------------------------------------------------------------------------
        returns
            frame : dict
                {<frame_name>: <tk.LabelFrame>, ...}
                no explicit return, mutable type amended in place
        --------------------------------------------------------------------------
        """
        # SiPMs

        self.frame['sipm'] = tk.LabelFrame(
            self.root,
            width=self.root_w,
            height=264,
            text='SiPMs',
        )
        self.frame['sipm'].grid(row=0, column=0, columnspan=2)
        self.frame['sipm'].grid_propagate(False)

        # supplemental details

        self.frame['supp'] = tk.LabelFrame(
            self.root,
            width=self.root_w,
            height=192,
            text='Supplemental details',
        )
        self.frame['supp'].grid(row=1, column=0, columnspan=2)
        self.frame['supp'].grid_propagate(False)

        # production date

        self.frame['date'] = tk.LabelFrame(
            self.root,
            width=self.root_w // 2,
            height=64,
            text='Production date/time (timezone: UTC)',
        )
        self.frame['date'].grid(row=2, column=0, columnspan=1)
        self.frame['date'].grid_propagate(False)

        # buttons

        self.frame['button'] = tk.LabelFrame(
            self.root,
            width=self.root_w // 2,
            height=64,
            text='Actions',
        )
        self.frame['button'].grid(row=3, column=0, columnspan=1)
        self.frame['button'].grid_propagate(False)

        # console for error messages and other status messages

        self.frame['console'] = tk.LabelFrame(
            self.root,
            width=self.root_w // 2,
            height=128,
            text='Console',
        )
        self.frame['console'].grid(row=2, column=1, columnspan=1, rowspan=2)
        self.frame['console'].grid_propagate(False)

    def populate_console_frame(self):
        """
        Populate the GUI button frame with gridded widgets.

        --------------------------------------------------------------------------
        args
            frame : dict
                {<frame_name>: <tk.LabelFrame>, ...}
                Contains details of GUI window frames.
            widgets : list
                Contains details of GUI widgets.
        --------------------------------------------------------------------------
        returns
            widgets : list
                no explicit return, mutable type amended in place
        --------------------------------------------------------------------------
        """
        wtmp = Widget(
            tk.Text(self.frame['console'], state=tk.DISABLED, height=7, width=70),
            itype=Itype.TEXT,
            cluster='console',
            category=None,
        )
        wtmp.instance.grid(column=0, row=0)

        # add scrollbar
        scroll_bar = tk.Scrollbar(
            self.frame['console'], command=wtmp.instance.yview, orient='vertical'
        )
        scroll_bar.grid(row=0, column=1, sticky='ns')
        wtmp.instance.configure(yscrollcommand=scroll_bar.set)

        self.widgets.append(wtmp)

    def populate_supplemental_frame(self):
        """
        Populate the supplemental frame with widgets.

        ----------------------------------------------------------------------
        args
            root : tk.Tk
                The top-level Tk widget for the main GUI window
            widgets : list
            dbi : ds20kdb.interface.Database
                Instance of the Database interface class; allows communication
                with the database.
        ----------------------------------------------------------------------
        returns
            widgets : list
                no explicit return, mutable type amended in place
        ----------------------------------------------------------------------
        """
        # structure the space with sub-frames
        self.frame['supp'].grid_rowconfigure(0, minsize=self.outer_split)
        self.frame['supp'].grid_rowconfigure(1)
        self.frame['supp'].grid_rowconfigure(2)
        self.frame['supp'].grid_rowconfigure(3, minsize=self.outer_split)
        self.frame['supp'].grid_rowconfigure(4)
        self.frame['supp'].grid_rowconfigure(5)
        self.frame['supp'].grid_rowconfigure(6, minsize=self.outer_split)
        self.frame['supp'].grid_rowconfigure(7)
        self.frame['supp'].grid_rowconfigure(8)
        self.frame['supp'].grid_rowconfigure(9, minsize=self.outer_split)

        self.frame['supp'].grid_columnconfigure(0, minsize=self.outer_split)
        self.frame['supp'].grid_columnconfigure(1)
        self.frame['supp'].grid_columnconfigure(2, minsize=self.outer_split)
        self.frame['supp'].grid_columnconfigure(3)
        self.frame['supp'].grid_columnconfigure(4, minsize=self.outer_split)
        self.frame['supp'].grid_columnconfigure(5)
        self.frame['supp'].grid_columnconfigure(6, minsize=self.outer_split)

        # vTile are produced by UK institutes, so reduce complexity by removing
        # other institutes from the combobox.
        exclude_institute = ['INFN', 'LNGS', 'NOA']
        inst = sorted(
            i for i in self.dbi.get('institute').data.name.values
            if not any(x in i for x in exclude_institute)
        )
        wtmp = Widget(
            ColourLabel(
                self.frame['supp'],
                text='Manufacturing institute',
                anchor='w',
            ),
            itype=Itype.LABEL,
            cluster='institute',
            category=None,
        )
        wtmp.instance.grid(sticky='w', column=1, row=1, columnspan=6)
        self.widgets.append(wtmp)

        wtmp = Widget(
            Supplemental(
                self.frame['supp'],
                textvariable='institute',
                values=inst,
                state='readonly',
                width=78,
            ),
            itype=Itype.COMBOBOX,
            cluster='institute',
            category=None,
        )
        wtmp.instance.grid(sticky='w', column=1, row=2, columnspan=6)
        # If the user changes the institute, the available solder syringes must
        # be updated to match it.
        wtmp.instance.bind(
            '<<ComboboxSelected>>',
            functools.partial(self.refresh_solder)
        )
        self.widgets.append(wtmp)

        # QR code

        qrcodes_not_allocated_to_vtiles = self.dbi.get_relevant_qrcodes()
        if qrcodes_not_allocated_to_vtiles is None:
            qrcodes_not_allocated_to_vtiles = []
        wtmp = Widget(
            ColourLabel(
                self.frame['supp'],
                text='QR code',
                anchor='w'
            ),
            itype=Itype.LABEL,
            cluster='qrcode',
            category=None,
        )
        wtmp.instance.grid(sticky='w', column=1, row=7)
        self.widgets.append(wtmp)
        wtmp = Widget(
            Supplemental(
                self.frame['supp'],
                textvariable='qrcode',
                values=[
                    qrcode_chunk(q) for q in qrcodes_not_allocated_to_vtiles
                ],
                state='normal',
                width=20,
            ),
            itype=Itype.COMBOBOX,
            cluster='qrcode',
            category=None,
        )
        wtmp.instance.grid(sticky='w', column=1, row=8)
        wtmp.instance.bind('<Key>', self.handle_ctrl_key_qr)
        self.widgets.append(wtmp)

        # solder_id

        # Attempt to get institute name.
        # This is a little inefficient, since we'll load this file again later.
        table_json = quiet_load_json(self.defaults_file_path)

        try:
            institute_text = table_json['institute|None']
        except KeyError:
            # No institute name in defaults.
            # Load everything: all syringe_ids, from all institutes
            sold = sorted(map(int, self.dbi.get('solder').data.solder_pid.values))
        else:
            # attempt to limit selection based on institute/date
            institute_id = self.dbi.get_institute_id(institute_text).data
            sold = self.dbi.get_relevant_solder_ids(institute_id)

        wtmp = Widget(
            ColourLabel(
                self.frame['supp'],
                text='PID of solder syringe',
                anchor='w'
            ),
            itype=Itype.LABEL,
            cluster='solder_id',
            category=None,
        )
        wtmp.instance.grid(sticky='w', column=1, row=4)
        self.widgets.append(wtmp)
        wtmp = Widget(
            Solder(
                self.frame['supp'],
                textvariable='solder_id',
                values=sold,
                state='readonly',
                width=4,
            ),
            itype=Itype.COMBOBOX,
            cluster='solder_id',
            category=None,
        )
        wtmp.instance.grid(sticky='w', column=1, row=5)
        if len(sold) == 1:
            wtmp.instance.set(sold[0])
        self.widgets.append(wtmp)

        # run_number

        runn = list(range(200))
        wtmp = Widget(
            ColourLabel(
                self.frame['supp'],
                text='Production run number',
                anchor='w'
            ),
            itype=Itype.LABEL,
            cluster='run_number',
            category=None,
        )
        wtmp.instance.grid(sticky='w', column=3, row=4)
        self.widgets.append(wtmp)
        wtmp = Widget(
            Supplemental(
                self.frame['supp'],
                textvariable='run_number',
                values=runn,
                state='readonly',
                width=4,
            ),
            itype=Itype.COMBOBOX,
            cluster='run_number',
            category=None,
        )
        wtmp.instance.grid(sticky='w', column=3, row=5)
        self.widgets.append(wtmp)

        # --------------------------------------------------------------------
        # comment
        wtmp = Widget(
            ColourLabel(
                self.frame['supp'],
                text='Comment',
                anchor='w'
            ),
            itype=Itype.LABEL,
            cluster='comment',
            category=None,
        )
        wtmp.instance.grid(sticky='w', column=3, row=7)
        self.widgets.append(wtmp)

        wtmp = Widget(
            Supplemental(
                self.frame['supp'],
                textvariable='comment',
                values=['Normal'],
                # allow user to enter their own values
                state='normal',
                width=96,
            ),
            itype=Itype.COMBOBOX,
            cluster='comment',
            category=None,
        )
        wtmp.instance.grid(sticky='w', column=3, row=8)
        wtmp.instance.bind('<Key>', self.handle_ctrl_key_comment)
        self.widgets.append(wtmp)

    def populate_production_date_frame(self):
        """
        Populate the GUI production date frame with gridded widgets.

        Limited selections for some values:

            year    : 2022 - 2032
            minutes : 15 minute increments
            seconds : omitted, since this value isn't relevant

        The date will need to be checked later to make sure the month/day
        values make sense together.

        The default values are set to the current date and time.

        ----------------------------------------------------------------------
        args
            root : tk.Tk
                The top-level Tk widget for the main GUI window
            frame : dict
                {<frame_name>: <tk.LabelFrame>, ...}
                Contains details of GUI window frames.
            widgets : list
                Contains details of GUI widgets.
            dbi : ds20kdb.interface.Database
                Instance of the Database interface class; allows communication
                with the database.
        ----------------------------------------------------------------------
        returns
            widgets : list
                no explicit return, mutable type amended in place
        ----------------------------------------------------------------------
        """
        # indices for default drop-down box values
        default_index = self.default_date_time()

        # year

        wtmp = Widget(
            ColourLabel(
                self.frame['date'],
                text='Year',
                anchor='w',
            ),
            itype=Itype.LABEL,
            cluster='production_date',
            category='year',
        )
        wtmp.instance.grid(sticky='w', column=0, row=0)
        self.widgets.append(wtmp)
        wtmp = Widget(
            Supplemental(
                self.frame['date'],
                values=self.dt_range['years'],
                state='readonly',
                width=8,
            ),
            itype=Itype.COMBOBOX,
            cluster='production_date',
            category='year',
        )
        wtmp.instance.current(default_index['year'])
        wtmp.instance.grid(sticky='w', column=0, row=1)
        self.widgets.append(wtmp)

        # month

        wtmp = Widget(
            ColourLabel(
                self.frame['date'],
                text='Month',
                anchor='w',
            ),
            itype=Itype.LABEL,
            cluster='production_date',
            category='month',
        )
        wtmp.instance.grid(sticky='w', column=1, row=0)
        self.widgets.append(wtmp)
        wtmp = Widget(
            Supplemental(
                self.frame['date'],
                values=self.dt_range['months'],
                state='readonly',
                width=8,
            ),
            itype=Itype.COMBOBOX,
            cluster='production_date',
            category='month',
        )
        wtmp.instance.current(default_index['month'])
        wtmp.instance.grid(sticky='w', column=1, row=1)
        self.widgets.append(wtmp)

        # day

        wtmp = Widget(
            ColourLabel(
                self.frame['date'],
                text='Day',
                anchor='w',
            ),
            itype=Itype.LABEL,
            cluster='production_date',
            category='day',
        )
        wtmp.instance.grid(sticky='w', column=2, row=0)
        self.widgets.append(wtmp)
        wtmp = Widget(
            Supplemental(
                self.frame['date'],
                values=self.dt_range['days'],
                state='readonly',
                width=8,
            ),
            itype=Itype.COMBOBOX,
            cluster='production_date',
            category='day',
        )
        wtmp.instance.current(default_index['day'])
        wtmp.instance.grid(sticky='w', column=2, row=1)
        self.widgets.append(wtmp)

        # hour

        wtmp = Widget(
            ColourLabel(
                self.frame['date'],
                text='Hour',
                anchor='w',
            ),
            itype=Itype.LABEL,
            cluster='production_date',
            category='hour',
        )
        wtmp.instance.grid(sticky='w', column=3, row=0)
        self.widgets.append(wtmp)
        wtmp = Widget(
            Supplemental(
                self.frame['date'],
                values=self.dt_range['hours'],
                state='readonly',
                width=8,
            ),
            itype=Itype.COMBOBOX,
            cluster='production_date',
            category='hour',
        )
        wtmp.instance.current(default_index['hour'])
        wtmp.instance.grid(sticky='w', column=3, row=1)
        self.widgets.append(wtmp)

        # minutes

        wtmp = Widget(
            ColourLabel(
                self.frame['date'],
                text='Minutes',
                anchor='w',
            ),
            itype=Itype.LABEL,
            cluster='production_date',
            category='minute',
        )
        wtmp.instance.grid(sticky='w', column=4, row=0)
        self.widgets.append(wtmp)
        wtmp = Widget(
            Supplemental(
                self.frame['date'],
                values=self.dt_range['minutes'],
                state='readonly',
                width=8,
            ),
            itype=Itype.COMBOBOX,
            cluster='production_date',
            category='minute',
        )
        wtmp.instance.current(default_index['minute'])
        wtmp.instance.grid(sticky='w', column=4, row=1)
        self.widgets.append(wtmp)

    def populate_action_button_frame(self):
        """
        Populate the GUI button frame with gridded widgets.

        --------------------------------------------------------------------------
        args
            root : tk.Tk
                The top-level Tk widget for the main GUI window
            frame : dict
                {<frame_name>: <tk.LabelFrame>, ...}
                Contains details of GUI window frames.
            widgets : list
                Contains details of GUI widgets.
            dbi : ds20kdb.interface.Database
                Instance of the Database interface class; allows communication
                with the database.
        --------------------------------------------------------------------------
        returns
            widgets : list
                no explicit return, mutable type amended in place
        --------------------------------------------------------------------------
        """
        self.frame['button'].grid_columnconfigure(0, weight=1)
        self.frame['button'].grid_columnconfigure(1, weight=1)

        # button to check user-entered values
        tk.Button(
            self.frame['button'],
            text='check',
            command=self.check,
        ).grid(column=0, row=0, sticky=tk.W)

        # button to submit vTile to the database
        wtmp = Widget(
            ButtonSubmit(
                self.frame['button'],
                text='submit',
                command=self.submit,
                state=tk.DISABLED,
            ),
            itype=Itype.BUTTON,
            cluster='submit',
            category=None,
        )
        wtmp.instance.grid(column=1, row=0, sticky=tk.E)
        self.widgets.append(wtmp)

    def populate_sipm_frame(self):
        """
        The SiPM numbering is shown looking at the PCB with SiPMs visible and
        towards the viewer, and the backside components(resistors, capacitors,
        ASIC etc.) facing away from the viewer. The location of the QR code and
        ASIC on the back-side of the PCB are also shown to provide orientation.

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

        Within the frame, each SiPM area is arranged like this:

        +------------------------------------------+
        | label                                    |
        +------------+--------------+--------+-----+
        | lot number | wafer number | column | row |
        +------------+--------------+--------+-----+

        --------------------------------------------------------------------------
        args
            frame : dict
                {<frame_name>: <tk.LabelFrame>, ...}
                Contains details of GUI window frames.
            widgets : list
                Contains details of GUI widgets.
            wafer_table_dataframe : Pandas DataFrame
                A copy of the wafer table from the database
        --------------------------------------------------------------------------
        returns
            widgets : list
                no explicit return, mutable type amended in place
        --------------------------------------------------------------------------
        """
        col_start = 0
        row_start = 0
        col_offset = 4
        row_offset = 2

        # left-most grid position of the four values that define the SiPM:
        # lot_number, wafer_number, column, row
        #
        # {sipm_number: (column, row), ...}
        positions = {
            19: (0, 0), 13: (1, 0), 7: (2, 0), 1: (3, 0),
            20: (0, 1), 14: (1, 1), 8: (2, 1), 2: (3, 1),
            21: (0, 2), 15: (1, 2), 9: (2, 2), 3: (3, 2),
            22: (0, 3), 16: (1, 3), 10: (2, 3), 4: (3, 3),
            23: (0, 4), 17: (1, 4), 11: (2, 4), 5: (3, 4),
            24: (0, 5), 18: (1, 5), 12: (2, 5), 6: (3, 5),
        }

        lots = sorted({lo[0] for lo in self.wafer_table_dataframe[['lot']].values})
        wafs = sorted({wn[0] for wn in self.wafer_table_dataframe[['wafer_number']].values})
        cols, rows = map(set, zip(*self.valid_locations))
        cols = sorted(cols)
        rows = sorted(rows)

        # set up SiPM labels and comboboxes
        for sipm, (column, row) in positions.items():

            column_base = col_start + col_offset * column
            row_base = row_start + row_offset * row

            # sipm label

            wtmp = Widget(
                ColourLabel(self.frame['sipm'], text=f'SiPM {sipm}'),
                itype=Itype.LABEL,
                cluster=f'sipm_{sipm}',
                category=None,
            )
            wtmp.instance.grid(column=column_base, row=row_base, sticky='w')
            self.widgets.append(wtmp)

            # 4 drop-down menus: lot number, wafer number, column, row

            row_base += 1

            wtmp = Widget(
                SipmLotNum(
                    self.frame['sipm'],
                    values=lots,
                    state='readonly',
                    width=11,
                ),
                itype=Itype.COMBOBOX,
                cluster=f'sipm_{sipm}',
                category='lot_number',
            )
            wtmp.instance.grid(column=column_base, row=row_base)
            wtmp.instance.set('lot')
            self.widgets.append(wtmp)

            wtmp = Widget(
                SipmWaferNum(
                    self.frame['sipm'],
                    values=wafs,
                    state='readonly',
                    width=5,
                ),
                itype=Itype.COMBOBOX,
                cluster=f'sipm_{sipm}',
                category='wafer_number',
            )
            wtmp.instance.grid(column=column_base+1, row=row_base)
            wtmp.instance.set('wafer')
            self.widgets.append(wtmp)

            wtmp = Widget(
                SipmColumn(
                    self.frame['sipm'],
                    values=cols,
                    state='readonly',
                    width=3,
                ),
                itype=Itype.COMBOBOX,
                cluster=f'sipm_{sipm}',
                category='column',
            )
            wtmp.instance.grid(column=column_base+2, row=row_base)
            wtmp.instance.set('col')
            self.widgets.append(wtmp)

            wtmp = Widget(
                SipmRow(
                    self.frame['sipm'],
                    values=rows,
                    state='readonly',
                    width=4,
                ),
                itype=Itype.COMBOBOX,
                cluster=f'sipm_{sipm}',
                category='row',
            )
            wtmp.instance.grid(column=column_base+3, row=row_base)
            wtmp.instance.set('row')
            self.widgets.append(wtmp)

    ##########################################################################
    # Build the GUI interface (top menu bar)
    ##########################################################################

    def populate_menu_bar(self):
        """
        Populate the GUI menu bar.

        --------------------------------------------------------------------------
        args : none
        --------------------------------------------------------------------------
        returns : none
            GUI state changed
        --------------------------------------------------------------------------
        """
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=False)
        tool_menu = tk.Menu(menubar, tearoff=False)
        sold_menu = tk.Menu(menubar, tearoff=False)
        repa_menu = tk.Menu(menubar, tearoff=False)
        help_menu = tk.Menu(menubar, tearoff=False)

        file_menu.add_command(
            label='Open...',
            command=self.load_file,
        )
        file_menu.add_command(
            label='Save',
            command=self.save_file_wrapper,
        )
        file_menu.add_command(
            label='Save As...',
            command=self.save_file_as,
        )

        # ------------------------------------------------------------------------
        file_menu.add_separator()
        file_menu.add_command(
            label='Import Tray...',
            command=self.import_tray,
        )
        file_menu.add_command(
            label='Export Python',
            command=self.export_python_wrapper,
        )
        file_menu.add_command(
            label='Export Python As...',
            command=self.export_python_as,
        )

        # ------------------------------------------------------------------------
        file_menu.add_separator()
        file_menu.add_command(
            label='Export Console Log',
            command=self.export_console_wrapper,
        )
        file_menu.add_command(
            label='Export Console Log As...',
            command=self.export_console_as,
        )

        # ------------------------------------------------------------------------
        file_menu.add_separator()
        file_menu.add_command(
            label='Save Defaults',
            command=self.save_defaults,
        )
        file_menu.add_command(
            label='Clear Defaults',
            command=self.clear_defaults,
        )

        # ------------------------------------------------------------------------
        file_menu.add_separator()
        file_menu.add_command(
            label='Quit',
            command=self.root.destroy,
        )

        tool_menu.add_command(
            label='Clear GUI',
            command=self.clear_gui,
        )
        tool_menu.add_command(
            label='Clear GUI and load defaults',
            command=self.clear_gui_load_defaults,
        )
        tool_menu.add_command(
            label='Clear cache',
            command=self.clear_cache,
        )
        tool_menu.add_separator()
        tool_menu.add_command(
            label='Set default tray file directory',
            command=self.set_default_tray_file_directory,
        )

        # ------------------------------------------------------------------------
        sold_menu.add_command(
            label='Add solder syringe to database',
            command=self.add_solder_syringe_popup,
        )
        sold_menu.add_separator()
        sold_menu.add_checkbutton(
            label="Strict solder syringe checking",
            onvalue=True, offvalue=False,
            variable=self.strict_solder_syringe_checking,
        )
        sold_menu.add_command(
            label='Reload solder syringes',
            command=self.refresh_solder
        )

        help_menu.add_command(
            label='About',
            command=self.about_popup,
        )
        help_menu.add_command(
            label='Documentation',
            command=lambda: webbrowser.open_new(
                'https://gitlab.in2p3.fr/darkside/productiondb_software/-/wikis/'
                'Submitting-vTiles-to-the-database-using-a-GUI'
            ),
        )

        # ------------------------------------------------------------------------
        repa_menu.add_command(
            label='Import vTile from database',
            command=self.import_vtile_from_db_popup,
        )
        repa_menu.add_separator()
        repa_menu.add_checkbutton(
            label="Repair mode",
            onvalue=True, offvalue=False,
            variable=self.repair_mode,
            command=self.repair_mode_status,
        )

        # add top level drop-down menu titles
        menubar.add_cascade(
            label='File',
            menu=file_menu,
            underline=0
        )
        menubar.add_cascade(
            label='Tools',
            menu=tool_menu,
            underline=0
        )
        menubar.add_cascade(
            label='Solder',
            menu=sold_menu,
            underline=0
        )
        menubar.add_cascade(
            label='Repair',
            menu=repa_menu,
            underline=0
        )
        menubar.add_cascade(
            label='Help',
            menu=help_menu,
            underline=0
        )

    ##########################################################################
    # File I/O relating to the GUI menu bar
    ##########################################################################

    def clear_defaults(self):
        """
        Removes the file containing user-set defaults, if it exists.

        --------------------------------------------------------------------------
        args : none
        --------------------------------------------------------------------------
        returns : none
            Possible filesystem change.
        --------------------------------------------------------------------------
        """
        try:
            os.remove(self.defaults_file_path)
        except FileNotFoundError:
            pass
        else:
            self.print_to_console(
                f'Deleted defaults file {self.defaults_file_path}'
            )

    def export_console(self, filename):
        """
        Exports all text from the console to a file.

        --------------------------------------------------------------------------
        args
            filename : string
        --------------------------------------------------------------------------
        returns : none
            file written to mass storage
        --------------------------------------------------------------------------
        """
        text = self.get_from_console()

        with open(filename, 'w', encoding='utf-8') as f:
            f.writelines(text)

    def export_console_as(self):
        """
        Save file with a time-stamped filename.

        --------------------------------------------------------------------------
        args : none
        --------------------------------------------------------------------------
        returns : none
            file written to mass storage
        --------------------------------------------------------------------------
        """
        suggested_filename = f'{self.session_timestamp}_console_log.txt'

        filename = filedialog.asksaveasfilename(
            initialfile=suggested_filename,
            defaultextension='.txt',
            filetypes=[
                ('Text Documents', '*.txt'),
                ('All Files', '*.*'),
            ]
        )

        with contextlib.suppress(AttributeError):
            self.export_console(filename)

    def export_console_wrapper(self):
        """
        Exports all text from the console to a file.

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns : none
            file written to mass storage
        ----------------------------------------------------------------------
        """
        self.export_console(f'{self.session_timestamp}_console_log.txt')

    def export_python(self, filename):
        """
        Exports GUI elements indicated as good after the user has used the CHECK
        button.

        --------------------------------------------------------------------------
        args
            filename : string
        --------------------------------------------------------------------------
        returns : none
            file written to mass storage
        --------------------------------------------------------------------------
        """
        # get table from GUI variable
        try:
            table = json.loads(self.table_json_string)
        except (TypeError, json.decoder.JSONDecodeError):
            self.print_to_console('No data to export.')
        else:
            with open(filename, 'w', encoding='utf-8') as outfile:
                outfile.write(f'table = {table}')

    def export_python_as(self):
        """
        Save file with a time-stamped filename.

        FIXME - this should pull directly from the GUI rather than from what
        was last submitted by CHECK

        --------------------------------------------------------------------------
        args : none
        --------------------------------------------------------------------------
        returns : none
            file written to mass storage
        --------------------------------------------------------------------------
        """
        suggested_filename = f'{self.session_timestamp}_post_vtile.py'

        filename = filedialog.asksaveasfilename(
            initialfile=suggested_filename,
            defaultextension='.py',
            filetypes=[
                ('Python Documents', '*.py'),
                ('All Files', '*.*'),
            ]
        )

        with contextlib.suppress(AttributeError):
            self.export_python(filename)

    def export_python_wrapper(self):
        """
        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns : none
            file written to mass storage
        ----------------------------------------------------------------------
        """
        self.export_python(f'{self.session_timestamp}_post_vtile.py')

    def load_defaults(self):
        """
        The defaults are loaded from the user's file at application start when
        the GUI comboboxes are empty, so there's no need to reset anything.

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns : none
            GUI state changed
        ----------------------------------------------------------------------
        """
        # update GUI from previously saved GUI default settings
        self.update_gui_from_dict(
            self.generic_load_json(self.defaults_file_path)
        )

        # this will take the institute from the GUI
        self.refresh_solder()

        # load default tray file location
        table_json = self.generic_load_json(self.defaults_tray_file_path)

        if not table_json:
            return

        try:
            dtf = table_json['tray_file_directory']
        except KeyError:
            self.print_to_console(
                'Error reading tray file default directory from '
                f'{self.defaults_tray_file_path}'
            )
        else:
            if os.path.isdir(dtf):
                self.tray_file_directory = dtf
            else:
                self.print_to_console(f'Default tray file directory does not exist: {dtf}')

    def set_default_tray_file_directory(self):
        """
        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns : none
        ----------------------------------------------------------------------
        """
        # filename will be a tuple for some reason
        directory = filedialog.askdirectory(
            initialdir=self.tray_file_directory,
            title='set default directory for tray files',
        )

        if directory:
            self.tray_file_directory = directory

            with open(self.defaults_tray_file_path, 'w', encoding='utf-8') as outfile:
                outfile.write(
                    json.dumps(
                        {'tray_file_directory': directory}
                    )
                )

    @staticmethod
    def sipm_key(key):
        """
        Check if a string represents a SiPM.

        --------------------------------------------------------------------------
        args
            key : string
                e.g. 'sipm_1' or 'sipm_23'
        --------------------------------------------------------------------------
        returns : int or None
            int if the SiPM information appears valid, None otherwise
            internal_key : string, e.g. 'sipm_1' return this to strip leading
            zeroes from 'sipm_01' if that representation was used in the tray
            file.
        --------------------------------------------------------------------------
        """
        try:
            sipm_text, number = key.split('_')
        except ValueError:
            sipm_text = number = internal_key = None
        else:
            number = int(number)
            internal_key = f'sipm_{number}'

        return internal_key, number if sipm_text == 'sipm' and 1 <= number <= 24 else None

    @staticmethod
    def lot_wafer(line):
        """
        Extract lot or wafer number value from text line.

        --------------------------------------------------------------------------
        args
            line : string
                e.g. 'lot, 9333249' or 'wafer_number 02'
        --------------------------------------------------------------------------
        returns : int or None
        --------------------------------------------------------------------------
        """
        parameter = None

        try:
            _, value = line
        except ValueError:
            return parameter

        with contextlib.suppress(ValueError):
            parameter = int(value)

        return parameter

    def process_sipm_definition(self, data, sipms_from_default_wafer, fail, fields):
        """
        Check if line defining a SiPM is valid.

        --------------------------------------------------------------------------
        args
            data : dict
            sipms_from_default_wafer : set
            fail : bool
            fields : list
        --------------------------------------------------------------------------
        returns : bool
            data : dict
                no explicit return, mutable type amended in place
        --------------------------------------------------------------------------
        """
        # long form: 5 values
        # short form: 3 values
        # named SiPM but no information, 1 or 2 values
        try:
            key, column, row, lot_num, wafer_num = fields
        except ValueError:
            try:
                key, column, row = fields
            except ValueError:
                # This is likely to be a line starting with sipm_xx and no
                # following information (an unfilled template line), so just
                # allow this case to be silently ignored.
                if len(fields) != 1:
                    fail = True
            else:
                # short form
                # sipm_number, wafer_column, wafer_row
                internal_key, sipm = self.sipm_key(key)
                if sipm is not None:
                    with contextlib.suppress(ValueError):
                        data[f'{internal_key}|column'] = int(column)
                        data[f'{internal_key}|row'] = int(row)
                        sipms_from_default_wafer.add(sipm)
                else:
                    # SiPM number is probably out of range
                    fail = True
        else:
            # long form
            # sipm_number, wafer_column, wafer_row, wlot, wnum

            internal_key, sipm = self.sipm_key(key)

            if sipm is not None:
                with contextlib.suppress(ValueError):
                    data[f'{internal_key}|column'] = int(column)
                    data[f'{internal_key}|row'] = int(row)
                    data[f'{internal_key}|lot_number'] = int(lot_num)
                    data[f'{internal_key}|wafer_number'] = int(wafer_num)
            else:
                # SiPM number is probably out of range
                fail = True

        return fail

    def save_defaults(self):
        """
        Save defaults that will be subsequently loaded at the next application
        start.

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns : none
            file written to mass storage
        ----------------------------------------------------------------------
        """
        def default_test(widget, def_clust):
            return (
                widget.itype == Itype.COMBOBOX
                and widget.cluster in def_clust
                and bool(widget.instance.get())
            )

        default_clusters = {'institute'}
        valid_default = functools.partial(
            default_test, def_clust=default_clusters
        )

        with open(self.defaults_file_path, 'w', encoding='utf-8') as outfile:
            outfile.write(
                json.dumps(
                    {
                        f'{w.cluster}|{w.category}': w.instance.get()
                        for w in self.widgets
                        if valid_default(w)
                    }
                )
            )

    def load_file(self):
        """
        Load JSON file containing previously saved GUI combobox contents.

        ----------------------------------------------------------------------
        args
            widgets : list
                Contains details of GUI widgets.
        ----------------------------------------------------------------------
        returns : none
            GUI state affected
        ----------------------------------------------------------------------
        """
        filename = filedialog.askopenfilename(
            initialdir=self.home_directory,
            defaultextension='.json',
            filetypes=[
                ('JSON Documents', '*.json'),
                ('All Files', '*.*'),
            ],
            title='load saved GUI state',
        )

        if not filename:
            return

        table_json = self.generic_load_json(filename)

        if table_json:
            self.clear_gui()
            self.update_gui_from_dict(table_json)

            # We want to leave the solder syringe that was loaded from the
            # file selected in the GUI, even if that syringe isn't in the
            # list of combobox values. This is so the user sees the file as
            # it is on disk, rather than automatically setting the solder
            # syringe to some other value, which may be confusing.

            try:
                institute_text = table_json['institute|None']
            except KeyError:
                # No institute name in defaults.
                pass
            else:
                # attempt to limit selection based on institute/date
                institute_id = self.dbi.get_institute_id(institute_text).data
                self.update_solder(institute_id, force=False)
                self.set_manufacturing_mode()

                # if a vTile was imported in repair mode, the submit button
                # may be active
                self.clear_submit_button()

    def generic_load_json(self, filename):
        """
        Load JSON file.

        ----------------------------------------------------------------------
        args
            widgets : list of class Widget
                Contains details of GUI widgets.
            filename : string
        ----------------------------------------------------------------------
        returns
            table_json : dict
                e.g. {
                    'sipm_19|lot_number': '9262109',
                    'sipm_19|wafer_number': '15',
                    'sipm_19|column': '10',
                    'sipm_19|row': '21', ...
                }
        ----------------------------------------------------------------------
        """
        table_json = {}

        with contextlib.suppress(FileNotFoundError):
            with open(filename, 'r', encoding='utf-8') as infile:
                try:
                    table_json = json.load(infile)
                except (json.JSONDecodeError, UnicodeDecodeError):
                    logging.error('could not read file: %s', filename)

                    self.print_to_console(f'Could not read file: {filename}')
                else:
                    self.print_to_console(f'Loaded file {filename}')

        unpack_qrcode(table_json)

        return table_json

    def save_file_wrapper(self):
        """
        --------------------------------------------------------------------------
        args
            session_timestamp : string
                e.g. '20221119_144629'
            widgets : list
                Contains details of GUI widgets.
        --------------------------------------------------------------------------
        returns : none
            file written to mass storage
        --------------------------------------------------------------------------
        """
        filename = f'{self.session_timestamp}_post_vtile.json'
        self.print_to_console(f'Saved to {os.path.join(os.getcwd(), filename)}')
        self.save_file(filename)

    def save_file(self, filename):
        """
        Save file with a time-stamped filename containing the values from all
        drop-down menus.

        ----------------------------------------------------------------------
        args
            widgets : list of class Widget
                Contains details of GUI widgets.
            filename : string
        ----------------------------------------------------------------------
        returns : none
            file written to mass storage
        ----------------------------------------------------------------------
        """
        with open(filename, 'w', encoding='utf-8') as outfile:
            outfile.write(
                json.dumps(
                    {
                        f'{w.cluster}|{w.category}': self.pack(w.cluster, w.instance.get())
                        for w in self.widgets
                        if w.itype == Itype.COMBOBOX
                    }
                )
            )

    @staticmethod
    def pack(cluster, value):
        """
        Ensure the QR code as saved in a JSON file is in its normal packed
        state, e.g. '23110613000720001' instead of the chunked state captured
        from the GUI '231106 1 30 00720 001'.

        ----------------------------------------------------------------------
        args
            cluster : string
            value : string
        ----------------------------------------------------------------------
        returns : string
        ----------------------------------------------------------------------
        """
        return value if cluster != 'qrcode' else qrcode_normal(value)

    def save_file_as(self):
        """
        Save file with a time-stamped filename.

        --------------------------------------------------------------------------
        args
            session_timestamp : string
                e.g. '20221119_144629'
            widgets : list of class Widget
                Contains details of GUI widgets.
        --------------------------------------------------------------------------
        returns : none
            file written to mass storage
        --------------------------------------------------------------------------
        """
        suggested_filename = f'{self.session_timestamp}_post_vtile.json'

        filename = filedialog.asksaveasfilename(
            initialfile=suggested_filename,
            defaultextension='.json',
            filetypes=[
                ('JSON Documents', '*.json'),
                ('All Files', '*.*'),
            ]
        )

        with contextlib.suppress(AttributeError):
            self.save_file(filename)

    def import_tray(self):
        """
        Import data recorded during the wafer picking stage, where a file
        represents the contents of a SiPM tray (24 SiPMS).

        The contents of the file should look something like this:

        tray, 1
        lot, 9262109
        wafer_number, 15
        # sipm_number, wafer_column, wafer_row
        sipm_1, 07, 23
        sipm_2, 08, 23
        sipm_3, 09, 23
        sipm_4, 10, 23
        sipm_5, 11, 23
        sipm_6, 12, 23
        sipm_7, 06, 22
        sipm_8, 07, 22
        sipm_9, 08, 22
        sipm_10, 09, 22
        sipm_11, 10, 22
        sipm_12, 11, 22
        sipm_13, 12, 22
        sipm_14, 13, 22
        sipm_15, 06, 21
        sipm_16, 07, 21
        sipm_17, 08, 21
        sipm_18, 09, 21
        sipm_19, 10, 21
        sipm_20, 11, 21
        sipm_21, 12, 21
        sipm_22, 13, 21
        sipm_23, 14, 21
        sipm_24, 04, 20

        For the SiPM lines, there are some variants for tray locations:

        (1) empty (n=1):

        sipm_number,
        sipm_number

        (2) has come from another wafer (n=5):

        sipm_number, wafer_column, wafer_row, wafer_lot, wafer_number

        At some stage, we should also allow SiPM PIDs to be used (n=2):

        sipm_number, sipm_pid

        --------------------------------------------------------------------------
        args
            widgets : list
                Contains details of GUI widgets.
        --------------------------------------------------------------------------
        returns : none
            GUI state affected
        --------------------------------------------------------------------------
        """
        filename = filedialog.askopenfilename(
            initialdir=self.tray_file_directory,
            defaultextension='.txt',
            filetypes=[
                ('TEXT Documents', '*.txt'),
                ('All Files', '*.*'),
            ],
            title='load SiPM tray file',
        )

        if not filename:
            return

        data = {}
        lot_number = wafer_number = None
        sipms_from_default_wafer = set()

        for line_number, no_comment, fields in self.tray_file_lines(filename):
            fail = False

            if fields[0].startswith('lot'):
                lot_number = self.lot_wafer(fields)
                if lot_number is None:
                    fail = True

            elif fields[0].startswith('wafer_number'):
                wafer_number = self.lot_wafer(fields)
                if wafer_number is None:
                    fail = True

            elif fields[0].startswith('sipm_'):
                fail = self.process_sipm_definition(
                    data, sipms_from_default_wafer, fail, fields
                )

            else:
                # issue a warning for any non-matching line
                fail = True

            if fail:
                self.print_to_console(
                    f'Check line {line_number}: "{no_comment}"'
                )

        # lot_number and/or wafer_number can be None as long as there are no
        # short-form (column/row only) entries that require that pair of values.
        if sipms_from_default_wafer and (lot_number is None or wafer_number is None):
            self.print_to_console(
                'Both lot/wafer numbers required to use short-form SiPM locations'
            )
            return

        # For SiPMs that didn't have a wafer lot and wafer number specified, fill
        # in the default values. We can't guarantee that the wafer and lot number
        # will precede SiPM definitions, so this can't be done earlier.
        for number in sipms_from_default_wafer:
            data[f'sipm_{number}|lot_number'] = lot_number
            data[f'sipm_{number}|wafer_number'] = wafer_number

        self.clear_gui_sipms_only()
        self.update_gui_from_dict(data)
        self.set_manufacturing_mode()
        self.clear_submit_button()

        self.print_to_console(f'Imported tray file {filename}')

    @staticmethod
    def tray_file_lines(filename):
        """
        Yield fields extracted from individual tray file lines.

        Fields are delimited by spaces and/or commas:

        'a,b,c'     -> ['a', 'b', 'c']
        'a b,c'     -> ['a', 'b', 'c']
        'a b, ,,,c' -> ['a', 'b', 'c']

        --------------------------------------------------------------------------
        args
            filename : string
        --------------------------------------------------------------------------
        yields : int, list
        --------------------------------------------------------------------------
        """
        with open(filename, 'r', encoding='utf-8') as infile:
            for line_number, line in enumerate(infile, start=1):
                no_comment = line.split('#')[0].strip()
                fields = [
                    field.strip() for field in re.split(r'[, ]+', no_comment)
                    if field.strip()
                ]

                # Only yield if there's something to process.
                # The tray number is for internal site usage only, it won't be
                # added to the database so ignore it.
                if fields and not fields[0].startswith('tray'):
                    yield line_number, no_comment, fields

    ##########################################################################
    # Build the GUI interface (pop-up windows for:
    #
    # Help -> About
    # Solder -> Add solder syringe to database
    ##########################################################################

    def about_popup(self):
        """
        Display the Help -> About window, centred on the main window.
        """
        current_w = self.root.winfo_width()
        current_h = self.root.winfo_height()

        root_win_x, root_win_y = (int(s) for s in self.root.geometry().split('+')[1:])

        about_x = root_win_x + (current_w // 2) - (self.about_w // 2)
        about_y = root_win_y + (current_h // 2) - (self.about_h // 2)

        top = tk.Toplevel(self.root)
        top.geometry(f'{self.about_w}x{self.about_h}+{about_x}+{about_y}')
        top.resizable(False, False)
        top.title('About')

        # add frame

        local_frame = tk.Frame(
            top,
            width=self.about_w,
            height=self.about_h,
        )
        local_frame.grid(row=0, column=0)
        local_frame.grid_propagate(False)

        # add contents (text)

        text = tk.Text(local_frame, height=11, width=70)
        text.grid(column=0, row=0)
        text.tag_configure('center', justify='center')
        message = (
            '\n'
            '- POST vTile -\n'
            f'ds20kdb interface version {interface.__version__}\n'
            '\n'
            'Adds a vTile to the DarkSide-20k\n'
            'production database, or updates\n'
            'an existing repaired vTile.\n'
            '\n'
            '- support -\n'
            'avt@hep.ph.liv.ac.uk'
        )
        text.insert(tk.END, message)
        text.tag_add(tk.CENTER, '1.0', tk.END)
        text.configure(state=tk.DISABLED)

        # add contents (button)

        tk.Button(
            local_frame,
            text='ok',
            command=lambda: self.release(top),
        ).grid(column=0, row=1)
        local_frame.columnconfigure(0, weight=1)   # Set weight to row and
        local_frame.rowconfigure(1, weight=1)      # column where the widget is

        # pop up should take focus from main window until dismissed
        top.grab_set()

    @staticmethod
    def release(window):
        """
        Return focus to main window then destroy pop-up window.

        --------------------------------------------------------------------------
        args
            window : <class 'tk.Toplevel'>
        --------------------------------------------------------------------------
        returns : none
            GUI state changed
        --------------------------------------------------------------------------
        """
        window.grab_release()
        window.destroy()

    def post_solder(self, window, syringe_widgets, institute_id):
        """
        Check user entries and POST to database if correct.

        --------------------------------------------------------------------------
        args
            dbi : ds20kdb.interface.Database
                Instance of the Database interface class; allows communication
                with the database.
            window :
            syringe_widgets :
            widgets :
            institute_id :
        --------------------------------------------------------------------------
        returns : none
        --------------------------------------------------------------------------
        """
        fail = False

        self.print_to_console(common.box_message('POST solder syringe', 62))

        # Get user entries for the new syringe from pop-up windows Text widget
        # fields.
        syringe = {
            k: v.get(1.0, tk.END).strip() for k, v in syringe_widgets.items()
        }

        # check if date/time strings are valid
        for k, v in syringe.items():
            if k.endswith('date') and not self.valid_ds20k_timestamp(v):
                self.print_to_console(f'solder syringe {k} incorrect: {v}')
                fail = True

        # The only remaining user-editable field that can be checked is syringe_id.
        sid = syringe['syringe_id']
        try:
            int(sid)
        except (TypeError, ValueError):
            self.print_to_console(f'solder syringe syringe_id incorrect: {sid}')
            return

        if fail:
            return

        post_successful = self.dbi.post_solder(syringe)

        # get solder id for the last syringe submitted
        solder_id = int(
            self.dbi.get(
                'solder',
                institute_id=syringe['institute_id']
            ).data.iloc[-1].solder_pid
        )

        if post_successful:
            status = 'succeeded'
            suffix = f': PID {solder_id}'
        else:
            status = 'failed'
            suffix = ''

        self.print_to_console(f'POST solder syringe {status}{suffix}')

        if post_successful:
            self.update_solder(institute_id)

        window.grab_release()
        window.destroy()

    def add_solder_syringe_popup(self):
        """
        The institute is required, but this should be taken from the main window.
        If not set, the user should be prompted to enter it there.

        Obtain values for the below from the institute's last last solder syringe.

        In the NEW section the (local) syringe_id can be incremented.

        Keep manufacturer, mass and solder_type together since they are unlikely
        to change over the course of the project.

        Success/fail of POST operation should be given in the main console window.

        Pop-up window:

        +-----------------+-----------------------+-------------+
        | PREVIOUS SYRINGE                        |             |
        +-----------------+-----------------------+-------------+
        | manufacturer    | mass                  |             |
        +-----------------+-----------------------+-------------+
        | solder_type                             |             |
        +-----------------+-----------------------+-------------+
        | production_date | room_temperature_date | expiry_date |
        +-----------------+-----------------------+-------------+
        | syringe_id      | lot                   |             |
        +-----------------+-----------------------+-------------+
        |                 |                       |             |
        +-----------------+-----------------------+-------------+
        | NEW SYRINGE     |                       |             |
        +-----------------+-----------------------+-------------+
        | manufacturer    | mass                  |             |
        +-----------------+-----------------------+-------------+
        | solder_type                             |             |
        +-----------------+-----------------------+-------------+
        | production_date | room_temperature_date | expiry_date |
        +-----------------+-----------------------+-------------+
        | syringe_id      | lot                   |             |
        +-----------------+-----------------------+-------------+
        |                 |                       |             |
        +-----------------+-----------------------+-------------+
        | CANCEL          |                       | POST        |
        +-----------------+-----------------------+-------------+
        """

        # find institute combobox widget
        institute_widget = next(
            widget.instance
            for widget in self.widgets
            if widget.cluster == 'institute' and widget.itype == Itype.COMBOBOX
        )

        # get value from widget
        #
        # If we get a non-empty value it has to be valid since combobox contents
        # were populated from the database. So we can create the window
        # immediately to give the user some feeling of progression, and we can
        # look up the institute_id later.
        institute_text = institute_widget.get()
        if not institute_text:
            self.print_to_console(
                'Please set institute name before attempting to add a solder syringe'
            )
            return

        institute_id = self.dbi.get_institute_id(institute_text).data

        # {
        #     'solder_pid': 31,
        #     'manufacturer': 4,
        #     'solder_type': 'Indium Paste NC-SMQ80 Ind#1E 52In48Sn Type 4 83%, P.No. 83752',
        #     'production_date': '2023-08-21 00:00:00',
        #     'room_temperature_date': '2024-02-13 12:00:00',
        #     'expiry_date': '2024-02-21 00:00:00',
        #     'syringe_id': 18,
        #     'lot': 'PS11130994',
        #     'mass': 10,
        #     'institute_id': 5
        # }

        try:
            last_syringe = self.dbi.get(
                'solder', institute_id=institute_id,
            ).data.to_dict('records')[-1]
        except IndexError:
            # This is the first syringe added for this institute.
            # No prior, so get the last syringe for any institute.
            last_syringe = self.dbi.get('solder').data.to_dict('records')[-1]
            first_syringe = True
        else:
            # Received the last syringe for the selected institute.
            first_syringe = False

        # create pop-up window

        padding = 8

        current_w = self.root.winfo_width()
        current_h = self.root.winfo_height()

        root_win_x, root_win_y = (int(s) for s in self.root.geometry().split('+')[1:])

        about_x = root_win_x + (current_w // 2) - (self.solder_w // 2)
        about_y = root_win_y + (current_h // 2) - (self.solder_h // 2)

        top = tk.Toplevel(self.root)
        top.geometry(f'{self.solder_w}x{self.solder_h}+{about_x}+{about_y}')
        top.resizable(False, False)
        top.title('Add solder syringe to database')

        # add frame

        local_frame = tk.Frame(
            top,
            width=self.solder_w,
            height=self.solder_h,
        )
        local_frame.grid(row=0, column=0)
        local_frame.grid_propagate(False)

        # add padding between elements

        local_frame.grid_rowconfigure(0, minsize=padding * 2)
        local_frame.grid_rowconfigure(1)
        local_frame.grid_rowconfigure(2, minsize=padding * 2)
        local_frame.grid_rowconfigure(3)
        local_frame.grid_rowconfigure(4, minsize=padding * 2)
        local_frame.grid_rowconfigure(5)
        local_frame.grid_rowconfigure(6, minsize=padding * 2)

        local_frame.grid_columnconfigure(0, minsize=padding)
        local_frame.grid_columnconfigure(1)
        local_frame.grid_columnconfigure(2, minsize=padding)

        ######################################################################
        # top

        suffix = ' (for ANY INSTITUTE)' if first_syringe else ''

        previous_frame = tk.LabelFrame(
            local_frame,
            width=self.solder_w - padding * 2,
            height=(self.solder_h - padding * 4 - 56) // 2 + 8,
            text=f'most recently added solder syringe in database{suffix}',
        )
        previous_frame.grid(column=1, row=1)
        previous_frame.grid_propagate(False)

        ######################################################################
        # middle
        new_frame = tk.LabelFrame(
            local_frame,
            width=self.solder_w - padding * 2,
            height=(self.solder_h - padding * 4 - 56) // 2 - 8,
            text=(
                'new solder syringe to add (white fields are fixed, '
                'blue fields were automatically generated)'
            ),
        )
        new_frame.grid(column=1, row=3)
        new_frame.grid_propagate(False)

        ######################################################################
        # bottom
        button_frame = tk.Frame(
            local_frame,
            width=self.solder_w - padding * 2,
            height=56,
        )
        button_frame.grid(column=1, row=5)
        button_frame.grid_propagate(False)

        ######################################################################
        # populate the above 3 frames

        previous_frame.grid_rowconfigure(0, minsize=padding // 2)
        previous_frame.grid_rowconfigure(1)
        previous_frame.grid_rowconfigure(2, minsize=padding // 2)
        previous_frame.grid_rowconfigure(3)
        previous_frame.grid_rowconfigure(4, minsize=padding // 2)

        previous_frame.grid_columnconfigure(0, minsize=padding // 2)
        previous_frame.grid_columnconfigure(1)
        previous_frame.grid_columnconfigure(2, minsize=padding // 2)
        previous_frame.grid_columnconfigure(3)
        previous_frame.grid_columnconfigure(4, minsize=padding // 2)

        for i, (l, t) in enumerate(last_syringe.items()):
            label = tk.Label(previous_frame, text=l)
            label.grid(column=1, row=i, pady=1, sticky=tk.W)
            label.grid_propagate(False)

            text = tk.Text(previous_frame, pady=1, height=1, width=62)
            text.grid(column=3, row=i)
            text.insert(tk.END, f'{t}')
            text.configure(state=tk.DISABLED)

        new_frame.grid_rowconfigure(0, minsize=padding)
        new_frame.grid_rowconfigure(1)
        new_frame.grid_rowconfigure(2, minsize=padding)
        new_frame.grid_rowconfigure(3)
        new_frame.grid_rowconfigure(4, minsize=padding)

        new_frame.grid_columnconfigure(0, minsize=padding // 2)
        new_frame.grid_columnconfigure(1)
        new_frame.grid_columnconfigure(2, minsize=padding // 2)
        new_frame.grid_columnconfigure(3)
        new_frame.grid_columnconfigure(4, minsize=padding // 2)

        new_syringe = last_syringe.copy()
        new_syringe.pop('solder_pid', None)
        new_syringe['syringe_id'] += 1
        new_syringe['room_temperature_date'] = timestamp_to_utc_ds20k(time.time())
        if first_syringe:
            # Do not carry over certain details from another institute's last
            # syringe, they will be incorrect for a first syringe at another
            # institute.
            new_syringe['production_date'] = ''
            new_syringe['expiry_date'] = ''
            new_syringe['lot'] = ''
            new_syringe['syringe_id'] = 1
            new_syringe['institute_id'] = institute_id

        colours = {}
        for key in new_syringe:
            if key in {'institute_id', 'mass', 'manufacturer', 'solder_type'}:
                # non-editable fields
                colours[key] = ['black', 'white']
            elif key in {'syringe_id', 'room_temperature_date'}:
                # editable fields, but automatically changed by this script
                colours[key] = ['black', 'cadetblue1']
            else:
                # everything else is editable
                colours[key] = ['black', 'burlywood1']

        text_widgets = {}
        for i, (l, t) in enumerate(new_syringe.items()):
            label = tk.Label(new_frame, text=l)
            label.grid(column=1, row=i, pady=1, sticky=tk.W)
            label.grid_propagate(False)

            text = tk.Text(new_frame, pady=1, height=1, width=62)
            text.grid(column=3, row=i)
            text.insert(tk.END, f'{t}')

            if l in {'institute_id', 'mass', 'manufacturer', 'solder_type'}:
                text.configure(state=tk.DISABLED)

            fg, bg = colours[l]
            text.configure(bg=bg, fg=fg)
            text_widgets[l] = text

        # buttons

        # ensure button can be right justified inside frame (weight usage)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        button_cancel = tk.Button(
            button_frame,
            text='CANCEL',
            command=lambda: self.release(top),
        )
        button_cancel.grid(column=0, row=0, sticky=tk.W)

        button_post = tk.Button(
            button_frame,
            text='POST TO DATABASE',
            # colours for button mouseover
            activebackground='crimson', activeforeground='white',
            # standard colours
            bg='firebrick', fg='white',
            command=lambda: self.post_solder(top, text_widgets, institute_id)
        )
        button_post.grid(column=1, row=0, sticky=tk.E)

        # pop up should take focus from main window until dismissed
        #
        # If there are many error messages, there is the risk that the user
        # may not be able to see them all, since they cannot interact with
        # the main window while the pop-up is active.
        top.grab_set()

    def import_vtile_from_db_popup(self):
        """
        Leave previously entered content in the QR code combobox.
        """
        # create pop-up window

        padding = 8

        current_w = self.root.winfo_width()
        current_h = self.root.winfo_height()

        root_win_x, root_win_y = map(int, self.root.geometry().split('+')[1:])

        popup_x = root_win_x + (current_w // 2) - (self.import_w // 2)
        popup_y = root_win_y + (current_h // 2) - (self.import_h // 2)

        top = tk.Toplevel(self.root)
        top.geometry(f'{self.import_w}x{self.import_h}+{popup_x}+{popup_y}')
        top.resizable(False, False)
        top.title('Import vTIle from database')

        # add frame

        local_frame = tk.Frame(
            top,
            width=self.import_w,
            height=self.import_h,
        )
        local_frame.grid(sticky='nsew', row=0, column=0)
        local_frame.grid_propagate(False)

        # add padding between elements

        local_frame.grid_rowconfigure(0, minsize=padding * 2)
        local_frame.grid_rowconfigure(1)
        local_frame.grid_rowconfigure(2, minsize=padding)
        local_frame.grid_rowconfigure(3)
        local_frame.grid_rowconfigure(4, minsize=padding * 2)
        local_frame.grid_rowconfigure(5)
        local_frame.grid_rowconfigure(6, minsize=padding * 2)

        local_frame.grid_columnconfigure(0, minsize=padding * 2)
        local_frame.grid_columnconfigure(1, weight=1)
        local_frame.grid_columnconfigure(2, minsize=padding * 2)
        local_frame.grid_columnconfigure(3, weight=1)
        local_frame.grid_columnconfigure(4, minsize=padding * 2)

        # populate

        # With vTile repairs now active, there may be more than one row per
        # vTile.
        pre_production_sernos = {*range(87), 123}
        try:
            vtile_qrcodes = interface.sort_qrcodes_by_serial_number(
                set(
                    q for q in self.dbi.vtile_qrcodes()
                    if int(q[-8:-3]) not in pre_production_sernos
                )
            )
        except TypeError:
            self.print_to_console('ERROR: No response from database')
            top.destroy()
            return

        label = tk.Label(local_frame, text='Production QR code')
        label.grid(column=1, row=1, columnspan=3)

        # Keeping the textvariable value the same as the main QR code
        # field 'qrcode' would ensure the value selected here is transferred
        # to the main QR code combobox. This would be convenient, but we don't
        # want that transfer to occur unless the user clicks on OK.
        self.qrcode_combobox_repair = Supplemental(
            local_frame,
            textvariable='qrcode_repair',
            values=[qrcode_chunk(q) for q in vtile_qrcodes],
            state='normal',
            width=20,
        )
        self.qrcode_combobox_repair.grid(sticky='nsew', column=1, row=3, columnspan=3)
        self.qrcode_combobox_repair.bind('<Key>', self.handle_ctrl_key_qr_repair)

        button_cancel = tk.Button(
            local_frame,
            text='CANCEL',
            command=lambda: self.release(top),
        )
        button_cancel.grid(column=1, row=5)

        button_post = tk.Button(
            local_frame,
            text='IMPORT',
            command=lambda: self.update_gui_from_db_vtile(top, label),
        )
        button_post.grid(column=3, row=5)

    ##########################################################################
    # Handle cut-and-paste
    ##########################################################################

    def handle_ctrl_key_comment(self, event):
        """
        Enable ctrl/command-V paste into the comment combobox.

        ----------------------------------------------------------------------
        args
            event : tkinter.Event
        ----------------------------------------------------------------------
        returns : none
        ----------------------------------------------------------------------
        """
        if self.paste_detected(event):

            # find start of text selection needed for paste later
            try:
                start = self.comment_combobox.index('sel.first')
            except tk.TclError:
                # no text was selected
                position = tk.INSERT
            else:
                position = start
                self.comment_combobox.delete(tk.SEL_FIRST, tk.SEL_LAST)

            # paste text
            self.comment_combobox.insert(
                position, self.root.selection_get(selection='CLIPBOARD')
            )

    def handle_ctrl_key_qr(self, event):
        """
        Enable ctrl/command-V paste into the QR code combobox.

        ----------------------------------------------------------------------
        args
            event : tkinter.Event
        ----------------------------------------------------------------------
        returns : none
        ----------------------------------------------------------------------
        """
        if self.paste_detected(event):

            # find start of text selection needed for paste later
            try:
                start = self.qrcode_combobox.index('sel.first')
            except tk.TclError:
                # no text was selected
                position = tk.INSERT
            else:
                position = start
                self.qrcode_combobox.delete(tk.SEL_FIRST, tk.SEL_LAST)

            # paste text
            self.qrcode_combobox.insert(
                position, self.root.selection_get(selection='CLIPBOARD')
            )

    def handle_ctrl_key_qr_repair(self, event):
        """
        Enable ctrl/command-V paste into the QR code combobox.

        ----------------------------------------------------------------------
        args
            event : tkinter.Event
        ----------------------------------------------------------------------
        returns : none
        ----------------------------------------------------------------------
        """
        if self.paste_detected(event):

            # find start of text selection needed for paste later
            try:
                start = self.qrcode_combobox_repair.index('sel.first')
            except tk.TclError:
                # no text was selected
                position = tk.INSERT
            else:
                position = start
                self.qrcode_combobox_repair.delete(tk.SEL_FIRST, tk.SEL_LAST)

            # paste text
            self.qrcode_combobox_repair.insert(
                position, self.root.selection_get(selection='CLIPBOARD')
            )

    def paste_detected(self, event):
        """
        Handle cross platform paste. KeyPress events are quite different
        between platforms.

        macOS:
        state=Mod2 keysym=v keycode=17 char='v'

        Linux:
        state=Control|Mod2 keysym=v keycode=55 char='\x16'

        Windows 10:
        send_event=True state=Control keysym=v keycode=86 char='\x16'
        """
        if self.system == 'Darwin':
            # macOS Ventura 13.6.5
            return event.keycode == 17 and event.state == 16

        if self.system == 'Linux':
            # Pop!_OS 22.04 LTS x86_64 + Debian GNU/Linux 12 (bookworm) aarch64
            return event.keycode == 55 and event.state == 20

        if self.system == 'Windows':
            # MWS Windows 10
            return event.keycode == 17 and event.state == 16

        # ASSUME anything else is related to Linux
        return event.keycode == 55 and event.state == 20

    ##########################################################################
    # Change the GUI interface state
    ##########################################################################

    @staticmethod
    def clear_cache():
        """
        Clear cache of wafer and SiPM PIDs.

        --------------------------------------------------------------------------
        args : none
        --------------------------------------------------------------------------
        returns : none
        --------------------------------------------------------------------------
        """
        get_sipm_pid_wrapper.cache_clear()
        get_wafer_pid_wrapper.cache_clear()

    def clear_gui(self, persist=False):
        """
        Return all drop-down menus and labels to their default state, discarding
        all user-entered information. Disable the submit button.

        --------------------------------------------------------------------------
        args
            widgets : list of class Widget
                Contains details of GUI widgets.
            persist : bool
                Allows values stored in the console and institute combobox to
                remain unchanged
        --------------------------------------------------------------------------
        returns : none
            GUI state affected
        --------------------------------------------------------------------------
        """
        for widget in self.widgets:
            if widget.itype in (Itype.COMBOBOX, Itype.LABEL, Itype.BUTTON):
                if widget.instance == self.institute_combobox and persist:
                    continue
                widget.instance.set_default()
            elif widget.itype == Itype.TEXT:
                if widget.instance == self.console_widget and persist:
                    continue
                widget.instance.configure(state=tk.NORMAL)
                widget.instance.delete('1.0', tk.END)
                widget.instance.configure(state=tk.DISABLED)

        self.strict_solder_syringe_checking.set(True)

        # Menu bar, Repair, repair mode: remove tick
        self.set_manufacturing_mode()

    def clear_gui_load_defaults(self):
        """
        Return the GUI state to that set at application start.

        --------------------------------------------------------------------------
        args
            widgets : list of class Widget
                Contains details of GUI widgets.
            defaults_file_path : string
                e.g. '/Users/avt/.ds20kdb_defaults'
        --------------------------------------------------------------------------
        returns : none
            GUI state affected
        --------------------------------------------------------------------------
        """
        self.clear_gui()
        self.load_defaults()
        self.set_date_time_gui()

    def clear_gui_sipms_only(self):
        """
        Return all SiPM drop-down menus and labels to their default state,
        discarding all user-entered information.

        ----------------------------------------------------------------------
        args
            widgets : list of class Widget
                Contains details of GUI widgets.
        ----------------------------------------------------------------------
        returns : none
            GUI state affected
        ----------------------------------------------------------------------
        """

        for widget in self.widgets:
            if widget.cluster.startswith('sipm_') and widget.itype in (Itype.COMBOBOX, Itype.LABEL):
                widget.instance.set_default()

    def clear_submit_button(self):
        """
        Disable the submit button.

        ----------------------------------------------------------------------
        args
            widgets : list of class Widget
                Contains details of GUI widgets.
        ----------------------------------------------------------------------
        returns : none
            GUI state affected
        ----------------------------------------------------------------------
        """
        for widget in self.widgets:
            if widget.cluster == 'submit' and widget.itype == Itype.BUTTON:
                widget.instance.set_default()

    def get_from_console(self):
        """
        Return contents of the console.

        ----------------------------------------------------------------------
        args
            widgets : list of class Widget instances
            line : string
        ----------------------------------------------------------------------
        returns : none
            GUI state affected
        ----------------------------------------------------------------------
        """
        return self.console_widget.get('1.0', tk.END)

    def print_to_console(self, line):
        """
        Print log messages to the GUI console.

        ----------------------------------------------------------------------
        args
            widgets : list of class Widget instances
            line : string
        ----------------------------------------------------------------------
        returns : none
            GUI state affected
        ----------------------------------------------------------------------
        """
        # ensure line is terminated
        line = line if line.endswith('\n') else f'{line}\n'

        self.console_widget.configure(state=tk.NORMAL)
        self.console_widget.insert(tk.END, line)
        self.console_widget.configure(state=tk.DISABLED)

        # scroll to the end of the console text
        self.console_widget.update()
        self.console_widget.yview(tk.END)

    def refresh_solder(self, _event=None):
        """
        Update the "PID of solder syringe" drop down box with values from the
        database when the user changes menu bar option
        "strict solder syringe checking".

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns : none
            GUI state affected
        ----------------------------------------------------------------------
        """
        # find solder combobox widget
        solder_items = self.solder_combobox

        institute_text = self.institute_combobox.get()
        if not institute_text:
            solder_items.set('')
            solder_items.configure(values=[])
            return

        institute_id = self.dbi.get_institute_id(institute_text).data
        sold = self.dbi.get_relevant_solder_ids(
            institute_id, strict=self.strict_solder_syringe_checking.get()
        )
        if sold is None:
            sold = []

        # Clear any existing user choice, then reload combobox with values
        # appropriate for the new institute.
        solder_items.set('')
        solder_items.configure(values=sold)
        if len(sold) == 1:
            solder_items.set(sold[0])

    def update_solder(self, institute_id, force=True):
        """
        Update the "PID of solder syringe" drop down box from the database.

        ----------------------------------------------------------------------
        args
            institute_id : int
            force : boolean
                This is used to bypass the default behaviour where a lone
                solder syringe in the combobox is selected, which may
                overwrite the existing selected value.
        ----------------------------------------------------------------------
        returns : none
            GUI state affected
        ----------------------------------------------------------------------
        """
        sold = self.dbi.get_relevant_solder_ids(institute_id)

        # find solder combobox widget
        solder_items = self.solder_combobox

        # Clear any existing user choice, then reload combobox with values
        # appropriate for the new institute.
        if force:
            solder_items.set('')

        solder_items.configure(values=sold)

        if len(sold) == 1 and force:
            solder_items.set(sold[0])

    def refresh_qrcodes(self):
        """
        Update the QR code drop down box with values from the database. This
        is typically called when the user has successfully submitted a
        vTile.

        ----------------------------------------------------------------------
        args
            widgets : list
            dbi : ds20kdb.interface.Database
                Instance of the Database interface class; allows communication
                with the database.
        ----------------------------------------------------------------------
        returns : none
            GUI state affected
        ----------------------------------------------------------------------
        """
        self.print_to_console('vTile submitted: updating QR codes.')

        qrcodes_not_allocated_to_vtiles = self.dbi.get_relevant_qrcodes()
        if qrcodes_not_allocated_to_vtiles is None:
            qrcodes_not_allocated_to_vtiles = []

        # Clear any existing user choice, then reload combobox with values
        # appropriate for the new institute.
        self.qrcode_combobox.set('')
        self.qrcode_combobox.configure(
            values=[
                qrcode_chunk(q) for q in qrcodes_not_allocated_to_vtiles
            ]
        )

    @staticmethod
    def set_button_state(button, disabled):
        """
        Generic set button state normal/disabled

        --------------------------------------------------------------------------
        args
            button : ButtonSubmit
                widget instance
            disabled : bool
                label status
        --------------------------------------------------------------------------
        returns : none
            GUI state affected
        --------------------------------------------------------------------------
        """
        button.configure(state=tk.DISABLED if disabled else tk.NORMAL)

    def set_date_time_gui(self):
        """
        Set the date and time in the GUI to the time now in UTC.

        --------------------------------------------------------------------------
        args : none
        --------------------------------------------------------------------------
        returns : none
            GUI state changed
        --------------------------------------------------------------------------
        """
        default_index = self.default_date_time()

        for category, widget_instance in self.datetime_comboboxes.items():
            widget_instance.current(default_index[category])

    @staticmethod
    def set_label_colour(label, good, unchanged=False):
        """
        Set the label colour of an individual widget to green (good=True),
        red (good=False) or blue (unchanged=True).

        Used for indicating to the user whether the values they have entered
        are correct.

        ----------------------------------------------------------------------
        args
            label : ColourLabel
                widget instance
            good : bool
                label status
            unchanged : bool
                State only used when repairing a vTile that already exists in
                the database. The blue colour is used to indicate that a SiPM
                has been imported from the database, and has not been changed
                by the user. It will be marked internally as 'good' and no
                checks will be performed on its validity.
        ----------------------------------------------------------------------
        returns : none
        ----------------------------------------------------------------------
        """
        colour = '#0000B0' if unchanged else '#00B000' if good else '#C00000'
        label.configure(foreground=colour)

    def update_gui_from_dict(self, table_json):
        """
        Used to update the GUI after a JSON file has been loaded.

        --------------------------------------------------------------------------
        args
            table_json : dict
                e.g. {
                    'sipm_19|lot_number': '9262109',
                    'sipm_19|wafer_number': '15',
                    'sipm_19|column': '10',
                    'sipm_19|row': '21', ...
                }
        --------------------------------------------------------------------------
        returns : none
            GUI state affected
        --------------------------------------------------------------------------
        """
        for k, wval in table_json.items():
            wclu, wcat = k.split('|')
            if wcat == 'None':
                wcat = None

            with contextlib.suppress(StopIteration):
                widget = next(
                    w for w in self.widgets
                    if w.cluster == wclu and w.category == wcat and w.itype == Itype.COMBOBOX
                )
                widget.instance.set(wval)

    ##########################################################################
    # properties
    ##########################################################################

    @functools.cached_property
    def console_widget(self):
        """
        Find the console widget. There's only one entry for it, so we can
        simply return the first search result.

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns : tk.Text
        ----------------------------------------------------------------------
        """
        return next(
            filter(lambda w: w.cluster == 'console', self.widgets)
        ).instance

    @functools.cached_property
    def qrcode_combobox(self):
        """
        Find the QR code widget. There's only one entry for it, so we can simply
        return the first search result.

        --------------------------------------------------------------------------
        args : none
        --------------------------------------------------------------------------
        returns : tk.ttk.Combobox
        --------------------------------------------------------------------------
        """
        return next(
            filter(
                lambda w: w.cluster == 'qrcode' and w.itype == Itype.COMBOBOX,
                self.widgets,
            )
        ).instance

    @functools.cached_property
    def solder_combobox(self):
        """
        Find the QR code widget. There's only one entry for it, so we can
        simply return the first search result.

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns : tk.ttk.Combobox
        ----------------------------------------------------------------------
        """
        return next(
            filter(
                lambda w: w.cluster == 'solder_id' and w.itype == Itype.COMBOBOX,
                self.widgets,
            )
        ).instance

    @functools.cached_property
    def comment_combobox(self):
        """
        Find the QR code widget. There's only one entry for it, so we can
        simply return the first search result.

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns : tk.ttk.Combobox
        ----------------------------------------------------------------------
        """
        return next(
            filter(
                lambda w: w.cluster == 'comment' and w.itype == Itype.COMBOBOX,
                self.widgets,
            )
        ).instance

    @functools.cached_property
    def institute_combobox(self):
        """
        Find the QR code widget. There's only one entry for it, so we can
        simply return the first search result.

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns : tk.ttk.Combobox
        ----------------------------------------------------------------------
        """
        return next(
            filter(
                lambda w: w.cluster == 'institute' and w.itype == Itype.COMBOBOX,
                self.widgets,
            )
        ).instance

    @functools.cached_property
    def institute_label(self):
        """
        Find the institute label widget. There's only one entry for it, so we
        can simply return the first search result.

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns : class ColourLabel(ttk.Label)
        ----------------------------------------------------------------------
        """
        return next(
            filter(
                lambda w: w.cluster == 'institute' and w.itype == Itype.LABEL,
                self.widgets,
            )
        ).instance

    @functools.cached_property
    def datetime_comboboxes(self):
        """
        Find the widgets for the production date comboboxes.

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns : dict
            {string: tk.ttk.Combobox, ...}
        ----------------------------------------------------------------------
        """
        return {
            w.category: w.instance
            for w in self.widgets
            if w.cluster == 'production_date' and w.itype == Itype.COMBOBOX
        }

    ##########################################################################
    # utilities
    ##########################################################################

    def database_alive(self):
        """
        Check if a connection to the database exists, and that it's
        responsive. In the process, load a small table that will be useful
        later.

        ----------------------------------------------------------------------
        args
            dbi : ds20kdb.interface.Database
                Instance of the Database interface class; allows communication
                with the database.
        ----------------------------------------------------------------------
        returns : pandas.core.frame.DataFrame
            contents of the entire wafer table
        ----------------------------------------------------------------------
        """
        response = self.dbi.get('wafer')

        if response.network_timeout:
            sys.exit('Check network connection: timeout')

        if response.data is None:
            sys.exit('No response from database')

        return response.data

    ##########################################################################
    # handling user-supplied values
    ##########################################################################

    def date_time_values_to_timestamp(self, dtf, table):
        """
        Convert discrete date/time values to a timestamp acceptable to the
        database.

        ----------------------------------------------------------------------
        args
            dtf : dict
                {string: {string: tk.Label, string: string}, ...}
                    e.g.
                        {
                            'year': {'label': tk.Label, 'year': '2022'},
                            'month': {'label': tk.Label, 'month': '12'},
                            ...
                        }
                Contains user-entered values from date/time related comboboxes.
            widgets : list of class Widget
                Contains details of GUI widgets.
            table : dict
        ----------------------------------------------------------------------
        returns
            table : dict
                no explicit return, mutable type amended in place
        ----------------------------------------------------------------------
        """
        timestamp = None

        # The DarkSide-20k database requires UTC date/time in this format:
        # YYYY-MM-DD hh:mm:ss, e.g. 2022-07-19 07:00:00
        date_time_string = (
            f'{dtf["year"]}-{dtf["month"]}-{dtf["day"]} '
            f'{dtf["hour"]}:{dtf["minute"]}:00'
        )
        with contextlib.suppress(ValueError):
            timestamp = parse(date_time_string, fuzzy=False).strftime('%Y-%m-%d %H:%M:%S')

        good = timestamp is not None

        # set colour of all date/time labels
        for widget in self.widgets:
            if widget.cluster == 'production_date' and widget.itype == Itype.LABEL:
                self.set_label_colour(widget.instance, good)

        if good:
            table['production_date'] = timestamp
        else:
            self.print_to_console('production date: incomplete/incorrect')

    @staticmethod
    def valid_ds20k_timestamp(date_time_string):
        """
        Check if a date/time string is formatted correctly for the ds20k
        database.

        ----------------------------------------------------------------------
        args
            date_time_string : string
                e.g. YYYY-MM-DD hh:mm:ss, 2022-07-19 07:00:00, timezone UTC
        ----------------------------------------------------------------------
        returns : bool
        ----------------------------------------------------------------------
        """
        try:
            parse(date_time_string, fuzzy=False).strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            return False

        return True

    def default_date_time(self):
        """
        Generate indices for the GUI's date/time drop-down boxes to match the
        date/time now.

        This script should be run on the day the vTile is manufactured,
        specifically just before the die-attach process. This is to ensure
        (1) we don't have any SiPMs that are already allocated to another
        vTile, and(2) that all SiPMs are of production standard according to
        the current state of the database. It's important these checks are
        made before we permanently bond the dies to the PCB. Hence, we'll
        default the GUI date/time drop-down boxes to today's date/time to
        save the user a few clicks.

        We'll work in UTC here for consistency. Since no-one's likely to be
        working around midnight, it shouldn't make any practical difference.

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns : dict
        ----------------------------------------------------------------------
        """
        utc = datetime.datetime.fromtimestamp(
            time.time(), datetime.timezone.utc
        )

        try:
            current_year_index = self.dt_range['years'].index(utc.year)
        except ValueError:
            # this script may be run in some distant future year
            current_year_index = None

        return {
            'year': current_year_index,
            'month': self.dt_range['months'].index(utc.month),
            'day': self.dt_range['days'].index(utc.day),
            'hour': self.dt_range['hours'].index(utc.hour),
            'minute': utc.minute // 15,
        }

    def process_other(self, table, other_definition):
        """
        Process any field that isn't a SiPM or a timestamp.

        All the values retrieved from the comboboxes were derived from the
        database, and none of the combobox values can contradict the others.
        It's still possible for database look-ups based on these values to
        fail.

        ----------------------------------------------------------------------
        args
            table : dict
            other_definition : tuple (string, string)
                (combobox widget cluster name, combobox widget value)
        ----------------------------------------------------------------------
        returns : none
        ----------------------------------------------------------------------
        """
        cluster, value = other_definition

        # get label associated with this widget combobox
        other_label_widget = next(
            w.instance for w in self.widgets
            if w.cluster == cluster and w.itype == Itype.LABEL
        )

        # exit early if the user hasn't selected a value from the drop-down menu
        user_selected_nothing = not bool(value)
        if user_selected_nothing and cluster != 'comment':
            self.print_to_console(f'{cluster}: no value selected')
            self.set_label_colour(other_label_widget, good=False)
            return

        # perform database look-ups for those fields that require it
        good = False

        if cluster == 'qrcode':
            # Even though the QR codes in the drop-down menu were obtained from
            # the database, there is a possibility that this database look-up
            # will fail if related content (vpcb_asic table) is missing/incorrect.
            response = self.dbi.get_vpcb_asic_pid_from_qrcode(qrcode_normal(value))
            vpcb_asic_pid = response.data
            if vpcb_asic_pid is None:
                self.print_to_console(f'{cluster}: failed vpcb_asic_pid look-up')
            else:
                good = True
                table['vpcb_asic_id'] = vpcb_asic_pid

        elif cluster == 'institute':
            # This database look-up should only fail if related database entries
            # were deleted/amended after this application was initially run.
            institute_id = self.dbi.get_institute_id(value).data
            if institute_id is None:
                self.print_to_console(f'{cluster}: no match found')
            else:
                good = True
                table['institute_id'] = institute_id

        elif cluster == 'solder_id':
            if self.strict_solder_syringe_checking.get():
                # strict check

                # Prevent POST if syringe is past expiry date or has been at room
                # temp for more than 30 days. It should not be possible to select
                # a solder syringe that is out of date, since the GUI will only
                # display in-date syringes.
                sold = self.dbi.get('solder', solder_pid=value).data.to_dict('records')[-1]

                dt_now = datetime.datetime.now()
                dt_exp = datetime.datetime.strptime(
                    sold['expiry_date'], '%Y-%m-%d %H:%M:%S'
                )
                dt_rtd = datetime.datetime.strptime(
                    sold['room_temperature_date'],
                    '%Y-%m-%d %H:%M:%S'
                )
                dt_rtd_p30 = dt_rtd + datetime.timedelta(days=30)

                solder_fail = False
                if dt_now > dt_exp:
                    self.print_to_console(f'{cluster}: check expiry date')
                    solder_fail = True
                if dt_now > dt_rtd_p30:
                    self.print_to_console(
                        f'{cluster}: check duration at room temperature'
                    )
                    solder_fail = True

                # Database entry should be performed at time of die attach, so we
                # can warn the user if the syringe they've selected has been at
                # room temperature too long, or if it's past its expiry date.
                good = not solder_fail
                if good:
                    table[cluster] = value
            else:
                # The user explicitly chosen this, so it's at their own risk.
                table[cluster] = value
                good = True

        else:
            # run_number and comment require no transformation or look-up
            good = True
            table[cluster] = value

        self.set_label_colour(other_label_widget, good=good)

    def process_sipm(self, table, used_sipms, sipm_definition, errors):
        """
        Process a single SiPM - check if the user-entered data makes sense:

        (1) Have all fields been entered?
        (2) Is the given (column, row) position a valid location on the wafer
        (3) Does the SiPM as defined by wafer and location exist in the
            database?

        ----------------------------------------------------------------------
        args
            table : dict
            used_sipms : dict
            sipm_definition : dict
            errors: list of strings
        ----------------------------------------------------------------------
        returns
            no explicit return, mutable types amended in place
                errors: list of strings
                table : dict
                used_sipms : dict
        ----------------------------------------------------------------------
        """
        sipm_ident, sipm_params = sipm_definition
        sipm_num = int(sipm_ident.split('_')[-1])

        # initial checks
        #
        # (1) all fields are present?
        # (2) wafer location allowable?

        try:
            lot_number = sipm_params['lot_number']
            wafer_number = sipm_params['wafer_number']
            column = sipm_params['column']
            row = sipm_params['row']
        except KeyError:
            # at least one field was missing
            errors.append(f'SiPM {sipm_num:>2}: missing field(s)')
            return

        if (column, row) not in self.valid_locations:
            errors.append(
                f'SiPM {sipm_num:>2}: invalid wafer location (col={column}, row={row})'
            )
            return

        # database checks

        # If we have the SiPM ID already (only applies for a vTile repair,
        # where the probability is high) avoid the following two database
        # look-ups. For a repair, the associated production standard checks
        # can also be safely ignored since these SiPMs are already bonded to
        # the vTile and have been previously vetted.
        location = (column, row, lot_number, wafer_number)
        try:
            sipm_pid = self.repair_sipm_location_to_id_lut[location]
        except KeyError:
            pass
        else:
            table[sipm_ident] = sipm_pid
            used_sipms[sipm_pid].add(sipm_num)
            return

        # see if this sipm as described can be found in the database
        sipm = SiPM(self.dbi, *location)
        sipm_pid = sipm.sipm_pid

        if sipm_pid is not None:
            # store this PID even if it is already in used_sipms
            # we will manually remove all duplicates later in one go
            table[sipm_ident] = sipm_pid
            used_sipms[sipm_pid].add(sipm_num)

            # Issue warning if this SiPM is not production standard. This may
            # be triggered in the unlikely case that the wafer was picked using an
            # old wafer map generated using a classification-only check.

            dfr_tmp = self.dbi.get('sipm_test', sipm_id=sipm_pid).data
            columns = ['classification', 'quality_flag', 'sipm_qc_id']

            # Get columns for row with highest sipm_qc_id value.
            try:
                classification, quality_flag, _ = dfr_tmp[columns].sort_values('sipm_qc_id').values[-1]
            except IndexError:
                # We will see IndexError for the four SiPMs at the far left/right
                # edges that are not tested.
                pass
            else:
                if not (classification == 'good' and quality_flag == 0):
                    errors.append(
                        f'SiPM {sipm_num:>2}: WARNING: '
                        f'NOT PRODUCTION STANDARD (sipm_pid={sipm_pid})'
                    )
        else:
            errors.append(
                f'SiPM {sipm_num:>2}: could not be found in the database'
            )

    def _identify_sipms_db_check(self, table):
        """
        ----------------------------------------------------------------------
        args
            table : dict
                contains SiPM idents and IDs
                e.g. {'sipm_1': 377314, ..., 'sipm_24': 377269}
        ----------------------------------------------------------------------
        returns
            sipm_pids : set of int
            unchanged : set of int
                IDs for the SiPMs that the user loaded from the db, but did
                not change.
            unchanged_idents : set of str
                e.g. {'sipm_17', ...}
        ----------------------------------------------------------------------
        """
        # SiPM PIDs from devices listed in the GUI
        sipm_pids = set(table.values())

        if self.repair_mode.get():
            # originally loaded from db
            skip_check_for_sipms = set(self.repair_row_sipms.values())

            unchanged = sipm_pids.intersection(skip_check_for_sipms)
            edited_sipm_ids = sipm_pids.difference(skip_check_for_sipms)

            unchanged_idents = {
                ident
                for ident, sipm_id in self.repair_row_sipms.items()
                if sipm_id in unchanged
            }

            # Get the physical SiPM ident numbers for all edited SiPMs so
            # these may be used to add details of the repair to the comment
            # combobox.
            sipm_numbers = {
                int(sipm_ident.split('_')[-1])
                for sipm_ident, sipm_pid in table.items()
                if sipm_pid in edited_sipm_ids
            }
            self.autofill_comment_replaced_sipms(sipm_numbers)
        else:
            unchanged = set()
            unchanged_idents = set()

        return sipm_pids, unchanged, unchanged_idents

    def check(self):
        """
        Check all information the user entered into the GUI drop-down menus.

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns
            Error log written to console.
        ----------------------------------------------------------------------
        """
        table = {}
        used_sipms = collections.defaultdict(set)

        ######################################################################
        self.print_to_console(
            f'Check start: {timestamp_to_utc_ds20k(time.time())}'
        )

        ######################################################################
        # container for deferred error messages
        errors = []

        ######################################################################
        # check values in user-entered comboboxes - and recolour labels based
        # on their validity

        # e.g. {'year': '2024', 'month': '2', 'day': '3', 'hour': '3', 'minute': '15'})
        timestamp_parts = collections.defaultdict(dict)

        # e.g. {'sipm_1: {'lot_number': 9262109, 'wafer_number': 5, ...}, ...'}
        sipm_definitions = collections.defaultdict(dict)

        # e.g. {
        #          'institute': 'University of Liverpool',
        #          'solder_id': '4',
        #          'qrcode': '22061703000047001',
        #          'run_number': '3'
        #      }
        other_definitions = {}

        # collect user-submitted information from GUI widgets

        combobox_widgets = filter(lambda w: w.itype == Itype.COMBOBOX, self.widgets)

        for widget in combobox_widgets:

            if widget.cluster.startswith('sipm_'):
                with contextlib.suppress(ValueError):
                    sipm_definitions[widget.cluster].update(
                        {widget.category: int(widget.instance.get())}
                    )
            elif widget.cluster == 'production_date':
                timestamp_parts[widget.category] = widget.instance.get()
            else:
                other_definitions[widget.cluster] = widget.instance.get()

        # sipm_definitions = {
        # 'sipm_1': {'lot_number': 9324029, 'wafer_number': 5, 'column': 14, 'row': 15},
        # ...
        # }

        # check SiPMs, this sets table = {sipm_ident: sipm_pid, ...}
        for sipm_definition in sipm_definitions.items():
            self.process_sipm(
                table, used_sipms, sipm_definition, errors
            )

        # table = {
        #     'sipm_1': 1438,
        #     ...
        #     'sipm_24': 1367,
        # }

        ######################################################################
        # issue warnings about any locally (GUI) duplicated SiPMs
        for sipm_numbers in used_sipms.values():
            if len(sipm_numbers) < 2:
                continue

            for sipm_number in sipm_numbers:
                table.pop(f'sipm_{sipm_number}')
                errors.append(f'SiPM {sipm_number:>2}: duplicate')

        ######################################################################
        # Check if any user-submitted SiPMs are already allocated to vTiles
        # in the database. The call to get_sipms_allocated will become
        # increasingly expensive as the database is populated.
        #
        # If repair mode is set then we will need to suspend checks on the
        # SiPMs brought over from the datebase, only checking those that the
        # user has changed.

        sipm_pids, unchanged, unchanged_idents = self._identify_sipms_db_check(table)

        # {23: True, 34: True, ...}
        sipm_dupe_check = self.dbi.get_sipms_allocated(sipm_pids, unchanged=unchanged)

        # {23, ...}
        duplicate_sipm_pids = {
            sipm_pid
            for sipm_pid, duplicate in sipm_dupe_check.items()
            if duplicate
        }

        # {16: [4], 56: [9]}
        vtile_pids = self.dbi.get_vtile_pids_from_sipm_pids(duplicate_sipm_pids)

        lut = self.dbi.vtile_id_to_qrcode_lut()

        for field, value in table.copy().items():
            if field.startswith('sipm_') and value in duplicate_sipm_pids:
                table.pop(field)
                qrcodes = ', '.join(lut[x] for x in vtile_pids[value])
                sipm_number = int(field.split('_')[-1])
                errors.append(
                    f'SiPM {sipm_number:>2}: already allocated to {qrcodes}'
                )

        if errors:
            self.print_to_console('\n'.join(sorted(errors)))

        ######################################################################
        # colour SiPM labels to indicate their status

        # set all SiPMs to False, only set the ones still present in table
        # (those that passed all the earlier tests) to True
        sipm_idents = {f'sipm_{x}': False for x in range(1, 24+1)}
        for field in table:
            if field.startswith('sipm_'):
                sipm_idents[field] = True

        for ident, good in sipm_idents.items():
            sipm_label_widget = next(
                w.instance for w in self.widgets
                if w.cluster == ident and w.itype == Itype.LABEL
            )
            self.set_label_colour(
                sipm_label_widget, good, ident in unchanged_idents
            )

        ######################################################################
        # check other parameters

        # check production date
        self.date_time_values_to_timestamp(timestamp_parts, table)

        # check supplementary parameters
        for other_definition in other_definitions.items():
            self.process_other(table, other_definition)

        # get the comment directly from the GUI
        if VTILE_REPAIR:
            table['comment'] = self.comment_combobox.get()

        # we'll need this for saving/exporting data file later
        self.table_json_string = json.dumps(table)

        ######################################################################
        self.print_to_console(
            f'Check complete: {timestamp_to_utc_ds20k(time.time())}\n'
        )

        ######################################################################
        # if the check passed, we can enable the submit button
        complete = len(table) == 30

        button_submit_widget = next(
            w.instance for w in self.widgets
            if w.cluster == 'submit' and w.itype == Itype.BUTTON
        )
        self.set_button_state(button_submit_widget, disabled=not complete)

        ######################################################################
        # Issue reminder for Liverpool

        # Liverpool uses version control for SiPM tray files. It's easy to
        # forget to use git pull to ensure the latest files are being used, so
        # remind the user before they press the SUBMIT button. Don't issue the
        # warning if this is a repair operation.
        inst_livp = 'Liverpool' in other_definitions['institute']
        manu_mode = not self.repair_mode.get()
        if complete and inst_livp and manu_mode:
            self.print_to_console(
                'CHECK: is this tray file up to date? Remember to use "git pull".\n'
            )

    def autofill_comment_replaced_sipms(self, sipm_numbers):
        """
        Generate repair comment based on user changes.

        It is ASSUMED that this method will only be called in repair mode.

        ----------------------------------------------------------------------
        args
            sipm_numbers : set
        ----------------------------------------------------------------------
        returns : none
            GUI state changed
        ----------------------------------------------------------------------
        """
        if not sipm_numbers:
            return

        changed_sipms = common.compact_integer_sequence(sipm_numbers)
        plural = 's:' if len(sipm_numbers) > 1 else ''

        self.comment_combobox.set(f'Replaced SiPM{plural} {changed_sipms}')

    def submit(self):
        """
        POST vTile to the production database.

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns
            Error log written to console.
        ----------------------------------------------------------------------
        """
        # get table from GUI variable
        table = json.loads(self.table_json_string)

        # add values not shown in the GUI
        if VTILE_REPAIR:
            table['version'] = self.version

        post_succeeded = False if DEBUG else self.dbi.post_vtile(table)
        loc_post_successful = False

        if post_succeeded:
            # Disable the submit button if the post succeeded to make sure the
            # user doesn't accidentally submit the same vTile more than
            # once.
            self.clear_submit_button()

            qrcode = self.dbi.get_qrcode_from_vpcb_asic_pid(table['vpcb_asic_id'])
            response = self.dbi.get(
                'vtile',
                vpcb_asic_id=table['vpcb_asic_id'],
                # obtain ID from the latest version only
                query_max_results=(1, 'version', 'd')
            )
            vtile_id = int(response.data.vtile_pid.values[-1])

            # -----------------------------------------------------------------
            # add location tag to database
            # -----------------------------------------------------------------

            loc_state = 'reworked' if self.repair_mode.get() else 'produced'

            # set location on creation of a newly manufactured vTile
            loc_table = {
                'vtile_id': vtile_id,
                'institute_id': table['institute_id'],
                'timestamp': table['production_date'],
                'comment': table['comment'],
                'state': loc_state,
            }
            loc_post_successful = self.dbi.post_item(
                loc_table, 'vtile_location'
            )

            # -----------------------------------------------------------------

            locset = 'set' if loc_post_successful else 'NOT SET'
            status = f'succeeded: {qrcode} (vtile_id {vtile_id}) (location {locset})'

            # After a successful POST, there should be at least one less QR code
            # on the list.
            self.refresh_qrcodes()

            # And clear the SiPM section, since none of that information is
            # required for the next submission
            self.clear_gui_sipms_only()

            self.set_manufacturing_mode()

        else:
            if DEBUG:
                status = 'skipped: DEBUG set'
                print('-' * 40)
                for k, v in table.items():
                    print(k, v)
            else:
                status = 'failed'

        self.print_to_console(f'POST {status}\n')

    ##########################################################################
    # repair mode handling
    ##########################################################################

    def set_repair_mode(self):
        """
        Set repair mode, disable manufacturing mode.
        """
        self.repair_mode.set(True)
        self.root.title(f'{self.base_title_text} [REPAIR]')
        self.institute_label.config(text='Repair institute')
        self.valid_locations = set(interface.wafer_map_valid_locations(legacy=True))
        self.clear_submit_button()

    def set_manufacturing_mode(self):
        """
        Set manufacturing mode, disable repair mode.
        """
        self.repair_mode.set(False)
        self.root.title(self.base_title_text)
        self.institute_label.config(text='Manufacturing institute')
        self.valid_locations = set(interface.wafer_map_valid_locations())
        self.clear_submit_button()

    def repair_mode_status(self):
        """
        Called when the repair mode is changed.

        Toggling of the variable itself is handled by the GUI.
        """
        if self.repair_mode.get():
            self.set_repair_mode()
        else:
            self.set_manufacturing_mode()

    def update_gui_from_db_vtile(self, top, label):
        """
        Given a vTile QR code fetch row(s) from the db vtile table and
        populate the GUI.

        The following fields are not propagated from the db to the GUI:

        * The repair version: this is incremented automatically.
        * Institute: since this will be replaced by the repair institute
        * Solder ID: repair will probably be performed with different solder
        * Comment: This will be replaced by the repair description
        * Date/time: The repair date will be newer

        ----------------------------------------------------------------------
        args
            top : <class 'tkinter.Toplevel'>
                The repair pop-up window
            label : <class 'tkinter.Label'>
                The status label from the repair pop-up window
        ----------------------------------------------------------------------
        returns : none
        ----------------------------------------------------------------------
        """
        qrcode = qrcode_normal(self.qrcode_combobox_repair.get())
        qr_pid_lut = self.dbi.vtile_id_to_qrcode_latest_vtile_only_lut(reverse=True)
        try:
            vtile_id = qr_pid_lut.get(qrcode)
        except AttributeError:
            # qr_pid_lut was None
            self.print_to_console(
                'Import vTile from database: no response from database'
            )
            # keep the pop-up window open
            return

        if vtile_id is None:
            self.print_to_console(
                'Import vTile from database: '
                'QR code is not yet allocated to a vTile'
            )

            # keep the pop-up window open
            return

        # only one row will be returned for any given vtile_id
        response = self.dbi.get(constants.TABLE_VTILE, vtile_pid=vtile_id)
        try:
            row = response.data.to_dict('records')[-1]
        except AttributeError:
            # response was None
            self.print_to_console(
                'Import vTile from database: no response from database'
            )
            # keep the pop-up window open
            return
        except IndexError:
            # KeyError: Caused by empty DataFrame
            self.print_to_console(
                'Import vTile from database: did not recognise QR code'
            )
            # keep the pop-up window open
            return

        # These are the SiPMs the database reports are attached to the vTile
        # {'sipm_1': 377314, ..., 'sipm_24': 377269}
        self.repair_row_sipms = {
            k: v for k, v in row.items() if k.startswith('sipm_')
        }

        ######################################################################
        # User-submitted QR code was acceptable: populate GUI
        #
        # row dict contents
        #
        # 'vtile_pid': 48, 'vpcb_asic_id': 21,
        # 'sipm_1': 1438, 'sipm_2': 1571, 'sipm_3': 1362, 'sipm_4': 1538,
        # 'sipm_5': 1510, 'sipm_6': 1561, 'sipm_7': 1366, 'sipm_8': 1581,
        # 'sipm_9': 1461, 'sipm_10': 1576, 'sipm_11': 1483, 'sipm_12': 1539,
        # 'sipm_13': 1413, 'sipm_14': 1360, 'sipm_15': 1474, 'sipm_16': 1381,
        # 'sipm_17': 1463, 'sipm_18': 1534, 'sipm_19': 1553, 'sipm_20': 1558,
        # 'sipm_21': 1600, 'sipm_22': 1429, 'sipm_23': 1596, 'sipm_24': 1367,
        # 'vpdu_id': nan, 'run_number': 1,
        # 'production_date': '2022-08-04 00:00:00',
        # 'solder_id': 8, 'institute_id': 6, 'comment': nan
        #
        # Transform into data dict for GUI update:
        #
        # For each SiPM:
        #
        # 'sipm_1|lot_number': '9333239',
        # 'sipm_1|wafer_number': '25',
        # 'sipm_1|column': '11',
        # 'sipm_1|row': '5',
        #
        # and the rest:
        #
        # 'institute|None': 'University of Liverpool',
        # 'qrcode|None': '24020513002184001',
        # 'solder_id|None': '41',
        # 'run_number|None': '6',
        # 'comment|None': 'test',
        # 'production_date|year': '2024',
        # 'production_date|month': '8',
        # 'production_date|day': '2',
        # 'production_date|hour': '12',
        # 'production_date|minute': '15'
        #
        # solder_id is left blank in the GUI. It's highly unlikely that the
        # solder used to make the vTile would still be valid, in-date and
        # available at the repair institute, for a repair to be performed
        # with it. The repair solder will almost always be different to the
        # original, and it's too easy for users to forget to to change it, so
        # force the user to choose a solder syringe.
        ######################################################################

        # The next step will require some database access and may take a few
        # seconds to complete, so leave the pop-up window in place, so the
        # user isn't left wondering why nothing appears to be happening.
        label.config(text='importing from database, please wait...', fg='red')

        self.print_to_console(
            f'Import vTile from database: {qrcode=}, {vtile_id=}'
        )

        # prepare data structure for GUI update

        data = {}

        # version : this field may not exist at this time.  For a repair, we
        # will need to set the version number one higher than the value in
        # the database, so it the data
        version = row.get('version')
        if version is None:
            self.print_to_console(
                'No version information for this vTile, setting to 1'
            )
            version = 1
        else:
            self.print_to_console(
                f'Latest vTile version on database: {version}'
            )

        self.version = version + 1
        data['version|None'] = self.version
        self.repair_sipm_location_to_id_lut = {}

        # Obtain origin of all SiPMs (lot/number/col/row)
        for ident, sipm_id in self.repair_row_sipms.items():
            # e.g. {'lot': 9262109, 'wafer_number': 3, 'column': 9, 'row': 18}
            origin = self.dbi.get_wafer_location_from_sipm_pid(sipm_id)

            # use this as a cache to avoid db lookup later
            # {(16, 14, 9262109, 24): 377314, ...}
            self.repair_sipm_location_to_id_lut[
                common.sipm_origin_to_tuple(origin)
            ] = sipm_id

            if origin is None:
                self.print_to_console('Problem getting SiPM origin from ID')

                # keep the pop-up window open
                return

            data[f'{ident}|lot_number'] = origin['lot']
            data[f'{ident}|wafer_number'] = origin['wafer_number']
            data[f'{ident}|column'] = origin['column']
            data[f'{ident}|row'] = origin['row']

        institute_row = self.dbi.get('institute', id=row['institute_id']).data
        self.print_to_console(
            f'Previous institute: {institute_row["acronym"].values[-1]}'
        )
        self.print_to_console(f'Previous solder_id: {row["solder_id"]}')

        data['qrcode|None'] = qrcode_chunk(qrcode)
        data['run_number|None'] = row['run_number']

        try:
            math.isnan(row['comment'])
        except TypeError:
            # there was a comment in the database which came across as a string
            comment_text = row['comment']
        else:
            # an empty comment in the db will show up as a float with a NaN
            # value, so replace this with an empty string
            comment_text = ''

        self.print_to_console(f'Previous comment: "{comment_text}"')

        # date/time
        #
        # Repairs will most probably be done on the current date, so we should
        # set that for the user, ignoring the date/time read from the db.

        utc = datetime.datetime.fromtimestamp(
            time.time(), datetime.timezone.utc
        )
        data['production_date|year'] = utc.year
        data['production_date|month'] = utc.month
        data['production_date|day'] = utc.day
        data['production_date|hour'] = utc.hour
        data['production_date|minute'] = utc.minute

        # Need this to make sure any coloured labels from a previous check
        # operation are set back to black, but do not reset repair mode.
        #
        # Note that self.clear_gui() needs to be performed before setting the
        # repair mode, otherwise the call will reset it to its default (False).
        self.clear_gui(persist=True)

        self.set_repair_mode()
        self.update_gui_from_dict(data)
        self.update_solder(row['institute_id'], force=False)
        self.load_defaults()

        self.release(top)


##############################################################################
# utilities
##############################################################################


def unpack_qrcode(table):
    """
    When loading a JSON file, make sure the QR code string matches the
    current chunked display method.

    --------------------------------------------------------------------------
    args
        table : dict
    --------------------------------------------------------------------------
    returns : no explicit return, mutable type amended in place
    --------------------------------------------------------------------------
    """
    try:
        qrcode_value = table['qrcode|None']
    except KeyError:
        pass
    else:
        table['qrcode|None'] = qrcode_chunk(qrcode_value)


def qrcode_normal(qrcode):
    """
    Remove the functional decomposition added by qrcode_chunk(), so the
    QR code may be processed by standard tools.

    --------------------------------------------------------------------------
    args
        qrcode : string
            E.g. '231106 1 30 00720 001'
    --------------------------------------------------------------------------
    returns : string
        E.g. '23110613000720001'
    --------------------------------------------------------------------------
    """
    return f'{qrcode}'.replace(' ', '')


def qrcode_chunk(qrcode):
    """
    Human factors consideration. Functionally decompose the QR code numerals
    into constituent parts so it's easier for the user to reliably identify
    the serial number when QR codes are shown in the GUI combobox.

    --------------------------------------------------------------------------
    args
        qrcode : string
            E.g. '23110613000720001'
    --------------------------------------------------------------------------
    returns : string
        E.g. '231106 1 30 00720 001'
    --------------------------------------------------------------------------
    """
    boundaries = [(0, 6), (6, 7), (7, 9), (9, 14), (14, 17)]
    normal_qrcode = qrcode_normal(f'{qrcode}')

    return ' '.join(
        normal_qrcode[start:end] for start, end in boundaries
    )


def timestamp_to_utc(tref):
    """
    Converts a timestamp into a string in UTC to the nearest second.

    e.g. 1567065212.1064236 converts to '20190829_075332'

    --------------------------------------------------------------------------
    args
        tref : float
            time in seconds since the epoch
    --------------------------------------------------------------------------
    returns : string
    --------------------------------------------------------------------------
    """
    utc = datetime.datetime.fromtimestamp(
        tref, datetime.timezone.utc
    ).isoformat().split('.')[0]

    return utc.replace('-', '').replace(':', '').replace('T', '_')


def timestamp_to_utc_ds20k(tref):
    """
    Converts a timestamp into a string in UTC to the nearest second.

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
    utc = datetime.datetime.fromtimestamp(
        tref, datetime.timezone.utc
    ).isoformat().split('.')[0]

    return utc.replace('T', ' ')


def quiet_load_json(filename):
    """
    Load JSON file.

    --------------------------------------------------------------------------
    args
        filename : string
    --------------------------------------------------------------------------
    returns
        table_json : dict
            e.g. {
                'sipm_19|lot_number': '9262109',
                'sipm_19|wafer_number': '15',
                'sipm_19|column': '10',
                'sipm_19|row': '21', ...
            }
    --------------------------------------------------------------------------
    """
    table_json = {}

    with contextlib.suppress(FileNotFoundError):
        with open(filename, 'r', encoding='utf-8') as infile:
            with contextlib.suppress(json.JSONDecodeError, UnicodeDecodeError):
                table_json = json.load(infile)

    return table_json


##############################################################################
def main():
    """
    GUI for POSTing DarkSide-20k vTiles to the production database.

    A 1024 x 576 pixel window should fit into any modern computer display
    without needing scrollbars.
    """
    gui = Gui()
    gui.run()


##############################################################################
if __name__ == '__main__':
    main()
