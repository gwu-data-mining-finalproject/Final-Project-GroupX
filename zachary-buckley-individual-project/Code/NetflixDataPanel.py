from Code.preprocessing.netflix_data import decompress, load_from_txt
from PyQt5.QtCore import QThread, pyqtSignal
import os
from sklearn.model_selection import train_test_split
import pandas as pd

## This is a snapshot of NetflixDataPanelCode as I was originally figuring out the pattern to use for
## progress bar and separate threads

## Thread objects each have 2 QT Signals:
##   - resultReady: used to pass finished df updates back to the main thread
##   - progressChanged: used to pass incremental process updates back to gui's progress bars
class NetflixDataPanel(object):
    def __init__(self, demo):
        self.demo = demo
        self.initListeners()
        self.checkPreviouslyDecompressed()

    def initListeners(self):
        self.demo.ui.nd_loadpreprocessed_Button.clicked.connect(self.nd_loadpreprocessed_clicked)
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

    def checkPreviouslyDownsampled(self):
        path = os.path.join(self.demo.data_dir, 'netflix-prize')
        files = [os.path.basename(f) for f in os.listdir(path)]
        if 'downsample.csv' in files:
            self.demo.ui.nd_loadpreprocessed_Button.setEnabled(True)

    def nd_loadpreprocessed_clicked(self):
        print('nd loadpreprocessed clicked')
        self.loader = LoadThread(self.demo.data_dir)
        self.loader.progressChanged.connect(self.nd_loadpreprocessed_progress_handler)
        self.loader.resultReady.connect(self.nd_resultHandler)
        self.loader.start()

    def nd_loadpreprocessed_progress_handler(self, progress):
        self.demo.ui.nd_loadpreprocessed_ProgressBar.setValue(progress)
        if progress == 100:
            self.demo.ui.nd_loadpreprocessed_Button.setEnabled(False)
            self.demo.ui.decompressButton.setEnabled(False)
            self.demo.ui.LoadButton.setEnabled(False)
            self.demo.ui.reduceMoviesButton.setEnabled(False)
            self.demo.ui.reduceUsersButton.setEnabled(False)
            self.demo.ui.reduceSRSWRButton.setEnabled(False)
            self.demo.ui.nd_saveButton.setEnabled(False)
            self.demo.ui.decompressProgressBar.setValue(100)
            self.demo.ui.loadProgressBar.setValue(100)
            self.demo.ui.reduceMoviesProgressBar.setValue(100)
            self.demo.ui.reduceUsersProgressBar.setValue(100)
            self.demo.ui.reduceSRSWRProgressBar.setValue(100)
            self.demo.ui.nd_saveProgressBar.setValue(100)

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
        self.reduceMoviesThread = MovieReducingThread(self.demo.df)
        self.reduceMoviesThread.progressChanged.connect(self.nd_reduceMovies_progress_handler)
        self.reduceMoviesThread.resultReady.connect(self.nd_resultHandler)
        self.reduceMoviesThread.start()

    def nd_reduceMovies_progress_handler(self, progress):
        self.demo.ui.reduceMoviesProgressBar.setValue(progress)
        if progress == 100:
            self.demo.ui.reduceMoviesButton.setEnabled(False)
            self.demo.ui.reduceUsersButton.setEnabled(True)

    def nd_reduceUsers_clicked(self):
        print('nd reduceUsers clicked')
        self.reduceUsersThread = UserReducingThread(self.demo.df)
        self.reduceUsersThread.progressChanged.connect(self.nd_reduceUsers_progress_handler)
        self.reduceUsersThread.resultReady.connect(self.nd_resultHandler)
        self.reduceUsersThread.start()

    def nd_reduceUsers_progress_handler(self, progress):
        self.demo.ui.reduceUsersProgressBar.setValue(progress)
        if progress == 100:
            self.demo.ui.reduceUsersButton.setEnabled(False)
            self.demo.ui.reduceSRSWRButton.setEnabled(True)

    def nd_SRSWR_clicked(self):
        print('nd srswr clicked')
        self.demo.ui.randomSeedSpinBox.setEnabled(False)
        self.srswrThread = SRSWRThread(self.demo.ui.randomSeedSpinBox.value(), self.demo.df)
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
        self.saveThread = SaveThread(self.demo.data_dir, self.demo.df)
        self.saveThread.progressChanged.connect(self.nd_save_progress_handler)
        self.saveThread.start()

    def nd_save_progress_handler(self, progress):
        self.demo.ui.nd_saveProgressBar.setValue(progress)
        if progress == 100:
            self.demo.ui.nd_saveButton.setEnabled(False)
            self.demo.ui.nd_loadpreprocessed_Button.setEnabled(False)
            self.demo.ui.nd_loadpreprocessed_ProgressBar.setValue(100)

