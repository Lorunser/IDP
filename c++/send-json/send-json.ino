#include <SoftwareSerial.h>

String data;

void setup() { 
  Serial.begin(9600); //initialize serial COM at 9600 baudrate
  pinMode(LED_BUILTIN, OUTPUT); //make the LED pin (13) as output
  digitalWrite (LED_BUILTIN, LOW);
  
  Serial.println("Connection Established");
}
 
void loop() {
}

void serialEvent(){
  while (Serial.available()){
    data = Serial.readString();
    String message = standard_json();
    transmit(message);
  }
}

void transmit(String x){
  Serial.println(x);
}

String standard_json(){
  String names[] = {"block", "active"};
  bool vals[] = {true, false};
  return build_json(names, vals);
}

String build_json(String var_names[], bool vals[]){
  //Build a json string based off of given vars 
  String json_string;
  json_string = "{";
  int n = sizeof(vals / vals[0]);
  
  for( int i = 0; i < n; i++){
    json_string = json_string + "'" + var_names[i] + "':'" + vals[i] + "'";
    if (i < n - 1){
      json_string = json_string + ",";
    }
  }

  json_string = json_string + "}";
}
