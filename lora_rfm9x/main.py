import board
import busio
import digitalio
import adafruit_rfm9x

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

#cs = digitalio.DigitalInOut(board.D5)
#reset = digitalio.DigitalInOut(board.D6)

cs = digitalio.DigitalInOut(board.RFM9X_CS)
reset = digitalio.DigitalInOut(board.RFM9X_RST)

rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 915.0)

while True:
    for ii in range(10):
        print(ii)
        rfm9x.send('Hello world!')
