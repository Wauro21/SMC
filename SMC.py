from PySide2.QtWidgets import QApplication
import os
import sys

from gui.MainWindow import SMC

if __name__ == '__main__':

    app = QApplication([])
    if os.name == 'nt':
            app.setStyle('Fusion')
    window = SMC()
    window.show()
    # For the moment fix the size
    h = window.height()
    w = window.width()
    window.setFixedSize(w, h)
    sys.exit(app.exec_())