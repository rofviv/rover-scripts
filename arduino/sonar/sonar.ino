// Definimos los pines de los sensores
const int numSensores = 1;  // Número de sensores que vas a usar
int echoPins[numSensores] = {12};  // 3, 5
int trigPins[numSensores] = {13};  // 2, 4
long distancias[numSensores];  // Array para almacenar distancias

void setup() {
  Serial.begin(9600);
  
  // Configuramos los pines para todos los sensores
  for (int i = 0; i < numSensores; i++) {
    pinMode(trigPins[i], OUTPUT);  // Pines trig como salida
    pinMode(echoPins[i], INPUT);   // Pines echo como entrada
  }
}

void loop() {
  for (int i = 0; i < numSensores; i++) {
    distancias[i] = medirDistancia(i);  // Medimos la distancia para cada sensor

    if (distancias[i] < 80) {  // Si detecta algo a menos de 80 cm
       // Enviamos los datos como "sensor,distancia"
      Serial.print(i + 1);  // Número de sensor
      Serial.print(",");  // Separador
      Serial.println(distancias[i]);  // Distancia medida
    }
  }
  delay(300);  // Esperamos 1 segundo antes de la siguiente medición
}

long medirDistancia(int sensorIndex) {
  digitalWrite(trigPins[sensorIndex], LOW);
  delayMicroseconds(2);
  digitalWrite(trigPins[sensorIndex], HIGH);
  delayMicroseconds(5);
  digitalWrite(trigPins[sensorIndex], LOW);

  long duracion = pulseIn(echoPins[sensorIndex], HIGH);  // Medimos el tiempo de eco
  return microsecondsToCentimeters(duracion);  // Convertimos a cm
}

long microsecondsToCentimeters(long microseconds) {
  return microseconds / 29 / 2;  // Calculamos la distancia en cm
}
