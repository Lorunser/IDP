#include <SoftwareSerial.h>
#include <String.h>

String data;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:

}

void motor_control(float dir, float pace = 1) {
  float right_speed, left_speed;
    
  if(dir >= 0){
    right_speed = 1;
    left_speed = 1 - 2 * dir;
  }

  else{
    right_speed = 1 + 2 * dir;
    left_speed = 1;
  }

  right_speed = right_speed * pace;
  left_speed = left_speed * pace;

  Serial.println("(" + String(left_speed) + "," + String(right_speed) + ")");
}

void serialEvent() {
  while (Serial.available()){
    float dir, pace;
    int comma_index;

    // data format = "dir,pace"
    // -1 < dir < 1 & -1 < pace < 1
    data = Serial.readString();
    comma_index = data.indexOf(',');

    // extract vals
    dir = data.substring(0, comma_index).toFloat();
    pace = data.substring(comma_index + 1).toFloat();

    // turn motors
    motor_control(dir, pace);
  }
}
