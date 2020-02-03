import board
import digitalio
import time
 
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT
 
while True:
    led.value = True
    print('ON')
    time.sleep(1)
    led.value = False
    print('OFF')
    time.sleep(1)
