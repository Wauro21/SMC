import sys
import os
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from gui.ConnectionFields import ConnectionFields
from gui.ControlFields import ControlFields
from SMCC.Constants import DEFAULTS, SOFTWARE_LIMITS
from gui.CommandHistory import CommandHistory

class CentralWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        #Objects 
        self.driver_controls = {
            'comms': None,
            'last_cmd': None,
            'micro_stepping': DEFAULTS.MICRO_STEPPING_DEFAULT,
            'reset': DEFAULTS.RESET_DEFAULT.value,  #Logic low for reset
            'enable': DEFAULTS.ENABLE_DEFAULT.value, #Logic low for enable
            'sleep': DEFAULTS.SLEEP_DEFAULT.value, # Logic low for sleep
            'direction': False, #counterclock by default
            'halt': False, # Halt flag
            'speed': SOFTWARE_LIMITS.MIN_SPEED_RPM.value, # 
            'steps': SOFTWARE_LIMITS.MIN_STEPS.value, # Requested number of steps
            'freq': 0, # Frequency for steps
            'freq_counter':0,
            'degrees_per_step':3.75, # Temporal
        }

        #Widgets
        self.comsWidget = ConnectionFields(self.driver_controls, self)
        self.controlsWidget = ControlFields(self.driver_controls, self)
        self.historyWidget = CommandHistory(self)

        # init routines
        self.controlsWidget.setEnabled(False)

        # Signals and Slots
        self.comsWidget.connect_signal.connect(self.unlockControls)
        self.comsWidget.disconnect_signal.connect(self.disconnectRoutine)
        self.controlsWidget.controller_says.connect(self.historyWidget.receivedCMD)
        self.controlsWidget.host_asks.connect(self.historyWidget.sentCMD)

        # Layout
        layout = QVBoxLayout()

        # -> Top row
        layout.addWidget(self.comsWidget)

        # -> Central row
        central_row = QHBoxLayout()
        central_row.addWidget(self.controlsWidget)

        layout.addLayout(central_row)
        layout.addWidget(self.historyWidget)

        self.setLayout(layout)

    def disconnectRoutine(self):
        # Lock controls
        self.lockControls()

        # Restore clean steps from controls
        self.controlsWidget.restoreSteps()


    def lockControls(self):
        self.controlsWidget.setEnabled(False)

    def unlockControls(self):
        self.controlsWidget.setEnabled(True)


if __name__ == '__main__':
    app = QApplication([])
    widget = CentralWidget()
    widget.show()
    sys.exit(app.exec_())