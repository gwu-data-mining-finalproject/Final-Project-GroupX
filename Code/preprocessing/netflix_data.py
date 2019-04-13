import os
import zipfile


def default_progress_handler(percentage):
    print('decompressing files: ' + str(percentage))


def decompress(data_dir, progress_handler=default_progress_handler):
    files = os.listdir(data_dir)
    for i in range(0, len(files)):
        if files[i].endswith('zip'):
            with zipfile.ZipFile(data_dir + '/' + files[i], "r") as zip_ref:
                zip_ref.extractall(data_dir)
        progress_handler((i+1)/len(files)*100)
