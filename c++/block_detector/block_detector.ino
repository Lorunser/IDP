//libraries
#include <SoftwareSerial.h>

//global consts
const long INTERVAL = 1000;
const byte LED_PIN = LED_BUILTIN;
const byte BLOCK_PIN = 1;
const byte ACTIVITY_PIN = 2;

//global vars
unsigned long current_millis = 0;
unsigned long previous_millis = 0
int led_state = LOW;

//volatile vars to change in ISRs
volatile bool block_present = false;
volatile bool block_active = false;


void setup() {
  //declare pin types
  pinMode(LED_PIN, OUTPUT);
  pinMode(BLOCK_PIN, INPUT_PULLUP)
  pinMode(ACTIVITY_PIN, INPUT)

  //attach interrupts
  attachInterrupt(digitalPinToInterrupt(BLOCK_PIN), interrupt_block_detected, RISING)
}


void loop() {
  // put your main code here, to run repeatedly:
  unsigned long current_millis = millis();

  if (current_millis - previous_milli >= INTERVAL){
    //save time
    previous_millis = current_millis;

    //toggle pin
    led_state = !led_state

    //send state
    digitalWrite(led_pin, led_state)
  }
}


void interrupt_block_detected(){
  block_present = true;
  block_active = digitalRead(ACTIVITY_PIN)
}
