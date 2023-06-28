#ifndef CONSTANTS_H
#define CONSTANTS_H

#include <Arduino.h>

/// @brief Pin I/O definitions
const byte outPin = 9; /// Step pin to the stepper controller.
const byte dirPin = 6; /// Direction pin to the stepper controller.
const byte highSwitch = 2; /// High limit switch pin.
const byte lowSwitch = 3; /// Low limit switch pin.
const byte ms2Pin = 11; /// Microstepping mode pin 2
const byte ms1Pin = 12; /// Microstepping mode pin 1
const byte ms0Pin = 13; /// Microstepping mode pin 0
const byte resetPin = 8; /// Reset pin for driver board. Logic low for reset.
const byte enablePin = 10; /// Enable pin for driver board. Logic low for enable. 
const byte sleepPin = 7; /// Sleep pin for driver board. Logic low for sleep.

/// @brief Describes the possible states that the controller can be
enum States {
    IDLE,
    SETUP,
    STEP,
    L_SWITCH,
    C_ERROR,
};


enum Serial_States {
    SERIAL_IDLE, 
    FIRST_BYTE,
    WAIT_1, 
    SECOND_BYTE,
    WAIT_2,
    THIRD_BYTE,
    DONE, 
    HALT
};

/// @brief Possible values for the bits[7:6] of the arriving control packet. 2 unused
/// states are available for coding (01-10).
enum CMD {
    STEP_CMD=0x00,
    INFO_CMD=0x01,
    SETUP_CMD=0x02,
    HALT_CMD = 0x03,
};

struct ARDUINO_CONTROLS{
    CMD command;
    byte micro_stepping;
    bool reset;
    bool enable;
    bool sleep;
    bool direction;
    bool halt;
    int steps;
    int interrupt_to_steps;
    int freq_counter;

    // Base constructor 
    ARDUINO_CONTROLS(){
        command = INFO_CMD;
        micro_stepping = 0x00;/// Full step by default
        reset = false;
        enable = true; /// Controller is connected by default
        sleep = false; /// This allows for default holding torque
        direction = false;
        halt = false;
        steps = 0;
        interrupt_to_steps = 0;
        freq_counter = 0;
        this->toCtrlPins();
    };

    void toCtrlPins(){
        byte ms2 = ((this->micro_stepping) >> 2);
        byte ms1 = ((this->micro_stepping) >> 2);
        byte ms0 = ((this->micro_stepping) & 0x01);
        /// Apply to pinout
        digitalWrite(ms2Pin, ms2); /// Pin 2 of microstepping controls
        digitalWrite(ms1Pin, ms1); /// Pin 1 of microstepping controls
        digitalWrite(ms0Pin, ms0); /// Pin 0 of microstepping controls
        digitalWrite(resetPin, this->reset); 
        digitalWrite(enablePin, this->enable);
        digitalWrite(sleepPin, this->sleep);
    }

    void toStepPins(){
        digitalWrite(dirPin, this->direction);        
    }

    int packageControls(){
        byte to_send_a = 0x00;
        byte to_send_b = 0x00;
        to_send_a |= (0x02 << 6) | (this->micro_stepping << 3) | (this->reset << 2) | (this-> enable << 1) | (this->sleep);
        to_send_b |= this->direction;
        return ((to_send_a << 8) | (to_send_b));
    }

};

#endif