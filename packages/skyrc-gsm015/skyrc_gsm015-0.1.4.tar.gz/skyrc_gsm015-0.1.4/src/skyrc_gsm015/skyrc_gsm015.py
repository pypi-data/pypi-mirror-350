#!/usr/bin/env python3
"""SkyRC GSM-015 USB Data Reader

Example command line usage:
  $ skyrc-gsm015 -r -o rawdata.bin
  $ skyrc-gsm015 -i rawdata.bin

Example library usage:
  #!/bin/python
  import skyrc_usb
  flights = get_all_flight_data()

Author: Mat Burnham
Last changed: 2025-18-05
"""

import argparse

from . import skyrc_usb
from . import parse
from . import igc

def save_data(filename, data):
  """Save the binary data to filename."""
  with open(filename, 'wb') as f:
      f.write(data)

def load_data(filename):
  """Load the binary data from filename."""
  with open(filename, 'rb') as f:
      data = f.read()
  return data 

def get_all_flight_data():
  """Get all flight data from the device."""
  dev, ep_out, ep_in = skyrc_usb.find_device_endpoints()
  skyrc_usb.request_data(ep_out)
  data = skyrc_usb.read_data_from_device(dev, ep_in)
  positions = parse.parse_positions(data)
  flights = parse.split_flights(positions)
  return flights

def main():
  parser = argparse.ArgumentParser(description="SkyRC GSM015 USB Data Reader")
  parser.add_argument("-r", "--read", action="store_true", help="Read data from device")
  parser.add_argument("-i", "--input", help="Read data from file")
  parser.add_argument("-o", "--output", help="Output data file")
  parser.add_argument("-e", "--export", help="Export IGC format file")
  args = parser.parse_args()

  if(args.read and args.input):
    parser.error("either --read and --input, but not both are required")
    exit(1)

  if(not args.read and args.output):
    parser.error("doesn't make sense to use --output without --read")
    exit(2)

  if(args.read):
    try:
      dev, ep_out, ep_in = skyrc_usb.find_device_endpoints()
    except ValueError as e:
      print("Error: {}".format(e))
      exit(1)
    skyrc_usb.request_data(ep_out)
    data = skyrc_usb.read_data_from_device(dev, ep_in)
    if(args.output):
      print("Storing data in {}".format(args.output));
      save_data(args.output, data)
  elif(args.input):
      data = load_data(args.input)
  else:
    parser.error("either --read or --input required")
    exit(2)
  
  # Parse the data and export IGC files
  positions = parse.parse_positions(data)
  flights = parse.split_flights(positions)
  print("Found {} flights".format(len(flights)))
  for flight in flights:
    r = flight[0]
    dt = r['DateTime'].strftime("%Y%m%d-%H%M%S")
    igc_export_filename = "{}-{}.igc".format(args.export, dt)
    if(args.export):
        export_written = " written to {}".format(igc_export_filename)
    else:
        export_written = ""
    print(" * Flight {} with {:5d} records{}".format(dt, len(flight), export_written))

    if(args.export):
        igc.write_igc(igc_export_filename, flight)

  if(not args.export):
    print("Re-run with --export to export IGC files")

if __name__ == "__main__":
  main()
