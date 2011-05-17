#!/usr/bin/env python
"""
Reads data from serial port using pySerial, and writes them to a simple text file.
The received data is assumed to consist of lines, each line made up of two whitespace-separated integers.

This code has only been tested on mac os x, and may not work on other OSes.

Some useful comments on serial data reading:
http://stackoverflow.com/questions/1093598/pyserial-how-to-read-last-line-sent-from-serial-device
"""
#from threading import Thread
import time
import serial
import os,sys,glob

# The Arduino device name is not persistent, and depends on the OS.
# You may have to enter the device name manually
# If you are on linux, this may be useful:
#  <http://hintshop.ludvig.co.nz/show/persistent-names-usb-serial-devices/>
dev = glob.glob('/dev/tty.usbmodem*')
if len(dev) == 1:
    dev = dev[0]
    print "Using ",dev
    arduino_port = dev
elif len(dev) == 0:
    print "Did not find a device /dev/tty.usbmodem*"
    sys.exit(1)
else:
    print "Found several devices /dev/tty.usbmodem*"
    sys.exit(1)

ser = serial.Serial(port = arduino_port, baudrate=9600, timeout=0.1)
if not ser: 
    print "Could not connect"
    sys.exit()

# Write to log every <delay> seconds
delay = 0.5

start = time.time()
while True:
    line = ser.readline()
    now = time.time()
    if (now - start) > delay:
        line = line.strip()
        line = line.split()
        if len(line) == 2:
            s1, s2 = [float(i) for i in line]

            # The raw value is an integer between 0 and 1024, corresponding to voltages between 0 and 5 V.
            voltage = s1/1024.*5.

            # The resistance over which the second reading is done (in ohm):
            resistance = 180.
            # Knowing the resistance, we can find the current (in mA):
            current = (s2/1024.*5.)/resistance * 1000

            # The power is then
            power = voltage * current

            # Log to file 
            f = open('serial.log','a')
            f.write("%f %.3f %.3f %.3f\n" % (now, voltage, current, power))
            f.close()

            start = now

