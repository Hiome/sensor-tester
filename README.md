# Hiome Door Test Firmware

## Installation

Make sure you are using Python 2.7. Install the dependencies:

    pip install -r requirements.txt

Connect known working Hiome Gateway board with FTDI adapter to computer.

Update `test_sensor.py` to use the serial port of your FTDI adapter.

    SERIAL_PORT = '/dev/cu.usbserial-AL05VI82'

## Testing Steps

1. Plug in the sensor to be tested and power it on.
2. Run `./test_sensor.py`

This script will flash the correct firmware for testing and reboot the sensor. After the update is done, the sensor will boot up and take about 30 seconds to calibrate. If the script doesn't output anything after 30 seconds, something likely went wrong.

### After it boots up:

Test thermal sensor is working by walking under the sensor. The script will output either entry or exit.

Test reed switches by placing magnet near them. The switch near the power pins should report door is closed, while other switch will say door is ajar.

## Troubleshooting

If the last message you received from the script is...

### could not open port

Either FTDI adapter is not connected or wrong serial port is defined in test_sensor.py

### Moteino: [FLX?NOK]

The sensor is not responding. This is either because it's not powered on or due to an issue with the ATMEGA chip, RFM69, or flash memory.

### Sensor updated! Waiting for it to boot up...

The sensor received the update correctly, but it could not boot up. This means the RFM69 radio and ATMEGA chips are working. Most likely failure points here are either AMG8833 or flash memory.

### Sensor booted up! Waiting for it to calibrate...

The sensor successfully rebooted, most components are good to go. If sensor doesn't print anything after 30 seconds, then the AMG88 sensor is most likely the point of failure.

### Door is open

The sensor calibrated!

If you can't get it to print entry/exit after walking under it, the AMG88 chip is the likely culprit. If you can't get it print door closed and door ajar, one or both reed switches is the issue.

## Success

Once you've seen at least one "Sensor detected entry" or "Sensory detected exit" event and all 3 of "Door is closed/ajar/open", the board is confirmed good!

You can manually kill the script now (`ctrl-c`) and restart it for the next board.
