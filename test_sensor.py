#!/usr/bin/python

import serial
import subprocess

SERIAL_PORT = '/dev/cu.usbserial-AL05VI82'

def check_sensor(nodeId):
  ser = serial.Serial(SERIAL_PORT, baudrate=19200, timeout=10, xonxoff=True, rtscts=False, dsrdtr=False)
  lastPacket = 0
  sensorSeen = False
  try:
    while True:
      data = ser.readline()
      data = data.decode('ascii', 'ignore')
      data = ''.join([s.strip('\0') for s in data])
      data = data.strip()
      if len(data) == 0: continue
      senderid, message, voltage = data[:-1].split(';')
      if senderid == str(nodeId):
        # ignore duplicates
        if data[-1] == lastPacket: continue
        lastPacket = data[-1]
        # print received packet
        log("> " + data)
        # but what does it mean?
        if message[0] == 'V': log("Sensor booted up! Waiting for it to calibrate...", "success")
        elif message == '1': log("Sensor detected entry", "entry")
        elif message == '2': log("Sensor detected exit", "exit")
        elif message == 'd0': log("Door is closed", "closed")
        elif message == 'd1': log("Door is open", "opened")
        elif message == 'd2': log("Door is ajar", "ajar")
        log("") # extra line break between packets
  finally:
    ser.close()
  if not sensorSeen:
    log("FAIL: received 0 packets from sensor", "fail")

def update_ota():
  try:
    log("Flashing firmware...")
    subprocess.check_call('./OTA.py -s ' + SERIAL_PORT + ' -b 19200 -f 13.hex -t 13', shell=True)
    log("Sensor updated! Waiting for it to boot up...")
  except:
    log("FAIL: could not wirelessly update sensor", "fail")

def log(txt, cmd=None):
  print("\n" + txt)
  # if cmd is not None:
  #   # speak phrase out load to notify tester. Only works on macOS
  #   subprocess.call("say " + cmd, shell=True)

update_ota()
check_sensor(13)
