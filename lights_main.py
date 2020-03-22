import board
import digitalio
import time
 
led = digitalio.DigitalInOut(board.A1)
led.direction = digitalio.Direction.OUTPUT
 
led2 = digitalio.DigitalInOut(board.A2)
led2.direction = digitalio.Direction.OUTPUT

led3 = digitalio.DigitalInOut(board.A3)
led3.direction = digitalio.Direction.OUTPUT
while True:
    led.value = True
    led2.value = True
    led3.value = True
    print('ON')
    time.sleep(1)
    led.value = False
    led2.value = False
    led3.value = False
    print('OFF')
    time.sleep(1)
