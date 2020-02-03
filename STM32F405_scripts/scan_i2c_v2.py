import board
import busio

i2c = busio.I2C(board.SCL, board.SDA)

print('Attempting to lock i2c')
while not i2c.try_lock():
    print('Waiting for i2c to be avaliable')

i2c_scan = i2c.scan()
try:
    print('There are {} items'.format(len(i2c_scan)))
    [print(hex(x)) for x in i2c_scan]
finally:
    i2c.unlock()
