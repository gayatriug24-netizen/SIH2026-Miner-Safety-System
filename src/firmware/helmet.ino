/*
  Jeevan Setu — Smart Miner Helmet Module (prototype)
  Components: ESP32 + MPU6050 + OLED + SOS button + buzzer

  Sends a JSON payload to the backend through Wi-Fi/HTTP.
  Replace WIFI_SSID, WIFI_PASSWORD and BACKEND_URL before testing.

  NOTE: Thresholds and hardware are prototype/demo values only.
*/
#include <Wire.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_Sensor.h>

const char* WIFI_SSID = "YOUR_WIFI";
const char* WIFI_PASSWORD = "YOUR_PASSWORD";
const char* BACKEND_URL = "http://YOUR_LAPTOP_IP:5000/api/worker/update";

#define SOS_PIN 25
#define BUZZER_PIN 26
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

Adafruit_MPU6050 mpu;
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

bool fallDetected = false;
bool movement = true;
unsigned long sosPressedAt = 0;

void connectWiFi() {
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  unsigned long started = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - started < 12000) delay(250);
}

void setup() {
  Serial.begin(115200);
  pinMode(SOS_PIN, INPUT_PULLUP);
  pinMode(BUZZER_PIN, OUTPUT);

  Wire.begin();
  mpu.begin();
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);

  if (display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    display.clearDisplay();
    display.setTextColor(SSD1306_WHITE);
    display.setTextSize(1);
    display.setCursor(0, 0);
    display.println("JEEVAN SETU");
    display.println("Helmet module ready");
    display.display();
  }
  connectWiFi();
}

void loop() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  float acceleration = sqrt(a.acceleration.x*a.acceleration.x +
                             a.acceleration.y*a.acceleration.y +
                             a.acceleration.z*a.acceleration.z);
  fallDetected = acceleration > 24.0; // demo threshold
  movement = fabs(g.gyro.x) + fabs(g.gyro.y) + fabs(g.gyro.z) > 0.18;

  bool sos = digitalRead(SOS_PIN) == LOW;
  if (sos) tone(BUZZER_PIN, 2200, 180);

  sendWorkerData(sos);
  updateDisplay(sos);
  delay(2500);
}

void sendWorkerData(bool sos) {
  if (WiFi.status() != WL_CONNECTED) return;

  HTTPClient http;
  http.begin(BACKEND_URL);
  http.addHeader("Content-Type", "application/json");
  String payload = String("{\"worker_id\":\"W03\",\"name\":\"Worker 03\",\"zone\":\"N4\",") +
                   String("\"heart_rate\":0,\"movement\":") + (movement ? "true" : "false") +
                   String(",\"sos\":") + (sos ? "true" : "false") +
                   String(",\"fall_detected\":") + (fallDetected ? "true" : "false") + "}";
  int code = http.POST(payload);
  Serial.printf("Worker update HTTP %d\n", code);
  http.end();
}

void updateDisplay(bool sos) {
  if (!display.width()) return;
  display.clearDisplay();
  display.setCursor(0,0);
  display.setTextSize(1);
  display.println("WORKER 03");
  display.print("Motion: "); display.println(movement ? "NORMAL" : "NONE");
  display.print("Fall: "); display.println(fallDetected ? "DETECTED" : "NO");
  display.print("SOS: "); display.println(sos ? "ACTIVE" : "READY");
  display.display();
}
