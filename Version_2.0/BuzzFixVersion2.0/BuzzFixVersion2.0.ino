**Updated Arduino Code (Buzzer ON until Drowsiness Ends)**

```cpp
#include "esp_camera.h"
#include <WiFi.h>
#include <WebServer.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

const char* ssid = "OPPO A54";
const char* password = "21692169";

#define BUZZER_PIN 2
#define RED_LED 12
#define GREEN_LED 13
#define SDA_PIN 14
#define SCL_PIN 15

LiquidCrystal_I2C lcd(0x27, 16, 2);
WebServer server(80);

void handleBuzzOn() {
  digitalWrite(BUZZER_PIN, HIGH);
  Serial.println("Buzzer ON");
  server.send(200, "text/plain", "Buzzer ON");
}

void handleBuzzOff() {
  digitalWrite(BUZZER_PIN, LOW);
  Serial.println("Buzzer OFF");
  server.send(200, "text/plain", "Buzzer OFF");
}

void handleCapture() {
  camera_fb_t* fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("Camera capture failed");
    server.send(500, "text/plain", "Camera capture failed");
    return;
  }
  server.sendHeader("Content-Type", "image/jpeg");
  server.sendHeader("Content-Length", String(fb->len));
  server.send(200);
  WiFiClient client = server.client();
  client.write(fb->buf, fb->len);
  esp_camera_fb_return(fb);
  Serial.println("Image sent");
}

void handleLCD() {
  if (server.hasArg("text")) {
    String text = server.arg("text");
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Status:");
    lcd.setCursor(0, 1);
    lcd.print(text.substring(0, 16));
    Serial.println("LCD Updated: " + text);
    server.send(200, "text/plain", "LCD Updated");
  } else {
    server.send(400, "text/plain", "Missing text argument");
  }
}

void handleLED() {
  if (server.hasArg("state")) {
    String state = server.arg("state");
    if (state == "green") {
      digitalWrite(GREEN_LED, HIGH);
      digitalWrite(RED_LED, LOW);
      Serial.println("LED: GREEN ON, RED OFF");
    } else if (state == "red") {
      digitalWrite(RED_LED, HIGH);
      digitalWrite(GREEN_LED, LOW);
      Serial.println("LED: RED ON, GREEN OFF");
    }
    server.send(200, "text/plain", "LED Updated");
  } else {
    server.send(400, "text/plain", "Missing state argument");
  }
}

void startWebServer() {
  server.on("/buzz_on", handleBuzzOn);
  server.on("/buzz_off", handleBuzzOff);
  server.on("/capture", handleCapture);
  server.on("/lcd", handleLCD);
  server.on("/led", handleLED);
  server.begin();
  Serial.println("Web server started");
}

void setup() {
  Serial.begin(115200);
  Wire.begin(SDA_PIN, SCL_PIN);
  lcd.begin(16, 2);
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Team: A2-4");
  delay(800);

  lcd.clear(); lcd.setCursor(0, 0); lcd.print("Project:"); lcd.setCursor(0, 1); lcd.print("AI Sleep Detect"); delay(1100);
  lcd.clear(); lcd.setCursor(0, 0); lcd.print("& Alert System"); lcd.setCursor(0, 1); lcd.print("for Drivers"); delay(1100);
  lcd.clear(); lcd.setCursor(0, 0); lcd.print("Discoverd by"); lcd.setCursor(0, 1); lcd.print("Future Engineers-"); delay(900);
  lcd.clear(); lcd.setCursor(0, 0); lcd.print("1.Vaibhav Kangane"); delay(900);
  lcd.clear(); lcd.setCursor(0, 0); lcd.print("2.Om Pardesi"); delay(900);
  lcd.clear(); lcd.setCursor(0, 0); lcd.print("3.Rohit Pawale "); delay(900);
  lcd.print("System Booting...");
  Serial.println("LCD Initialized");

  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(RED_LED, OUTPUT);
  pinMode(GREEN_LED, OUTPUT);
  digitalWrite(BUZZER_PIN, LOW);
  digitalWrite(RED_LED, LOW);
  digitalWrite(GREEN_LED, LOW);

  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = 5; config.pin_d1 = 18; config.pin_d2 = 19; config.pin_d3 = 21;
  config.pin_d4 = 36; config.pin_d5 = 39; config.pin_d6 = 34; config.pin_d7 = 35;
  config.pin_xclk = 0; config.pin_pclk = 22; config.pin_vsync = 25; config.pin_href = 23;
  config.pin_sccb_sda = 26; config.pin_sccb_scl = 27; config.pin_pwdn = 32; config.pin_reset = -1;
  config.xclk_freq_hz = 20000000; config.pixel_format = PIXFORMAT_JPEG;
  config.frame_size = FRAMESIZE_QVGA; config.jpeg_quality = 12;
  config.fb_count = 1; config.fb_location = CAMERA_FB_IN_PSRAM;
  config.grab_mode = CAMERA_GRAB_LATEST;

  if (esp_camera_init(&config) != ESP_OK) {
    Serial.println("Camera init failed");
    lcd.setCursor(0, 1); lcd.print("Camera Error!");
    return;
  }

  WiFi.begin(ssid, password);
  WiFi.setSleep(false);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500); Serial.print(".");
  }
  Serial.println("\nWiFi connected!");
  Serial.print("IP Address: "); Serial.println(WiFi.localIP());

  startWebServer();

  lcd.clear();
  lcd.setCursor(0, 0); lcd.print("System Ready to");
  lcd.setCursor(0, 1); lcd.print("detect Drowsiness...");
}

void loop() {
  server.handleClient();
}
```

