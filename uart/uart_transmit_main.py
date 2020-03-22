# CircuitPython Demo - USB/Serial echo
import time
import board
import busio
import digitalio

led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

uart = busio.UART(board.TX, board.RX, baudrate=9600)

while True:
    #data = uart.read(32)  # read up to 32 bytes
    nbytes = uart.write(bytes([0x11, 0x12, 0xFF]))
    print('Wrote {} bytes'.format(nbytes))
    time.sleep(1)

