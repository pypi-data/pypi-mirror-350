#!/usr/bin/env python3
"""
GUI prototype
"""

import collections
import contextlib
from enum import IntEnum
import functools
import itertools
import json
import os
from pathlib import Path
import platform
import sys
import webbrowser

import tkinter
from tkinter import ttk
from tkinter import filedialog
from tkinter import font

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
# data structures
##############################################################################

# tab name
Tab = IntEnum('Tab', ['GREEN', 'YELLOW'])


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


class Gui:
    """
    Construct/operate GUI.
    """
    # window extent
    root_w = 896
    root_h = 528

    inner_split = 16
    outer_split = 8
    left_frame_width = right_frame_width = (root_w - outer_split * 3) // 2

    max_filenames_per_tab = 12
    directory_label_width_chars = 64
    console_width_chars = 58
    console_height_chars = 20

    try:
        dbi = interface.Database()
    except AssertionError:
        sys.exit()

    def __init__(self):
        self.root = tkinter.Tk()
        self.root.geometry(f'{self.root_w}x{self.root_h}+0+0')
        self.root.title('DarkSide-20k generate tray files')
        self.root.resizable(False, False)

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

        self.frame = {}
        self.button = {}
        self.combobox = {}
        self.filenames = collections.defaultdict(set)

        # default directory setting

        self.defaults_tray_filename = '.ds20kdb_tray_defaults'
        self.home_directory = os.path.expanduser('~')
        self.defaults_tray_file_path = os.path.join(
            self.home_directory, self.defaults_tray_filename
        )

        self.tray_file_directory = self.home_directory

        # build GUI

        self.frame_tab = {}
        self.frame_tab_filename_labels = collections.defaultdict(list)

        self.liverpool_wafers = None
        self.wafer_table_dataframe = self.database_alive()

        # Only load wafers that are located at the University of Liverpool.
        self.lots = self.local_wafers()

        self.populate_menu_bar()
        self.populate_window_with_frames()
        self.populate_left_frame_with_subframes()
        self.populate_right_frame_with_subframes()

        self.load_defaults()

    ##########################################################################
    # utilities
    ##########################################################################

    def database_alive(self):
        """
        Load something relatively small to check connectivity, and also gives
        us a resource that will be used later.

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns : pandas.core.frame.DataFrame
            contents of the entire wafer table
        ----------------------------------------------------------------------
        """
        response = self.dbi.get('wafer')

        if response.network_timeout:
            sys.exit('Check network connection: timeout')

        return response.data

    def local_wafers(self):
        """
        Obtain a list of wafer lot numbers for wafers present at the
        University of Liverpool.

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns : list of wafer lot numbers, in ascending order
        ----------------------------------------------------------------------
        """
        # Institute ID

        response = self.dbi.get_institute_id('Liverpool')

        if response.network_timeout:
            sys.exit('Check network connection: timeout')

        institute_id = response.data

        # Wafer IDs for institute ID

        response = self.dbi.get('wafer_location', institute_id=institute_id)

        if response.network_timeout:
            sys.exit('Check network connection: timeout')

        wafer_pids = set(response.data.wafer_id)

        # Wafer lots

        pidlot = self.wafer_table_dataframe[['wafer_pid', 'lot', 'wafer_number']]
        self.liverpool_wafers = {
            tuple(pidlot[pidlot['wafer_pid']==i].iloc[-1][['lot', 'wafer_number']])
            for i in wafer_pids
        }
        lots, _wafer_numbers = (set(x) for x in zip(*self.liverpool_wafers))

        return sorted(lots)

    def wafer_numbers_for_lot(self, _event):
        """
        When the user changes the wafer lot, change the wafer numbers to only
        those that are located at Liverpool.

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns : none
            GUI state affected
        ----------------------------------------------------------------------
        """
        lot = int(self.combobox['lot'].get())
        wafer_number = self.combobox['wafer_number'].get()

        try:
            wafer_numbers = sorted(
                {f'{wn:02}' for ln, wn in self.liverpool_wafers if ln == lot}
            )
        except TypeError:
            pass
        else:
            self.combobox['wafer_number'].configure(values=wafer_numbers)

            # Address the case where the user, with a newly loaded GUI,
            # selects the wafer number before the lot number.
            if wafer_number not in wafer_numbers:
                self.combobox['wafer_number'].set('wafer')

    ##########################################################################
    # File I/O relating to the GUI menu bar
    ##########################################################################

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
                    self.print_to_console(f'Could not read file: {filename}')
                else:
                    self.print_to_console(f'Loaded file {filename}')

        return table_json

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
        # load default tray file location

        table_json = self.generic_load_json(self.defaults_tray_file_path)

        if not table_json:
            return

        try:
            directory = table_json['tray_file_directory']
        except KeyError:
            self.print_to_console(
                'Error reading tray file default directory from '
                f'{self.defaults_tray_file_path}'
            )
        else:
            if os.path.isdir(directory):
                self.update_tray_file_directories(directory)
                self.draw_directory()
            else:
                self.print_to_console(
                    f'Default tray file directory does not exist: {directory}'
                )

    def update_tray_file_directories(self, directory):
        """
        Set directory for tray files, and the yellow tray file subdirectory.

        ----------------------------------------------------------------------
        args
            directory : string
        ----------------------------------------------------------------------
        returns : none
        ----------------------------------------------------------------------
        """
        self.tray_file_directory = directory

    ##########################################################################
    # build GUI
    ##########################################################################

    def populate_menu_bar(self):
        """
        Populate the GUI menu bar.

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns : none
        ----------------------------------------------------------------------
        """
        menubar = tkinter.Menu(self.root)
        self.root.config(menu=menubar)

        tool_menu = tkinter.Menu(menubar, tearoff=False)
        help_menu = tkinter.Menu(menubar, tearoff=False)

        tool_menu.add_command(
            label='Set default tray file directory',
            command=self.set_default_tray_file_directory,
        )

        help_menu.add_command(
            label='About',
            command=self.about_popup,
        )
        help_menu.add_command(
            label='Documentation',
            command=lambda: webbrowser.open_new(
                'https://gitlab.in2p3.fr/darkside/productiondb_software/-/wikis/'
                'Generate-tray-files'
            ),
        )

        menubar.add_cascade(
            label='Tools',
            menu=tool_menu,
            underline=0
        )
        menubar.add_cascade(
            label='Help',
            menu=help_menu,
            underline=0
        )

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
            self.update_tray_file_directories(directory)
            self.draw_directory()

            with open(self.defaults_tray_file_path, 'w', encoding='utf-8') as outfile:
                outfile.write(
                    json.dumps(
                        {'tray_file_directory': directory}
                    )
                )

    def about_popup(self):
        """
        Display the Help -> About window, centred on the main window.

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns : none
        ----------------------------------------------------------------------
        """
        about_w, about_h = 320, 192

        current_w = self.root.winfo_width()
        current_h = self.root.winfo_height()

        root_win_x, root_win_y = (int(s) for s in self.root.geometry().split('+')[1:])

        about_x = root_win_x + (current_w // 2) - (about_w // 2)
        about_y = root_win_y + (current_h // 2) - (about_h // 2)

        top = tkinter.Toplevel(self.root)
        top.geometry(f'{about_w}x{about_h}+{about_x}+{about_y}')
        top.resizable(False, False)
        top.title('About')

        # add frame

        local_frame = ttk.Frame(
            top,
            width=about_w,
            height=about_h,
        )
        local_frame.grid(row=0, column=0)
        local_frame.grid_propagate(False)

        # add contents (text)

        text = tkinter.Text(local_frame, height=11, width=70)
        text.grid(column=0, row=0)
        text.tag_configure('center', justify='center')
        message = (
            '\n'
            '- Generate tray files -\n'
            f'ds20kdb interface version {interface.__version__}\n'
            '\n'
            'Creates wafer tray files for the given\n'
            'wafer lot/number and fills any empty\n'
            'spaces in selected tray files.\n'
            '\n'
            '- support -\n'
            'avt@hep.ph.liv.ac.uk'
        )
        text.insert(tkinter.END, message)
        text.tag_add('center', '1.0', 'end')
        text.configure(state='disabled')

        # add contents (button)

        ttk.Button(
            local_frame,
            text='ok',
            command=lambda: self.release(top),
        ).grid(column=0, row=1)
        local_frame.columnconfigure(0, weight=1)   # Set weight to row and
        local_frame.rowconfigure(1, weight=1)      # column where the widget is

        # pop-up window should take focus away from main window until dismissed
        top.grab_set()

    @staticmethod
    def release(window):
        """
        Return focus to main window then destroy pop-up window.

        --------------------------------------------------------------------------
        args
            window : <class 'tkinter.Toplevel'>
        --------------------------------------------------------------------------
        returns : none
            GUI state changed
        --------------------------------------------------------------------------
        """
        window.grab_release()
        window.destroy()

    def populate_window_with_frames(self):
        """
        Build the grid into which the core two frames (left and right) will sit.

        (col, row)

        +------+--------------------+------+--------------------+------+
        | 0, 0 | 1, 0               | 2, 0 | 3, 0               | 4, 0 |
        +------+--------------------+------+--------------------+------+
        | 0, 1 | 1, 1               | 2, 1 | 3, 1               | 4, 1 |
        |      |                    |      |                    |      |
        |      |                    |      |                    |      |
        |      |                    |      |                    |      |
        |      |    left_frame      |      |    right_frame     |      |
        |      |                    |      |                    |      |
        |      |                    |      |                    |      |
        |      |                    |      |                    |      |
        |      |                    |      |                    |      |
        +------+--------------------+------+--------------------+------+
        | 0, 2 | 1, 2               | 2, 2 | 3, 2               | 4, 2 |
        +------+--------------------+------+--------------------+------+

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns : none
        ----------------------------------------------------------------------
        """
        # add padding between elements

        self.root.grid_rowconfigure(0, minsize=self.outer_split)
        self.root.grid_rowconfigure(1)
        self.root.grid_rowconfigure(2, minsize=self.outer_split)

        self.root.grid_columnconfigure(0, minsize=self.outer_split)
        self.root.grid_columnconfigure(1)
        self.root.grid_columnconfigure(2, minsize=self.outer_split)
        self.root.grid_columnconfigure(3)
        self.root.grid_columnconfigure(4, minsize=self.outer_split)

        ######################################################################
        # left side
        self.frame['left_frame'] = ttk.Frame(
            self.root,
            width=self.left_frame_width,
            height=self.root_h,
        )
        self.frame['left_frame'].grid(column=1, row=1)
        self.frame['left_frame'].grid_propagate(False)

        ######################################################################
        # right side
        self.frame['right_frame'] = ttk.Frame(
            self.root,
            width=self.right_frame_width,
            height=self.root_h,
        )
        self.frame['right_frame'].grid(column=3, row=1)
        self.frame['right_frame'].grid_propagate(False)

    def populate_left_frame_with_subframes(self):
        """
        Add frames for:

            * selection of wafer (lot/number)
            * selection of directory for writing tray files into
            * partially empty tray files that can have free slots filled from
                  the wafer above

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns : none
        ----------------------------------------------------------------------
        """

        # add padding between elements

        self.frame['left_frame'].grid_rowconfigure(0)
        self.frame['left_frame'].grid_rowconfigure(1, minsize=self.inner_split)
        self.frame['left_frame'].grid_rowconfigure(2)
        self.frame['left_frame'].grid_rowconfigure(3, minsize=self.inner_split)
        self.frame['left_frame'].grid_rowconfigure(4)

        # --------------------------------------------------------------------
        # row 0 : select wafer to generate tray files for
        # --------------------------------------------------------------------

        self.frame['select_wafer'] = tkinter.LabelFrame(
            self.frame['left_frame'],
            width=self.left_frame_width,
            height=56,
            text='select wafer to generate tray files for',
        )
        self.frame['select_wafer'].grid(column=0, row=0)
        self.frame['select_wafer'].grid_propagate(False)

        self.combobox['lot'] = SipmLotNum(
            self.frame['select_wafer'],
            values=self.lots,
            state='readonly',
            width=11,
        )
        self.combobox['lot'].grid(column=0, row=0, padx=8, pady=4)
        self.combobox['lot'].set('lot')
        self.combobox['lot'].bind('<<ComboboxSelected>>', self.wafer_numbers_for_lot)

        wafs = [f'{x:02}' for x in range(1, 26)]
        self.combobox['wafer_number'] = SipmWaferNum(
            self.frame['select_wafer'],
            values=wafs,
            state='readonly',
            width=5,
        )
        self.combobox['wafer_number'].grid(column=1, row=0)
        self.combobox['wafer_number'].set('wafer')

        # --------------------------------------------------------------------
        # row 2 : select location for creating new wafer lot directories
        # --------------------------------------------------------------------

        self.frame['select_top'] = tkinter.LabelFrame(
            self.frame['left_frame'],
            width=self.left_frame_width,
            height=64+16,
            text='select location for creating new wafer lot directories',
        )
        self.frame['select_top'].grid(column=0, row=2)
        self.frame['select_top'].grid_propagate(False)

        self.frame['select_top'].grid_rowconfigure(0, minsize=8)
        self.frame['select_top'].grid_rowconfigure(1, minsize=8)
        self.frame['select_top'].grid_rowconfigure(2, minsize=8)

        self.button['select_directory'] = ttk.Button(
            self.frame['select_top'],
            text='select directory',
            command=self.select_directory,
        )
        self.button['select_directory'].grid(column=0, row=0, padx=8, pady=2, sticky=tkinter.W)

        self.frame['show_directory'] = ttk.Label(
            self.frame['select_top'],
            text=self.tray_file_directory,
        )
        self.frame['show_directory'].grid(column=0, row=2, padx=8, sticky=tkinter.W)
        self.frame['show_directory'].grid_propagate(False)

        # --------------------------------------------------------------------
        # row 4 : Select existing partially-empty SiPM tray files to fill
        # --------------------------------------------------------------------

        self.frame['select_bottom'] = tkinter.LabelFrame(
            self.frame['left_frame'],
            width=self.left_frame_width,
            height=344,
            text='Select existing partially-empty SiPM tray files to fill (if required)',
        )
        self.frame['select_bottom'].grid(column=0, row=4)
        self.frame['select_bottom'].grid_propagate(False)

        # padding above notebook tabs
        self.frame['select_bottom'].grid_rowconfigure(0, minsize=8)
        self.frame['select_bottom'].grid_rowconfigure(1)

        notebook = ttk.Notebook(self.frame['select_bottom'])
        notebook.grid(row=1, column=0, sticky='nw')

        self.frame_tab[Tab.GREEN] = ttk.Frame(
            notebook, width=self.left_frame_width - 8, height=290
        )
        self.frame_tab[Tab.GREEN].grid(column=0, row=0)
        self.frame_tab[Tab.GREEN].grid_propagate(False)

        notebook.add(self.frame_tab[Tab.GREEN], text='GREEN (production standard)')

        # populate tabs
        self.button['select_green'] = ttk.Button(
            self.frame_tab[Tab.GREEN],
            text='select file(s)',
            command=lambda: self.select_tray_filenames(Tab.GREEN),
        )
        self.button['select_green'].grid(column=0, row=0, padx=8, pady=8, sticky=tkinter.W)
        self.button['clear_green'] = ttk.Button(
            self.frame_tab[Tab.GREEN],
            text='clear file list',
            command=lambda: self.clear_filenames(Tab.GREEN),
        )
        self.button['clear_green'].grid(column=1, row=0, sticky=tkinter.W)

        # add blank labels to each tab
        for tab, row in itertools.product(
            [Tab.GREEN], range(1, 1 + self.max_filenames_per_tab)
        ):
            a = tkinter.Label(self.frame_tab[tab], text='')
            a.grid(column=0, row=row, columnspan=2, sticky=tkinter.W)
            self.frame_tab_filename_labels[tab].append(a)

    def populate_right_frame_with_subframes(self):
        """
        Add frames for:

            * PREVIEW button
            * console frame
            * GO button

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns : none
        ----------------------------------------------------------------------
        """

        # add padding between elements

        self.frame['right_frame'].grid_rowconfigure(0)
        self.frame['right_frame'].grid_rowconfigure(1, minsize=self.inner_split)
        self.frame['right_frame'].grid_rowconfigure(2)
        self.frame['right_frame'].grid_rowconfigure(3, minsize=self.inner_split)
        self.frame['right_frame'].grid_rowconfigure(4)

        # --------------------------------------------------------------------
        # row 0 : preview button
        # --------------------------------------------------------------------

        self.frame['preview_button_frame'] = tkinter.LabelFrame(
            self.frame['right_frame'],
            width=self.right_frame_width - 8,
            height=56,
            text='generate preview in console without changing/creating files',
        )
        self.frame['preview_button_frame'].grid(column=0, row=0)
        self.frame['preview_button_frame'].grid_propagate(False)

        self.button['preview'] = tkinter.Button(
            self.frame['preview_button_frame'],
            text='PREVIEW',
            # colours for button mouseover
            activebackground='green', activeforeground='white',
            # standard colours
            bg='darkgreen', fg='white',
            command=self.preview,
        )
        self.button['preview'].grid(column=3, row=1, padx=8, pady=2, sticky=tkinter.E)

        # --------------------------------------------------------------------
        # row 2 : console and clear console button
        # --------------------------------------------------------------------

        self.frame['console'] = ttk.LabelFrame(
            self.frame['right_frame'],
            width=self.right_frame_width - 8,
            height=256+96+12,
            text='console',
        )
        self.frame['console'].grid(column=0, row=2)
        self.frame['console'].grid_propagate(False)

        # console itself

        self.frame['console_text'] = tkinter.Text(
            self.frame['console'], state='disabled',
            height=self.console_height_chars, width=self.console_width_chars
        )
        self.frame['console_text'].grid(column=0, row=0)
        self.frame['console_text'].grid_propagate(False)

        # add scrollbar
        scroll_bar = tkinter.Scrollbar(
            self.frame['console'], command=self.frame['console_text'].yview, orient='vertical'
        )
        scroll_bar.grid(row=0, column=1, sticky='ns')
        self.frame['console_text'].configure(yscrollcommand=scroll_bar.set)

        # clear button

        self.button['clear_console'] = tkinter.Button(
            self.frame['console'],
            text='CLEAR CONSOLE',
            command=self.clear_console,
        )
        self.button['clear_console'].grid(column=0, row=1, padx=8, pady=8, sticky=tkinter.W)

        # --------------------------------------------------------------------
        # row 4 : GO button
        # --------------------------------------------------------------------

        # frame to contain GO button
        self.frame['preview_and_go_button_frame'] = tkinter.LabelFrame(
            self.frame['right_frame'],
            width=self.right_frame_width - 8,
            height=56,
            text='change/create files',
        )
        self.frame['preview_and_go_button_frame'].grid(column=0, row=4)
        self.frame['preview_and_go_button_frame'].grid_propagate(False)

        # ensure button can be right justified inside frame
        self.frame['preview_and_go_button_frame'].grid_columnconfigure(0, weight=2)
        self.frame['preview_and_go_button_frame'].grid_columnconfigure(1, weight=1)

        self.button['go'] = tkinter.Button(
            self.frame['preview_and_go_button_frame'],
            text='GO',
            # colours for button mouseover
            activebackground='crimson', activeforeground='white',
            # standard colours
            bg='firebrick', fg='white',
            command=self.go,
        )
        self.button['go'].grid(column=1, row=1, padx=8, sticky=tkinter.E)

    def print_to_console(self, line):
        """
        Print log messages to the GUI console.

        ----------------------------------------------------------------------
        args
            line : string
        ----------------------------------------------------------------------
        returns : none
            GUI state affected
        ----------------------------------------------------------------------
        """
        # ensure line is terminated
        try:
            line = line if line.endswith('\n') else f'{line}\n'
        except AttributeError:
            pass
        else:
            self.frame['console_text'].configure(state=tkinter.NORMAL)
            self.frame['console_text'].insert(tkinter.END, line)
            self.frame['console_text'].configure(state=tkinter.DISABLED)

    def console_end(self):
        """
        Scroll to the end of the console text.

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns : none
            GUI state affected
        ----------------------------------------------------------------------
        """
        self.frame['console_text'].update()
        self.frame['console_text'].yview(tkinter.END)

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

        ----------------------------------------------------------------------
        args
            tkf : <class 'tkinter.font.Font'>
        ----------------------------------------------------------------------
        returns : none
            GUI state changed
        ----------------------------------------------------------------------
        """
        font_list = [
            'Noto Sans', 'Liberation Mono', 'Courier New', 'DejaVu Sans Mono'
        ]
        details = tkf.actual()
        if details['family'] in font_list and details['size'] > 9:
            tkf.configure(size=9)

    ##########################################################################
    # GUI button actions
    ##########################################################################

    def clear_console(self):
        """
        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns : none
            GUI state changed
        ----------------------------------------------------------------------
        """
        self.frame['console_text'].configure(state=tkinter.NORMAL)
        self.frame['console_text'].delete(1.0, tkinter.END)
        self.frame['console_text'].configure(state=tkinter.DISABLED)

    def select_tray_filenames(self, tab):
        """
        ----------------------------------------------------------------------
        args
            widgets : list
                Contains details of GUI widgets.
        ----------------------------------------------------------------------
        returns : tuple containing filename(s)
        ----------------------------------------------------------------------
        """
        # filename will be a tuple for some reason
        filenames = filedialog.askopenfilenames(
            defaultextension='.txt',
            filetypes=[
                ('Text Documents', '*.txt'),
                ('All Files', '*.*'),
            ],
            title=f'{tab.name} SiPM tray file(s)',
        )

        try:
            self.filenames[tab] |= set(filenames)
        except TypeError:
            pass
        else:
            # ensure there are no duplicate files between tabs
            tmp = list(self.filenames[tab])[:self.max_filenames_per_tab]

            if len(filenames) > self.max_filenames_per_tab:
                self.print_to_console(
                    f'Maximum number of files exceeded ({self.max_filenames_per_tab})'
                )

            self.filenames[tab] = set(tmp)

            self.draw_filename_labels(tab)

    def select_directory(self):
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
            title='select directory',
        )

        if directory:
            self.update_tray_file_directories(directory)
            self.draw_directory()

    def common_preview_go(self, write):
        """
        Code common to both PREVIEW and GO buttons.

        --------------------------------------------------------------------------
        args
            write : bool
                permission to modify/write files
        --------------------------------------------------------------------------
        returns : none
            Files may be amended/created
            GUI state may be altered
        --------------------------------------------------------------------------
        """
        # check if wafer exists

        try:
            lot = int(self.combobox['lot'].get())
            wafer_number = int(self.combobox['wafer_number'].get())
        except ValueError:
            self.print_to_console('ERROR: Wafer definition incomplete/missing\n\n')
            return

        wafer_pid = self.wafer_table_dataframe.loc[
            (self.wafer_table_dataframe['wafer_number'] == wafer_number)
            & (self.wafer_table_dataframe['lot'] == lot)
        ].wafer_pid.values[-1]

        message = f'Wafer {lot}.{wafer_number:02}: PID {wafer_pid}'
        self.print_to_console(message)

        # obtain (col, row) locations for good/bad SiPMs

        self.print_to_console('Retrieving wafer map details, please wait...')

        try:
            wafer_map_green, _wafer_map_yellow, wafer_map_red = common.identify_sipm_status(
                self.dbi,
                wafer_pid=wafer_pid,
                sequential=False,
                no_b_grade=True,
            )
        except TypeError:
            self.print_to_console('Identifying SiPM status failed.')
            return

        # these variables may be altered during generation of tray files
        wmg = wafer_map_green.copy()
        wmr = wafer_map_red.copy()

        # sort: highest column first, then lowest row first
        wafer_map_green = sorted(wafer_map_green, key=lambda x: (-x[1], x[0]))

        self.print_to_console(
            f'green {len(wafer_map_green)}, '
            f'red {len(wafer_map_red)}'
        )

        existing_green = common.evaluate_tray_files(self.filenames[Tab.GREEN])

        ##########################################################################
        # fill existing tray files with SiPMs
        ##########################################################################

        tasks = [
            ('GREEN', existing_green, wafer_map_green),
        ]

        if any([existing_green]):
            self.print_to_console(
                f'\n{"#" * 58}\n# Filling existing files\n{"#" * 58}'
            )
        else:
            self.print_to_console(
                f'\n{"#" * 58}\n# No existing files to fill\n{"#" * 58}'
            )

        status_lines = map(
            functools.partial(
                common.fill_files,
                lot=lot,
                wafer_number=wafer_number,
                write=write,
            ),
            tasks,
        )

        for i in itertools.chain.from_iterable(status_lines):
            self.print_to_console(i)

        ##########################################################################
        # create new tray files
        ##########################################################################

        self.print_to_console(f'\n{"#" * 58}\n# New tray files\n{"#" * 58}')

        path = self.destination_directory(lot, wafer_number)

        if write:
            # Create this path even if there are no green SiPMs since the wafer map
            # will be written to this location in all cases.
            Path(path).mkdir(parents=True, exist_ok=True)

        # sipm type, wafer map, directory, file number offset
        tasks = [
            ('green', wafer_map_green, path, 0),
        ]

        status_lines = map(
            functools.partial(
                common.create_tray_files,
                lot=lot,
                wafer_number=wafer_number,
                write=write,
            ),
            tasks,
        )

        for i in itertools.chain.from_iterable(status_lines):
            self.print_to_console(i)

        self.console_end()

        if not write:
            return

        sipm_groups = [
            {
                'name': 'good',
                'locations': wmg,
                'sipm_colour': 'green',
                'text_colour': 'black',
            },
            {
                'name': 'bad_lfoundry-visual_noa-cryoprobe',
                'locations': wmr,
                'sipm_colour': 'darkred',
                'text_colour': 'lightgrey',
            },
        ]

        restore_cwd = os.getcwd()
        os.chdir(path)
        visual.DrawWafer(
            wafer_lot=lot,
            wafer_number=wafer_number,
            sipm_groups=sipm_groups
        ).save()
        os.chdir(restore_cwd)

        self.print_to_console(f'\nWafer map saved to {path}')

    def destination_directory(self, lot, wafer_number):
        """
        Create path for new tray files, and create directories as required.

        ----------------------------------------------------------------------
        args
            lot : int
            wafer_number : int
        ----------------------------------------------------------------------
        returns : none
        ----------------------------------------------------------------------
        """
        path = os.path.join(
            self.tray_file_directory, f'{lot}', f'{wafer_number:02}'
        )

        return path

    def preview(self):
        """
        PREVIEW button. Go through the motions of amending/creating files based
        on the wafer map. Report progress in the console, but don't actually make
        the changes.

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns : none
        ----------------------------------------------------------------------
        """
        self.print_to_console(
            common.box_message(
                'PREVIEW ONLY - NO FILES WILL BE AMENDED/CREATED',
                self.console_width_chars,
            )
        )
        self.common_preview_go(write=False)

    def go(self):
        """
        GO button. Report progress in the console, amend/create files as
        required.

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns : none
        ----------------------------------------------------------------------
        """
        self.print_to_console(
            common.box_message(
                'AMEND/CREATE FILES',
                self.console_width_chars,
            )
        )

        self.common_preview_go(write=True)

    ##########################################################################
    # change GUI state
    ##########################################################################

    def draw_filename_labels(self, tab):
        """
        ----------------------------------------------------------------------
        args
            tab : <enum 'Tab'>
                identifier for green and yellow notebook tabs
        ----------------------------------------------------------------------
        returns : none
        ----------------------------------------------------------------------
        """
        for index, filename in enumerate(sorted(self.filenames[tab])):
            self.frame_tab_filename_labels[tab][index].config(text=os.path.basename(filename))

    def clear_filenames(self, tab):
        """
        ----------------------------------------------------------------------
        args
            tab : <enum 'Tab'>
                identifier for green and yellow notebook tabs
        ----------------------------------------------------------------------
        returns : none
        ----------------------------------------------------------------------
        """
        for index, _filename in enumerate(self.filenames[tab]):
            self.frame_tab_filename_labels[tab][index].config(text='')

        self.filenames[tab] = set()

    def draw_directory(self):
        """
        Update GUI label containing the name of the directory in which new tray
        files will be created.

        ----------------------------------------------------------------------
        args : none
        ----------------------------------------------------------------------
        returns : none
        ----------------------------------------------------------------------
        """
        self.frame['show_directory'].config(
            text=self.tray_file_directory
        )


##############################################################################
def main():
    """
    GUI prototype
    """
    gui = Gui()
    gui.run()


##############################################################################
if __name__ == '__main__':
    main()
