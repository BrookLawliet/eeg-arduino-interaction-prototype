void setup() {
  pinMode(13, OUTPUT);        // Set digital pin 13 (built-in LED) as output
  Serial.begin(9600);         // Initialize serial communication at 9600 baud
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');  // Read command until newline
    command.trim();  // Remove any whitespace or newline characters

    if (command == "ON") {
      digitalWrite(13, HIGH);  // Turn LED on
    } 
    else if (command == "OFF") {
      digitalWrite(13, LOW);   // Turn LED off
    }
  }
}
