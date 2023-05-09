import serial

class Arduino:
	def __init__(self, baudios):
		self.baudios = baudios

	def getDatos(self):

		valor=serial.Serial('/dev/ttyACM0', self.baudios).readline()
		if 48 in valor:
			print(valor)
			print('CERO\n')
		elif 49 in valor:
			print(valor)
			print('UNO\n')
		else:
			print(valor)
			print('DOS\n')

while True:
	data = Arduino(9600)
	data.getDatos()

