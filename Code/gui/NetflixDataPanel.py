from Code.preprocessing.netflix_data import decompress, load_from_txt
from Code.preprocessing.downsample import reduce_movies, reduce_users, reduce_SRSWR
from PyQt5.QtCore import QThread, pyqtSignal
import os
import pandas as pd


class NetflixDataPanel(object):
    """
    This Class is responsible for handling the NetflixDataPanel interactions
    Ultimately it will update the Demo.df object to contain the downsampled
    dataset we'll be using throughout the other panels in the gui
    """
    def __init__(self, demo):
        self.demo = demo
        self.initListeners()
        self.checkPreviouslyDecompressed()

    def initListeners(self):
        self.demo.ui.decompressButton.clicked.connect(self.nd_decompress_clicked)
        self.demo.ui.LoadButton.clicked.connect(self.nd_load_clicked)
        self.demo.ui.reduceMoviesButton.clicked.connect(self.nd_reduceMovies_clicked)
        self.demo.ui.reduceUsersButton.clicked.connect(self.nd_reduceUsers_clicked)
        self.demo.ui.reduceSRSWRButton.clicked.connect(self.nd_SRSWR_clicked)
        self.demo.ui.nd_saveButton.clicked.connect(self.nd_save_clicked)

    def checkPreviouslyDecompressed(self):
        path = os.path.join(self.demo.data_dir, 'netflix-prize')
        neededfiles = ['combined_data_' + str(x) + '.txt' for x in range(1, 5)]
        files = [os.path.basename(f) for f in os.listdir(path)]
        if set(neededfiles).issubset(files):
            self.demo.ui.LoadButton.setEnabled(True)
            self.demo.ui.decompressProgressBar.setValue(100)
            self.demo.ui.decompressButton.setEnabled(False)

    def nd_decompress_clicked(self):
        print('nd decompress clicked')
        self.demo.ui.decompressButton.setEnabled(False)
        self.decompresser = DecompressionThread(self.demo.data_dir)
        self.decompresser.progressChanged.connect(
            self.nd_decompress_progress_handler)
        self.decompresser.start()

    def nd_decompress_progress_handler(self, progress):
        self.demo.ui.decompressProgressBar.setValue(progress)
        if progress == 100:
            self.demo.ui.decompressButton.setEnabled(False)
            self.demo.ui.LoadButton.setEnabled(True)

    def nd_load_clicked(self):
        print('nd load clicked')
        self.demo.ui.LoadButton.setEnabled(False)
        self.raw_loader = RawDataLoadThread(self.demo.data_dir)
        self.raw_loader.progressChanged.connect(self.nd_load_progress_handler)
        self.raw_loader.resultReady.connect(self.nd_resultHandler)
        self.raw_loader.start()

    def nd_resultHandler(self, result):
        self.demo.df = result

    def nd_load_progress_handler(self, progress):
        self.demo.ui.loadProgressBar.setValue(progress)
        if progress == 100:
            self.demo.ui.LoadButton.setEnabled(False)
            self.demo.ui.reduceMoviesButton.setEnabled(True)

    def nd_reduceMovies_clicked(self):
        print('nd reduceMovies clicked')
        self.demo.ui.reduceMoviesButton.setEnabled(False)
        self.reduceMoviesThread = MovieReducingThread(
            self.demo.df,
            self.demo.ui.nd_movieRatingsCuttoffSpinBox.value())
        self.reduceMoviesThread.progressChanged.connect(
            self.nd_reduceMovies_progress_handler)
        self.reduceMoviesThread.resultReady.connect(self.nd_resultHandler)
        self.reduceMoviesThread.start()

    def nd_reduceMovies_progress_handler(self, progress):
        self.demo.ui.reduceMoviesProgressBar.setValue(progress)
        if progress == 100:
            self.demo.ui.reduceMoviesButton.setEnabled(False)
            self.demo.ui.reduceUsersButton.setEnabled(True)

    def nd_reduceUsers_clicked(self):
        print('nd reduceUsers clicked')
        self.demo.ui.reduceUsersButton.setEnabled(False)
        self.reduceUsersThread = UserReducingThread(
            self.demo.df,
            self.demo.ui.nd_userRatingsCutoffSpinBox.value())
        self.reduceUsersThread.progressChanged.connect(
            self.nd_reduceUsers_progress_handler)
        self.reduceUsersThread.resultReady.connect(self.nd_resultHandler)
        self.reduceUsersThread.start()

    def nd_reduceUsers_progress_handler(self, progress):
        self.demo.ui.reduceUsersProgressBar.setValue(progress)
        if progress == 100:
            self.demo.ui.reduceUsersButton.setEnabled(False)
            self.demo.ui.reduceSRSWRButton.setEnabled(True)

    def nd_SRSWR_clicked(self):
        print('nd srswr clicked')
        self.demo.ui.reduceSRSWRButton.setEnabled(False)
        self.demo.ui.randomSeedSpinBox.setEnabled(False)
        self.srswrThread = SRSWRThread(
            self.demo.ui.randomSeedSpinBox.value(),
            self.demo.df)
        self.srswrThread.progressChanged.connect(self.nd_SRSWR_progress_handler)
        self.srswrThread.resultReady.connect(self.nd_resultHandler)
        self.srswrThread.start()

    def nd_SRSWR_progress_handler(self, progress):
        self.demo.ui.reduceSRSWRProgressBar.setValue(progress)
        if progress == 100:
            self.demo.ui.reduceSRSWRButton.setEnabled(False)
            self.demo.ui.nd_saveButton.setEnabled(True)

    def nd_save_clicked(self):
        print('nd save clicked')
        self.demo.ui.nd_saveButton.setEnabled(False)
        self.saveThread = SaveThread(self.demo.data_dir, self.demo.df)
        self.saveThread.progressChanged.connect(self.nd_save_progress_handler)
        self.saveThread.start()

    def nd_save_progress_handler(self, progress):
        self.demo.ui.nd_saveProgressBar.setValue(progress)
        if progress == 100:
            self.demo.ui.nd_saveButton.setEnabled(False)


