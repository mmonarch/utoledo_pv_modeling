#!/usr/bin/python3
#
# analyze_year.py

import datetime as dt

from configparser import ConfigParser
from ut_pv.pv_io import load_date

YEAR_CONFIG='sample_year.ini'
YEAR_BASIC_SECTION='Basic'
YEAR_PATCH_SECTION='Patch_Dates'

BASE_YEAR_KEY='base_year'
DATE_FMT_KEY='date_fmt'

def run_year(daily_analysis, year_config=None, **kwargs):
    # If no config specified, load config from current directory
    if not year_config:
        year_config = ConfigParser(interpolation=None)
        year_config.read(YEAR_CONFIG)

    # Load settings from config
    base_year = year_config.getint(YEAR_BASIC_SECTION, BASE_YEAR_KEY)
    date_fmt = year_config.get(YEAR_BASIC_SECTION, DATE_FMT_KEY)

    # Set dates
    active_date = dt.datetime(year=base_year, month=1, day=1)
    end_date = dt.datetime(year=base_year+1, month=1, day=1)

    # Loop through days
    res = {}
    while active_date < end_date:
        date_str = active_date.strftime('%m/%d/%y')
        if date_str in year_config[YEAR_PATCH_SECTION]:
            patch = dt.datetime.strptime(
                year_config.get(YEAR_PATCH_SECTION, date_str),
                date_fmt)
            day_data = load_date(date=patch, set_index=True)
        else:
            day_data = load_date(date=active_date, set_index=True)

        res[active_date] = daily_analysis(day_data, **kwargs)

        active_date += dt.timedelta(days=1)

    return res
