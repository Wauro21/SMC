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


/// @brief Possible values for the bits[7:6] of the arriving control packet. 2 unused
/// states are available for coding (01-10).
enum CMD {
    STEP_CMD=0x0,
    SETUP_CMD=0x3,
};


#endif