#!/usr/bin/python3
#
# weather.py

from ut_pv.r1_utils import (get_toledo,
                            toledo_lat,
                            toledo_lon,
                            toledo_alt)

# Return the clear sky data
def get_clear_sky(times, location=None, winds=None, temp=None, tz=4):
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
def get_erbs_weather(pv_data, location=None, winds=None, temp=None, tz=4):
    # Set location
    if not location:
        location = get_toledo(tz)

    # Initialize time offset
    t_offset = dt.timedelta(hours=tz)

    # Create list of DNIs and DHIs
    dnis = []
    dhis = []
    for t, row in pv_data.iterrows():
        solar_pos = get_solarposition(t + t_offset, toledo_lat,
                toledo_lon, toledo_alt)
        irradiance_data = erbs(row['ghi'], solar_pos['zenith'],
                t + t_offset)
        dnis.append(irradiance_data['dni'][0])
        dhis.append(irradiance_data['dhi'][0])

    # Build dataframe
    weather_data = DataFrame({'date': times})
    weather_data = weather_data.set_index('date')
    weather_data['ghi'] = list(pv_data['ghi'])
    weather_data['dni'] = dnis
    weather_data['dhi'] = dhis

    # Set wind speeds and air temperatures if provided
    if winds:
        weather_data["wind_speed"] = winds
    if temp:
        weather_data["air_temp"] = temp

    return weather_data


