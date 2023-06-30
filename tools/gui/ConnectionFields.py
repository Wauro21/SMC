import sys
from PySide2.QtWidgets import QWidget, QComboBox, QPushButton, QLabel, QApplication, QHBoxLayout
from PySide2.QtCore import Qt, Signal
from gui.MessageBox import ErrorBox, WarningBox
import serial
import serial.tools.list_ports
import time
from core.Commands import INFO_CMD, STEP_CMD, sendCommand, SETUP_CMD
from bitarray.util import deserialize
__version__ ='0.1'
__author__ = 'maurio.aravena@sansano.usm.cl'

# Default values
CONNECTION_STATUS_LABEL = 'Connection status {}'
SERIAL_TIMEOUT = 10.0


class ConnectionFields(QWidget):
    # Signals
    connect_signal = Signal()
    disconnect_signal = Signal()

    def __init__(self, ctrl_dict, parent=None):
        super().__init__(parent)

        # Objects
        self.ctrl_dict = ctrl_dict


        #Widgets
        self.serial_ports = QComboBox()
        self.refresh_btn = QPushButton('Refresh')
        self.connect_btn = QPushButton('Connect')
        self.status_label = QLabel(CONNECTION_STATUS_LABEL.format('Not Connected'))


        #init routines
        self.status_label.setAlignment(Qt.AlignCenter)
        self.SerialList()


        #Signals and slots
        self.refresh_btn.clicked.connect(self.SerialList)
        self.connect_btn.clicked.connect(self.ConnectionHandler)

        # Layout
        layout = QHBoxLayout()
        layout.addWidget(self.serial_ports)
        layout.addWidget(self.refresh_btn)
        layout.addWidget(self.connect_btn)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def SerialList(self):
        # Clear combobox 
        self.serial_ports.clear()

        # Get list of available ports
        show_ports = []
        ports = serial.tools.list_ports.comports()
        for port, _, _ in sorted(ports):
            show_ports.append(port)

        # If no ports found disable connect button
        if(len(show_ports) == 0):
            self.connect_btn.setEnabled(False)
            return
        else:
            # Add ports to combobox
            self.serial_ports.addItems(show_ports)
            # Enable connect button
            self.connect_btn.setEnabled(True)

    def ConnectionHandler(self):
        
        port = self.serial_ports.currentText()
        if not(port):
            # No port is selected 
            warning = WarningBox('No port was found. Try refreshing!')
            warning.exec_()
            return
        
        try:
            if(self.ctrl_dict['comms']):
                self.ctrl_dict['comms'].close()
                self.ctrl_dict['comms'] = None
                self.disconnect_signal.emit()
                connect_btn_txt = 'Connect'
                status_label_txt = 'Not Connected'
                port_list_refresh_enable = True

            else:
                self.ctrl_dict['comms'] = serial.Serial(port, 9600, timeout=SERIAL_TIMEOUT)
                # Wait a second for arduino to reboot after setting up the connection
                time.sleep(5)
                self.ConnectionTest()
                self.connect_signal.emit()
                connect_btn_txt = 'Disconnect'
                status_label_txt = 'Connected'
                port_list_refresh_enable = False

            # Update values of widget
            self.connect_btn.setText(connect_btn_txt)
            self.status_label.setText(status_label_txt)
            self.lock(port_list_refresh_enable)

        except Exception as e:
            self.ctrl_dict['comms'].close()
            self.ctrl_dict['comms'] = None
            self.lock(True)
            show_error = ErrorBox(e, self)
            show_error.exec_()


    def lock(self, key):
        self.serial_ports.setEnabled(key)
        self.refresh_btn.setEnabled(key)


    def ConnectionTest(self):
        # To test the connection write default data to controller and compare response
        # -> Setup
        setup_cmd = SETUP_CMD(self.ctrl_dict)
        print(setup_cmd)
        setup_response = sendCommand(self.ctrl_dict['comms'], setup_cmd)
        print(setup_response)
        if(setup_cmd['cmd'] != setup_response): raise Exception('Controller <SETUP> response does not match sent command. Check connection or reste the board')
        
        # -> Step
        step_cmd = STEP_CMD(self.ctrl_dict)
        print(step_cmd)
        step_response = sendCommand(self.ctrl_dict['comms'], step_cmd)
        print(step_response)
        if(step_cmd['cmd'] != step_response): raise Exception('Controller <STEP> response does not match sent command. Check connection or reste the board')

        return True

if __name__ == '__main__':
    app = QApplication([])
    widget = ConnectionFields()
    widget.show()
    sys.exit(app.exec_())