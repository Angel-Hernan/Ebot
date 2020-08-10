#include "Traccion.h"

Traccion::Traccion(uint8_t _IN1, uint8_t _IN2, uint8_t _IN3, uint8_t _IN4, uint8_t _Velocidad_p1, uint8_t _Velocidad_p2, uint8_t _VELOCIDAD_CHANNEL_1, uint8_t _VELOCIDAD_CHANNEL_2){
  IN1 = _IN1;                 // entrada 1 del L298, pin 21
  IN2 = _IN2;                 // entrada 2 del L298, pin 19
  IN3 = _IN3;                 // entrada 3 del L298, pin 18
  IN4 = _IN4;                 // entrada 4 del L298, pin 5
  Velocidad_1 = _Velocidad_p1;                      // pin velocidad motor 1, pin 4
  Velocidad_2 = _Velocidad_p2;                      // pin velocidad motor 2, pin 15
  VELOCIDAD_CHANNEL_1 = _VELOCIDAD_CHANNEL_1;      // canal PWM para veloicidad 1, canal 2
  VELOCIDAD_CHANNEL_2 = _VELOCIDAD_CHANNEL_2;      // canal PWM para veloicidad 2, canal 3
  direccion_actual = "stop";
  const uint8_t LEDC_CTIMER_12_BIT = 12;
  const uint8_t LEDC_BASE_FREQ     = 50;

  // datos control l298
  pinMode(IN1, OUTPUT);    // entrada 1
  pinMode(IN2, OUTPUT);    // entrada 2
  pinMode(IN3, OUTPUT);    // entrada 3
  pinMode(IN4, OUTPUT);    // entrada 4
  ledcSetup(VELOCIDAD_CHANNEL_1, LEDC_BASE_FREQ, LEDC_CTIMER_12_BIT);
  ledcSetup(VELOCIDAD_CHANNEL_2, LEDC_BASE_FREQ, LEDC_CTIMER_12_BIT);
  ledcAttachPin(Velocidad_1, VELOCIDAD_CHANNEL_1);   // control de velocidad motor 1 
  ledcAttachPin(Velocidad_2, VELOCIDAD_CHANNEL_2);   // control de velocidad motor 1 
}

void Traccion::traccion_direccion(String _direccion){
  if (_direccion == "100") {
    direccion_actual = "adelante";
    digitalWrite(IN4, HIGH);
    digitalWrite(IN3, LOW);
    digitalWrite(IN2, HIGH);
    digitalWrite(IN1, LOW);
    }
  else if (_direccion == "200") {
    direccion_actual = "atras";
    digitalWrite(IN4, LOW);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN2, LOW);
    digitalWrite(IN1, HIGH);
    }
  else if (_direccion == "300") {
    direccion_actual = "izquierda";
    digitalWrite(IN4, LOW);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN2, HIGH);
    digitalWrite(IN1, LOW);
    }
  else if (_direccion == "400") {
    direccion_actual = "derecha";
    digitalWrite(IN4, HIGH);
    digitalWrite(IN3, LOW);
    digitalWrite(IN2, LOW);
    digitalWrite(IN1, HIGH);
    }
  else{
    direccion_actual = "stop";
    digitalWrite(IN4, LOW);
    digitalWrite(IN3, LOW);
    digitalWrite(IN2, LOW);
    digitalWrite(IN1, LOW);
    }
}

// funcion para definir los valores de velocidad para el modulo L298 
void Traccion::traccion_velocidad(String _velocidad_1, String _velocidad_2) {
  int numAA1 = (_velocidad_1.toInt()) * (4096/100);
  int numAA2 = (_velocidad_2.toInt()) * (4096/100);
  ledcWrite(VELOCIDAD_CHANNEL_1, numAA1);
  ledcWrite(VELOCIDAD_CHANNEL_2, numAA1);
}
