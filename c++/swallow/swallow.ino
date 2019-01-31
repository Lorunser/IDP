#include <SoftwareSerial.h>
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"
#include <Servo.h>

String data;

//initialise motors
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_DCMotor *left_motor = AFMS.getMotor(1);
Adafruit_DCMotor *right_motor = AFMS.getMotor(2);

Servo swiper_servo;
Servo back_flap_servo;

//constants
int SWIPER_ANGLE
int BACK_FLAP_ANGLE

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  AFMS.begin();
  swiper_servo.attach(9);
  back_flap_servo.attach(10);
  
  for (pos = 0; pos <= 90; pos += 3) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    swiper_servo.write(pos);              // tell servo to go to position in variable 'pos'
    back_flap_servo.write(pos);
    delay(15);                       // waits 15ms for the servo to reach the position
  }
  for (pos = 90; pos >= 0; pos -= 3) { // goes from 180 degrees to 0 degrees
    swiper_servo.write(pos);              // tell servo to go to position in variable 'pos'
    back_flap_servo.write(pos);
    delay(15);                       // waits 15ms for the servo to reach the position
  }
}

void loop() {
  
}


void swipe_right() {
  for (int pos = 0; pos <= SWIPER_ANGLE; pos += 1){
    swiper_servo.write(pos)
    delay(15)
  }
}

void swipe_left() {
  for (int pos = SWIPER_ANGLE; pos >= 0; pos -= 1){
    swiper_servo.write(pos)
    delay(15)
  }
}



void open_back_flap(){
  
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
