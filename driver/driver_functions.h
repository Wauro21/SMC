#ifndef DRIVER_FUNCTIONS_H
#define DRIVER_FUNCTIONS_H

#include <Arduino.h>


/// @brief confTimer1 setups the 16-bit timer 1 register of the arduino Uno.
/// Operation is set to CTC and enables interrupt masking of the counter.
/// This only setups mode of operation, clock selection is left unconnected. 
/// @param max_counter corresponds to the max number that the counter can
/// reach before starts over. It's related with the desired frequency 
/// according to the equation : f_out = f_clk / (2 * N * (1 + max_counter))
void confTimer1(int max_counter=15624);


/// @brief Starts the timer 1 by connecting the clock source, with its corresponding
/// prescaler, to the counter logic. 
/// @param prescaler prescaler for the clock source. valid values are: 1, 8, 64, 256, 1024.
void startTimer1(int prescaler=64);

/// @brief Stops the timer 1 (and by extension the output), by disconecting the clock source.
void stopTimer1();

/// @brief Performs the desired steps in the selected direction
/// @param direction Indicates if clockwise operation (true) or counterclockwise (false)
/// @param steps Number of steps to perform
/// @param n_interrupts The address of the number of interrupts counter. This is used to
/// estimate the number of steps already taken before stopping the counter.
void step(bool direction, int steps, int* n_interrupts);


void ctrlFSM(volatile States* state, byte* control_packet, byte* m_s, bool* reset, bool* enable, bool* sleep);

bool serialFSM(volatile States* state, volatile Serial_States* serial_state, byte* f_byte, byte* s_byte, byte* t_byte);

void serialDecoder(ARDUINO_CONTROLS* ctrl, byte f_byte, byte s_byte, byte t_byte);

#endif