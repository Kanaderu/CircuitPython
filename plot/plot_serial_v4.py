#!/usr/bin/env python
from threading import Thread
import serial
import time
import collections
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import struct
import pandas as pd


class SerialPlot:
    def __init__(self, signals, serial_port = '/dev/ttyUSB0', serial_baud = 38400, plot_length = 100, scale_data=None):
        self.port = serial_port
        self.baud = serial_baud
        self.plotMaxLength = plot_length
        self.x_axis_time = collections.deque([0] * plot_length, maxlen=plot_length)

        self.rawData = None
        self.signals = signals
        self.data = [collections.deque([0] * plot_length, maxlen=plot_length) for _ in range(len(signals))]
        self.scale_data = [1 for _ in range(len(signals))] if scale_data is None else scale_data

        self.isRunning = True
        self.isReceiving = False
        self.thread = None
        self.plotTimer = 0
        self.previousTimer = 0
        self.startTime = time.perf_counter()

        print('Trying to connect to: {} at {} BAUD'.format(serial_port, serial_baud))
        try:
            self.serialConnection = serial.Serial(serial_port, serial_baud, timeout=4)
            print('Connected to {} at {} BAUD'.format(serial_port, serial_baud))
        except Exception:
            print('Failed to connect to {} at {} BAUD'.format(serial_port, serial_baud))

    def read_serial(self):
        if self.thread is None:
            self.thread = Thread(target=self.background_thread)
            self.thread.start()
            # Block till we start receiving values
            while not self.isReceiving:
                time.sleep(0.1)

    def get_serial_data(self, frame, lines, lines_text, time_text, ax):
        currentTimer = time.perf_counter()
        self.plotTimer = int((currentTimer - self.previousTimer) * 1000)     # the first reading will be erroneous
        self.previousTimer = currentTimer
        time_text.set_text('Plot Interval = ' + str(self.plotTimer) + 'ms')
        self.x_axis_time.append(currentTimer - self.startTime)

        values = [float(val.decode('ascii')) for val in self.rawData.split(b',')]
        for signal, data, scale, value, line, line_text in zip(self.signals, self.data, self.scale_data, values, lines, lines_text):
            scaled_value = value * scale
            data.append(scaled_value)
            #line.set_data(range(self.plotMaxLength), data)
            line.set_data(self.x_axis_time, data)
            ax.set_xlim(min(self.x_axis_time), max(self.x_axis_time))
            line_text.set_text('{} = {:.5f}'.format(signal, scaled_value))

    def background_thread(self):
        time.sleep(1.0)
        self.serialConnection.reset_input_buffer()
        while(self.isRunning):
            self.rawData = self.serialConnection.readline()
            self.isReceiving = True

    def close(self):
        self.isRunning = False
        self.thread.join()
        self.serialConnection.close()
        print('Disconnected...')


def main():
    port_name = '/dev/ttyACM0'
    baud_rate = 115200
    max_plot_length = 100

    line_labels = ['Power (W)', 'Voltage (V)', 'Current (A)']
    scale_data = [1., 1., 1./1000.] # scale current by 1000 to convert from mA to A
    s = SerialPlot(line_labels, port_name, baud_rate, max_plot_length, scale_data)
    s.read_serial() # starts background thread

    # plotting starts below
    pltInterval = 50    # Period at which the plot animation updates [ms]
    xmin = 0
    xmax = max_plot_length
    ymin = 0
    ymax = 5
    fig = plt.figure()
    ax = plt.axes(xlim=(xmin, xmax), ylim=(float(ymin - (ymax - ymin) / 10), float(ymax + (ymax - ymin) / 10)))
    ax.set_title('Serial Read')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude Value')

    y_text_offset = 0.95
    timeText = ax.text(0.50, y_text_offset, '', transform=ax.transAxes)
    lines = [ax.plot([], [], label=label)[0] for label in line_labels]
    text_values = [ax.text(0.50, y_text_offset - (idx+1)*0.05, '', transform=ax.transAxes) for idx in range(len(line_labels))]
    anim = animation.FuncAnimation(fig, s.get_serial_data, fargs=(lines, text_values, timeText, ax), interval=pltInterval)

    plt.legend(loc="upper left")
    plt.grid()
    plt.show()

    s.close()


if __name__ == '__main__':
    main()
