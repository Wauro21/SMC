#include "constants.h"
#include "driver_functions.h"

// When two commands are sent they overwrite each other -> Add stack or something like that

// Allow for halt flag 
volatile bool halt = false;
volatile int interruptCounter = 0;
int interrupts_to_steps = 0;
int cmd = 0;


void setup() {

  /// Setup serial communication for control
  Serial.begin(9600);

  /// Pin mode initialization
  pinMode(outPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(highSwitch, INPUT_PULLUP); /// Interrupt mode
  pinMode(lowSwitch, INPUT_PULLUP);  /// Interrupt mode

  /// Default values for I/O
  digitalWrite(outPin, LOW);
  digitalWrite(dirPin, LOW);

  /// Attach intterupt to switch pins
  attachInterrupt(digitalPinToInterrupt(highSwitch), limitHalt, LOW);
  attachInterrupt(digitalPinToInterrupt(lowSwitch), limitHalt, LOW);

  confTimer1(); /// Setup timer configuration
  sei(); /// allow interrupts
}

void limitHalt(){
  Serial.println("I should really stop here...");

}

void loop() {

  // Serial data
  if(Serial.available()){
    // Read CMD
    cmd = Serial.parseInt(SKIP_ALL);
    step(false, cmd, &interrupts_to_steps);
  }
}


ISR(TIMER1_COMPA_vect){

  if(interruptCounter < interrupts_to_steps) interruptCounter+=1;
  else{
    stopTimer1();
    interruptCounter = 0;
    Serial.println("END");
  } 
    

}