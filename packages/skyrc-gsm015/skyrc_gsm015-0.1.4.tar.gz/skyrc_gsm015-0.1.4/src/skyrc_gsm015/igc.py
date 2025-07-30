"""SkyRC GSM015 USB Data Reader - Export IGC format files."""

import datetime
import aerofiles

def write_igc(filename, flight_positions):
    """Write the flight positions to the specified filename in IGC format."""
    with open(filename, 'wb') as fp:
        writer = aerofiles.igc.Writer(fp)

        # Note: https://aerofiles.readthedocs.io/en/latest/guide/igc-writing.html suggests=
        # using the FXA extension, but we don't have accuracy data to use.       
        # e.g. writer.write_fix_extensions([('FXA', 3), ('SIU', 2), ('ENL', 3)])

        need_headers = True
        dt = None

        for r in flight_positions:
            if r['Data Type'] == 'DateTime':
                dt = r['DateTime']

                # Write header as soon as we've got a date
                if(need_headers):
                    writer.write_headers({
                        'manufacturer_code': 'SKY',
                        'logger_id': '015',
                        'date': dt.date(),
                        'logger_type': 'SKYRC,GSM-015',
                        'gps_receiver': 'Unknown',
                    })
                    need_headers = False

            elif r['Data Type'] == 'Position':
                if dt is None:
                    continue
                writer.write_fix(
                    dt.time(),
                    latitude=r['Latitude'],
                    longitude=r['Longitude'],
                    valid=True,
                    gps_alt=int(r['Altitude']),
                )
                dt = dt + datetime.timedelta(seconds=1)
            elif r['Data Type'] in ['NOP', 'Distance']:
                pass
            else:
                print(r)
