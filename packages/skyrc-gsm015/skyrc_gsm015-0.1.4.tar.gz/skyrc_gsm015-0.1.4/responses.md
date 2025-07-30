# Response N - Serial number

| Element| Length | Example | Notes |
|-|-|-|-|
| Endpoint | 1 byte | 0x02 | |
| Reponse identifier | 1 byte | 'N' | |
| Serial number | 16 bytes | '3530303032340100000000010f0100c3' | Serial number |

Example input received:
```
0000   02 4e 35 30 30 30 32 34 01 00 00 00 00 01 0f 01   .N500024........
0010   00 c3 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0020   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0030   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
```

# Response G - Basic data

| Element| Length | Example | Notes |
|-|-|-|-|
| Endpoint | 1 byte | 0x02 | |
| Reponse identifier | 1 byte | 'G' | |
| Miles | 1 byte | 0x01 | 0: KM; 1: Miles (assumed, not checked) |
| Frequency | 1 byte | 0x0a | 1: 10Hz; 2: 5Hz; 5; 2Hz; 10: 1Hz |
| Time zone | 1 byte | 0x0c | 12 = UTC |
| Unknown | 1 byte | 0x01 | Not processed by vendor software |
| Firmware Version | 2 bytes | 0x010f | High.Low (1.15) |
| Unknown | 1 byte | 0x01 | Not processed by vendor software |

Example input received:
```
0000   02 47 01 0a 0c 01 01 0f 01 00 00 00 00 01 0f 01   .G..............
0010   00 c3 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0020   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0030   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
```

# Response P - Position

Position responses have some special cases to indicate special data types:

| Element| Length | Example | Notes |
|-|-|-|-|
| Endpoint | 1 byte | 0x02 | |
| Reponse identifier | 1 byte | P | |
| Data type identifier | 3 bytes | 0xEEEEEE | ??? |
| Payload data | Remainder | | |

Where there is no special data type identifier, the data type identifier forms part of the payload data. See below.

## Data type 0xFFFFFF - Unknown

Note: This is a NOP in the supplied software.

## Data type 0xEEEEEE - Date/time

| Element| Length | Example | Notes |
|-|-|-|-|
| Endpoint | 1 byte | 0x02 | |
| Reponse identifier | 1 byte | P | |
| Data type identifier | 3 bytes | 0xEEEEEE | ??? |
| Timestep | 1 byte | ? | ??? |
| MilMode | 1 byte | ? | ??? |
| TimeZone | 1 byte | ? | ??? |
| Year | 1 byte | ? | Convert to YYYY with 2000 + year |
| Month | 1 byte | ? | ??? |
| Day | 1 byte | ? | ??? |
| Hour | 1 byte | ? | ??? |
| Minute | 1 byte | ? | ??? |
| Second | 1 byte | ? | ??? |

## Data type 0xDDDDDD - Distance

| Element| Length | Example | Notes |
|-|-|-|-|
| Endpoint | 1 byte | 0x02 | |
| Reponse identifier | 1 byte | P | |
| Data type identifier | 3 bytes | 0xDDDDDD | ??? |
| Distance | 3 bytes | ? | Double value |

## Data type anything other value - Position

| Element| Length | Example | Notes |
|-|-|-|-|
| Endpoint | 1 byte | 0x02 | |
| Response identifier | 1 byte | P | |
| Speed | 3 bytes | ? | ??? |
| Altitude | 3 bytes | ? | ??? | ??? |
| Longitude polarity | 1 byte | ? | 
| Longitude degrees | 1 byte | ? | ??? |
| Longitude minutes | 3 bytes | ? | ??? |
| Latitude polarity | 1 byte | ? | 
| Latitude degrees | 1 byte | ? | ??? |
| Latitude minutes | 3 bytes | ? | ??? |


Example input received:
```
0000   02 50 00 0a 0c 01 00 00 01 0f 01 00 00 00 00 00   .P..............
0010   00 00 01 0a 0c 01 00 00 01 0f 01 00 00 00 00 00   ................
0020   00 00 01 0a 0c 01 00 00 01 0f 02 00 00 00 00 00   ................
0030   00 00 01 0a 0c 01 00 00 01 0f 07 00 00 00 00 00   ................
```
...

```
0000   02 50 ff ff ff ff ff ff ff ff ff ff ff ff ff ff   .P..............
0010   ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff   ................
0020   ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff   ................
0030   ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff   ................
```
...
```
0000   02 50 ff ff ff ff 4a 00 4a 01 4a 02 4a 03 4a 04   .P....J.J.J.J.J.
0010   4a 05 4a 06 4a 07 4a 08 4a 09 4a 0a 4a 0b 4a 0c   J.J.J.J.J.J.J.J.
0020   4a 0d 4a 0e 4a 0f 4a 10 4a 11 4a 12 4a 13 4a 14   J.J.J.J.J.J.J.J.
0030   4a 15 4a 16 4a 17 4a 18 4a 19 4a 1a 4a 1b 4a 1c   J.J.J.J.J.J.J.J.
```
...
```
0000   02 50 4a 1d 4a 1e 4a 1f 4a 20 4a 21 4a 22 4a 23   .PJ.J.J.J J!J"J#
0010   4a 24 4a 25 4a 26 4a 27 4a 28 4a 29 4a 2a 4a 2b   J$J%J&J'J(J)J*J+
0020   4a 2c 4a 2d 4a 2e 4a 2f 4a 30 4a 31 4a 32 4a 33   J,J-J.J/J0J1J2J3
0030   4a 34 4a 35 4a 36 4a 37 4a 38 4a 39 4a 3a 4a 3b   J4J5J6J7J8J9J:J;
```

Note: The first 8K appears to be thrown away and data continues to 1M

# Response E - Unknown

Response E seems to be sent at the end of the data

| Element | Length | Example | Notes |
|-|-|-|-|
| Endpoint | 1 byte | 0x02 | |
| Reponse identifier | 1 byte | E | |
| Unknown | Remainder | 0xff | Unknown |

Example input received:
```
0000   02 45 ff ff ff ff ff ff ff ff ff ff ff ff ff ff   .E..............
0010   ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff   ................
0020   ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff   ................
0030   ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff   ................
```