#!/usr/sbin/python3
#
# pv_model.py

import pandas as pd

# Generate results from R1 model
def run_models(models, weather, times=None, seperate_rows=False):
    # Create DataFrame
    if times:
        results = pd.DataFrame({'Datetime': times})
    else:
        results = pd.DataFrame({'Datetime': weather.index})
    results = results.set_index('Datetime')
    results['total_dc_power'] = 0
    results['total_ac_power'] = 0

    # Method to save row data
    def _record_row_results(model, name, df):
        df['{}_dc_power'.format(name)] = \
                (model.dc['i_mp'] * model.dc['v_mp']).fillna(0)
        df['{}_ac_power'.format(name)] = model.ac.fillna(0)
        df['{}_module_temp'.format(name)] = model.cell_temperature
        df['{}_effective_irradiance'.format(name)] = \
                model.effective_irradiance

    # Iterate over models
    for i, model in enumerate(models):
        # Run model
        if times:
            model.run_model(weather, times)
        else:
            model.run_model(weather)

        # Save row data if specified
        if seperate_rows:
            _record_row_results(model, "row{}".format(i), results)

        # Update total powers
        results['total_dc_power'] += \
                (model.dc['i_mp'] * model.dc['v_mp']).fillna(0)
        results['total_ac_power'] += model.ac.fillna(0)

        # Record a temp. and irradiance if not saving all row data
        if not seperate_rows and 'module_temp' not in results:
            results['module_temp'] = model.cell_temperature
            results['effective_irradiance'] = \
                    model.effective_irradiance

    return results

