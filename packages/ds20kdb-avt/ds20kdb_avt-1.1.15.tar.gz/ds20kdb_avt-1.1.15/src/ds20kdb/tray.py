"""
Data structures to support working with tray files as used to document trays
of 24 SiPMs.
"""

import collections
import contextlib
import copy
from enum import IntEnum
import functools
import io
import itertools
import re


###############################################################################
# data structures
###############################################################################


KEYWORDS = IntEnum(
    'Keywords',
    [
        # usable for production
        'FAIL',
        'PASS',
        # type(s) of flaw present
        'BUBBLE',
        'CHIP',
        'CONTAMINATION',
        'EM',
        'MBD',
        'MD',
        'NRP',
        'PADFLAW',
        'SCRATCH',
        'SCUFF',
        'SD',
        'SILICONRESIDUE',
        'VERTRAILFLAW',
        'OTHER',
    ]
)


class Tray:
    """
    Encapsulate the contents of a SiPM tray file.
    """

    __slots__ = {
        'path': 'The full Path to the original tray file.',
        'sipms': 'All SiPMs loaded from the tray file.',
        'sipms_good': (
            'All SiPMs with a PASS visual inspection category, or with no '
            'visual inspection categories specified'
        ),
        'sipms_bad': 'All SiPMs with a FAIL visual inspection category.',
        'keywords': (
            'Full list of visual inspection categories for all SiPMs in this '
            'tray'
        ),
        'import_errors': 'Any errors found while importing the tray file.'
    }

    def __init__(self, path):
        self.path = path
        self.sipms = {}
        self.sipms_good = {}
        self.sipms_bad = {}
        self.keywords = []
        self.import_errors = []

        self.import_from_file()

    def __str__(self):
        sipm_area = '\n'.join(map(self.pretty_print_sipm, self.sipms))
        stats = (
            f'SiPMs: good {len(self.sipms_good):>2}, '
            f'bad {len(self.sipms_bad):>2}'
        )
        return '\n'.join([sipm_area, stats])

    ###########################################################################
    # visual inspection keyword/category handling
    ###########################################################################

    @property
    def keywords_human_readable(self):
        """
        Return a count of the visual inspection categories for this tray
        excluding the overall PASS/FAIL assessment.

        -----------------------------------------------------------------------
        args : none
        -----------------------------------------------------------------------
        returns : dict
            E.g. {'SILICONRESIDUE': 7}
        -----------------------------------------------------------------------
        """
        return dict(
            collections.Counter(
                KEYWORDS(k).name for k in self.keywords
                if k not in {KEYWORDS.PASS, KEYWORDS.FAIL}
            )
        )

    @staticmethod
    def keywords_string(keywords):
        """
        Expand tokenised keyword list.

        -----------------------------------------------------------------------
        args
            keywords : list
        -----------------------------------------------------------------------
        returns : string
            E.g. [4, 5, 1] -> '[CHIP, CONTAMINATION, FAIL]'
        -----------------------------------------------------------------------
        """
        try:
            return f'[{", ".join(KEYWORDS(x).name for x in keywords)}]'
        except TypeError:
            return None

    ###########################################################################
    # utilities
    ###########################################################################

    def pretty_print_sipm(self, sipm_number):
        """
        Generate a string for the SiPM record based on information derived
        from the tray file.

        -----------------------------------------------------------------------
        args
            sipm_number : int
        -----------------------------------------------------------------------
        returns : string
            e.g. 'sipm_17,  3,  9, 9346469, 14 # [SILICONRESIDUE, PASS]'
        -----------------------------------------------------------------------
        """
        snu = self.sipms[sipm_number]
        line = ', '.join(
            [
                f'sipm_{sipm_number:02}',
                f'{snu['column']:>2}',
                f'{snu['row']:>2}',
                f'{snu['lot_number']}',
                f'{snu['wafer_number']:>2}',
            ]
        )
        keyword_text = self.keywords_string(snu['keywords'])
        return line if keyword_text is None else ' # '.join([line, keyword_text])

    ###########################################################################
    # search
    ###########################################################################

    def dusty(self):
        """
        Return SiPM numbers with silicon residue.

        -----------------------------------------------------------------------
        args : none
        -----------------------------------------------------------------------
        returns : list
            sorted SiPM numbers afflicted with silicon residue
        -----------------------------------------------------------------------
        """
        return sorted(
            sipm_number
            for sipm_number, details in self.sipms.items()
            if (
                details.get('keywords') is not None
                and KEYWORDS.SILICONRESIDUE in details['keywords']
            )
        )

    def get_sipm(self, ident):
        """
        Return the full record for a given SiPM in this tray file.

        -----------------------------------------------------------------------
        args
            ident : dict or iterable that preseves order
                e.g. {
                    'column': 3, 'row': 10,
                    'lot_number': 9346469, 'wafer_number': 14
                }
                or
                (3, 10, 9346469, 14)
        -----------------------------------------------------------------------
        returns : dict or None
            e.g. {
                'column': 3, 'row': 10,
                'line': 'sipm_03,  3, 10  # [SILICONRESIDUE, PASS]',
                'keywords': [13, 2], 'sipm_number': 3,
                'lot_number': 9346469, 'wafer_number': 14,
                'path': '.../9346469/14/9346469_14_green_tray_07.txt'
            }
        -----------------------------------------------------------------------
        """
        if isinstance(ident, tuple):
            ident = {
                'column': ident[0],
                'row': ident[1],
                'lot_number': ident[2],
                'wafer_number': ident[3],
            }

        def h(s, ident, keys):
            _k, v = s
            return s if all(map(lambda x: v[x] == ident[x], keys)) else None

        keys = ['column', 'row', 'lot_number', 'wafer_number']
        match = functools.partial(h, ident=ident, keys=keys)

        try:
            result = next(
                itertools.dropwhile(
                    lambda x: x is None, map(match, self.sipms.items())
                )
            )
        except StopIteration:
            result = None

        if result is not None:
            sipm_number, details = result
            return details | {'path': f'{self.path}', 'sipm_number': sipm_number}

        return result

    @property
    def wafers(self):
        """
        Return a set of unique wafers used in this tray file.

        -----------------------------------------------------------------------
        args : none
        -----------------------------------------------------------------------
        returns : set
            e.g. {'9346499.13', '9346499.14', '9346499.15'}
        -----------------------------------------------------------------------
        """
        return {
            f'{details["lot_number"]}.{details["wafer_number"]:02}'
            for details in self.sipms.values()
        }

    ###########################################################################
    # import from file
    ###########################################################################

    @staticmethod
    def lot_wafer(line):
        """
        Extract lot or wafer number value from tray file line.

        -----------------------------------------------------------------------
        args
            line : iterable of two strings
                e.g. ['lot', '9473059'] or ['wafer_number', '10']
        -----------------------------------------------------------------------
        returns : int or None
        -----------------------------------------------------------------------
        """
        parameter = None

        try:
            _, value = line
        except ValueError:
            return parameter

        with contextlib.suppress(ValueError):
            parameter = int(value)

        return parameter

    def process_sipm_definition(self, line, fields, keywords):
        """
        Check if line defining a SiPM is valid.

        -----------------------------------------------------------------------
        args
            line : string or None
                e.g. 'sipm_18, 11, 13'
            fields : list of str or None
                e.g. ['sipm_18', '11', '13']
            keywords : list of int or None
                e.g. [13, 2]
        -----------------------------------------------------------------------
        returns : bool
            tray_file_sipms : list of dict
                no explicit return, mutable type amended in place
                e.g.
                [
                    {
                        'column': 6, 'row': 19,
                        'lot_number': 9324029, 'wafer_number': 4,
                        'line': 'sipm_24,  6, 19, 9324029,  4,  # [NRP, MD, PASS]',
                        'keywords': [9, 8, 2], 'sipm_number': 24
                    }
                ]
        -----------------------------------------------------------------------
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
                pass
            else:
                # short form
                # sipm_number, wafer_column, wafer_row
                _, sipm_num = sipm_key(key)

                if sipm_num is not None:
                    with contextlib.suppress(ValueError):
                        self.sipms[sipm_num] = {
                            'column': int(column), 'row': int(row),
                            'line': line.strip(), 'keywords': keywords,
                        }
        else:
            # long form
            # sipm_number, wafer_column, wafer_row, wlot, wnum
            _, sipm_num = sipm_key(key)

            if sipm_num is not None:
                with contextlib.suppress(ValueError):
                    self.sipms[sipm_num] = {
                        'column': int(column), 'row': int(row),
                        'line': line.strip(), 'keywords': keywords,
                        'lot_number': int(lot_num),
                        'wafer_number': int(wafer_num),
                    }

    def tray_file_lines(self):
        """
        Yield fields extracted from individual tray file lines.
        Extracts and validates condition keyword list for each SiPM.

        Fields are delimited by spaces and/or commas:

        'a,b,c'     -> ['a', 'b', 'c']
        'a b,c'     -> ['a', 'b', 'c']
        'a b, ,,,c' -> ['a', 'b', 'c']

        -----------------------------------------------------------------------
        args
            filename : string
        -----------------------------------------------------------------------
        yields : int, list
        -----------------------------------------------------------------------
        """
        with open(self.path, 'r', encoding='utf-8') as infile:

            for _line_number, line in enumerate(infile, start=1):

                # parts = line.split('#')[0].strip()

                no_comment, _, comment = line.partition('#')
                no_comment = no_comment.strip()
                comment = comment.strip()

                try:
                    keywords_string = re.search(r'\[.*\]', comment).group(0)
                except AttributeError:
                    keywords = None
                else:
                    # kwo is a list to preserve order
                    kwo = []
                    fail = False
                    for kstr in keywords_string[1:-1].split(','):
                        try:
                            kwo.append(KEYWORDS[kstr.strip()].real)
                        except KeyError:
                            fail = True

                    keywords = None if fail else kwo

                    if keywords is not None:
                        # The keyword list should always contain PASS or FAIL,
                        # other condition codes are optional.
                        if not any(x in keywords for x in [KEYWORDS.PASS, KEYWORDS.FAIL]):
                            keywords = None

                fields = [
                    field.strip()
                    for field in re.split(r'[, ]+', no_comment)
                    if field.strip()
                ]

                # Only yield if there's something to process.
                # The tray number is for internal site usage only, it won't be
                # added to the database so ignore it.
                if fields and not fields[0].startswith('tray'):
                    yield line, fields, keywords

    def import_from_file(self):
        """
        Import data recorded during the wafer picking stage, where a file
        represents the contents of a SiPM tray (24 SiPMS).

        -----------------------------------------------------------------------
        args : none
        -----------------------------------------------------------------------
        returns : none
        -----------------------------------------------------------------------
        """
        lot_number = wafer_number = None

        for line, fields, keywords in self.tray_file_lines():

            if fields[0].startswith('lot'):
                lot_number = self.lot_wafer(fields)

            elif fields[0].startswith('wafer_number'):
                wafer_number = self.lot_wafer(fields)

            elif fields[0].startswith('sipm_'):
                self.process_sipm_definition(line, fields, keywords)

        # For SiPMs that didn't have a wafer lot and wafer number explicitly
        # specified, fill in the default values. We can't guarantee that the
        # wafer and lot number will precede SiPM definitions, so this can't
        # be done earlier.

        default_wafer_present = lot_number is not None and wafer_number is not None

        for sipm_number, details in copy.deepcopy(self.sipms).items():
            if any(x not in details for x in ['lot_number', 'wafer_number']):
                if default_wafer_present:
                    self.sipms[sipm_number].update(
                        {'lot_number': lot_number, 'wafer_number': wafer_number}
                    )
                else:
                    del self.sipms[sipm_number]
                    self.import_errors.append(
                        'default wafer lot and/or number missing: '
                        f'required by SiPM {sipm_number}'
                    )

        # store SiPMs

        for sipm_number, details in self.sipms.items():
            try:
                fail = KEYWORDS.FAIL in details['keywords']
            except TypeError:
                # keyword is None, convention is that no keywords present
                # indicates a good SiPM.
                self.sipms_good[sipm_number] = details
            else:
                self.keywords.append(details['keywords'])
                if fail:
                    self.sipms_bad[sipm_number] = details
                else:
                    self.sipms_good[sipm_number] = details

        # flatten keywords list
        self.keywords = list(itertools.chain.from_iterable(self.keywords))

    ###########################################################################
    # export to file
    ###########################################################################

    def export_to_file(self, path):
        """
        Write tray file to filestore.

        -----------------------------------------------------------------------
        args
            path : string or io.StringIO
                E.g. '/Users/avt/tmp/reprocessed_vif_green_15.txt'
        -----------------------------------------------------------------------
        returns : none
        -----------------------------------------------------------------------
        """
        lines = [f'{line}\n' for line in map(self.pretty_print_sipm, self.sipms)]
        lines.insert(0, '# sipm_num, wafer_col, wafer_row, lot, wafer_num\n')

        if isinstance(path, io.StringIO):
            path.writelines(lines)
        else:
            with open(path, 'w', encoding='utf-8') as file:
                file.writelines(lines)

###############################################################################
# support functions
###############################################################################


def sipm_key(key):
    """
    Check if a string represents a SiPM.

    ----------------------------------------------------------------------
    args
        key : string
            e.g. 'sipm_1', 'sipm_01' or 'sipm_23'
    ----------------------------------------------------------------------
    returns : (str, int) or (None, None)
        e.g. ('sipm_1', 1)
            int if the SiPM information appears valid, None otherwise
            internal_key : string, e.g. 'sipm_1' return this to strip leading
            zeroes from 'sipm_01' if that representation was used in the tray
            file.
    ----------------------------------------------------------------------
    """
    try:
        sipm_text, number = key.split('_')
    except (AttributeError, ValueError):
        sipm_text = number = internal_key = None
    else:
        number = int(number)
        internal_key = f'sipm_{number}'

    return internal_key, (
        number if sipm_text == 'sipm' and 1 <= number <= 24 else None
    )
