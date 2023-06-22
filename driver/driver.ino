// When two commands are sent they overwrite each other -> Add stack or something like that

const byte outPin = 9;
const byte dirPin = 7; // Temporal

int direction = 0;

volatile int interruptCounter = 0;
int steps_to_perform = 0;
int cmd = 0;
void stopTimer1(){
  TCCR1B &= ~((1 << CS12) | (1 << CS11) | (1 << CS10));
  TCNT1 = 0;
}

void startTimer1(){
  TCCR1B |= (0 << CS12) | (1 << CS11) | (1 << CS10);
}

void setup() {  

  Serial.begin(9600);
  // put your setup code here, to run once:
    pinMode(outPin, OUTPUT);
    pinMode(dirPin, OUTPUT);

    // Default direction
    digitalWrite(dirPin, direction);

    // put your main code here, to run repeatedly:
    TCCR1A = 0; // set entire TCCR1A register to 0
    TCCR1B = 0; // same for TCCR1B
    TCCR1C = 0;
    TCNT1  = 0; // initialize counter value to 0
    OCR1A = 15624; // = 16000000 / (64 * 8) - 1 (must be <65536)

    // Register setup
    TCCR1B |= (1 << WGM12);
    TCCR1A |= (0 << COM1A1) | (1 << COM1A0);
    // TCCR1C |= (1 << FOC1A);
    TIMSK1 |= (1 << OCIE1A);
    sei(); // allow interrupts
}

void loop() {

  // Serial data
  if(Serial.available()){
    // Read CMD
    cmd = Serial.parseInt(SKIP_ALL);
    step(1, cmd);
  }
}


void step(int dir, int steps){

  if(steps == 0) {
    Serial.println("not a valid number of steps!");
    return;
  }

  // Set direction
  digitalWrite(dirPin, dir);

  // Calculate necessary values for counter - TO BE IMPLEMENTED 

  // set number of interrupts to count
  steps_to_perform = 2*steps-1;

  // Start timer
  startTimer1();
  Serial.print("STEPPING ");
  Serial.println(steps, DEC);
}



ISR(TIMER1_COMPA_vect){

  if(interruptCounter < steps_to_perform) interruptCounter+=1;
  else{
    stopTimer1();
    interruptCounter = 0;
    Serial.println("END");
  } 
    

}