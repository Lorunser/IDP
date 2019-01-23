#include <SoftwareSerial.h>
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"

String data;

//initialise motors
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_DCMotor *left_motor = AFMS.getMotor(1);
Adafruit_DCMotor *right_motor = AFMS.getMotor(2);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  AFMS.begin();
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

  //set speeds
  right_speed = right_speed * pace;
  left_speed = left_speed * pace;

  //run motors
  run_motor(right_speed, right_motor);
  run_motor(left_speed, left_motor);
  
  //feedback to motor
  Serial.println("(" + String(left_speed) + "," + String(right_speed) + ")");
}

void run_motor(float motor_speed, Adafruit_DCMotor *motor)
{
  //-1 < motor_speed < 1 
  int abs_speed = (int)abs(motor_speed * 255);
  
  //set speed
  motor->setSpeed(abs_speed);

  //forwards or backwards
  if (motor_speed > 0){
    motor->run(FORWARD);
  }
  else{
    motor->run(BACKWARD);
  }
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
