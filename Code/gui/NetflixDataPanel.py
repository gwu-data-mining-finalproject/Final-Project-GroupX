from Code.preprocessing.netflix_data import decompress
from PyQt5.QtCore import QThread, pyqtSignal

class NetflixDataPanel(object):
    def __init__(self, demo):
        self.demo = demo
        self.initListeners()

    def initListeners(self):
        self.demo.ui.nd_loadpreprocessed_Button.clicked.connect(self.nd_loadpreprocessed_clicked)
        self.demo.ui.decompressButton.clicked.connect(self.nd_decompress_clicked)
        self.demo.ui.LoadButton.clicked.connect(self.nd_load_clicked)
        self.demo.ui.reduceMoviesButton.clicked.connect(self.nd_reduceMovies_clicked)
        self.demo.ui.reduceUsersButton.clicked.connect(self.nd_reduceUsers_clicked)
        self.demo.ui.reduceSRSWRButton.clicked.connect(self.nd_SRSWR_clicked)
        self.demo.ui.nd_saveButton.clicked.connect(self.nd_save_clicked)

    def nd_loadpreprocessed_clicked(self):
        print('nd loadpreprocessed clicked')

    def nd_decompress_clicked(self):
        print('nd decompress clicked')
        self.decompresser = DecompressionThread(self.demo.data_dir)
        self.decompresser.progressChanged.connect(self.nd_decompress_progress_handler)
        self.decompresser.start()

    def nd_decompress_progress_handler(self, progress):
        self.demo.ui.decompressProgressBar.setValue(progress)
        if progress == 100:
            self.demo.ui.decompressButton.setEnabled(False)
            self.demo.ui.LoadButton.setEnabled(True)

    def nd_load_clicked(self):
        print('nd load clicked')
        self.demo.ui.reduceMoviesButton.setEnabled(True)

    def nd_reduceMovies_clicked(self):
        print('nd reduceMovies clicked')
        self.demo.ui.reduceUsersButton.setEnabled(True)

    def nd_reduceUsers_clicked(self):
        print('nd reduceUsers clicked')
        self.demo.ui.reduceSRSWRButton.setEnabled(True)

    def nd_SRSWR_clicked(self):
        print('nd srswr clicked')
        self.demo.ui.nd_saveButton.setEnabled(True)

    def nd_save_clicked(self):
        print('nd save clicked')


class DecompressionThread(QThread):
    """
    Runs the decompression process
    """
    progressChanged = pyqtSignal(int)

    def __init__(self, data_dir):
        super().__init__()
        self.data_dir = data_dir


    def run(self):
        decompress(self.data_dir, progress_handler=self.progress_handler)

    def progress_handler(self, num):
        self.progressChanged.emit(num)
