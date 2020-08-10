/*  Interfaz RP4-ESP32-Potencia v0.9 
 *  este progrma sirve como interfaz de potencia para el proyecto E-bot, se espera que sea corrido en un ESP32-WROOM32 
 *  pues en este es donde se ha comprobado su funcionamiento, la via de comunicacion se realiza mediente el uart 2 de la
 *  placa con una Raspberry Pi 4 en la uart 5 con la configuracion de 8bits, sin bit de paridad con un bit stop(SERIAL_8N1), 
 *  atendiendo esto, aun no se implementa la parte de control de flujo en el programa siendo una extension a futuro
 *  de momento esa parte esta definida en la placa RP4, aunque es funcional, aun falta corregir los errores por conflictos de señales
 *  de entrada a lo cual abra actualizaciones futuras para tal cosa, la definicon de pines se hace tomando la referencia
 *  el Pinout general de la placa. 
*/

#include "Traccion.h"
#include "Base.h"
#include "Ultrasonico.h"
#include "Qtr8a.h"


#define RXD2 16                        // Comunicacion serial
#define TXD2 17
#define PIN_INTERRUPTION   2           // pin de interrupcion para la maquina de estados
#define LEDC_CTIMER_12_BIT 12          // Resolucion de los canales PWM
#define LEDC_BASE_FREQ     50          // frecuencia de los canales PWM

unsigned long tiempo = 0;
String estado = "esperando";
String modulo = "esperando";
String clase  = "esperando";
String dato_recivido = "ninguno";
String NUMERO1 = "000";
String NUMERO2 = "000";
const String Vmodulo[] = {"TR","BA","UT","QT","EN"};
const int   Vmod_num[] = {0,1,2,3,4};

// inicializacion de modulos
Traccion L298     = Traccion(2, 19, 18, 5, 4, 15, 2, 3);; //21 POR 2
Base Base1        = Base(22, 23, 0, 1);; // 2 por 23
Ultrasonico Ultra = Ultrasonico(13,12);;
Qtr8a QTURED      = Qtr8a(34, 35, 32, 33, 25, 26);

// funcion para el reset de la maquina de estados
void IRAM_ATTR reset_isr() { 
  estado = "esperando";
  modulo = "00";
  clase  = "0" ;
  NUMERO1 = "000";
  NUMERO2 = "000"; 
  }
 
void setup()
{
  // datos inicializacion puerto serie
  Serial.begin(115200);
  Serial.begin(115200, SERIAL_8N1);                // Inicializacion pruebas desde computadora, UART 0
  //Serial.begin(115200, SERIAL_8N1, RXD2, TXD2);  // Inicializacion RP4, UART 2
  tiempo = millis();

  // maquina de estados
  estado = "esperando";
  pinMode(PIN_INTERRUPTION, INPUT_PULLUP); 
  attachInterrupt(PIN_INTERRUPTION, reset_isr, FALLING);
}

// reset maquina de estados
void reset_ME(){
  estado = "esperando";
  modulo = "00";
  clase  = "0" ;
  NUMERO1 = "000";
  NUMERO2 = "000";
}

// funcion de prueba
void imprimir(char sel){
  Serial.println("EL MODULO ES ");
  Serial.println(modulo);
  Serial.println("TERMINA MODULO");
  Serial.println(clase);
  Serial.println(NUMERO1);
  Serial.println(NUMERO2);
  Serial.println(sel);
  //tiempo = millis();
  //Serial.println(tiempo);
}

void Send_Data_numeric(int Data[]){
  int longitud = sizeof(Data)+1;
  for (int i=0; i <= longitud; i++){
    Serial.println(Data[i]); 
  }
  Serial.println("DataEnd");
  delay(10);
}

void loop() {
  if (estado == "esperando"){
    if (Serial.available()>0) {
      //tiempo = millis();
      dato_recivido = Serial.readStringUntil('\n');
      estado = "ejecucion";
      Serial.println(dato_recivido);
    }
  }
  else if (estado == "ejecucion"){
    modulo = dato_recivido.substring(0, 2);
    clase = dato_recivido.substring(2, 3);
    NUMERO1 = dato_recivido.substring(3, 6);
    NUMERO2 = dato_recivido.substring(6, 9);
    String clase_s = dato_recivido.substring(0, 3);
    char clasec[3];
    clase_s.toCharArray(clasec, 4);
    char SELECCION = clasec[2];
    //imprimir(SELECCION);

// Modulo de traccion, L298
    if (modulo == Vmodulo[Vmod_num[0]]){
      switch(SELECCION){
        case 'A':
          L298.traccion_direccion(NUMERO1);
          break;
        case 'U':{
          L298.traccion_velocidad(NUMERO1, NUMERO2);
          break;}
        default:
          break;
        }
      reset_ME(); 
      }

// Modulo de la base para la base, 2 servos
    else if (modulo == Vmodulo[Vmod_num[1]]){
      switch(SELECCION){
        case 'U':{
          Base1.Base_Posicion(NUMERO1, NUMERO2);
          break;}
          
        default:
          break;
        }
        
      reset_ME(); 
      }

// Modulo sensor ultrasonico, HC-SR04
    else if (modulo == Vmodulo[Vmod_num[2]]){
      switch(SELECCION){
        case 'D':{
          Ultra.Distancia_UT();
          int cm = Ultra.medida;
          Serial.println(cm);
          Serial.println("DataEnd");
          delay(10);
          break;}
          
        default:
          break;
        }
        
      reset_ME();
      }

// Modulo sensor infrarrojo, QTR-8A
    else if (modulo == Vmodulo[Vmod_num[3]]){
      switch(SELECCION){
        case 'D':{
          QTURED.mesure();
          int valorqt[6];
          for (int i=0; i <= 5; i++){
            valorqt[i] = QTURED.medida[i];
            }
          Send_Data_numeric(valorqt);
          break;}
          
        default:
          break;
        }
        
      reset_ME();
      }

      else{
      reset_ME();
    }
  }
  // cualquier otro caso regresa a la espera
  else{
    reset_ME();
  }
}
