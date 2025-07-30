#!/usr/bin/env python3
"""
Draw wafer map.
"""

import itertools
import types

import PIL
from PIL import Image, ImageDraw, ImageFont

from ds20kdb import interface

if tuple(map(int, PIL.__version__.split('.'))) < (9, 0, 0):
    raise RuntimeError(
        'PIL 9.0.0 or newer required to run this script\n'
        f'version {PIL.__version__} found.'
    )


##############################################################################
# data structures
##############################################################################


class DrawWafer:
    """
    Draw wafer map.
    """
    colour = types.SimpleNamespace(
        # grey/red
        sipm_dot=(0x80, 0x61, 0x51),
        # grey/green
        sipm_generic=(0x49, 0x4E, 0x3D),
        # muted gold
        sipm_gold=(0xB1, 0xC5, 0x65),
        # other
        sipm_outline='black',
    )

    # SiPM geometry, aspect ratio ~1.5:1 (actual 11.7mm x 7.9mm, AR ~1.48:1)
    sipm_v_size_px = 40
    half_sipm_v_size_px = sipm_v_size_px // 2
    sipm_h_size_px = int(sipm_v_size_px * 1.5)
    half_sipm_h_size_px = sipm_h_size_px // 2

    # wafer plot area
    # PIL coordinate system: (0, 0) is the upper left corner. Any pixels drawn
    # outside the image bounds are discarded.
    side_px = max(
        sipm_h_size_px * 18,
        sipm_v_size_px * 24,
    )
    half_side_px = side_px // 2

    # wafer plot area
    img = Image.new(mode='RGBA', size=(side_px, side_px))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    # extent defines the mask diameter
    extent = int(sipm_v_size_px * 0.80)

    col, row = zip(*interface.wafer_map_valid_locations())
    minc, maxc = min(col), max(col)
    minr, maxr = min(row), max(row)

    sipms_with_upper_dots = {(4, 21), (15, 21)}
    sipms_with_lower_dots = {(2, 8), (17, 8)}
    dotted_sipms = sipms_with_upper_dots.union(sipms_with_lower_dots)

    def __init__(self, wafer_lot, wafer_number, sipm_groups, group_name=False):
        self.wafer_lot = wafer_lot
        self.wafer_number = wafer_number
        self.group_name = group_name
        self._draw_wafer(sipm_groups)

    def _calculate_text_position(self, centre_x, centre_y, label):
        """
        Note that bounding box calculation is slightly different between API
        versions which is understandable since the default font is different
        for 10.1.0 and newer, but the difference isn't substantial.

        -----------------------------------------------------------------------
        args
            centre_x : int
            centre_y : int
            label : string
        -----------------------------------------------------------------------
        returns : int, int
        -----------------------------------------------------------------------
        """
        left, top, right, bottom = self.draw.textbbox(
            (centre_x, centre_y), label
        )

        if tuple(map(int, PIL.__version__.split('.'))) >= (10, 1, 0):
            return left, top

        xdiff = (right - left) // 2
        ydiff = (bottom - top) // 2
        return centre_x - xdiff, centre_y - ydiff

    def _apply_mask(self):
        """
        Apply circular mask to remove the superfluous outer image data.

        -----------------------------------------------------------------------
        args : none
        -----------------------------------------------------------------------
        returns : none
            features are drawn on self.img
        -----------------------------------------------------------------------
        """
        # image: mask
        mask_img = Image.new(mode='1', size=(self.side_px, self.side_px))
        mask_draw = ImageDraw.Draw(mask_img)
        # construct mask
        # extent defines the mask diameter
        mask_draw.ellipse(
            (
                (self.extent, self.extent),
                (self.side_px - self.extent, self.side_px - self.extent),
            ),
            fill='white',
        )
        # notch
        notch_rad_px = self.sipm_v_size_px >> 2
        notch_cent_x = self.half_side_px
        notch_cent_y = self.side_px - self.extent
        mask_draw.ellipse(
            (
                (notch_cent_x - notch_rad_px, notch_cent_y - notch_rad_px),
                (notch_cent_x + notch_rad_px, notch_cent_y + notch_rad_px),
            ),
            fill='black',
        )

        # apply mask
        self.img.putalpha(mask_img)

    def _sipm_centre_corners(self, col, row):
        """
        Calculate SiPM centre position on the image bitmap, and its bounding
        rectangle.

        -----------------------------------------------------------------------
        args
            col : int
                wafer column
            row : int
                wafer row
        -----------------------------------------------------------------------
        returns
            int, int, (int, int, int, int)
                All values in pixels.
        -----------------------------------------------------------------------
        """
        x_centre_px = col * self.sipm_h_size_px - self.half_sipm_h_size_px
        y_centre_px = self.side_px - self.sipm_v_size_px - row * self.sipm_v_size_px

        # corner 1 & 2 for the SiPM
        c1x = x_centre_px - self.half_sipm_h_size_px
        c1y = y_centre_px - self.half_sipm_v_size_px
        c2x = x_centre_px + self.half_sipm_h_size_px
        c2y = y_centre_px + self.half_sipm_v_size_px

        return x_centre_px, y_centre_px, (c1x, c1y, c2x, c2y)

    def _draw_dot(self, location, x_centre_px, y_centre_px):
        """
        Draw SiPM dot if required by its location.

        -----------------------------------------------------------------------
        args
            location : tuple (column, row)
            x_centre_px : int
                centre of SiPM in pixels (image x-axis)
            y_centre_px : int
                centre of SiPM in pixels (image y-axis)
        -----------------------------------------------------------------------
        returns : bool
            True if dot was drawn
        -----------------------------------------------------------------------
        """
        if location not in self.dotted_sipms:
            return False

        dot_rad_px = self.sipm_v_size_px >> 3
        sign = 1 if location in self.sipms_with_lower_dots else -1
        dot_cent_y = y_centre_px + (dot_rad_px << 1) * sign

        self.draw.ellipse(
            (
                (x_centre_px - dot_rad_px, dot_cent_y - dot_rad_px),
                (x_centre_px + dot_rad_px, dot_cent_y + dot_rad_px),
            ),
            fill=self.colour.sipm_dot,
        )

        return True

    def _draw_sipm(self, location, fill_colour, text_colour, name):
        """
        Draw an individual SiPM on the wafer.

        -----------------------------------------------------------------------
        args
            location : tuple (column, row)
            fill_colour : string ('black') or tuple (0x80, 0x61, 0x51)
            text_colour : string ('black') or tuple (0x80, 0x61, 0x51)
            name : string, name of SiPM group
        -----------------------------------------------------------------------
        returns : none
            features are drawn on self.img
        -----------------------------------------------------------------------
        """
        try:
            col, row = location
        except ValueError:
            return

        # draw SiPM rectangle
        x_centre_px, y_centre_px, corners = self._sipm_centre_corners(col, row)
        self.draw.rectangle(
            corners,
            fill=fill_colour,
            outline=self.colour.sipm_outline,
        )

        # draw SiPM dot if required
        dot_drawn = self._draw_dot(location, x_centre_px, y_centre_px)

        if text_colour is None or dot_drawn:
            return

        # draw column/row text
        label = name if self.group_name else f'c{col:02} r{row:02}'

        self.draw.text(
            self._calculate_text_position(x_centre_px, y_centre_px, label),
            label,
            fill=text_colour,
            anchor='mm',
        )

    def _draw_sipms(self, sipm_groups):
        """
        Draw all groups of SiPMs with the specified fill and text colours.

        -----------------------------------------------------------------------
        args sipm_groups : itertools.chain
            Contains all groups of SiPMs to
            be drawn. sipm_groups is expected to be ordered from background
            to foreground. This ensures that background features (encountered
            first) are overwritten in the dict by foreground features (bad
            SiPMs) that are encountered later.
            e.g.
                (
                    {
                        'name': 'Wafer map BAD',
                        # location tuples are (column, row)
                        'locations': {(8, 10), (10, 6), (7, 8)},
                        'sipm_colour': 'red',
                        'text_colour': 'white'
                    },
                    ...
                )
        -----------------------------------------------------------------------
        returns : none
            features are drawn on self.img
        -----------------------------------------------------------------------
        """
        # Create dict containing SiPMs to be plotted. Foreground SiPMs will
        # replace background SiPMs at the same col/row location, minimising the
        # number of draw calls that need to be issued.
        sipms_to_draw = {}
        for sipm_group in sipm_groups:
            for location in sipm_group['locations']:
                sipms_to_draw[location] = (
                    sipm_group['sipm_colour'],
                    sipm_group['text_colour'],
                    sipm_group['name'],
                )

        # draw SiPMs
        for location, (fill_colour, text_colour, name) in sipms_to_draw.items():
            self._draw_sipm(location, fill_colour, text_colour, name)

    def _draw_wafer(self, sipm_groups):
        """
        Draw the wafer with SiPMs in valid locations coloured per group,
        exterior silicon (SiPMs outside the valid locations), location
        notch and wafer number.

        -----------------------------------------------------------------------
        args
            sipm_groups : list of dicts
                The caller may supply groups
                e.g.
                [
                    {
                        'name': 'Wafer map BAD',
                        # location tuples are (column, row)
                        'locations': {(8, 10), (10, 6), (7, 8)},
                        'sipm_colour': 'red',
                        'text_colour': 'white'
                    },
                    ...
                ]
        -----------------------------------------------------------------------
        returns : none
            features are drawn on self.img
        -----------------------------------------------------------------------
        """
        # generic SiPM structures outside the valid locations
        rect = itertools.product(
            range(self.minc - 2, self.maxc + 3),
            range(self.minr - 1, self.maxr + 2),
        )
        gold = itertools.chain(
            # top right
            itertools.product(range(15, 16 + 1), range(21, 23 + 1)),
            # top left
            itertools.product(range(3, 4 + 1), range(21, 23 + 1)),
            # bottom left
            itertools.product(range(1, 2 + 1), range(5, 8 + 1)),
            # bottom right
            itertools.product(range(17, 18 + 1), range(5, 8 + 1)),
            # top line
            itertools.product(range(7, 12 + 1), [25]),
            # bottom line
            itertools.product(range(7, 12 + 1), [0]),
        )

        # groups must be listed in background to foreground order
        groups_common_to_all_wafers = [
            {
                'name': 'rect',
                'locations': rect,
                'sipm_colour': self.colour.sipm_generic,
                'text_colour': None,
            },
            {
                'name': 'gold',
                'locations': gold,
                'sipm_colour': self.colour.sipm_gold,
                'text_colour': None,
            },
        ]
        all_sipm_groups = itertools.chain(groups_common_to_all_wafers, sipm_groups)

        self._draw_sipms(all_sipm_groups)
        self._draw_wafer_ident()
        self._apply_mask()

    def _draw_wafer_ident(self):
        """
        Draw wafer ident.

        -----------------------------------------------------------------------
        args : none
        -----------------------------------------------------------------------
        returns : none
            features are drawn on self.img
        -----------------------------------------------------------------------
        """
        # black background for white wafer ident text
        wic_cent_x = self.half_side_px
        wic_cent_y = self.extent
        rect_half_width = int(self.sipm_h_size_px * 1.2)
        rect_half_height = self.sipm_v_size_px >> 1
        # corners
        c1x = wic_cent_x - rect_half_width
        c1y = wic_cent_y - rect_half_height
        c2x = wic_cent_x + rect_half_width
        c2y = wic_cent_y + rect_half_height
        self.draw.rectangle(
            (c1x, c1y, c2x, c2y),
            fill='black',
            outline='black',
        )

        # wafer ident in white text - e.g. 9262109.16
        if self.group_name:
            return

        label = f'{self.wafer_lot}.{self.wafer_number:02}'

        self.draw.text(
            self._calculate_text_position(
                self.half_side_px, self.sipm_v_size_px, label
            ),
            label,
            fill='white',
            anchor='mm',
        )

    def save(self):
        """
        Save wafer map as a PNG file complete with alpha.

        -----------------------------------------------------------------------
        args : none
        -----------------------------------------------------------------------
        returns : none
            image written to mass storage
        -----------------------------------------------------------------------
        """
        if self.group_name:
            suffix = 'groups'
        else:
            suffix = f'{self.wafer_lot}_{self.wafer_number:02}'

        self.img.save(f'wafer_{suffix}.png')
