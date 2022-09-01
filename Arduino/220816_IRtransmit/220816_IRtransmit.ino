#include <IRremote.h>

// TXD -> digtal 3 pin

IRsend irsend;

void setup(){
  Serial.begin(9600);

}

void loop(){
  char i=Serial.read();

  // add later : if SSDAMy get certain inputs, sendRC5 certain HEX
  if (i == 'a'){
    irsend.sendRC5(0x88C0051, 28);
    Serial.println("Sent");
  }
}
