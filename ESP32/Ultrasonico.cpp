#include "Ultrasonico.h"

Ultrasonico::Ultrasonico(uint8_t _TriggerPin, uint8_t _EchoPin){
  TriggerPin = _TriggerPin;
  EchoPin    = _EchoPin;
  medida     = 0;
  
  // Inicializacion sensor de distancia ultrasonico
  pinMode(TriggerPin, OUTPUT);
  pinMode(EchoPin, INPUT);
}

void Ultrasonico::Distancia_UT() {
  //Ultrasonico_pin Ultrasonico_datos = {13,12};
  long duration, distanceCm;
   
  digitalWrite(TriggerPin, LOW);  //para generar un pulso limpio ponemos a LOW 4us
  delayMicroseconds(4);
  digitalWrite(TriggerPin, HIGH);  //generamos Trigger (disparo) de 10us
  delayMicroseconds(10);
  digitalWrite(TriggerPin, LOW);
   
  duration = pulseIn(EchoPin, HIGH);  //medimos el tiempo entre pulsos, en microsegundos
   
  distanceCm = duration * 10 / 292/ 2;   //convertimos a distancia, en cm
  medida = distanceCm;
}
