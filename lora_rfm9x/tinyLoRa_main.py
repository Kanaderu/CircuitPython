import time
import board
import busio
import digitalio

from adafruit_tinylora.adafruit_tinylora import TTN, TinyLoRa


# Board LED
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT


# Create library object using our bus SPI port for radio
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# RFM9x Breakout Pinouts
# cs = digitalio.DigitalInOut(board.D5)
# irq = digitalio.DigitalInOut(board.D6)
# rst = digitalio.DigitalInOut(board.D4)

# Feather M0 RFM9x Pinouts
cs = digitalio.DigitalInOut(board.RFM9X_CS)
irq = digitalio.DigitalInOut(board.RFM9X_D0)
rst = digitalio.DigitalInOut(board.RFM9X_RST)

# TTN Device Address, 4 Bytes, MSB
devaddr = bytearray([0x26, 0x02, 0x1B, 0x92])

# TTN Network Key, 16 Bytes, MSB
nwkey = bytearray([0x30, 0x08, 0x4B, 0x76, 0xCE, 0xE2, 0x5B, 0x26, 0x6A, 0xF3, 0x3F, 0x41, 0xD6, 0x75, 0x87, 0xD9])

# TTN Application Key, 16 Bytess, MSB
app = bytearray([0x5C, 0x12, 0x39, 0x05, 0x47, 0x67, 0x50, 0x2E, 0x79, 0x69, 0x46, 0xF6, 0xFA, 0xDA, 0x79, 0x36])

ttn_config = TTN(devaddr, nwkey, app, country="US")

lora = TinyLoRa(spi, cs, irq, rst, ttn_config)

# Data Packet to send to TTN
data = bytearray(4)

while True:
    temp_val = 0#sensor.temperature
    humid_val = 0#sensor.relative_humidity
    print("Temperature: %0.2f C" % temp_val)
    print("relative humidity: %0.1f %%" % humid_val)

    # Encode float as int
    temp_val = int(temp_val * 100)
    humid_val = int(humid_val * 100)

    # Encode payload as bytes
    data[0] = (temp_val >> 8) & 0xFF
    data[1] = temp_val & 0xFF
    data[2] = (humid_val >> 8) & 0xFF
    data[3] = humid_val & 0xFF

    # Send data packet
    print("Sending packet...")
    lora.send_data(data, len(data), lora.frame_counter)
    print("Packet Sent!")
    led.value = True
    lora.frame_counter += 1
    time.sleep(2)
    led.value = False
