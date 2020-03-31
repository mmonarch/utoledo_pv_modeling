#!/usr/bin/python3
#
# pv_io.py

import datetime as dt
import pandas as pd

from configparser import ConfigParser
from os import path
from ut_pv.pv_exceptions import (PVIllegalArgumentError,
                                 PVIOError,
                                 PVConfigError)

PV_CONFIG='config.ini'
PV_DATA_SECTION='PV_DATA'

PV_DATAPATH_KEY='database_path'
PV_FILENAME_KEY='filename_format'

# Load in config file
def load_config(file_path):
    pv_config = ConfigParser(interpolation=None)
    pv_config.read(PV_CONFIG)
    return pv_config

# Load the given pv data file.
def read_pv_file(file_path, set_index=False):

    # Raise error if file does not exist
    if not path.exists(file_path):
        raise PVIOError("'{}' does not exist.".format(file_path))

    # Read in recorded data
    pv_data = pd.read_csv(filepath_or_buffer=file_path,
                          names=['date', 'total energy',
                                 'module temperature',
                                 'air temperature',
                                 'ac power', 'ghi'],
                          skiprows=2,
                          parse_dates=['date'])

    # Set index if specified
    if set_index:
        pv_data = pv_data.set_index(['date'])

    # Return data
    return pv_data

# Load recorded data for a certain date.
def load_date(date=None, year=None, month=None, day=None,
        pv_config=None, set_index=False, **kwargs):

    # Verify correct arguments are present
    if not date:
        if year and month and day:
            date = dt.datetime(year, month, day)
        else:
            raise PVIllegalArgumentError("'year', 'month', and " \
                    "'day' parameters must be specified when 'date' " \
                    "omitted.")

    # If no config specified, load config from current directory
    if not pv_config:
        pv_config = ConfigParser(interpolation=None)
        pv_config.read(PV_CONFIG)

    # Create filename from date and verify it exists
    try:
        database_path = pv_config.get(PV_DATA_SECTION, PV_DATAPATH_KEY)
        filename = date.strftime(
                pv_config.get(PV_DATA_SECTION, PV_FILENAME_KEY))
        file_path = path.join(database_path, filename)
    except:
        raise PVConfigError("An error exists in the \'{}\' section " \
                "of the config file.".format(PV_DATA_SECTION))

    # Load data from file
    return read_pv_file(file_path, set_index)

