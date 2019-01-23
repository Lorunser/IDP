#include <SoftwareSerial.h>

String data;

void setup() { 
  Serial.begin(9600); //initialize serial COM at 9600 baudrate
  pinMode(LED_BUILTIN, OUTPUT); //make the LED pin (13) as output
  digitalWrite (LED_BUILTIN, LOW);
}
 
void loop() {
}

void serialEvent(){
  while (Serial.available()){
    data = Serial.readString();
    String message = standard_csv();
    transmit(message);
  }
}

void transmit(String x){
  Serial.println(x);
}

String standard_csv(){
  //{"block_presence", "active", "x_pos", y_pos};
  byte vals[] = {124, 1, 200, 164};
  int n = sizeof(vals);
  return build_csv(vals, n);
}

String build_csv(byte vals[], int n){
  //Build a csv string based off of given vars 
  //"val[0],val[1],val[2]...,val[n-1]"

  String csv_string;
  //int n = sizeof(vals); //each val is 1 byte
  
  for( int i = 0; i < n; i++){
    csv_string = csv_string + String(vals[i]);
    
    if (i < n - 1){
      csv_string = csv_string + ",";
    }
  }

  return csv_string;
}
