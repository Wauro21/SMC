from PySide2 import QtGui
from PySide2.QtWidgets import QMainWindow, QStatusBar
from gui.CentralWidget import CentralWidget


class SMC(QMainWindow):
    def __init__(self, parent=None):

        super().__init__(parent)

        # objects

        # widgets
        self.SMC_Widget = CentralWidget(self)
        #self.statusBar = QStatusBar(self)

        # init routines
        self.setWindowTitle('Stepper Motor Controller')
        self.setCentralWidget(self.SMC_Widget)
        self.setWindowIcon(QtGui.QIcon('../rsrcs/icon.png'))

        # signals and slots

        # layout