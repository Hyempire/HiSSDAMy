
#include <IRremote.h>

IRsend irsend;

void setup() {
  Serial.begin(9600);

  pinMode(8, INPUT_PULLUP); //조이스틱 z축
}

void loop() {
  // x coordinate
  Serial.print(analogRead(A1));
  Serial.print(" ");
  // y coordinate
  Serial.print(analogRead(A0));
  Serial.print(" ");
  // z coordinate (switch status)
  Serial.print(digitalRead(8));

  char i=Serial.read();
  if (i == 'a'){
    irsend.sendRC5(0x5ED9768, 28);   // 0x 뒤에 입력하고 싶은 HEX 값 기입
    Serial.println();
    Serial.print("Sent");
  }

  Serial.println();
  delay(100);

}
