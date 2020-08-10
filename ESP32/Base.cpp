#include "Base.h"

Base::Base(uint8_t _ServoPin1, uint8_t _ServoPin2, uint8_t _ServoChannel1, uint8_t _ServoChannel2){
  ServoPin1 = _ServoPin1;         // pin velocidad motor 1, pin 22
  ServoPin2 = _ServoPin2;         // pin velocidad motor 2, pin 23
  ServoChannel1 = _ServoChannel1;      // canal PWM para veloicidad 1, canal 0
  ServoChannel2 = _ServoChannel2;      // canal PWM para veloicidad 2, canal 1
  
  const uint8_t LEDC_CTIMER_12_BIT = 12;
  const uint8_t LEDC_BASE_FREQ     = 50;
  
  // datos inicializacion base, PWM para el control de servomotres
  ledcSetup(ServoChannel2, LEDC_BASE_FREQ, LEDC_CTIMER_12_BIT);
  ledcSetup(ServoChannel2, LEDC_BASE_FREQ, LEDC_CTIMER_12_BIT);
  ledcAttachPin(ServoPin1, ServoChannel1);
  ledcAttachPin(ServoPin2, ServoChannel2);
}

// Funcion para escrivir los valores PWM para el posicionamiento de los servos
void Base::Base_Posicion(String _angulo_1, String _angulo_2) {
  // valor entre 100 y 480
  int numAB1 = (_angulo_1.toInt()) * (4096/100);
  int numAB2 = (_angulo_2.toInt()) * (4096/100);
  ledcWrite(ServoChannel1, numAB1);
  ledcWrite(ServoChannel2, numAB2);
}
