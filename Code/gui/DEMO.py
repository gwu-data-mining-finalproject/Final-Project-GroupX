from .generated_gui import Ui_MainWindow
from .NetflixDataPanel import NetflixDataPanel
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow

class DEMO():
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.df = None
        self.ui = Ui_MainWindow()
        self.mw = QMainWindow()
        self.ui.setupUi(self.mw)
        # setup netflix data panel handlers
        self.nd = NetflixDataPanel(self)
        # ultimately pop-up application
        self.mw.show()