class DecompressionThread(QThread):
    """
    Runs the decompression process
    """
    progressChanged = pyqtSignal(int)

    def __init__(self, data_dir):
        super().__init__()
        self.data_dir = data_dir

    def run(self):
        decompress(
            self.data_dir,
            progress_handler=self.progress_handler)

    def progress_handler(self, num):
        self.progressChanged.emit(num)


class RawDataLoadThread(QThread):
    """
    Runs the data load process
    """
    progressChanged = pyqtSignal(int)
    resultReady = pyqtSignal(object)

    def __init__(self, data_dir):
        super().__init__()
        self.data_dir = data_dir
        self.df = None

    def run(self):
        self.df = load_from_txt(
            self.data_dir,
            progress_handler=self.progress_handler)
        print('resulting df shape:', self.df.shape)
        self.progress_handler(100)
        self.resultReady.emit(self.df)

    def progress_handler(self, num):
        self.progressChanged.emit(num)


class MovieReducingThread(QThread):
    """
    Runs the reduction based on reviews per movie operation
    """
    progressChanged = pyqtSignal(int)
    resultReady = pyqtSignal(object)

    def __init__(self, df, ratings_cutoff):
        super().__init__()
        self.df = df
        self.ratings_cutoff = ratings_cutoff

    def run(self):
        self.df = reduce_movies(
            self.df,
            self.ratings_cutoff,
            progress_handler=self.progress_handler)
        print('resulting df shape:', self.df.shape)
        self.progress_handler(100)
        self.resultReady.emit(self.df)

    def progress_handler(self, num):
        self.progressChanged.emit(num)


class UserReducingThread(QThread):
    """
    Runs the reduction based on reviews per user operation
    """
    progressChanged = pyqtSignal(int)
    resultReady = pyqtSignal(object)

    def __init__(self, df, ratings_cutoff):
        super().__init__()
        self.df = df
        self.ratings_cutoff = ratings_cutoff

    def run(self):
        self.df = reduce_users(
            self.df,
            self.ratings_cutoff,
            progress_handler=self.progress_handler)
        print('resulting df shape:', self.df.shape)
        self.progress_handler(100)
        self.resultReady.emit(self.df)

    def progress_handler(self, num):
        self.progressChanged.emit(num)


class SRSWRThread(QThread):
    """
    Runs the SRSWR Operation
    """
    progressChanged = pyqtSignal(int)
    resultReady = pyqtSignal(object)

    def __init__(self, random_state, df):
        super().__init__()
        self.random_state = random_state
        self.df = df

    def run(self):
        self.df = reduce_SRSWR(
            self.df,
            self.random_state,
            progress_handler=self.progress_handler)
        print('resulting df shape:', self.df.shape)
        self.progress_handler(100)
        self.resultReady.emit(self.df)

    def progress_handler(self, num):
        self.progressChanged.emit(num)


class SaveThread(QThread):
    """
    Saves the reduced DataFrame to disk
    """
    progressChanged = pyqtSignal(int)

    def __init__(self, data_dir, df):
        super().__init__()
        self.data_dir = data_dir
        self.df = df

    def run(self):
        self.df.to_csv(
            os.path.join(
                self.data_dir,
                'netflix-prize',
                'downsampled-csv',
                'few_samples.csv'),
            index=False)
        self.progress_handler(100)

    def progress_handler(self, num):
        self.progressChanged.emit(num)