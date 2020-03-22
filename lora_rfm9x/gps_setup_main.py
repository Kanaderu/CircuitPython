# CircuitPython Demo - USB/Serial echo
import time
import board
import busio
import digitalio
import struct

import adafruit_gps

led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

uart = busio.UART(board.TX, board.RX, baudrate=9600)
gps = adafruit_gps.GPS(uart, debug=False)     # Use UART/pyserial
data_format = 'fffHBBBBB'

#i2c = busio.I2C(board.SCL, board.SDA)
#gps = adafruit_gps.GPS_GtopI2C(i2c, debug=False)  # Use I2C interface

# Turn on the basic GGA and RMC info (what you typically want)
gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')

# Set update rate to once a second (1hz) which is what you typically want.
gps.send_command(b'PMTK220,1000')

last_print = time.monotonic()
cnt = 0
while True:
    gps.update()
    # Every second print out current location details if there's a fix.
    current = time.monotonic()
    if current - last_print >= 1.0:
        last_print = current
        if not gps.has_fix:
            # Try again if we don't have a fix yet.
            print('{} Waiting for fix...'.format(cnt))
            cnt+=1
            continue
        # We have a fix! (gps.has_fix is true)
        # Print out details about the fix like location, date, etc.
        data = dict()
        data['latitude'] = gps.latitude
        data['longitude'] = gps.longitude
        data['altitude'] = gps.altitude_m
        ts = gps.timestamp_utc
        print(data)
        ##ts = gps.timestamp_utc
        ##ts_str = '{:04}-{:02}-{:02}T{:02}:{:02}:{:02}+{:04}'.format(
        ##        ts.tm_year, ts.tm_mon, ts.tm_mday, ts.tm_hour, ts.tm_min, ts.tm_sec, 0)
        #ts_str = '2020-03-22T16:47:07+00:00'
        #data['time'] = ts_str
        #print(data)

        #byte_payload = bytearray(struct.pack(data_format,
        #                                     data['latitude'],
        #                                     data['longitude'],
        #                                     data['altitude'],
        #                                     ts.tm_year,
        #                                     ts.tm_mon,
        #                                     ts.tm_mday,
        #                                     ts.tm_hour,
        #                                     ts.tm_min,
        #                                     ts.tm_sec))
        #print(byte_payload)

        #nbytes = uart.write(byte_payload)
        #print('Wrote {} bytes'.format(nbytes))
