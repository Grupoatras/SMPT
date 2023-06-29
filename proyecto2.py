import psycopg2
import serial
import adafruit_fingerprint
import time
import numpy as np
import os
import sys
import face_recognition
import cv2

conn = psycopg2.connect(
	host = "192.168.1.11", 
	database = "Proyecto",
	user = "postgres",
	password = "Admin.123")
cursor = conn.cursor()


ser = serial.Serial("/dev/ttyS0", baudrate = 57600, timeout = 1)
lector = adafruit_fingerprint.Adafruit_Fingerprint(ser)

def enviar_info(i, nombre, apellido, codigo_carrera, grado_seguridad, ubicacion_foto1, ubicacion_foto2):
	cursor.execute("""INSERT INTO public."Usuario" VALUES ({},'{}','{}',{},{})""".format(i, nombre, apellido, codigo_carrera, grado_seguridad))
	cursor.execute("""INSERT INTO public."Fotos" VALUES({},'{}','{}')""".format(i, ubicacion_foto1, ubicacion_foto2))
	conn.commit()

def ingreso(id_u, id_s, estado_ingreso):
	cursor.execute("""INSERT INTO public."Ingreso" VALUES ({},{},'{}')""".format(id_u, id_s, estado_ingreso))
	conn.commit()

def extraccion_huella(location):
	for img_huella in range(1,3):
		while True:
			f = lector.get_image()
			if f == adafruit_fingerprint.OK:
				print("\nHuella Escaneada")
				break
			if f == adafruit_fingerprint.NOFINGER:
				print(".", end = "")
			elif f == adafruit_fingerprint.IMAGEFAIL:
				print("Error en la imagen")
				return False

		print("Escaneando...", end = "")
		f = lector.image_2_tz(img_huella)
		if f == adafruit_fingerprint.OK:
			print("Escaneado")
		else:
			if f == adafruit_fingerprint.IMAGEMESS:
				print("Imagen borrosa")
			elif f == adafruit_fingerprint.FEATUREFAIL:
				print("Caracteristicas no distinguidas")
			elif f == adafruit_fingerprint.INVALIDIMAGE:
				print("Imagen Invalida")
			return False

		if img_huella == 1:
			print("\nQuite el dedo y repita el proceso.")
			while f != adafruit_fingerprint.NOFINGER:
				f = lector.get_image()


	print("Creando modelo...", end = "")
	f = lector.create_model()
	if f == adafruit_fingerprint.OK:
		print("Modelo Listo")
	else:
		if f == adafruit_fingerprint.ENROLLMISMATCH:
			print("Las huellas no concidieron")
		else:
			print("Error")
		return False

	print("Guardando modelo %d..." % location, end = "")
	f = lector.store_model(location)
	if f == adafruit_fingerprint.OK:
		print("Modelo Guardado")
	else:
		if i == adafruit_fingerprint.BADLOCATION:
			print("Error en lugar de almacenamiento")
		elif i == adafruit_fingerprint.FLASHERR:
			print("Error en memoria flash")
		else:
			print("Error")
		return False

	print("Quite el dedo")
	return True

def asignar_ID():
	i = 0
	while (i > 100) or (i < 1):
		try:
			i = int(input("Ingrese una ID entre 1 - 100: "))
		except ValueError:
			pass
	return i


def buscar_info():
	print("\nNombre del Usuario:")
	nombre = input("> ")
	print("\nApellido del Usuario:")
	apellido = input("> ")
	print("\nIngrese ID de la carrera:")
	print("(1) Ingenieria Civil Electronica")
	print("(2) Ingeniería Civil Eléctrica")
	print("(3) Ingeniería Electrónica")
	print("(4) Ingeniería Eléctrica")
	print("(5) Ingeniería Civil Mecánica")
	codigo_carrera = input("> ")
	print("\nAsigne el grado de seguridad entre 1 - 5:")
	grado_seguridad = input("> ")

	return nombre, apellido, codigo_carrera, grado_seguridad

def buscar_huella():
	print("\nColoque su dedo")
	while lector.get_image() != adafruit_fingerprint.OK:
		pass
	print("Quite el dedo")
	time.sleep(2)
	print("Procesando...")
	if lector.image_2_tz(1) != adafruit_fingerprint.OK:
		return False
	print("Buscando...")
	if lector.finger_search() != adafruit_fingerprint.OK:
		return False
	return True

def buscar_sala():
	print("\nIngrese ID de la sala:")
	print("(1) Laboratorio de Mediciones Eléctricas (Grado de seguridad: 3)")
	print("(2) Laboratorio de Sistemas de Control (Grado de seguridad: 5)")
	print("(3) Laboratorio de Redes de Computadores (Grado de seguridad: 4)")
	print("(4) Biblioteca (Grado de seguridad: 1)")
	print("(5) LabSens (Grado de seguridad: 4)")
	ID_sala = input("> ")
	ID_sala = int(ID_sala)
	query = """SELECT "Grado_seguridad" FROM public."Salas" WHERE "ID_Sala" = {}"""
	cursor.execute(query.format(ID_sala))
	for fila in cursor:
		grado_seguridad = fila[0]

	return grado_seguridad, ID_sala

