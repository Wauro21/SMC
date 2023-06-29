from bitarray import bitarray
from bitarray.util import int2ba, zeros
from enum import Enum

ARDUINO_CLOCK = 16000000
ARDUINO_PRESCALER = 64

class MicroStepping(Enum):
    FULL_STEP = ['Full-Step', bitarray('00 000 000')]
    HALF_STEP = ['Half-Step',bitarray('00 001 000')]
    QUARTER_STEP = ['1/4 Step', bitarray('00 010 000')]
    EIGHT_MICRO = ['1/8 Step', bitarray('00 011 000')]
    SIXTEEN_MICRO = ['1/16 Step', bitarray('00 100 000')]
    THIRTY_TWO_MICRO = ['1/32 Step', bitarray('00 111 000')] # Can be 101 - 110 -

# Defaults for controller
MICRO_STEPPING_DEFAULT = MicroStepping.FULL_STEP # Full step
RESET_DEFAULT = False # not-reseted
ENABLE_DEFAULT = True # Enabled
SLEEP_DEFAULT = True # Disable sleep

# Commands defined by the controller

SETUP_BLANK = { #Works as a template for SETUP and STEP CMD
    'cmd': [
            bitarray('10000000'), 
            bitarray('00000000'), 
            bitarray('00000000')
            ],
    'response_size': 3, # 3 bytes
}

STEP_BLANK = { #Works as a template for SETUP and STEP CMD
    'cmd': [
            bitarray('00000000'), 
            bitarray('00000000'), 
            bitarray('00000000')
            ],
    'response_size': 3, # 3 bytes
}

INFO_CMD = {
    'cmd': [
            bitarray('01000000'), # Command packet
            bitarray('00000000'), # Filler packets
            bitarray('00000000')
            ],
    'response_size': 6, # 3 bytes for : setup + freq_counter
                        # 3 bytes for : step + step_counter
}


def fillBool(values, start=0):
    padded = bitarray('0000 0000')
    n_bits = len(values)

    if(n_bits + start > 8): 
        raise Exception('Padded value needs more than 8 bits from starting poing {}'.format(start))
    
    for i, bool_val in enumerate(values):
        padded[start+i] = bool_val

    return padded






def SETUP_CMD(control_dict):

    # Load template
    k_cmd, k_r_size = SETUP_BLANK

    # Build the CMD: first byte
    cmd = SETUP_BLANK[k_cmd]
    ms = control_dict['micro_stepping'].value[1]
    flags = fillBool([control_dict['reset'], control_dict['enable'], control_dict['sleep']], 5)    
    cmd[0] |= ms
    cmd[0] |= flags

    # Build the CMD: second byte
    freq_counter_bit = convert2Binary(control_dict['freq_counter'],16)
    cmd[1] |= freq_counter_bit[0:8]
    cmd[2] |= freq_counter_bit[8:16]

    setup_cmd = SETUP_BLANK.copy()
    setup_cmd['cmd'] = cmd

    return setup_cmd


def STEP_CMD(control_dict):

    # Load template
    k_cmd, k_r_size = STEP_BLANK

    # Build the CMD: first byte
    cmd = STEP_BLANK[k_cmd]
    flags = fillBool([control_dict['direction']], 7)
    cmd[0] |= flags

    # Build the CMD: second byte
    steps = convert2Binary(control_dict['steps'],16)
    cmd[1] |= steps[0:8]
    cmd[2] |= steps[8:16]

    step_cmd = STEP_BLANK.copy()
    step_cmd['cmd'] = cmd

    return step_cmd




def sendCommand(coms, cmd):
    k_cmd, k_r_size = cmd
    # Write command
    for byte_arr in cmd[k_cmd]:
        coms.write(byte_arr)

    # Wait for automatic reply
    response = coms.read(cmd[k_r_size])
    # Convert the response to bitarrays
    int_response = int(response)
    bin_response = convert2Binary(int_response, cmd[k_r_size]*8)
    
    n_response = []
    pivot = 0
    for i in range(cmd[k_r_size]):
        n_response.append(bin_response[pivot:pivot+8])
        pivot += 8

    n_response.reverse()
    return n_response

def convert2Binary(number, size):
    number_bin = int2ba(number)
    if(len(number_bin) < size):
        number_bin = zeros(size - len(number_bin)) + number_bin

    return number_bin