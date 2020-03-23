#!/usr/bin/python3
#
# basic_examples.py

import ut_pv.r1_utils as r1

from ut_pv.pv_analysis import total_energy
from ut_pv.pv_io import load_date
from ut_pv.pv_model import run_models
from ut_pv.weather import get_clear_sky

import datetime as dt
import matplotlib.pyplot as plt

#
def clear_sky_irradiance(data):
    times = data.index.tz_localize('EST')
    cs_data = get_clear_sky(times)

    plt.plot(r1_data.index, r1_data['ghi'], label='actual')
    plt.plot(times, cs_data['ghi'], label='modeled')
    plt.legend()
    plt.show()

def clear_sky_power(data):
    times = data.index.tz_localize('EST')
    cs_data = get_clear_sky(times)

    rows = r1.create_r1_model()
    res = run_models(rows, cs_data)

    plt.plot(data.index, data['ac power'], label='actual')
    plt.plot(times, res['total_ac_power'], label='modeled')
    plt.legend()
    plt.show()

def daily_energy(data):
    times = data.index.tz_localize('EST')
    cs_data = get_clear_sky(times)

    rows = r1.create_r1_model()
    res = run_models(rows, cs_data)

    actual_energy = total_energy(data) / 1000
    model_energy = total_energy(res) / 1000

    print("Actual energy: {} kWh   Modeled energy: {} kWh".format(
        actual_energy, model_energy))

if __name__ == "__main__":
    try:
        r1_data = load_date(year=2016, month=4, day=23, set_index=True)
    except Exception as e:
        print("Failed to load data")
        exit()

    clear_sky_irradiance(r1_data)
    clear_sky_power(r1_data)
    daily_energy(r1_data)
