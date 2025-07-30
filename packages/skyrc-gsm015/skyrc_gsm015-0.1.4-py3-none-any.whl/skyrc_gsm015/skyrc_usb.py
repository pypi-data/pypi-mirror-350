"""SkyRC GSM015 USB Data Reader - USB functions

Reads data from the SkyRC GSM015 device via USB and parses it into a more usable format.
"""

import usb.core
import usb.util
import struct

# Try to use tqdm if installed, otherwise fall back to quiet
try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterator, *args, **kwargs):
        return iterator

def find_device_endpoints():
  """Find the USB device and its endpoints."""
  dev = usb.core.find(idVendor=0x28E9, idProduct=0x028A)
  if dev is None:
      raise ValueError('SkyRC GSM-015 USB device not found')

  # set the active configuration. With no arguments, the first
  # configuration will be the active one
  dev.set_configuration()

  cfg = dev.get_active_configuration()
  intf = cfg[(0,0)]

  ep_out = usb.util.find_descriptor(
      intf,
      # match the first OUT endpoint
      custom_match = \
      lambda e: \
          usb.util.endpoint_direction(e.bEndpointAddress) == \
          usb.util.ENDPOINT_OUT)
  assert ep_out is not None

  ep_in = usb.util.find_descriptor(
      intf,
      # match the first IN endpoint
      custom_match = \
      lambda e: \
          usb.util.endpoint_direction(e.bEndpointAddress) == \
          usb.util.ENDPOINT_IN)
  assert ep_in is not None

  return dev, ep_out, ep_in

def request_data(ep_out):
  """Build and send the request data command to the device."""

  base_address = 0x08004000
  cmd = list(struct.pack("<b4sI55p", ep_out.bEndpointAddress, b'CMDP', base_address, b''))

  # Note: the above struct.pack is doing the same as this:
  # cmd = [0] * 64
  # cmd[0]=1
  # cmd[1]=0x43
  # cmd[2]=0x4d
  # cmd[3]=0x44
  # cmd[4]=0x50
  # cmd[5]=base_address & 255
  # cmd[6]=(base_address >> 8) & 255
  # cmd[7]=(base_address >> 16) & 255
  # cmd[8]=(base_address >> 24) & 255

  ep_out.write(cmd);

def read_data_from_device(dev, ep_in):
  """Read the data from the device."""

  # With 18 hours storage at 1Hz logging, I'd expect 60 sec x 60 min x 18 hours = 64800 records, but it
  # reads 64 bytes at a time. Each record is 16 bytes. So 60 x 60 x 18 / 4 = 16200 records. There's slightly more
  # read before it throws an exception.

  # Each record has a two byte header, which we don't need so throw away.

  total_records = 16914
  data = bytearray()
  print("Reading data from device")
  try:
    for i in tqdm(range(total_records)):
      record = dev.read(ep_in.bEndpointAddress, ep_in.wMaxPacketSize)
      assert(len(record)==64)
      data.extend(record[2:])
  except usb.core.USBError as e:
    if e.errno == 110:  # Timeout error
      print("Read timeout, no data received.")
    else:
      print(f"USBError: {e}")

  return data
