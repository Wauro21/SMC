import sys
import os
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from gui.ConnectionFields import ConnectionFields
from gui.ControlFields import ControlFields
from smc_core.Commands import MICRO_STEPPING_DEFAULT, RESET_DEFAULT, ENABLE_DEFAULT, SLEEP_DEFAULT, MIN_SPEED_RPM, MIN_STEPS
from gui.CommandHistory import CommandHistory

class CentralWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        #Objects 
        self.driver_controls = {
            'comms': None,
            'last_cmd': None,
            'micro_stepping': MICRO_STEPPING_DEFAULT,
            'reset': RESET_DEFAULT,  #Logic low for reset
            'enable': ENABLE_DEFAULT, #Logic low for enable
            'sleep': SLEEP_DEFAULT, # Logic low for sleep
            'direction': False, #counterclock by default
            'halt': False, # Halt flag
            'speed': MIN_SPEED_RPM, # 
            'steps': MIN_STEPS, # Requested number of steps
            'freq': 0, # Frequency for steps
            'freq_counter':0,
        }

        #Widgets
        self.comsWidget = ConnectionFields(self.driver_controls, self)
        self.controlsWidget = ControlFields(self.driver_controls, self)
        self.historyWidget = CommandHistory(self)

        # init routines
        self.controlsWidget.setEnabled(False)

        # Signals and Slots
        self.comsWidget.connect_signal.connect(self.unlockControls)
        self.comsWidget.disconnect_signal.connect(self.lockControls)
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

    def lockControls(self):
        self.controlsWidget.setEnabled(False)

    def unlockControls(self):
        self.controlsWidget.setEnabled(True)


if __name__ == '__main__':
    app = QApplication([])
    widget = CentralWidget()
    widget.show()
    sys.exit(app.exec_())