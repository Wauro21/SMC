#include <AFMotor.h>

#define STEPS 360/7.5
#define M_PORT 1

AF_Stepper motor(STEPS, M_PORT);

void setup() {

  // put your setup code here, to run once:
  Serial.begin(9600);

  motor.setSpeed(100);  // 10 rpm   

  // motor.step(100, FORWARD, SINGLE);
  motor.release();

}

void loop() {

  int cmd = 0;
  

  // Check if command is available
  // if(Serial.available()){
  //    cmd = Serial.parseInt();

  //    switch(cmd){
      
  //     case 1: motor.step(1, FORWARD, MICROSTEP);

  //     case 2: motor.step(1, BACKWARD, MICROSTEP);

  //     default:{
  //       Serial.println("Not a valid CMD!");
  //     }
  //    }

  //    cmd = 0;
  // }


  // put your main code here, to run repeatedly:
  // motor.step(100, FORWARD, SINGLE); 
  // motor.step(100, BACKWARD, SINGLE); 

  // motor.step(100, FORWARD, DOUBLE); 
  // motor.step(100, BACKWARD, DOUBLE);

  // motor.step(100, FORWARD, INTERLEAVE); 
  // motor.step(100, BACKWARD, INTERLEAVE); 

  motor.step(100, FORWARD, MICROSTEP); 
  motor.step(100, BACKWARD, MICROSTEP); 
}
