# Device

| Item | Value |
| --- | --- |
| Device Name | GPSMeter |
| Description | USB Input Device |
| Device Type |	HID (Human Interface Device) |
| VendorID | 28000000000 |
| ProductID | 028a |
| Service Name | HidUsb |
| Service Description | @input.inf,%HID.SvcDesc%;Microsoft HID Class Driver |
| Driver Filename | hidusb.sys |
| Device Class | 0 |
| Device Mfg | (Standard system devices) |
| Friendly Name | 0 |
| Power | 100 mA |
| USB Version | 2 |
| Driver Description | USB Input Device |
| Instance ID | USB\VID_28E9&PID_028A\5&e8824e1&0&1 |
| Capabilities | Removable, SurpriseRemovalOK |

Looks like it's just a generic USB HID device (like a keyboard, mouse, etc.) which can throw data in/out.

# Device identifier

| Key | Value | Notes |
|-|-|-|
| VID | 28E9 | GDMicroelectronics |
| PID | 028A | Unlisted |

The only GDMicroelectronics PID is 0189. That's the GD32 DFU Bootloader (Longan Nano). I wonder if I could get it in DFU mode by pressing buttons. That might confirm the chip inside.

# Windows software

At first glance, only the Read Data button works properly. Configuration gives odd 'errors', although seems to actually still do the job.

The software is C#. It's pretty poorly written. "Form1" has the following function decompiled in dnSpy:

```
		// Token: 0x06000086 RID: 134 RVA: 0x000054AC File Offset: 0x000036AC
		private void btn_search_device_Click(object sender, EventArgs e)
		{
			...
			int i = 0;
			byte[] report_buf = new byte[64];
			report_buf[i++] = 1;
			report_buf[i++] = 67; // 'C'
			report_buf[i++] = 77; // 'M'
			report_buf[i++] = 68; // 'D'
			report_buf[i++] = 80; // 'P'
			int base_address = 134234112; // 0x8004000
			report_buf[i++] = (byte)(base_address & 255);
			report_buf[i++] = (byte)((base_address >> 8) & 255);
			report_buf[i++] = (byte)((base_address >> 16) & 255);
			report_buf[i++] = (byte)((base_address >> 24) & 255);
			this.CDProcess.SendBytes(report_buf);
			...
```

# Wireshark

This code sends a packet like this:

```
0000   01 43 4d 44 4e 00 40 00 08 00 00 00 00 00 00 00   .CMDN.@.........
0010   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0020   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0030   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
```

It appears to be a pack something like this:

| Element| Length | Example |
|-|-|-|
| Unknown | 1 byte | 0x01 |
| Command | 4 bytes | CMDN |
| Address | 4 bytes | 0x08004000 |

Base address appears to be fixed.

Other commands seem to be:

| Command | Meaning |
| - | - |
| CMDN | Configuration #1 |
| CMDG | Configuration #2 |
| CMDS | ? |
| CMDP | Read data |

# Configuration

Opening up the configuration window, sends CMDN then CMDG...

## CMDN

```
0000   01 43 4d 44 4e 00 40 00 08 00 00 00 00 00 00 00   .CMDN.@.........
0010   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0020   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0030   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
```

## Response

```
0000   02 4e 35 30 30 30 32 34 01 00 00 00 00 01 0f 01   .N500024........
0010   00 c3 ff ff ff ff ff ff ff ff ff ff ff ff ff ff   ................
0020   ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff   ................
0030   ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff   ................
```

## CMDG

```
0000   01 43 4d 44 47 00 40 00 08 00 00 00 00 00 00 00   .CMDG.@.........
0010   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0020   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0030   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
```

## Response

```
0000   1b 00 20 d9 6c 78 8b e2 ff ff 00 00 00 00 09 00   .. .lx..........
0010   01 01 00 03 00 81 01 40 00 00 00 02 47 01 0a 0c   .......@....G...
0020   01 01 0f 01 00 00 00 00 01 0f 01 00 c3 ff ff ff   ................
0030   ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff   ................
0040   ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff   ................
0050   ff ff ff ff ff ff ff ff ff ff ff                  ...........
```

# Set time zone

Set time zone to "UTC (+0:00)" brings up an error on screen, but sends:

## CMDS

```
0000   01 43 4d 44 53 01 0a 0c 01 00 40 00 08 00 00 00   .CMDS.....@.....
0010   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0020   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0030   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
```

