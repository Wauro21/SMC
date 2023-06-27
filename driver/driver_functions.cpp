#include "constants.h"
#include "driver_functions.h"
#include <Arduino.h>

void confTimer1(int max_counter=15624){

    /// Setup register for timer A - All control register to zero
    TCCR1A = 0; 
    TCCR1B = 0;
    TCCR1C = 0;
    TCNT1  = 0;

    OCR1A = max_counter; /// Assign to the counter register the selected value.

    /// Control register setup
    TCCR1A |= (0 << COM1A1) | (1 << COM1A0); /// Output toggles on match
    TCCR1B |= (1 << WGM12);  /// Set CTC mode of operation.
    TIMSK1 |= (1 << OCIE1A); /// Enables globals interrupts for the timer. 

}

void startTimer1(int prescaler=64){

    uint8_t clock_selection = 0;

    switch(prescaler){
        case 1: 
            clock_selection |= (1 << CS10); /// Prescaler : 1
            break;

        case 8:
            clock_selection |= (1 << CS11); /// Prescaler : 8
            break;

        case 64:
            clock_selection |= (1 << CS11) | (1 << CS10); /// Prescaler : 64
            break;

        case 256:
            clock_selection |= (1 << CS12); /// Prescaler : 256
            break;

        case 1024:
            clock_selection |= (1 << CS12) | (1 << CS10); /// Prescaler : 1024
            break;

        default:
            clock_selection = 0; /// No valid data provided. Clock is disconnected.
    }

    TCCR1B |= clock_selection; 
}


void stopTimer1(){
    TCCR1B &= ~((1 << CS12) | (1 << CS11) | (1 << CS10)); /// Disconnects the clock source.
    TCNT1 = 0; /// Clean the counter. 
}


void step(bool direction, int steps, int* n_interrupts){
    
    // Check if number of steps is valid
    if(steps == 0){
        Serial.println("Not a valid number of steps!"); /// Replace with actual coded message.
        return;
    }
    
    digitalWrite(dirPin, direction); /// Set step direction

    *n_interrupts = 2*steps -1; /// Number of count reach interrupts before completion.

    startTimer1();

    /// Inform via serial what's being done
    Serial.print("Stepping ");
    Serial.println(steps, DEC);   

}

States cmdDecoder(byte serial_in){

    byte cmd = serial_in >> 6;

    switch(cmd){
        case STEP_CMD: return STEP;
        case SETUP_CMD: return SETUP;
        default: return IDLE;
    }
};

void setupDecoder(byte serial_in, byte* m_s, bool* reset, bool* enable, bool* sleep){
    *m_s = (serial_in & 0x38) >> 3;
    *reset = (serial_in & 0x04) >> 2;
    *enable = (serial_in & 0x02) >> 1;
    *sleep = (serial_in & 0x01);

    /// Unpack to bit-like value before assignement
    byte ms2 = (*m_s >> 2);
    byte ms1 = (*m_s >> 2);
    byte ms0 = (*m_s & 0x01);

    /// Apply to pinout
    digitalWrite(ms2Pin, ms2); /// Pin 2 of microstepping controls
    digitalWrite(ms1Pin, ms1); /// Pin 1 of microstepping controls
    digitalWrite(ms0Pin, ms0); /// Pin 0 of microstepping controls
    digitalWrite(resetPin, *reset); 
    digitalWrite(enablePin, *enable);
    digitalWrite(sleepPin, *sleep);
}



void ctrlFSM(volatile States* state, byte* control_packet, byte* m_s, bool* reset, bool* enable, bool* sleep){

    switch(*state){
        case IDLE:{            
            if(Serial.available()){
                *control_packet = Serial.read();
                Serial.print("Readed cmd: ");
                Serial.println(*control_packet, HEX);
                *state = cmdDecoder(*control_packet);
            }
            else *state = IDLE;
            break;
        }

        case SETUP:{
            Serial.println("SETUP-STATE");
            setupDecoder(*control_packet, m_s, reset, enable, sleep);
            *state = IDLE;
            break;
        }

        default:{
            Serial.print("State was");
            Serial.println(*state, HEX);
            *state = IDLE;
        }
    }

}