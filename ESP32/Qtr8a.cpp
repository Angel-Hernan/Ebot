#include "Qtr8a.h"

Qtr8a::Qtr8a(uint8_t _Pin1, uint8_t _Pin2, uint8_t _Pin3, uint8_t _Pin4, uint8_t _Pin5, uint8_t _Pin6){
  Pin[0] = _Pin1; Pin[1] = _Pin2; Pin[2] = _Pin3; Pin[3] = _Pin4; Pin[4] = _Pin5; Pin[5] = _Pin6;
  
  medida[0] = 0; medida[1] = 0; medida[2] = 0; medida[3] = 0; medida[4] = 0; medida[5] = 0;
  
  // inicializacion datos sensor qrt-8a se coloca la resolucion
  analogReadResolution(12);  // resolucion para las lecturas analogicas
}

void Qtr8a::mesure(){
  for (int i=0; i <= 5; i++){
    int value = 0;
    value = analogRead(Pin[i]);
    delay(1);
    medida[i] = value; 
    Serial.println(value);// comentar
  }
}
