#!/usr/sbin/python3
#
# pv_analysis.py

# Return the total energy generated over a certain time
def total_energy(data, **kwargs):
    if 'hdr' in kwargs:
        hdr = kwargs['hdr']
    else:
        headings = ['ac power', 'total_ac_power']
        for heading in headings:
            if heading in data:
                hdr = heading
                break

    try:
        _ = data[1]
        int_idx = True
    except KeyError:
        int_idx = False

    data = data.fillna(0)

    p_date = None
    p_power = None
    energy = 0
    for i, row in data.iterrows():
        if int_idx:
            c_date = row['date']
        else:
            c_date = i

        # TODO: Add start and end time

        c_power = row[hdr]

        if not p_date:
            p_date = c_date
            p_power = c_power
            continue

        energy += (p_power + c_power) * (c_date - p_date).total_seconds() / 7200

        p_date = c_date
        p_power = c_power

    return energy
