#!/usr/bin/env python

from threading import Thread
import serial
import time
import collections
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import struct
import pandas as pd


class serialPlot:
    def __init__(self, serialPort = '/dev/ttyUSB0', serialBaud = 38400, plotLength = 100, dataNumBytes = 2):
        self.port = serialPort
        self.baud = serialBaud
        self.plotMaxLength = plotLength
        self.dataNumBytes = dataNumBytes
        self.rawData = bytearray(dataNumBytes)
        self.data = [collections.deque([0] * plotLength, maxlen=plotLength) for _ in range(3)]
        self.isRun = True
        self.isReceiving = False
        self.thread = None
        self.plotTimer = 0
        self.previousTimer = 0
        # self.csvData = []

        print('Trying to connect to: ' + str(serialPort) + ' at ' + str(serialBaud) + ' BAUD.')
        try:
            self.serialConnection = serial.Serial(serialPort, serialBaud, timeout=4)
            print('Connected to ' + str(serialPort) + ' at ' + str(serialBaud) + ' BAUD.')
        except:
            print("Failed to connect with " + str(serialPort) + ' at ' + str(serialBaud) + ' BAUD.')

    def readSerialStart(self):
        if self.thread == None:
            self.thread = Thread(target=self.backgroundThread)
            self.thread.start()
            # Block till we start receiving values
            while self.isReceiving != True:
                time.sleep(0.1)

    def getSerialData(self, frame, lines, lineValueText, lineLabel, timeText, idx):
        currentTimer = time.perf_counter()
        self.plotTimer = int((currentTimer - self.previousTimer) * 1000)     # the first reading will be erroneous
        self.previousTimer = currentTimer
        timeText.set_text('Plot Interval = ' + str(self.plotTimer) + 'ms')
        #value,  = struct.unpack('f', self.rawData)    # use 'h' for a 2 byte integer
        values = [float(val.decode('ascii')) for val in self.rawData.split(b',')]
        #value = values[0]
        self.data[0].append(values[0])    # we get the latest data point and append it to our array
        self.data[1].append(values[1])    # we get the latest data point and append it to our array
        self.data[2].append(values[2]/1000)    # we get the latest data point and append it to our array
        lines[0].set_data(range(self.plotMaxLength), self.data[0])
        lines[1].set_data(range(self.plotMaxLength), self.data[1])
        lines[2].set_data(range(self.plotMaxLength), self.data[2])
        lineValueText[0].set_text('{} = {:.3f}'.format(lineLabel[0], values[0]))
        lineValueText[1].set_text('{} = {:.3f}'.format(lineLabel[1], values[1]))
        lineValueText[2].set_text('{} = {:.3f}'.format(lineLabel[2], values[2]/1000))
        # self.csvData.append(self.data[-1])

    def backgroundThread(self):    # retrieve data
        time.sleep(1.0)  # give some buffer time for retrieving data
        self.serialConnection.reset_input_buffer()
        while (self.isRun):
            self.rawData = self.serialConnection.readline()
            #line = self.serialConnection.readline()
            #line = line.split(b',')
            #self.rawData = [float(val.decode('ascii')) for val in line]
            #print(self.rawData)
            #self.rawData = line
            #self.serialConnection.readinto(self.rawData)
            self.isReceiving = True
            #print(self.rawData)

    def close(self):
        self.isRun = False
        self.thread.join()
        self.serialConnection.close()
        print('Disconnected...')
        # df = pd.DataFrame(self.csvData)
        # df.to_csv('/home/rikisenia/Desktop/data.csv')


def main():
    # portName = 'COM5'     # for windows users
    portName = '/dev/ttyACM0'
    baudRate = 115200
    maxPlotLength = 100
    dataNumBytes = 4        # number of bytes of 1 data point
    s = serialPlot(portName, baudRate, maxPlotLength, dataNumBytes)   # initializes all required variables
    s.readSerialStart()                                               # starts background thread

    # plotting starts below
    pltInterval = 50    # Period at which the plot animation updates [ms]
    xmin = 0
    xmax = maxPlotLength
    ymin = -(1)
    ymax = 5
    fig = plt.figure()
    ax = plt.axes(xlim=(xmin, xmax), ylim=(float(ymin - (ymax - ymin) / 10), float(ymax + (ymax - ymin) / 10)))
    ax.set_title('Arduino Analog Read')
    ax.set_xlabel("time")
    ax.set_ylabel("AnalogRead Value")

    lineLabel = 'Power (W)'
    timeText = ax.text(0.50, 0.95, '', transform=ax.transAxes)
    lines_W = ax.plot([], [], label=lineLabel)[0]
    lines_V = ax.plot([], [], label='Voltage (V)')[0]
    lines_C = ax.plot([], [], label='Current (A)')[0]
    lineValueText_W = ax.text(0.50, 0.90, '', transform=ax.transAxes)
    lineValueText_V = ax.text(0.50, 0.85, '', transform=ax.transAxes)
    lineValueText_C = ax.text(0.50, 0.80, '', transform=ax.transAxes)
    anim = animation.FuncAnimation(fig, s.getSerialData, fargs=([lines_W, lines_V, lines_C], [lineValueText_W, lineValueText_V, lineValueText_C], [lineLabel, 'Voltage (V)', 'Current (A)'], timeText, 0), interval=pltInterval)    # fargs has to be a tuple

    plt.legend(loc="upper left")
    plt.show()

    s.close()


if __name__ == '__main__':
    main()
