import sys
import os
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout
from gui.ConnectionFields import ConnectionFields
from core.Commands import MICRO_STEPPING_DEFAULT, RESET_DEFAULT, ENABLE_DEFAULT, SLEEP_DEFAULT

class CentralWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        #Objects 
        self.driver_controls = {
            'last_cmd': None,
            'micro_stepping': MICRO_STEPPING_DEFAULT,
            'reset': RESET_DEFAULT,  #Logic low for reset
            'enable': ENABLE_DEFAULT, #Logic low for enable
            'sleep': SLEEP_DEFAULT, # Logic low for sleep
            'direction': False, #counterclock by default
            'halt': False, # Halt flag
            'steps': 0, # Requested number of steps
            'freq': 0, # Frequency for steps
            'freq_counter':0,
        }

        #Widgets
        self.comsWidget = ConnectionFields(self.driver_controls, self)

        # Signals and Slots

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.comsWidget)

        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication([])
    widget = CentralWidget()
    widget.show()
    sys.exit(app.exec_())