def sacar_foto(p):
	print("Presionar Enter para tomar la primera fotografía\n")
	input(">")
	print("Capturando")
	ubicacion_foto1 = ubicacion + "/" + "imagenes" + "/" + p + "/foto1.jpg"
	os.system("fswebcam -i 0 -d /dev/video0 -r 640x480 -q --title @raspberry {}".format(ubicacion_foto1))
	time.sleep(2)
	print("Presionar Enter para tomar la segunda fotografía\n")
	input(">")
	ubicacion_foto2 = ubicacion + "/" + "imagenes" + "/" + p + "/foto2.jpg"
	os.system("fswebcam -i 0 -d /dev/video0 -r 640x480 -q --title @raspberry {}".format(ubicacion_foto2))
	print("Fotografías tomadas con éxito")
	
	return ubicacion_foto1, ubicacion_foto2 

def recon_facial(r):
	cursor.execute("""SELECT "Ubicacion_foto1", "Ubicacion_foto2" FROM public."Fotos" WHERE "Codigo_usuario_id" = {}""".format(r))
	for fila in cursor:
		foto1 = fila[0]
		foto2 = fila[1]
	foto = ubicacion + "/imagenes/" + r + "/comparacion.jpg"
	print("\nPresionar Enter para iniciar el reconocimiento facial\n")
	input(">")
	print("Capturando")
	os.system("fswebcam -i 0 -d /dev/video0 -r 640x480 -q --title @raspberry {}".format(foto))
	print("\nFotografía tomada. Buscando coincidencias...")

	comparacion_imagenes = cv2.imread(foto)
	cara = face_recognition.face_locations(comparacion_imagenes)[0]
	codificacion = face_recognition.face_encodings(comparacion_imagenes, known_face_locations = [cara])[0]
	
	foto1 = cv2.imread(foto1)
	foto2 = cv2.imread(foto2)
	
	ubicacion1 = face_recognition.face_locations(foto1)[0]
	codificacion1 = face_recognition.face_encodings(foto1, known_face_locations = [ubicacion1])[0]

	resultado = face_recognition.compare_faces([codificacion], codificacion1)
	
	if resultado[0] == True:
		print("Coincidencia encontrada")
		coincidencia = 1
	else:
		ubicacion2 = face_recognition.face_locations(foto2)[0]
		codificacion2 = face_recognition.face_encodings(foto2, known_face_locations = [ubicacion2])[0]

		resultado = face_recognition.compare_faces([codificacion], codificacion2)
		if resultado[0] == True:
			print("Coincidencia encontrada")
			coincidencia = 1
		else:
			coincidencia = 0

	return coincidencia, foto


ubicacion = os.getcwd()
ingresar_usuario = 0
encontrar_usuario = 0

while True:
	a = 0
	print("\nEscoja una opcion")
	print("a) Guardar Usuario")
	print("b) Buscar Usuario")
	
	a = input("> ")

	if lector.read_templates() != adafruit_fingerprint.OK:
		raise RuntimeError("Error al leer Plantillas")

	if a == "a":
		IDs = []
		lista = 0
		ingresar_usuario = 1
		i = asignar_ID()
		i = str(i)
		query = """SELECT "ID_Usuario" FROM public."Usuario";"""
		cursor.execute(query)
		for fila in cursor:
			IDs.append(fila)

		for n in IDs:
			n = str(n)
			if i in n:
				print("ID Ocupada")
				False

		IDs = []
		if lista == 0:
			i = int(i)
			print("Poner el dedo en el sensor")

			extraccion_huella(i)
			i = str(i)
			nombre, apellido, codigo_carrera, grado_seguridad = buscar_info()
			ubicacion_foto = ubicacion + "/" + "imagenes" + "/" + i
			os.mkdir(ubicacion_foto)
			ubicacion_foto1, ubicacion_foto2 = sacar_foto(i)
			enviar_info(i,nombre,apellido,codigo_carrera,grado_seguridad,ubicacion_foto1,ubicacion_foto2)
		ingresar_usuario = 0 
		
	elif a == "b":
		seguridad_sala, id_sala = buscar_sala()
		encontrar_usuario = 1
		if buscar_huella():
			numero = lector.finger_id
			numero_str = str(numero)
			numero = int(numero)

			print("\nCoincidencia encontrada: ")
			query = """SELECT "Nombre", "Apellido", "Grado_Seguridad" FROM public."Usuario" WHERE "ID_Usuario" = {}"""
			cursor.execute(query.format(numero))
			for fila in cursor:
				nombre = fila[0]
				apellido = fila[1]
				grado_seguridad = fila[2]

			if grado_seguridad >= seguridad_sala:
				print("Nombre: ", nombre)
				print("Apellido: ", apellido)
				print("Grado de seguridad: ", grado_seguridad)

				coincidencia, foto = recon_facial(numero_str)
				if coincidencia == 1:
					print("Acceso permitido")
					print("---------------------------------------------")
					ingreso(numero, id_sala, "Permitido")
				else:
					print("Acceso denegado, rostro no coincide")
					print("---------------------------------------------")
					ingreso(numero, id_sala, "Denegado")
			else:
				print("Nombre: ", nombre)
				print("Apellido: ", apellido)
				print("Grado de seguridad: ", grado_seguridad)
				print("Acceso denegado, grado de seguridad insuficiente.")
				print("---------------------------------------------")
				ingreso(numero, id_sala, "Denegado")

		else:
			print("Huella no encontrada")
			print("---------------------------------------------")
		encontrar_usuario = 0


