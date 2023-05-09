
from w1thermsensor import W1ThermSensor #Se importa la libreria para utilizar el sensor de temperatura
import time #Se importa la libreria que permite el uso del timestamp

class sensorTemperatura: #Se define la clase sensorTemperatura
	def __init__(self, temperature, mi_lista): #se definen los constructores, con los argumentos temperature, que permite 
						   #obtener valores del sensor, y mi_lista, para crear una lista vacia 
		self.temperature = temperature #Se asigna temperature a self.temperature
		self.mi_lista = mi_lista #Se asigna mi_lista a self.mi_lista

	def readTemperature(self,duration): #Se define el metodo readTemperature, que permite obtener la temperatura desde el sensor
		start_time=time.time() #Se define el tiempo de inicio desde  el que se tomaran datos
		end_time=start_time+duration #Se define el tiempo final en el que se tomaran datos

		while time.time() < end_time: #Se genera un siclo while con la condicion de que el tiempo de inicio sea menor al tiempo final
			temperature=self.temperature.get_temperature() #Se obtiene la temperatura
			self.mi_lista.append(temperature) #Se guarda este valor en la lista vacia 
			timestamp=time.time() #Se obtiene el timestamp
			print("Temperatura: ",temperature,"[°C]") #Se muestra por pantalla la temperatura
			print("Timestamp: ",timestamp,"[s]" ) #Se muestra por pantalla el timestamp
			print("Lista :", self.mi_lista) #Se muestra por pantalla como se llena la lista 
			time.sleep(30) #Se esperan 30 segundos para volver a realizar el procedimiento

	def promedioTemperatura(self,filename): #Se define el metodo promedioTemperatura, para calcular el promedio con los valores
						#de temperaturas guardadas en la lista
			promedio=sum(self.mi_lista)/len(self.mi_lista) #Se calcula el promedio
			with open(filename, "w") as f: #Se crea un archivo llamado f
				f.write("Temperatura promedio: {:.2f}".format(promedio)) #Se escribe en el archivo la temperatura promedio

listaTemp = [] #Se crea la variable listaTemp, la cual sera una lista vacia 
sensor=W1ThermSensor() #Se crea la variable sensor para almacenar la conexion con el sensor de temperatura
while True: #Se genera un ciclo while con la condicion True, para tener un loop infinito
	temp=sensorTemperatura(sensor,listaTemp) #Se crea el objeto temp
	temp.readTemperature(300) #Se llama al metodo readTemperature, especificando que se debe realizar por 5 min (300 segundos)
	temp.promedioTemperatura("temperatura_promedio.txt") #se llama al metodo promedioTemperatura, dandole el nombre que se le quiere
							      #dar al archivo, esto ocurrirá despues de los 5 minutos.
