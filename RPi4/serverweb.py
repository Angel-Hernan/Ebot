#!/usr/bin/env python3
# ip de la computadora 192.168.1.68:81000 pagina de pruebas, varia dependiendo de donde
# se corra el programa, revisalo, windows>cmd>ipconfig y linux>terminal>ifconfig

# importando librerias
import cv2
import sys
from flask import Flask, render_template, Response, make_response, request, redirect, url_for
from flask_basicauth import BasicAuth
import webcamvideostream as wcs 
import time
import threading
import os
import Maquina_Estados as mq

# clasificador de objetos camara
#object_classifier = cv2.CascadeClassifier("models/fullbody_recognition_model.xml") # an opencv classifier

# cualquier carpeta que se quiera cargar, esta debe estar en la carpeta 
# static dentro del directorio del proyecto, en otro caso no funciona
PEOPLE_FOLDER = os.path.join('static', 'imagenes')

# se crea un objeto flask, este sera el servidor local
app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'UPG'
app.config['BASIC_AUTH_PASSWORD'] = 'Robotica'
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)
last_epoch = 0

# variables necesarias
camera_thread = wcs.WebcamVideoStream().start()
Comunicacion = mq.Maquina()
leght_ut = [0]
qtr_val  = [0, 0, 0, 0, 0, 0]

# se carga dentro del servido el directorio
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
#
#@app.route('/')
#@app.route('/index')
#def show_index():
#
#    # sacamos los archivos a utilizar dentro de la plantilla html
#    logo = os.path.join(app.config['UPLOAD_FOLDER'], 'OIP.jpg')
#    Icon = os.path.join(app.config['UPLOAD_FOLDER'], 'iconop.ico')
#
#    # retornamos la plantilla que queramos mostrar en la direccion
#    return render_template("controll_manual.html", user_image = logo,
#                           Iconop = Icon)
@app.route('/')
@basic_auth.required
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        if camera.stopped:
            break
        frame = camera.read()
        ret, jpeg = cv2.imencode('.jpg',frame)
        if jpeg is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
        else:
            print("frame is none")

@app.route('/video_feed')
def video_feed():        
    return Response(gen(camera_thread),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/modo_manual')
def interfaz_manual():
    return render_template('control_manual.html', val_ut = leght_ut[0], valq_1 = qtr_val[0],
                           valq_2 = qtr_val[1], valq_3 = qtr_val[2], valq_4 = qtr_val[3], 
                           valq_5 = qtr_val[4], valq_6 = qtr_val[5])

# usa los comando de la libreia Maquina de estados para interactuar con
# los actuadores y sensores en el esp32
@app.route('/modo_manual/comando_directo/<string:comando_d>', methods=['POST', "GET"])
def comando_directo(comando_d):
    estado_e, dato_e, des_error, com_env = Comunicacion.seleccion_comando(comando_d)
    tipo_c = com_env[0:2]
    if tipo_c == "UT":
        global leght_ut
        leght_ut = dato_e
    
    elif tipo_c == "QT":
        global qtr_val
        qtr_val = dato_e
        
    print(com_env)
    response = make_response(redirect(url_for('interfaz_manual')))
    return(response)

@app.route("/modo_manual/comando_armado/<string:clase>", methods=['POST', "GET"])
def route(clase):
    if request.method == "POST":
        if clase == "base":
            comando_i = "BAU"
            valor_s1 = request.form['Servo1']
            valor_s2 = request.form['Servo2']
            val_s1 = verificar_longitud(valor_s1)
            val_s2 = verificar_longitud(valor_s2)
            comando_final = comando_i + val_s1 + val_s2
        
        elif clase == "traccion":
            comando_i = "TRU"
            valor_v1 = request.form['Velocidad_1']
            valor_v2 = request.form['Velocidad_2']
            val_v1 = verificar_longitud(valor_v1)
            val_v2 = verificar_longitud(valor_v2)
            comando_final = comando_i + val_v1 + val_v2

        elif clase == "comandos":
            comando = request.form['comando']
            if len(comando) == 0:
                comando_final = "ZZZ"
            else:
                comando_final = comando
        
        estado_e, dato_e, des_error, com_env = Comunicacion.seleccion_comando(comando_final)
        print(com_env)
        #print(comando_final)

    response = make_response(redirect(url_for('interfaz_manual')))
    return(response)

def verificar_longitud(numero):
    longitud = len(numero)

    if longitud == 1:
        dato = "00" + numero
    elif longitud == 2:
        dato = "0" + numero
    elif longitud == 3:
        dato = numero
    else:
        dato = "000"
    
    return dato

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8100, threaded=True)
