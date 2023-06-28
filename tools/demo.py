import serial
from bitarray import bitarray
import time 

serial_port = serial.Serial('/dev/ttyACM0',9600)

time.sleep(5)

# setup 16hz 
serial_port.write(bitarray('10000000'))
serial_port.write(bitarray('00000110'))
serial_port.write(bitarray('00011001'))
time.sleep(5)


# Turn 4 times to direction = false
serial_port.write(bitarray('00000000'))
serial_port.write(bitarray('00000011'))
serial_port.write(bitarray('00000000'))

time.sleep(10)

# Halt and turn one time direction=true
serial_port.write(bitarray('11000000'))
serial_port.write(bitarray('00000000'))
serial_port.write(bitarray('00000000'))

serial_port.write(bitarray('00000001'))
serial_port.write(bitarray('00000000'))
serial_port.write(bitarray('01100000'))