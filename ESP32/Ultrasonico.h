#ifndef ULTRASONICO_H
#define ULTRASONICO_H
#include <Arduino.h>

class Ultrasonico{
  public:
    // metodos publicos
    Ultrasonico(uint8_t _TriggerPin, uint8_t _EchoPin);
    void Distancia_UT();

    // atributos publicos
    int medida;

  private:
    uint8_t TriggerPin;       // pin para la terminal trigger del hc-sr04, pin 13
    uint8_t EchoPin;         // pin para la terminal echo del hc-sr04, 12
};
#endif
