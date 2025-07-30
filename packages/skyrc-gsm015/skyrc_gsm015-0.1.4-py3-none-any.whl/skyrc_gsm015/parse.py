"""SkyRC GSM015 USB Data Reader - Parsiong functions

Takes raw data read from the SkyRC GSM015 device and parses it into positions and flights.

Note: this module is based on a limited understanding of the data format.
It may not be entirely correct, but errors should become apparent quickly.
"""

import datetime

def parse_positions(d):
    """Returns a list of parsed positions (and other records) from the raw datastream."""

    # The first 8192 bytes of the data do not appear to relate directly to flights.
    # The format of this header data is not fully understood. The first 8192 bytes
    # could be simply skipped, but this data appears to confirm to a similar record
    # structure so can be skipped until the first DateTime record indicating the
    # start of a flight.

    RECORD_SIZE = 16
    positions = []
    started = False
    for i in range(0, len(d), RECORD_SIZE):
        p = d[i:i+RECORD_SIZE]
        pos = parse_position(p)
        if started or pos['Data Type'] == 'DateTime':
            # print(pos)
            started = True
            positions.append(pos)
    return positions

def parse_position(p):
    """Returns an object by parsing the data in a single position or other record."""
    data_type = p[:3].hex()
    
    if data_type == 'ffffff':
        return {'Data Type': 'NOP', 'Payload': p.hex()}
    elif data_type == 'eeeeee':
        timestep = p[0]
        milmode = p[1]
        timezone = p[2]
        year = 2000 + p[6]
        month = p[7]
        day = p[8]
        hour = p[9]
        minute = p[10]
        second = p[11]
        return {'Data Type': 'DateTime',
                'Timestep': timestep,
                'MilMode': milmode,
                'TimeZone': timezone,
                'DateTime': datetime.datetime(year, month, day, hour, minute, second)
                }
    elif data_type == 'dddddd':
        distance = int.from_bytes(p[:3], 'big')
        return {'Data Type': 'Distance', 'Distance': distance}
    else:
        speed = int.from_bytes(p[0:3], 'big') / 1000
        altitude = int.from_bytes(p[3:6], 'big') / 10 # TODO: consider sign in top bit
        lon_polarity = "+" if p[6]==0 else "-"
        lon_degrees = p[7]
        lon_minutes = int.from_bytes(p[8:11], 'big')
        lat_polarity = "+" if p[11]==0 else "-"
        lat_degrees = p[12]
        lat_minutes = int.from_bytes(p[13:16], 'big')
        return({'Data Type': 'Position',
                'Speed': speed,
                'Altitude': altitude,
                'Longitude': float("{}{}.{:07d}".format(lon_polarity, lon_degrees, lon_minutes)),
                'Latitude': float("{}{}.{:07d}".format(lat_polarity, lat_degrees, lat_minutes))})

def dump_rec_type(data):
    """Dump the number of records of each type. Useful for debugging and to understand the data format."""
    prev = None
    i = 1
    for r in data:
        if r['Data Type'] == prev:
            i = i+1
        else:
            print('{} x {}'.format(prev, i))
            i = 1
        prev = r['Data Type']

def dump_recs(data):
    """Dump all records. Useful for debugging and to understand the data format."""
    for r in data:
        if r['Data Type'] != 'NOP':
            print(r)

def split_flights(data):
    """Returns a list of flights based on the parsed positions.
    A flight starts with a DateTime record and ends with a Distance record,
    although we just look for another DateTime or EOF."""
    flights = []
    flight = []
    # Flights start with a DateTime record, accumulate until we get a DateTime record, or EOF
    for r in data:
        if r['Data Type'] == 'NOP':
            continue
        elif r['Data Type'] == 'DateTime':
            if len(flight) > 0:
                flights.append(flight)
            flight = []
        flight.append(r)
    flights.append(flight)
    return flights