# based on decompress routing in netflix_data.py written by me
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

# based on optimized (by me) version of parsing code Pedro originally wrote
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
        self.df = load_from_txt(self.data_dir, progress_handler=self.progress_handler)
        self.resultReady.emit(self.df)

    def progress_handler(self, num):
        self.progressChanged.emit(num)

# Movie reducing thread based on early code Pedro wrote in downsample.py
class MovieReducingThread(QThread):
    """
    Runs the reduction based on reviews per movie operation
    """
    progressChanged = pyqtSignal(int)
    resultReady = pyqtSignal(object)

    def __init__(self, df):
        super().__init__()
        self.df = df

    def run(self):
        print(self.df.head())
        print(self.df.columns)
        tmp = self.df[['movie_id', 'rating']].groupby('movie_id').\
            count().rename(columns={'rating': 'count'}).sort_values('count')
        self.progress_handler(33)
        tmp = tmp[tmp['count'] > 214]
        self.progress_handler(66)
        self.df = self.df[self.df.movie_id.isin(tmp.index)]
        self.progress_handler(100)

    def progress_handler(self, num):
        self.progressChanged.emit(num)

## User reducing thread base on early code Pedro wrote in downsample.py
class UserReducingThread(QThread):
    """
    Runs the reduction based on reviews per user operation
    """
    progressChanged = pyqtSignal(int)
    resultReady = pyqtSignal(object)

    def __init__(self, df):
        super().__init__()
        self.df = df

    def run(self):
        tmp = self.df[['user_id', 'rating']].groupby('user_id').\
            count().rename(columns={'rating': 'count'}).sort_values('count')
        self.progress_handler(33)
        tmp = tmp[tmp['count'] > 30]
        self.progress_handler(66)
        self.df = self.df[self.df.user_id.isin(tmp.index)]
        self.progress_handler(100)

    def progress_handler(self, num):
        self.progressChanged.emit(num)

## Thread object created based on early SRSWR code Pedro wrote in downsample.py
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
        print(self.df['user_id'].unique().shape)
        #print(self.df.shape)
        _, small_sample_of_users = train_test_split(self.df['user_id'].unique(),
                                                    test_size=0.005,
                                                    random_state=self.random_state)
        print(self.df.shape)
        print(small_sample_of_users.shape)
        self.progress_handler(50)
        self.df = self.df[self.df['user_id'].isin(small_sample_of_users)]
        print(self.df.shape)
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
        self.df.to_csv(os.path.join(self.data_dir, 'netflix-prize', 'downsampled.csv'), index=False)
        self.progress_handler(100)

    def progress_handler(self, num):
        self.progressChanged.emit(num)


class LoadThread(QThread):
    """
    Loads previously reduced data, stored in csv format.
    Provides faster way around re-reducing data each time.
    """
    progressChanged = pyqtSignal(int)
    resultReady = pyqtSignal(object)

    def __init__(self, data_dir):
        super().__init__()
        self.data_dir = data_dir
        self.df = None

    def run(self):
        self.df = pd.read_csv(os.path.join(self.data_dir, 'netflix-prize', 'downsampled.csv'))
        self.progress_handler(100)
        self.resultReady.emit(self.df)

    def progress_handler(self, num):
        self.progressChanged.emit(num)
