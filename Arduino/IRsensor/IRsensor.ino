#include <IRremote.h>
 
int IRsensor = A1;        // 적외선 수신 센서를 연결한 핀
IRrecv irrecv(IRsensor);  // IRrecv 객체 생성
decode_results results;   // 수신한 데이터를 저장할 변수

IRsend irsend;
 
void setup()
{
  Serial.begin(9600);     // 9600bps 속도로 시리얼 통신 시작
  
  irrecv.enableIRIn();    // 적외선 센서의 수신 시작
  pinMode(13, OUTPUT);   // 디지털 13번핀(송신) output 설정
}
 
void loop()
{
  
  if(irrecv.decode(&results)) {         // 리모컨의 버튼이 눌렸으면
    Serial.println(results.value, HEX); // 시리얼 모니터에 버튼 값 16진수(HEX)로 출력

    Serial.println("input");
//    irsend.sendNEC(0x122428D7, 32);
    
    irrecv.resume();                    // 다음 값 받기
  }
}
