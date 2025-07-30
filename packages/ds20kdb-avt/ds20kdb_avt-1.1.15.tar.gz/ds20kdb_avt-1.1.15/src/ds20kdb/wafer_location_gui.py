#!/usr/bin/env python3
"""
The GUI permits to add entries in the wafer_location table in order to update
the location of a wafer.

Author: P.Franchini - p.franchini@lancaster.ac.uk
"""


import datetime
import itertools
import tkinter as tk
from tkinter import ttk

from tkcalendar import Calendar

from ds20kdb import interface


##############################################################################
# data structures
##############################################################################


class Object:
    """
    Container for GUI and database interaction.
    """

    dbi = interface.Database()

    def __init__(self):

        ######################################################################
        # build GUI
        ######################################################################

        self.root = tk.Tk()
        self.root.title("Set Wafer Location GUI")

        # Set the window size (width x height)
        window_width = 300
        window_height = 450
        self.root.geometry(f"{window_width}x{window_height}")

        # Create a label for error messages
        self.error_label = tk.Label(self.root, text="", fg="red")
        self.error_label.pack()

        # Create a label for output messages
        self.output_label = tk.Label(self.root, text="", fg="green")
        self.output_label.pack()

        # Create labels and text boxes for Lot, Wafer Number
        self.lot_label = tk.Label(self.root, text="Lot:")
        self.lot_label.pack()
        self.lot_var = tk.StringVar(self.root)
        self.lot_entry = tk.Entry(self.root, textvariable=self.lot_var)
        self.lot_entry.pack()

        self.wafer_number_label = tk.Label(self.root, text="Wafer Number:")
        self.wafer_number_label.pack()
        self.wafer_number_var = tk.StringVar(self.root)
        self.wafer_number_entry = tk.Entry(self.root, textvariable=self.wafer_number_var)
        self.wafer_number_entry.pack()

        # comment
        self.comment_label = tk.Label(self.root, text="Comment:")
        self.comment_label.pack()
        self.comment_var = tk.StringVar(self.root)
        self.comment_entry = tk.Entry(self.root, textvariable=self.comment_var)
        self.comment_entry.pack()

        # Location: institute
        self.location_label = tk.Label(self.root, text="Institute:")
        self.location_label.pack()

        # first database lookup: strict check
        response = self.dbi.get('institute')
        if response.network_timeout:
            print('Network timeout')
            return
        if response.data is None:
            print('No response')
            return

        dfr = response.data
        locations = dfr.name.tolist()
        self.location_var = tk.StringVar(self.root)
        self.location_dropdown = ttk.Combobox(
            self.root, textvariable=self.location_var, values=locations,
            width=50
        )
        self.location_dropdown.pack()

        self.timestamp_label = tk.Label(self.root, text="Timestamp:")
        self.timestamp_label.pack()

        self.timestamp_date_var = tk.StringVar(self.root)
        self.timestamp_date_var.set(datetime.datetime.now().strftime('%Y-%m-%d'))
        self.timestamp_date_entry = tk.Entry(
            self.root, textvariable=self.timestamp_date_var
        )
        self.timestamp_date_entry.pack()
        self.timestamp_date_button = tk.Button(
            self.root, text="Select Date", command=self.open_calendar
        )
        self.timestamp_date_button.pack()

        self.timestamp_time_var = tk.StringVar(self.root)
        self.timestamp_time_var.set(datetime.datetime.now().strftime('%H:%M:%S'))
        self.timestamp_time_entry = tk.Entry(
            self.root, textvariable=self.timestamp_time_var
        )
        self.timestamp_time_entry.pack()
        self.timestamp_time_button = tk.Button(
            self.root, text="Select Time", command=self.open_time_selection
        )
        self.timestamp_time_button.pack()

        # Create the submit button
        self.spacer_label = tk.Label(self.root, text="")
        self.spacer_label.pack()
        # Change the font size as needed
        submit_font = ("Helvetica", 14)
        self.submit_button = tk.Button(
            self.root, text="Submit", command=self.submit_command, font=submit_font
        )
        # NOT IN ORIGINAL self.submit_button.config(state="disabled")
        self.submit_button.pack()

    @staticmethod
    def is_valid_date_format(input_string):
        """
        Dates supplied from tkcalendar.Calendar will be valid and in the
        correct format. The GUI also supports manually entered dates, so we
        have to detect plausible-looking but invalid entries such as
        '2023-2-31', partial entries ('2023-2'), and other broken dates.

        ----------------------------------------------------------------------
        args
            input_string : string
                e.g. '2023-01-31'
        ----------------------------------------------------------------------
        returns : bool
        ----------------------------------------------------------------------
        """
        try:
            datetime.date(*map(int, input_string.split('-')))
        except (TypeError, ValueError):
            return False

        return True

    @staticmethod
    def is_valid_time_format(input_string):
        """
        Times supplied from the drop-down box will be valid and in the
        correct format. The GUI also supports manually entered times, so we
        have to detect plausible-looking but invalid entries such as
        '14-30-61', partial entries ('14-30'), and other broken times.

        ----------------------------------------------------------------------
        args
            input_string : string
                e.g. '14:30:26'
        ----------------------------------------------------------------------
        returns : bool
        ----------------------------------------------------------------------
        """
        try:
            hour, minute, second = map(int, input_string.split(':'))
            datetime.time(hour=hour, minute=minute, second=second)
        except ValueError:
            return False

        return True

    def submit_command(self):
        """
        Submit information to database.
        """

        # reset the error message label
        self.error_label.config(text='')
        self.output_label.config(text='')

        selected_location = self.location_var.get()

        selected_date = self.timestamp_date_var.get()
        selected_time = self.timestamp_time_var.get()
        timestamp = f'{selected_date}T{selected_time}'

        # check timestamp
        if not self.is_valid_date_format(selected_date):
            self.error_label.config(text='Date is not in the specified format')
            return

        if not self.is_valid_time_format(selected_time):
            self.error_label.config(text='Time is not in the specified format')
            return

        selected_lot = self.lot_var.get()
        selected_wafer_number = self.wafer_number_var.get()
        comment = self.comment_var.get()

        # get wafer_id
        try:
            wafer_id = self.dbi.get(
                'wafer',
                lot=selected_lot,
                wafer_number=selected_wafer_number,
            ).data.wafer_pid[0]
        except KeyError:
            self.error_label.config(text="Wrong Wafer Lot and/or Number")
            return

        # get institute_id
        try:
            institute_id = self.dbi.get('institute', name=selected_location).data.id[0]
        except KeyError:
            self.error_label.config(text='Please select an institute')
            return

        # Post the table
        table = {
            'wafer_id': int(wafer_id),
            'institute_id': int(institute_id),
            'timestamp': timestamp,
            'comment': comment,
            'state': '',
        }
        print(table)

        post_successful = self.dbi.post_item(table, 'wafer_location')
        if post_successful:
            status = 'succeeded'
            self.output_label.config(text=f'POST {status} - wafer_id: {wafer_id}')
        else:
            status = 'failed'
            self.error_label.config(text=f'POST {status}')

        print(f'POST {status}')

    def _set_date(self, top, calendar_widget):
        selected_date = calendar_widget.get_date()
        # Convert the selected date to a datetime object
        selected_date = datetime.datetime.strptime(selected_date, '%d/%m/%Y')
        selected_date_formatted = selected_date.strftime('%Y-%m-%d')  # Format the date
        self.timestamp_date_var.set(selected_date_formatted)
        top.destroy()

    def open_calendar(self):
        """
        Calendar selector pop-up
        """
        top = tk.Toplevel(self.root)
        top.title('Select Date')

        calendar_widget = Calendar(top)
        calendar_widget.pack()

        set_button = tk.Button(
            top,
            text='Set Date',
            command=lambda: self._set_date(top, calendar_widget)
        )
        set_button.pack()

    def _set_time(self, top, time_selection_var):
        """
        Set time; add missing seconds field if required
        """
        selected_time = time_selection_var.get()
        if ':' in selected_time and selected_time.count(':') == 1:
            selected_time += ':00'
        self.timestamp_time_var.set(selected_time)
        top.destroy()

    def open_time_selection(self):
        """
        Time selector pop-up
        """
        top = tk.Toplevel(self.root)
        top.title("Select Time")

        hours_minutes = itertools.product(range(24), range(0, 60, 15))
        time_selection_var = tk.StringVar(top)
        time_selection = ttk.Combobox(
            top,
            textvariable=time_selection_var,
            values=[f'{hour:02}:{minute:02}' for (hour, minute) in hours_minutes]
        )
        time_selection.pack()

        set_button = tk.Button(
            top,
            text="Set Time",
            command=lambda: self._set_time(top, time_selection_var)
        )
        set_button.pack()

    def mainloop(self):
        """
        Run GUI
        """
        self.root.mainloop()


##############################################################################
def main():
    """
    The GUI permits to add entries in the wafer_location table in order to
    update the location of a wafer.
    """
    gui = Object()
    gui.mainloop()


##############################################################################
if __name__ == '__main__':
    main()
