//libraries
#include <SoftwareSerial.h>

//global consts
const long INTERVAL = 1000;
const byte LED_PIN = LED_BUILTIN;
const byte BLOCK_PIN = 2;
const byte ACTIVITY_PIN = 3;

//global vars
unsigned long current_millis = 0;
unsigned long previous_millis = 0;
int led_state = LOW;

//volatile vars to change in ISRs
volatile bool block_present = false;
volatile bool block_active = false;


void setup() {
  //open serial connection
  Serial.begin(9600);
  
  //declare pin types
  pinMode(LED_PIN, OUTPUT);
  pinMode(BLOCK_PIN, INPUT_PULLUP);
  pinMode(ACTIVITY_PIN, INPUT);

  //attach interrupts
  attachInterrupt(digitalPinToInterrupt(BLOCK_PIN), interrupt_block_detected, CHANGE);
}


void loop() {
  // put your main code here, to run repeatedly:
  current_millis = millis();

  if (current_millis - previous_millis >= INTERVAL){
    //save time
    previous_millis = current_millis;

    //toggle pin
    led_state = !led_state;

    //send state
    digitalWrite(LED_PIN, led_state);
  }
}


void interrupt_block_detected(){
  //block_present = true;
  //block_active = digitalRead(ACTIVITY_PIN);
  //digitalWrite(LED_PIN, HIGH);
  Serial.println("DETECTED");
  
}
