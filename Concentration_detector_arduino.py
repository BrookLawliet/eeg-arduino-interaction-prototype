#define LED_PIN 9        // LED on D9
#define BUZZER_PIN 10    // Buzzer on D10

void setup() {
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "LED_ON") {
      digitalWrite(LED_PIN, HIGH);
    } else if (command == "LED_OFF") {
      digitalWrite(LED_PIN, LOW);
    } else if (command == "BEEP") {
      tone(BUZZER_PIN, 1000);   // 1 kHz tone
      delay(1000);
      noTone(BUZZER_PIN);
    }
  }
}
