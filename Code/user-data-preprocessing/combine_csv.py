import os
import pandas as pd


def default_progress_handler(percentage):
    print('reading csvs and merging: ' + str(percentage))


def get_massive_csv(progress_handler=default_progress_handler):

    path = os.getcwd()[:os.getcwd().find("user-data-preprocessing")] + "data-collection/"
    os.chdir(path)

    from netflix_data import *
    os.chdir(path[:path.find("data-collection/")] + "user-data-preprocessing/")
    decompress(os.getcwd()[:os.getcwd().find("Code")] + "Data/netflix-prize/csv-data")

    print("Reading the csv files and combining them")
    df = pd.read_csv(os.getcwd()[:os.getcwd().find("Code")] + "Data/netflix-prize/csv-data/user_data_1.csv",
                    index_col=0)
    progress_handler(25)
    i = 2
    for fl in ["user_data_2.csv", "user_data_3.csv", "user_data_4.csv"]:
        df = pd.concat([df, pd.read_csv(os.getcwd()[:os.getcwd().find("Code")] + 
                                        "Data/netflix-prize/csv-data/" + fl,
                    index_col=0)])
        progress_handler(25*i)
        i += 1

    print("Saving as a massive csv\nNote: You might want to delete the unzipped csv files at this point to save disk space")
    df.to_csv(os.getcwd()[:os.getcwd().find("Code")] + "Data/netflix-prize/complete-csv/all_samples.csv")


if __name__ == "__main__":
    get_massive_csv()
