#ifndef QTR8A_H
#define QTR8A_H
#include <Arduino.h>

class Qtr8a{
  public:
    // metodos publicos
    Qtr8a(uint8_t _Pin1, uint8_t _Pin2, uint8_t _Pin3, uint8_t _Pin4, uint8_t _Pin5, uint8_t _Pin6);
    void mesure();
    
    // atributos publicos
    int medida[6];

  private:
    uint8_t Pin[6];
  
};
#endif
