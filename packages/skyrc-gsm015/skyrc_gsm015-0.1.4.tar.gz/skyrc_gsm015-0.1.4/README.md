# SkyRC-GSM015 GNSS Speed Meter data extractor
The SkyRC GSM-015 GNSS Speed Meter happens to work as a GNSS logger as well as it's speed functions.

![Picture of SkyRC GSM-015 GNSS Speed Meter](https://github.com/matburnham/skyrc-gsm015/raw/main/doc/device.jpg)

The OEM software supplied is not ideal for automated download of track logs. This command line Python tool/library allows automatic download of the track logs and export in IGC format.

## Installation

```bash
pip install skyrc_gsm015[tqdm]
```

## Usage

Example command line usage:
```bash
  $ skyrc-gsm015 -r -o rawdata.bin
  $ skyrc-gsm015 -i rawdata.bin
```

Example library usage:
```python
  #!/bin/python
  import skyrc_usb
  flights = get_all_flight_data()
```

## Limitations
Setting of the device configuration options is not currently supported. Appropriate configuration should be set using the OEM tool.

## Links
* [OEM marketing material, manuals and software](https://www.skyrc.com/gpsgsm015)

