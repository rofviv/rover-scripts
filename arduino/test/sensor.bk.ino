#include <NewPing.h>
// se definen los pines para el sensor 1 
#define TRIGGER_sensor_1  2
#define ECHO_sensor_1     3

// se definen los pines para el sensor 2 
#define TRIGGER_sensor_2  4
#define ECHO_sensor_2     5

// se definen los pines para el sensor 3 
#define TRIGGER_sensor_3  6
#define ECHO_sensor_3     7

// se definen los pines para el sensor 4 
#define TRIGGER_sensor_4  8
#define ECHO_sensor_4     9

// se definen los pines para el sensor 5 
#define TRIGGER_sensor_5  10
#define ECHO_sensor_5     11



#define MAX_DISTANCE 200
 
NewPing sensor_1(TRIGGER_sensor_1, ECHO_sensor_1, MAX_DISTANCE);
NewPing sensor_2(TRIGGER_sensor_2, ECHO_sensor_2, MAX_DISTANCE);
NewPing sensor_3(TRIGGER_sensor_3, ECHO_sensor_3, MAX_DISTANCE);
NewPing sensor_4(TRIGGER_sensor_4, ECHO_sensor_4, MAX_DISTANCE);
NewPing sensor_5(TRIGGER_sensor_5, ECHO_sensor_5, MAX_DISTANCE);
 
void setup() {
  Serial.begin(9600);
  // mandamos un comando para la hiperterminal limpiar pantalla
Serial.write(12);
}
 
void loop() {
  delay(2000);
  Serial.print("distancia del sensor 1: ");
  Serial.print(sensor_1.ping_cm());
  Serial.println("cm");


  delay(2000);
  Serial.print("distancia del sensor 2: ");
  Serial.print(sensor_2.ping_cm());
  Serial.println("cm");

  delay(2000);
  Serial.print("distancia del sensor 3: ");
  Serial.print(sensor_3.ping_cm());
  Serial.println("cm");


  delay(2000);
  Serial.print("distancia del sensor 4: ");
  Serial.print(sensor_4.ping_cm());
  Serial.println("cm");
  
  delay(2000);
  Serial.print("distancia del sensor 5: ");
  Serial.print(sensor_5.ping_cm());
  Serial.println("cm");



}