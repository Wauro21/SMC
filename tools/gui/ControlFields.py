import sys
from PySide2.QtWidgets import QWidget, QComboBox, QPushButton, QLabel, QApplication, QFormLayout, QVBoxLayout, QLineEdit, QHBoxLayout, QSpinBox
from core.Commands import HALT_CMD, SETUP_CMD, MicroStepping, MIN_SPEED_RPM, MAX_SPEED_RPM, MIN_STEPS, MAX_STEPS, STEP_CMD, getFrequency, sendCommand
from gui.Constants import SPEED_SUFFIX
from PySide2.QtCore import Qt, Signal
import copy

__version__ ='0.1'
__author__ = 'maurio.aravena@sansano.usm.cl'


class ControlFields(QWidget):

    # Signals

    def __init__(self,ctrl_dict, parent=None):
        super().__init__(parent)

        # Objects
        self.ctrl = ctrl_dict
        self.freq_flag = False

        #Widgets
        # -> Left column
        self.speed_field = QSpinBox(self)
        self.factor_field = QLineEdit(self)
        self.micro_stepping = QComboBox(self)
        self.steps_field = QSpinBox(self)
        self.send_btn = QPushButton('SEND')

        # -> Center column
        self.up_btn = QPushButton('UP')
        self.down_btn = QPushButton('DOWN')

        # -> Right column
        self.single_up_step_btn = QPushButton('Single UP')
        self.single_down_step_btn = QPushButton('Single DOWN')
        self.halt_btn = QPushButton('HALT')

        #Init routines
        self.initSteps()
        self.initSpeed()
        self.populateMS()

        #Slots and signals
        self.speed_field.valueChanged.connect(self.assignSpeed)
        self.steps_field.valueChanged.connect(self.assignSteps)
        self.micro_stepping.activated.connect(self.assignMode)
        self.send_btn.clicked.connect(self.sendSteps)
        self.halt_btn.clicked.connect(self.haltAction)
        self.up_btn.clicked.connect(self.setDirUp)
        self.down_btn.clicked.connect(self.setDirDown)
        self.single_up_step_btn.clicked.connect(self.singleStepUp)
        self.single_down_step_btn.clicked.connect(self.singleStepDown)

        #Layout
        layout = QHBoxLayout()

        # -> Left column
        left_layout = QFormLayout()
        left_layout.addRow('Speed:',  self.speed_field)
        left_layout.addRow('Factor:', self.factor_field)
        left_layout.addRow('Micro Stepping:', self.micro_stepping)
        left_layout.addRow('Steps:', self.steps_field)
        left_layout.addRow(self.send_btn)

        # -> Center column
        center_layout = QVBoxLayout()
        center_layout.addWidget(self.up_btn)
        center_layout.addWidget(self.down_btn)

        # -> Right Column
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.single_up_step_btn)
        right_layout.addWidget(self.halt_btn)
        right_layout.addWidget(self.single_down_step_btn)

        layout.addLayout(left_layout)
        layout.addLayout(center_layout)
        layout.addLayout(right_layout)

        self.setLayout(layout)

    def singleStepUp(self):
        #Coms
        comms = self.ctrl['comms']

        # Save current values
        direction = self.ctrl['direction']
        steps = self.ctrl['steps']

        # Single mode - Up  -- clockwise
        self.ctrl['direction'] = True
        self.ctrl['steps'] = 1

        # CMD 
        cmd = STEP_CMD(self.ctrl)

        # Send CMD 
        response = sendCommand(comms, cmd)

        # Restore values
        self.ctrl['direction'] = direction
        self.ctrl['steps'] = steps

    def singleStepDown(self):
        #Coms
        comms = self.ctrl['comms']

        # Save current values
        direction = self.ctrl['direction']
        steps = self.ctrl['steps']

        # Single mode - Up  -- clockwise
        self.ctrl['direction'] = False
        self.ctrl['steps'] = 1

        # CMD 
        cmd = STEP_CMD(self.ctrl)

        # Send CMD 
        response = sendCommand(comms, cmd)

        # Restore values
        self.ctrl['direction'] = direction
        self.ctrl['steps'] = steps

        


    def setDirUp(self):
        # Clockwise for up
        self.ctrl['direction'] = True

    def setDirDown(self):
        # CounterClockWise for Down
        self.ctrl['direction'] = False

    def haltAction(self):
        comms = self.ctrl['comms']
        response = sendCommand(comms, HALT_CMD)
        print('Halt response {}'.format(response))

    def initSteps(self):
        self.steps_field.setRange(MIN_STEPS, MAX_STEPS)
        self.steps_field.setValue(self.ctrl['steps'])

    def assignSteps(self):
        steps = self.steps_field.value()
        self.ctrl['steps'] = steps
        self.freq_flag = True


    def initSpeed(self):
        self.speed_field.setRange(MIN_SPEED_RPM, MAX_SPEED_RPM)
        self.speed_field.setSuffix(SPEED_SUFFIX)
        self.speed_field.setValue(self.ctrl['speed'])

    def assignSpeed(self):
        speed = self.speed_field.value()
        self.ctrl['speed'] = speed
        self.freq_flag = True

    def populateMS(self):
        for mode in MicroStepping:
            self.micro_stepping.addItem(mode.value[0])

    def assignMode(self):
        mode = self.micro_stepping.currentText()
        for i in MicroStepping:
            if mode == i.value[0]:
                self.ctrl['micro_stepping'] = i
        self.freq_flag = True


    def sendSteps(self):
        comms = self.ctrl['comms']
        try:
            # Check if freq must be configured with new setup
            if(self.freq_flag):

                # Update freq values on control dict
                _, freq, counter = getFrequency(self.ctrl)
                self.ctrl['freq'] = freq
                self.ctrl['freq_counter'] = counter

                # Inform arduino
                setup_cmd = SETUP_CMD(self.ctrl)
                setup_response = sendCommand(comms, setup_cmd)
                print('Setup response is {}'.format(setup_response))

                self.freq_flag = False

            # Build step CMD 
            step_cmd = STEP_CMD(self.ctrl)
            # send the command and get response from controller
            step_response = sendCommand(comms, step_cmd)
            print('Step response is {}'.format(step_response))

        except Exception as e: 
            print(e)


if __name__ == '__main__':
    app = QApplication([])
    widget = ControlFields(dict())
    widget.show()
    sys.exit(app.exec_())