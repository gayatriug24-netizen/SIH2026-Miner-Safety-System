/*
  Jeevan Setu — Reconnaissance Rover (prototype)
  Components: Arduino Nano + L298N + 2WD motors + HC-SR04 + MQ-2 + DHT11

  This sketch drives the rover locally and prints sensor values over Serial.
  ESP32-CAM can be used separately for the video/wireless stream.
*/
#include <DHT.h>

#define IN1 5
#define IN2 6
#define IN3 9
#define IN4 10
#define ENA 3
#define ENB 11
#define TRIG 7
#define ECHO 8
#define MQ2 A0
#define DHTPIN 4
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  pinMode(IN1, OUTPUT); pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT); pinMode(IN4, OUTPUT);
  pinMode(ENA, OUTPUT); pinMode(ENB, OUTPUT);
  pinMode(TRIG, OUTPUT); pinMode(ECHO, INPUT);
  dht.begin();
  stopMotors();
}

void loop() {
  long distance = readDistanceCm();
  int gas = analogRead(MQ2);
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  if (distance > 0 && distance < 25) {
    stopMotors();
    delay(250);
  } else {
    forward(150);
  }

  Serial.print("gas="); Serial.print(gas);
  Serial.print(",temp="); Serial.print(temperature);
  Serial.print(",humidity="); Serial.print(humidity);
  Serial.print(",distance="); Serial.println(distance);
  delay(500);
}

long readDistanceCm() {
  digitalWrite(TRIG, LOW); delayMicroseconds(2);
  digitalWrite(TRIG, HIGH); delayMicroseconds(10);
  digitalWrite(TRIG, LOW);
  long duration = pulseIn(ECHO, HIGH, 30000);
  if (!duration) return -1;
  return duration * 0.0343 / 2.0;
}

void forward(int speedVal) {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);
  analogWrite(ENA, speedVal);
  analogWrite(ENB, speedVal);
}

void stopMotors() {
  digitalWrite(IN1, LOW); digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW); digitalWrite(IN4, LOW);
  analogWrite(ENA, 0); analogWrite(ENB, 0);
}
