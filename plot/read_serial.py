import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import random
import serial

#initialize serial port
ser = serial.Serial()
ser.port = '/dev/ttyACM1' #Arduino serial port
#ser.baudrate = 9600
ser.baudrate = 115200
ser.timeout = 10 #specify timeout when using readline()
ser.open()
if ser.is_open==True:
    print("\nAll right, serial port now open. Configuration:\n")
    print(ser, "\n") #print serial parameters

while True:
    line = ser.readline()      #ascii
    line = line.split(b',')
    voltage = float(line[0].decode('ascii'))
    current = float(line[1].decode('ascii'))
    print('Voltage = {} V'.format(voltage))
    print('Current = {} A'.format(current))
