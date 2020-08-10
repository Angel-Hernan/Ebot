#ifndef BASE_H
#define BASE_H
#include <Arduino.h>

class Base{
  public:
  Base(uint8_t _ServoPin1, uint8_t _ServoPin2, uint8_t _ServoChannel1, uint8_t _ServoChannel2);
  void Base_Posicion(String _angulo1, String _angulo2);
  
  private:
  uint8_t ServoPin1;         // pin velocidad motor 1, pin 22
  uint8_t ServoPin2;         // pin velocidad motor 2, pin 23
  uint8_t ServoChannel1;      // canal PWM para veloicidad 1, canal 0
  uint8_t ServoChannel2;      // canal PWM para veloicidad 2, canal 1
  
};
#endif
