import os
import zipfile


def default_progress_handler(percentage):
    print('decompressing files: ' + str(percentage))


def decompress(data_dir, progress_handler=default_progress_handler):
    netflix_path = os.path.join(data_dir, 'netflix-prize')
    print('netflix path: ', netflix_path)
    files = os.listdir(netflix_path)
    for i in range(0, len(files)):
        if files[i].endswith('zip') and files[i].startswith('combined'):
            with zipfile.ZipFile(os.path.join(netflix_path, files[i]), "r") as zip_ref:
                zip_ref.extractall(netflix_path)
        progress_handler(int((i+1)/len(files)*100))
    progress_handler(100)
