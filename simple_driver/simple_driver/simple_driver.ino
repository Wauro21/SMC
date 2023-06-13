void setup() {
  

  // Enable serial port 
  Serial.begin(9600);

}

void loop() {
  
  int cmd = 0;

  // ping pong serial
  if(Serial.available()){    

    cmd = Serial.read();
    switch(cmd){

      case 0x31: 
        Serial.println("Caso 1");
        break;

      default: Serial.println("Not valid");

    }

  }



}
