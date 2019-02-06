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
const int FLAP_OPEN = 170;
const int FLAP_CLOSED = 80;
const int DELAY_TIME = 3000;

//enum constants
const char NO_BLOCK = '0';
const char BLOCK_DETECTED = '1';
const char BLOCK_ACCEPTED = '2';
const char BLOCK_REJECTED = '3';

//input pins
const byte MAG_PIN_1 = 2;
const byte MAG_PIN_2 = 3;
const byte LDR_PIN = 4;

//output pins
const byte RED_LED_FLASHER = 5;
const byte AMBER_LED_FLASHER = 6;

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

  pinMode(RED_LED_FLASHER, OUTPUT);
  pinMode(AMBER_LED_FLASHER, OUTPUT);

  //initialise swipers
  close_swiper();
  close_flap();

}

void loop() {
  bool block_present = digitalRead(LDR_PIN);

  if(block_present){
    freeze();
    handle_block();
  }
/*
  while(true){
    open_swiper();
    close_swiper();
    open_flap();
    close_flap();
  }
  */
}


//block handling routines
#pragma region
void handle_block() {
  //alert pc
  relay_info(BLOCK_DETECTED);

  bool mag_1, mag_2;
  bool mag_active = false;

  int step_time = 50;
  for(int i = 0; i < 3; i += 1){    
    mag_1 = digitalRead(MAG_PIN_1);
    mag_2 = digitalRead(MAG_PIN_2);

    if(mag_1 or mag_2);
    {
      mag_active = true;
    }

    //move on and check again
    inch_forward(step_time);
    delay(step_time * 10);
  }
  
  if (mag_active){
    reject_block();
  }

  else {
    accept_block();
  }

  delay(1000);
  onwards();
}

void accept_block() {
  open_swiper();
  inch_forward(DELAY_TIME);
  close_swiper();
  relay_info(BLOCK_ACCEPTED);
}

void reject_block() {
  close_swiper();
  inch_forward(DELAY_TIME);
  open_swiper();
  relay_info(BLOCK_REJECTED);
}
#pragma endregion

//servo routines
#pragma region 
void open_swiper() {
  freeze();  
  swiper_servo.write(SWIPER_OPEN);
  delay(500);
}

void close_swiper() {
  freeze();
  swiper_servo.write(SWIPER_CLOSED);
  delay(500);
}

void open_flap(){
  freeze();
  flap_servo.write(FLAP_OPEN);
  delay(500);
}

void close_flap(){
  freeze();
  flap_servo.write(FLAP_CLOSED);
  delay(500);
}
#pragma endregion

//driving routines
#pragma region
void freeze(){
  left_motor->setSpeed(0);
  right_motor->setSpeed(0);

  left_motor->run(FORWARD);
  right_motor->run(FORWARD);

  //turn off AMBER_LED
  digitalWrite(AMBER_LED_FLASHER, LOW);
}

void onwards(){
  left_motor->setSpeed(100);
  right_motor->setSpeed(100);

  left_motor->run(FORWARD);
  right_motor->run(FORWARD);

  //turn on amber LED
  digitalWrite(AMBER_LED_FLASHER, HIGH);
}

void inch_forward(int delay_time){
  //forwards and stop
  onwards();
  delay(delay_time);
  freeze();
}

void drive(float dir, float pace) {
  float right_speed, left_speed;

  if(dir < 2.1 and dir > 1.9){
    open_flap();
    return;
  }
  
  
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

  //set LEDs
  if(pace == 0){
    digitalWrite(AMBER_LED_FLASHER, LOW);
  }
  else{
    digitalWrite(AMBER_LED_FLASHER, HIGH);
  }
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
void relay_info(char code){
  Serial.println(code);
}


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
