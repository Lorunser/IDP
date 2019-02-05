#include <SoftwareSerial.h>
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"
#include <Servo.h>

//variables
String data;
bool block_present;

//initialise motors
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_DCMotor *left_motor = AFMS.getMotor(1);
Adafruit_DCMotor *right_motor = AFMS.getMotor(2);

Servo swiper_servo;
Servo flap_servo;

//constants
const int SWIPER_OPEN = 0;
const int SWIPER_CLOSED = 20;
const int FLAP_OPEN = 90;
const int FLAP_CLOSED = 0;
const int DELAY_TIME = 500;

//pins
const byte MAG_PIN_1 = 2;
const byte MAG_PIN_2 = 3;
const byte LDR_PIN = 4;

void setup() {
  Serial.begin(9600);

  //motors
  AFMS.begin();
  swiper_servo.attach(9);
  flap_servo.attach(10);

  //pins
  pinMode(MAG_PIN_1, INPUT);
  pinMode(MAG_PIN_2, INPUT);
  pinMode(LDR_PIN, INPUT);

  //start driving
  onwards();
}

void loop() {
  block_present = digitalRead(LDR_PIN);

  if(block_present){
    freeze();
    delay(1000);
    handle_block();
  }
}


//block handling routines
#pragma region
void handle_block() {
  bool mag_1 = digitalRead(MAG_PIN_1);
  bool mag_2 = digitalRead(MAG_PIN_2);
  bool mag_active = mag_1 or mag_2;
  
  if (mag_active){
    reject_block();
  }

  else {
    accept_block();
  }

  //send back mag active state
  delay(1000);
  onwards();
}

void accept_block() {
  open_swiper();
  inch_forward();
  close_swiper();
  //send info to pc
}

void reject_block() {
  close_swiper();
  inch_forward();
  open_swiper();
}
#pragma endregion

//servo routines
#pragma region 
void open_swiper() {
  swiper_servo.write(SWIPER_OPEN);
}

void close_swiper() {
  swiper_servo.write(SWIPER_CLOSED);
}

void open_flap(){
  flap_servo.write(FLAP_OPEN);
}

void close_flap(){
  flap_servo.write(FLAP_CLOSED);
}
#pragma endregion

//driving routines
#pragma region
void freeze(){
  left_motor->setSpeed(0);
  right_motor->setSpeed(0);

  left_motor->run(FORWARD);
  right_motor->run(FORWARD);
}

void onwards(){
  left_motor->setSpeed(255);
  right_motor->setSpeed(255);

  left_motor->run(FORWARD);
  right_motor->run(FORWARD);
}

void inch_forward(){
  //forwards and stop
  onwards();
  delay(DELAY_TIME);
  freeze();
}

void drive(float dir, float pace) {
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
}

void run_motor(float motor_speed, Adafruit_DCMotor *motor) {
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
#pragma endregion

//serial comms
#pragma region
void serialEvent() {
  float dir, pace;
  int comma_index;
  
  while (Serial.available()){
    // data format = "dir,pace"
    // -1 < dir < 1 & -1 < pace < 1
    data = Serial.readStringUntil('&');
  }
    comma_index = data.indexOf(',');

    // extract vals
    dir = data.substring(0, comma_index).toFloat();
    pace = data.substring(comma_index + 1).toFloat();

    // turn motors
    drive(dir, pace);
}
#pragma endregion
