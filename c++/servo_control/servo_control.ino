#include <SoftwareSerial.h>
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"
# include <Servo.h>

String data;

//initialise motors
Servo swiper_servo;
Servo back_flap_servo;

int pos = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  swiper_servo.attach(9);
  back_flap_servo.attach(10);
  
  /*for (pos = 0; pos <= 90; pos += 3) { // goes from 0 degrees to 180 degrees
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
  */
  swiper_servo.write(0);
  back_flap_servo.write(0);
}

void loop() {
  swiper_servo.write(0);
  back_flap_servo.write(0);

  delay(2000);

  //swiper_servo.write(90);
  //back_flap_servo.write(90);

  delay(1000);
}


void swipe() {
  
}


void open_back_flap(){
  
}
