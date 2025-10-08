/* ESP32 Ultrasonic + SIM800L SMS alert + Buzzer
   - HC-SR04: triggerPin -> GPIO 14, echoPin -> GPIO 27
   - SIM800L TX->RX0 (GPIO3) / RX->TX0 (GPIO1) OR use SoftSerial pins (careful with HW Serial)
   - Buzzer on GPIO 12 (active HIGH via transistor)
   - Note: use level shifting and proper power for SIM800L
*/

#include <HardwareSerial.h>

const int trigPin = 14;
const int echoPin = 27;
const int buzzerPin = 12;

HardwareSerial simSerial(1); // use UART1 for SIM800L (avoid Serial0 used for logs)

long measureDistanceCm() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  long duration = pulseIn(echoPin, HIGH, 30000); // timeout 30ms
  if (duration == 0) return -1;
  long distance = duration * 0.034 / 2;
  return distance;
}

void sendSMS(const char* number, const char* text) {
  simSerial.println("AT");
  delay(500);
  simSerial.println("AT+CMGF=1"); // text mode
  delay(500);
  simSerial.print("AT+CMGS=\"");
  simSerial.print(number);
  simSerial.println("\"");
  delay(500);
  simSerial.print(text);
  simSerial.write(26); // Ctrl+Z
  delay(3000);
}

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(buzzerPin, OUTPUT);
  digitalWrite(buzzerPin, LOW);

  Serial.begin(115200);
  delay(1000);
  // UART1: TX=17, RX=16 (example) - change per wiring
  simSerial.begin(9600, SERIAL_8N1, 16, 17); // RX pin, TX pin
  Serial.println("System ready");
}

unsigned long lastAlert = 0;
const unsigned long alertCooldown = 5UL * 60UL * 1000UL; // 5 minutes cooldown

void loop() {
  long d = measureDistanceCm();
  if (d > 0) {
    Serial.print("Distance: ");
    Serial.print(d);
    Serial.println(" cm");
    // Heuristic: object closer than 300 cm and large (for elephant maybe closer) 
    // (Tune thresholds in field)
    if (d < 400 && (millis() - lastAlert) > alertCooldown) {
      Serial.println("Possible large object detected, alerting...");
      // Local alarm
      digitalWrite(buzzerPin, HIGH);
      delay(3000);
      digitalWrite(buzzerPin, LOW);
      // Send SMS (replace number)
      sendSMS("+91XXXXXXXXXX", "ALERT: Large animal detected near Village - check immediately.");
      lastAlert = millis();
    }
  } else {
    Serial.println("No echo");
  }
  delay(1000);
}
