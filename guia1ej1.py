import serial
from serial import Serial
ser_com = serial.Serial('/dev/ttyACM0', 9600)

while True:
	read_serial = ser_com.readline()
	if 48 in read_serial: #si la entrada contiene un 0
		print('CERO')
	elif 49 in read_serial: #si la entrada contiene un 1
		print('UNO')
	else:
		print('DOS')

