void setup() {
  Serial.begin(9600);

  pinMode(8, INPUT_PULLUP);
}

void loop() {
  // x coordinate
  Serial.print(analogRead(A1));
  // y coordinate
  Serial.print(analogRead(A0));
  // z coordinate (switch status)
  Serial.print(digitalRead(8));

}
