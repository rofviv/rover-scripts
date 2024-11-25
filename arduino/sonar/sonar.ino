#include <NewPing.h>

const int numSensores = 5;
const int trigPins[numSensores] = {2, 4, 6, 8, 10};
const int echoPins[numSensores] = {3, 5, 7, 9, 11};
const int MAX_DISTANCE = 200;

NewPing* sensors[numSensores];

void setup() {
  Serial.begin(9600);
  for(int i = 0; i < numSensores; i++) {
    sensors[i] = new NewPing(trigPins[i], echoPins[i], MAX_DISTANCE);
  }
}

void loop() {
  for(int i = 0; i < numSensores; i++) {
    int distance = sensors[i]->ping_cm();
    if(distance > 0 && distance < 100) {
      Serial.print(i + 1);
      Serial.print(",");
      Serial.println(distance);
    }
    delay(300); // Pequeño delay entre sensores
  }
}