#!/usr/bin/python3
#
# irradiance.py

from pvlib.irradiance import (erbs,
                              gti_dirint,
                              aoi)
from pvlib.solarposition import get_solarposition
from ut_pv.r1_utils import (get_toledo,
                            toledo_lat,
                            toledo_lon,
                            toledo_alt)

import datetime as dt
from pandas import DataFrame

# Return the clear sky data
def get_clear_sky(times, location=None, winds=None, temp=None,
        tz='America/Detroit'):
    # Set location
    if not location:
        location = get_toledo(tz)

    # Retrieve clear sky irradiane
    cs_data = location.get_clearsky(times)

    # Set wind speeds and air temperatures if provided
    if winds:
        cs_data["wind_speed"] = winds
    if temp:
        cs_data["air_temp"] = temp

    return cs_data

# Use erbs model along with collected ghi to generate weather data
def get_erbs_weather(pv_data, location=None, winds=None, temp=None,
        tz='America/Detroit'):
    # Set location
    if not location:
        location = get_toledo(tz)

    # Initialize time offset
    times = pv_data.index.tz_localize('Etc/GMT+{}'.format(tz))
    pv_data.index = times

    # Create list of DNIs and DHIs
    solar_pos = location.get_solarposition(times)
    weather_data = erbs(row['ghi'], solar_pos['zenith'], times)

    # Set wind speeds and air temperatures if provided
    if winds:
        weather_data["wind_speed"] = winds
    if temp:
        weather_data["air_temp"] = temp

    return weather_data

# Use gti_dirint
def get_sam_weather(pv_data, location=None, winds=None, temp=None,
        tz='America/Detroit'):
    # Set location
    if not location:
        location = get_toledo(tz)

    # Initialize time offset
    times = pv_data.index.tz_localize(tz)
    pv_data.index = times

    # Calculate irradiance
    solar_pos = get_solarposition(times, toledo_lat,
                    toledo_lon, toledo_alt)
    aoi_ = aoi(35, 180, solar_pos['zenith'], solar_pos['azimuth'])
    weather_data = gti_dirint(pv_data['total energy'], aoi_, 
                        solar_pos['zenith'], solar_pos['azimuth'],
                        times, 35, 180)

    # Add wind and temp
    if winds:
        weather_data["wind_speed"] = winds
    if temp:
        weather_data["air_temp"] = temp

    return weather_data

