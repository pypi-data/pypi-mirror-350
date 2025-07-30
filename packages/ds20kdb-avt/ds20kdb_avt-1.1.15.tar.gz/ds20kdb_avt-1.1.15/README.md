# DarkSide-20k pre-production database low-level interaction

This is a cross-platform Python interface to the DarkSide-20k pre-production database. It is sufficiently friendly to be used interactively, and can be used as a foundation to build more complex database interactions. The package includes a number of command-line automation scripts.

The software can be obtained/upgraded from [pypi.org](https://pypi.org/project/ds20kdb-avt/) using `python3 -m pip install --upgrade ds20kdb-avt`.

The software requires Python 3.8 or newer for full functionality, though it will tolerate Python 3.6 and 3.7.

## Example interactive usage

The following can be performed once authentication has been configured:

```python
macbook:packaging avt$ . ~/dev/pve312/bin/activate
(pve312) macbook:packaging avt$ python3
Python 3.12.0 (main, Oct  2 2023, 18:38:13) [Clang 14.0.3 (clang-1403.0.22.14.1)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from ds20kdb import interface

>>> # check version number with
>>> interface.__version__
'0.1.20'

>>> # create an instance so we can interact with the database
>>> db = interface.Database()

>>> # basic describe and get operations
>>> db.describe().data
['vasic', 'vasic_grip_ring', 'vasic_wafer', 'vcable', 'detector', 'dummy', 'user_test', 'dummyload_test', 'motherboard', 'sipm', 'wafer', 'pcb', 'pdu', 'pdu_pulse_test', 'attribute_description', 'solder', 'attribute', 'vpcb', 'vpdu', 'vpcb_asic', 'vpcb_asic_test', 'vmotherboard', 'vpcb_test', 'vmotherboard_test', 'tile_test', 'wafer_defects', 'vtile', 'pcb_test', 'tile', 'dummyload', 'cryoprobe_card', 'tile_setup', 'vpdu_test', 'vtile_cold_test', 'noa_users', 'vtile_test', 'pdu_status', 'vasic_test', 'tile_status', 'sipm_qc', 'sipm_test', 'vpdu_cold_test', 'acs', 'wafer_status', 'pcb_status', 'motherboard_status', 'amicra_settings']
>>> db.describe('wafer').data
['wafer_pid', 'manufacturer', 'lot', 'wafer_number', 'production_date', 'spad_size', 'dose', 'description', 'checksum']
>>> db.get('wafer').data
      wafer_pid  manufacturer      lot  ...  dose                                        description  checksum
0             5             2  9262109  ...     3  backside: Au2 L pressure 1week waiting run B -...        --
1             6             2  9262109  ...     3  backside: Au1 H pressure 1week waiting run A -...        --
2             2             2  9262109  ...     3  backside: Au1 H pressure 2weeks waiting run A ...        --
3             4             2  9262109  ...     3  backside: Au1 H pressure 1week waiting run A -...        --
4             3             2  9262109  ...     3  backside: Au3 L pressure 1week waiting run C -...        --
...         ...           ...      ...  ...   ...                                                ...       ...
1610       1599             2  9473059  ...     3                                     production lot        E0
1611       1600             2  9473059  ...     3                                     production lot        D3
1612       1602             2  9473059  ...     3                                     production lot        C1
1613       1601             2  9473059  ...     3                                     production lot        C6
1614          1             2  9262109  ...     3  backside: Au2 L pressure 2weeks waiting run B ...        --

[1615 rows x 9 columns]

>>> # narrow the selection
>>> db.get('wafer', lot=9262109, wafer_number=3).data
   wafer_pid  manufacturer  ...                                        description  checksum
0          1             2  ...  backside: Au2 L pressure 2weeks waiting run B ...       NaN

[1 rows x 9 columns]

>>> # obtain specific values, such as the expiry data of a syringe of solder using something like this:
>>> db.get('solder', solder_pid=1).data.expiry_date.values[-1]
'2022-12-02 00:00:00'
>>> db.get('solder', solder_pid=1).data.solder_type.values[-1]
'Indium Paste NC-SMQ80 Ind#1E 52In48Sn Type 4 83%, P.No. 83752'

>>> # and create new entries easily
>>> # E.g. to create a new solder syringe, first find one that we can modify:
>>> solder_pid = db.get('solder', solder_pid=4).data.solder_pid.values[-1]
>>> solder_pid
4
# take a quick look at the dictionary that defines it:
>>> select = {'solder_pid': solder_pid}
>>> db.get_table_row_and_modify('solder', select)
{'manufacturer': 4, 'solder_type': 'Indium Paste NC-SMQ80 Ind#1E 52In48Sn Type 4 83%, P.No. 83752', 'production_date': '2022-06-02 00:00:00', 'room_temperature_date': '2022-10-26 19:45:00', 'expiry_date': '2022-12-02 00:00:00', 'syringe_id': 8, 'lot': 'PS11120734', 'mass': 25}

>>> # plan to change the room temperature data and the syringe id
>>> modify = {'room_temperature_date': '2022-11-26 11:00:00', 'syringe_id': 9}

>>> # create a new dictionary with the desired changes
>>> wdict = db.get_table_row_and_modify('solder', select, modify)
>>> wdict
{'manufacturer': 4, 'solder_type': 'Indium Paste NC-SMQ80 Ind#1E 52In48Sn Type 4 83%, P.No. 83752', 'production_date': '2022-06-02 00:00:00', 'room_temperature_date': '2022-11-26 11:00:00', 'expiry_date': '2022-12-02 00:00:00', 'syringe_id': 9, 'lot': 'PS11120734', 'mass': 25}

>>> # we can then write this to the database with:
>>> db.write_solder(wdict)
```
