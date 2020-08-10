'''
	E-Bot Verificador de errores v-0.2
	Este programa corresponde a la verificacion de errores en los comandos
	que se introducen desde la interfaz de usuario, a este solo entra el 
	comando deseado y verifica si es correcto mandandolo a ejecutar desde 
	la interfaz RP4_ESP32 al controlador esp-32, dentro de este solo se 
	llama a la funcion seleccion_comando y esta se encarga de todo, siempre
	regrasa cuatro elementos, un estrig con el estado de la operacion, una
	lista que puede estar o no vacia, una descripcion del error que se dio
	y finalmente el comando que se evaluo, que puede ser o no el introducido
	dependiendo de si se pudo corregir o no
'''

import RP4_ESP32 as rpc
import time

class Maquina:
	
	# al inio se estancia un objeto de la clase comunicacion serial, se
	# se establece el estado de la conexion, y se incluyen variables globales
	def __init__(self):
		self.ESP = rpc.Comunicacion_serial()
		
		if self.ESP.estatus == "establecido":
			self.estatus = "establecido"
		
		self.error_exp =["nulo", "no se encontro el modulo deseado {}", 
						 "el comando no pertenece a una clase X",
						 "el comando no tiene longitud estandar"]
		
		# Modulos usables hasta el momento				 
		self.dic_modulog = ["TR", "BA", "UT", "QT", "EN"]
		# posibles acciones que se pueden llevar a cabo
		self.dic_claseg  = ["A", "D", "U", "S"]
	
	
	def marcar_error(self, numero, tipo="ZZ"):
		error_exp =["nulo", "no se encontro el modulo deseado {}".format(tipo), 
						 "el comando no pertenece a una clase X",
						 "el comando no tiene longitud estandar"]
						 
		return error_exp[numero]
	
	# verifica los comandos tipo u (envio de datos, upload), si puede corrige
	# los errores de estos
	def verificacion_9s_u(self, tipo_u, comando_u, num1_u, num2_u):
		dic_ver_u = {"TR":100 , "BA":180}

		try:
			dato = dic_ver_u[tipo_u]
		except:
			dato = 10
		
		if dato != 10:
			if (num1_u <= dato) and (num1_u >= 0):
				dato_1 = comando_u[3:6]
			else:
				dato_1 = "000"
			
			if (num2_u <= dato) and (num2_u >= 0):
				dato_2 = comando_u[6:9]
			else:
				dato_2 = "000"
				
			comando_bien = comando_u[0:3] + dato_1 + dato_2
			
			estado = self.ESP.accion(comando_bien)
			#print(comando_bien)
			return estado, [], self.error_exp[0], comando_bien

		else:
			#print("error")
			estado_error = self.marcar_error(numero=1, tipo=tipo_u)
			return "error", [], estado_error, comando_u
	
	# verifica los comandos tipo d (solicitud de datos, download), si puede
	# corrige los posibles errores		
	def verificacion_9s_d(self, tipo_d, comando_d, num1_d, num2_d):
		dic_ver_d = {'UT': 3, "QT": 8, "EN": 4}
		dic_com_d = {'UT': "UTD003001", "QT": "QTD008001", "EN": "END004001"}
		
		try:
			dato = dic_ver_d[tipo_d]
		except:
			dato = 0
			
		if dato != 0:
			if (num1_d == dato) and (num2_d == 1):
				comando_bien_d = comando_d
			
			else:
				comando_bien_d = dic_com_d[tipo_d]
				
			datos_r, estado_d = self.ESP.solicitar_datos(comando_bien_d)
		
			#print(datos_r, estado_d)
		
			return estado_d, datos_r, self.error_exp[0], comando_bien_d
			
		else:
			estado_error = self.marcar_error(numero=1, tipo=tipo_d)
			return "error", datos_r, estado_error, comando
	
	# verifica los comandos tipo a		
	def verificacion_9s_a(self, tipo_a, comando_a, num1_a, num2_a):
		if tipo_a in self.dic_modulog:
			estado = self.ESP.accion(comando_a)
			return estado, [], self.error_exp[0], comando_a
		else:
			estado_error = self.marcar_error(numero=1, tipo=tipo_a)
			return "error", [], estado_error, comando_a
	
	# metodo principal, selecciona el tipo de verificacion y regresa a la 
	# funcion que lo llama las 4 variables mencionadas en el encabezado
	def seleccion_comando(self, comando):
		verificacion = len(comando)    # verifica si el comando tiene la longitud estandar
		
		if verificacion == 9:       # se verifican comandos de longitud estandar 9
			try:
				clase_c = comando[2].upper()   # verifica la clase del comando hasta el momento: A,D,U
				tipo = comando[0:2].upper()            # Verifica el modulo para accionar: TR, BA, UT, QT y EN
				num1 = int(comando[3:6])
				num2 = int(comando[6:9])
			except:                     # si no se puede se asigna unos por defecto
				num1 = 999
				num2 = 999
			#print(comando, tipo, num1, num2, clase_c)
			
			if (clase_c == "A"):
				estado_e, dato_e, des_error, com_env = self.verificacion_9s_a(tipo_a=tipo, comando_a=comando, num1_a= num1, num2_a=num2)
				return estado_e, dato_e, des_error, com_env
				
			elif clase_c == "U":
				#print(self.verificacion_9s_u(tipo_u = tipo, comando_u = comando, num1_u = num1, num2_u = num2))
				estado_e, dato_e, des_error, com_env = self.verificacion_9s_u(tipo_u=tipo, comando_u=comando, num1_u = num1, num2_u=num2)
				return estado_e, dato_e, des_error, com_env
					
			elif (clase_c == "D"):
				#print(self.verificacion_9s_d(tipo_d = tipo, comando_d = comando, num1_d = num1, num2_d = num2))
				estado_e, dato_e, des_error, com_env = self.verificacion_9s_d(tipo_d=tipo, comando_d=comando, num1_d = num1, num2_d=num2)
				return estado_e, dato_e, des_error, com_env
			
			else:
				return "error", [], self.error_exp[2], comando
		
		else:                       # se verifican comandos que no tienen logitud estandar
			# sin implementar, en algun momento se hara
			return "error", [], self.error_exp[3], comando

	def correccion_errores(self, comando):
		# por implementar, tratara de corregir errores con respecto a los comandos
		pass	
			