## Response

```
0000   02 53 01 0a 0c 01 01 0f 01 00 00 00 00 01 0f 01   .S..............
0010   00 c3 ff ff ff ff ff ff ff ff ff ff ff ff ff ff   ................
0020   ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff   ................
0030   ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff   ................
```

# Save

Saving with MPH and 1Hz recording frequency send:

## CMDS

```
0000   01 43 4d 44 53 01 0a 0c 01 00 40 00 08 00 00 00   .CMDS.....@.....
0010   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0020   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0030   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
```

## Response

```
0000   02 53 01 0a 0c 01 01 0f 01 00 00 00 00 01 0f 01   .S..............
0010   00 c3 ff ff ff ff ff ff ff ff ff ff ff ff ff ff   ................
0020   ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff   ................
0030   ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff   ................
```

# Read data

The "Read data" button sends CMDP, then data streams back

## CMDP

```
0000   01 43 4d 44 50 00 40 00 08 00 00 00 00 00 00 00   .CMDP.@.........
0010   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0020   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0030   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
```

## Response

```
0000   02 50 00 0a 0c 01 00 00 01 0f 01 00 00 00 00 00   .P..............
0010   00 00 01 0a 0c 01 00 00 01 0f 01 00 00 00 00 00   ................
0020   00 00 01 0a 0c 01 00 00 01 0f 02 00 00 00 00 00   ................
0030   00 00 01 0a 0c 01 00 00 01 0f 07 00 00 00 00 00   ................
```

There's code elsewhere to process the response and turn it into usable data. That should be relatively easy to figure out.

# Response format 

| Element| Length | Example |
|-|-|-|
| Unknown | 1 byte | 0x02 |
| Command | 1 byte | N |
| ? | # bytes | ? |

# Config response processing

```
		public void DataReceived(byte[] data)
		{
			byte[] send_buf = new byte[64];
			byte b = data[0];
			if (b <= 67)
			{
				if (b == 1)
				{
					int count = this.BinBuff.Length;
					int currindex = 0;
					int sendcount = count / 62 + ((count % 62 > 0) ? 1 : 0);
					this.pb_update.Maximum = sendcount;
					for (int i = 0; i < sendcount; i++)
					{
						send_buf[0] = 1;
						send_buf[1] = 3;
						for (int j = 2; j < 64; j++)
						{
							if (currindex + j - 2 < count)
							{
								send_buf[j] = this.BinBuff[currindex + j - 2];
							}
							else
							{
								send_buf[j] = 0;
							}
						}
						currindex += 62;
						this.CDProcess.SendBytes(send_buf);
						this.pb_update.Value = i + 1;
					}
					return;
				}
				if (b == 2)
				{
					send_buf[0] = 1;
					send_buf[1] = 4;
					this.CDProcess.SendBytes(send_buf);
					MessageBox.Show(ResourceCluture.GetString("update_success"), ConfigHelper.GetAppConfig("APPLICATION_NAME"), MessageBoxButtons.OK, MessageBoxIcon.None);
					return;
				}
				if (b != 67)
				{
					return;
				}
				MessageBox.Show(ResourceCluture.GetString("clear_msg_text"), ConfigHelper.GetAppConfig("APPLICATION_NAME"), MessageBoxButtons.OK, MessageBoxIcon.None);
				return;
			}
			else if (b <= 78)
			{
				if (b == 71)
				{
					this.setBasicInfo(data);
					return;
				}
				if (b != 78)
				{
					return;
				}
				StringBuilder snSB = new StringBuilder();
				for (int k = 1; k < 17; k++)
				{
					snSB.Append(data[k].ToString("x2"));
				}
				this.deviceSN = snSB.ToString();
				return;
			}
			else
			{
				if (b == 82)
				{
					MessageBox.Show(ResourceCluture.GetString("reset_msg_text"), ConfigHelper.GetAppConfig("APPLICATION_NAME"), MessageBoxButtons.OK, MessageBoxIcon.None);
					this.sendBasicInfoCmd();
					return;
				}
				if (b != 83)
				{
					return;
				}
				MessageBox.Show(ResourceCluture.GetString("save_msg_text"), ConfigHelper.GetAppConfig("APPLICATION_NAME"), MessageBoxButtons.OK, MessageBoxIcon.None);
				return;
			}
		}
```
