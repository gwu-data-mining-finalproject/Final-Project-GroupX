## This file was added by me as a gui startup routine..
## The path passed into Demo was made relative by Aaron in a later version (see as relative below)
## Note: GUI code in my directory will not run correctly on it's own. Please run shared version instead

# This is intended to be the 'main method' for the larger gui application
# based loosely on https://pythonspot.com/pyqt5-buttons/
import sys
import os
from PyQt5.QtWidgets import QApplication

from Code.gui.DEMO import DEMO

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = DEMO('Data')
    sys.exit(app.exec_())
