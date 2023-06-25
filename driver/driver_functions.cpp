#include "constants.h"
#include "driver_functions.h"

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