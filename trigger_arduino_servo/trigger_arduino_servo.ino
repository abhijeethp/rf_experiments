#include <Servo.h>


#define STATUS_OFF 0
#define STATUS_ON 1
#define STATUS_SET_POS 2 
#define STATUS_RUN_FIXED_CYCLES 3

Servo myservo;  
int pos = 0;   
int divfactor = 4;

int current_status = STATUS_OFF;
int loop_num = 0;

int antenna_stand_still_duration_ms = 25;


void setup() {
  myservo.attach(9);
  Serial.begin(9600);
  myservo.write(pos);
}

void loop() {

  // change status if command trigerred
  if(Serial.available() > 0) {
    current_status = Serial.parseInt();
    Serial.println("Status changed to " + String(current_status));      
  }

  if(current_status == STATUS_OFF)
    return;
  
  if(current_status == STATUS_SET_POS) {
    pos = Serial.parseInt();
    myservo.write(pos);
    current_status = STATUS_OFF;
    return;
  }

  if(current_status == STATUS_RUN_FIXED_CYCLES) {
    if(loop_num == 0) {
      loop_num = Serial.parseInt();
    } else if(loop_num == 1) {
      loop_num = 0;
      current_status = STATUS_OFF;
      Serial.println("Status changed to " + String(current_status));
      return;
    } else {
      loop_num -= 1;
    }
  }
    
  Serial.println(String(pos));
  delay(antenna_stand_still_duration_ms);

  while (pos <= 80) { 
    myservo.write(pos++); delay(45/divfactor);
    myservo.write(pos++); delay(40/divfactor);
    myservo.write(pos++); delay(30/divfactor);
    myservo.write(pos++); delay(15/divfactor);
    myservo.write(pos++); delay(10/divfactor);
    myservo.write(pos++); delay(10/divfactor);
    myservo.write(pos++); delay(15/divfactor);
    myservo.write(pos++); delay(30/divfactor);
    myservo.write(pos++); delay(40/divfactor);
    myservo.write(pos++); delay(45/divfactor); 
    Serial.println(String(pos));
    delay(antenna_stand_still_duration_ms);
  }

  Serial.println(String(pos));
  delay(antenna_stand_still_duration_ms);

  while (pos >= 10) { 
    myservo.write(pos--); delay(45/divfactor);
    myservo.write(pos--); delay(40/divfactor);
    myservo.write(pos--); delay(30/divfactor);
    myservo.write(pos--); delay(15/divfactor);
    myservo.write(pos--); delay(10/divfactor);
    myservo.write(pos--); delay(10/divfactor);
    myservo.write(pos--); delay(15/divfactor);
    myservo.write(pos--); delay(30/divfactor);
    myservo.write(pos--); delay(40/divfactor);
    myservo.write(pos--); delay(45/divfactor);
    Serial.println(String(pos));
    delay(antenna_stand_still_duration_ms);
  }

  Serial.println(String(pos));
  delay(antenna_stand_still_duration_ms);  
}