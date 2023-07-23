from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidgetItem, QListWidget
from PySide2.QtGui import QIcon
import datetime

class CommandHistory(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Objects

        # Widgets
        self.history_list = QListWidget(self)

        # init routines
        self.history_list.setMaximumHeight(60)

        # Slots and Signals

        # layout
        layout = QVBoxLayout()
        layout.addWidget(self.history_list)
        self.setLayout(layout)

    def sentCMD(self, array):
        cmd = array['cmd']
        # Unpack 
        temp = ''
        for i in cmd:
            temp += i.to01()+' '

        time_stamp = datetime.datetime.now()
        time_stamp = time_stamp.strftime("%H:%M:%S")
        
        formated_string = '[{}]: {}'.format(time_stamp, temp)
        item = QListWidgetItem(formated_string)
        icon = QIcon('rsrcs/sent_arrow.png')
        item.setIcon(icon)

        self.history_list.addItem(item)
        self.history_list.scrollToBottom()

    def receivedCMD(self, array):
        # Unpack 
        temp = ''
        for i in array:
            temp += i.to01()+' '

        time_stamp = datetime.datetime.now()
        time_stamp = time_stamp.strftime("%H:%M:%S")
        
        formated_string = '[{}]: {}'.format(time_stamp, temp)
        item = QListWidgetItem(formated_string)
        icon = QIcon('rsrcs/received_arrow.png')
        item.setIcon(icon)

        self.history_list.addItem(item)
        self.history_list.scrollToBottom()