# Techbench
'''
espd = Maquina()
estado_e, dato_e, des_error, com_env = espd.seleccion_comando("TXU180100")
print(estado_e, dato_e, des_error, com_env)
time.sleep(1)
estado_e, dato_e, des_error, com_env = espd.seleccion_comando("TRA100100")
print(estado_e, dato_e, des_error, com_env)
time.sleep(1)
estado_e, dato_e, des_error, com_env  = espd.seleccion_comando("BAU190100")
print(estado_e, dato_e, des_error, com_env)
time.sleep(1)
estado_e, dato_e, des_error, com_env  = espd.seleccion_comando("BaU190100")	
print(estado_e, dato_e, des_error, com_env)
time.sleep(1)
estado_e, dato_e, des_error, com_env  = espd.seleccion_comando("QTD008001")
print(estado_e, dato_e, des_error, com_env)
time.sleep(1)
estado_e, dato_e, des_error, com_env  = espd.seleccion_comando("QTD009001")
print(estado_e, dato_e, des_error, com_env)
time.sleep(1)
estado_e, dato_e, des_error, com_env  = espd.seleccion_comando("QTS009001")
print(estado_e, dato_e, des_error, com_env)
time.sleep(1)
estado_e, dato_e, des_error, com_env  = espd.seleccion_comando("EVANGELIO")
print(estado_e, dato_e, des_error, com_env)
'''
