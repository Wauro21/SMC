#include "constants.h"
#include "driver_functions.h"

// When two commands are sent they overwrite each other -> Add stack or something like that

// Allow for halt flag 
volatile bool halt = false;
volatile int interruptCounter = 0;
volatile States state = IDLE;
int interrupts_to_steps = 0;
int cmd = 0;

// TEMP
byte control_packet = 0x00;

/// Operation controls
byte micro_stepping = 0x00; /// Full step by default
bool reset = false;
bool enable = true; /// Controller is connected by default
bool sleep = false; /// This allows for default holding torque


void setup() {

  /// Setup serial communication for control
  Serial.begin(9600);

  /// Pin mode initialization
  pinMode(outPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(highSwitch, INPUT_PULLUP); /// Interrupt mode
  pinMode(lowSwitch, INPUT_PULLUP);  /// Interrupt mode
  pinMode(ms2Pin, OUTPUT); /// M_2 for microstepping
  pinMode(ms1Pin, OUTPUT); /// M_1 for microstepping
  pinMode(ms0Pin, OUTPUT); /// M_0 for microstepping
  pinMode(resetPin, OUTPUT); /// reset pin for driver board
  pinMode(enablePin, OUTPUT); /// enable pin for driver board
  pinMode(sleepPin, OUTPUT); /// sleep pin for driver board


  /// Default values for I/O
  digitalWrite(outPin, LOW);
  digitalWrite(dirPin, LOW);
  digitalWrite(ms2Pin, LOW);
  digitalWrite(ms1Pin, LOW);
  digitalWrite(ms0Pin, LOW);
  digitalWrite(resetPin, HIGH);
  digitalWrite(enablePin, LOW);
  digitalWrite(sleepPin, HIGH);


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

  ctrlFSM(&state, &control_packet, &micro_stepping, &reset, &enable, &sleep);
}


ISR(TIMER1_COMPA_vect){

  if(interruptCounter < interrupts_to_steps) interruptCounter+=1;
  else{
    stopTimer1();
    interruptCounter = 0;
    Serial.println("END");
  } 
    

}