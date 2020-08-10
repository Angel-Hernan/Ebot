#!/usr/bin/env python3

'''
    E-bot RP4-ESP32-POTENCIA v0.5
    Este programa corresponde a la interfaz de comunicacion serie con el 
    modulo esp32, por lo cual es un complemento al mismo, se utiliza la UART
    5 de la RP4 para entablar relacion, con motivo de dejar otras disponibles
    Este program es funcional aunque aun requiere de la verificacion de errores
'''
import serial
import time
import gpiozero as gpio

# clase que se encarga establecer y realizar la comunicacion serial con
# el esp32, hace uso de la UART 5 de la RP4
class Comunicacion_serial():
    # inicializacion de la clase, se utiliza protocolo UART, la 5 de la 
    # tarjeta, como habilitarlo lo encuentras en:
    # https://www.youtube.com/watch?v=L6s489mcy8A&t=328s
    def __init__(self):
        try:
            self.ESP32 = serial.Serial(
                port='/dev/ttyAMA1',
                baudrate = 115200,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=5)
            self.estatus = "establecido"
            
        except:
            self.estatus = "sin establecer"
        
        finally:
            self.Pin_Reset = gpio.LED(21)
            self.Pin_Reset.off()

#    metodo para solicitar datos al ESP32, requiere de un comando, hasta el 
#    el momento se han implementado los comandos QTA008001  ENA004001 y 
#    UTA003001, regresa dos elementos, el primero una lista con los datos
#    solicitados y el segundo con el estado de ejecucion, indicando si los 
#    datos vienen en el formato de lista y del tamaño solicitado. para los 
#    comandos: las primeras dos letras hacen referencia al componenete que
#    se solicitara, el tercero indica que es una busqueda, del 4-6 indica
#    el maximo numero de datos a recibir, y del 7-9 inidica el rango de los 
#    datos a recibir
    def solicitar_datos(self, comando):
        longitud_max = int(comando[3:6])
        numero_resta = int(comando[6:9])
        #print(longitud_max, numero_resta)
        self.ESP32.reset_input_buffer()
        self.ESP32.flush()
        self.ESP32.write(comando.encode('utf-8'))
        self.ESP32.write(b'\n')
        time.sleep(0.001)
        estado = "recibir"
        estatus_final = "error"
        counter = 0
        dato_enviado = "no definido"
        datos_adquiridos = []
        data = []
        i = 0
        
        while estado == "recibir":
            x = self.ESP32.readline().decode('utf-8').rstrip()
            if x != b'':
                datos_adquiridos.append(str(x))
                i += 1
                #print(x)
                
                if (i == longitud_max) and (x == 'DataEnd'):
                    estado = "espera"
                
                elif i > longitud_max:
                    estado = "error"
                    break
        
        if estado == "espera":
            #print(datos_adquiridos)
            dato_enviado = datos_adquiridos[0]
            
            for i in range(1,len(datos_adquiridos)-numero_resta):
                try:
                    numero = int(datos_adquiridos[i])
                except:
                    numero = 0
                    estado = "error"
                    
                data.append(numero)
        
        if estado == "espera":
            estatus_final = "correcto"
        
        return data, estatus_final

#   metodo para ralizar alguna accion con el ESP32, recibe un estring con 
#   algun comando y regresa un string indicando si se realizo la accion o no
    def accion(self, comando):
        self.ESP32.reset_input_buffer()
        self.ESP32.flush()
        self.ESP32.write(comando.encode('utf-8'))
        self.ESP32.write(b'\n')
        time.sleep(0.001)
        estado = "recibir"
        estatus_final = "error"
        i = 0
        
        while (estado == "recibir") and (i <= 3):
            x = self.ESP32.readline().decode('utf-8').rstrip()
            if x != b'':
                i +=1
                if x ==comando:
                    estado = "recivido"
        
        estatus_final = "Correcto"
        
        #print(estatus_final)
        return estatus_final
        
    def reset(self, comando):
        self.Pin_Reset.off()
        time.sleep(0.01)
        self.Pin_Reset.on()
        time.sleep(0.01)
        self.Pin_Reset.off()
        
        return "correcto"
        
### Metodos por implementar
    def estado(self):
        #por implentar, solicita el estado de un bloque al esp32
        pass
        
    # recordar implementar esto a futuro
    def reset_encoders(self, comando):
        #por implementar
        pass
        
### funcion para probar agregados a otras funciones, no va a llegar a la 
#   version final
    def pruebas(self, comando):
        self.ESP32.reset_input_buffer()
        self.ESP32.flush()
        self.ESP32.write(comando.encode('utf-8'))
        self.ESP32.write(b'\n')
        time.sleep(0.001)
        estado = "recibir"
        data = []
        i = 0
        
        while estado == "recibir":
            x = self.ESP32.readline().decode('utf-8').rstrip()
            if x != b'':
                data.append(x)
                #print(x)
                i+=1
            if (i == 3) and (x == 'DataEnd'):
                estado = "recivido"
                medida = int(data[i-2])
        
        return medida, estado

# testbench

'''
print("iniciando")
esp32_UART5 = Comunicacion_serial()
print("iniciado")
DATOS_R, ESTADO = esp32_UART5.solicitar_datos("QTD008001")
print(DATOS_R, ESTADO)
print("qrt verificado")
time.sleep(1)
DATOS_R, ESTADO = esp32_UART5.solicitar_datos("END004001")
print(DATOS_R, ESTADO)
print("encoder verificado")
time.sleep(1)
DATOS_R, ESTADO = esp32_UART5.solicitar_datos("UTD003001")
print(DATOS_R, ESTADO)
print("ultrasonico verificado")
time.sleep(1)
ESTADO = esp32_UART5.accion("TRA100100")
print(ESTADO)
time.sleep(1)
ESTADO = esp32_UART5.accion("TRU050050")
print(ESTADO)
time.sleep(1)
ESTADO = esp32_UART5.accion("BAU050050")
print(ESTADO)
'''
