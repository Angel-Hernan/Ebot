#ifndef TRACCION_H
#define TRACCION_H
#include <Arduino.h>

class Traccion{
  public:
    Traccion(uint8_t _IN1, uint8_t _IN2, uint8_t _IN3, uint8_t _IN4, uint8_t _Velocidad_p1, uint8_t _Velocidad_p2, uint8_t _VELOCIDAD_CHANNEL_1, uint8_t _VELOCIDAD_CHANNEL_2);
    void traccion_direccion(String _direccion);
    void traccion_velocidad(String _velocidad_1, String _velocidad_2);
    
  private:
    uint8_t IN1;                 // entrada 1 del L298, pin 21
    uint8_t IN2;                 // entrada 2 del L298, pin 19
    uint8_t IN3;                 // entrada 3 del L298, pin 18
    uint8_t IN4;                 // entrada 4 del L298, pin 5
    uint8_t Velocidad_1;         // pin velocidad motor 1, pin 4
    uint8_t Velocidad_2;         // pin velocidad motor 2, pin 15
    uint8_t VELOCIDAD_CHANNEL_1;      // canal PWM para veloicidad 1, canal 2
    uint8_t VELOCIDAD_CHANNEL_2;      // canal PWM para veloicidad 2, canal 3
    String direccion_actual;
};
#endif
