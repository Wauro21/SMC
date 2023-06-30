import sys
import os
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from gui.ConnectionFields import ConnectionFields
from gui.ControlFields import ControlFields
from core.Commands import MICRO_STEPPING_DEFAULT, RESET_DEFAULT, ENABLE_DEFAULT, SLEEP_DEFAULT, MIN_SPEED_RPM, MIN_STEPS

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

        # Signals and Slots

        # Layout
        layout = QVBoxLayout()

        # -> Top row
        layout.addWidget(self.comsWidget)

        # -> Central row
        central_row = QHBoxLayout()
        central_row.addWidget(self.controlsWidget)

        layout.addLayout(central_row)

        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication([])
    widget = CentralWidget()
    widget.show()
    sys.exit(app.exec_())