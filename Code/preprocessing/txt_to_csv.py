import os
import pandas as pd


def default_progress_handler(percentage):
    print('processing text: ' + str(percentage))


def process_to_csv(progress_handler=default_progress_handler):

    path = os.getcwd()[:os.getcwd().find("Code")] + "Data/netflix-prize/"
    f = 0
    for fl in ["combined_data_1.txt", "combined_data_2.txt", "combined_data_3.txt", "combined_data_4.txt"]:
        f += 1
        if f > 1:
            del movie_ids, user_ids, ratings, dates
            del movie_ids_agg, user_ids_aggs, ratings_aggs, dates_aggs
        movie_ids, user_ids, ratings, dates = [], [], [], []
        movie_ids_agg, user_ids_aggs, ratings_aggs, dates_aggs = [], [], [], []
        count = 0
        with open(path + fl, "r") as s:
            data = s.read()
        n_lines = data.count("\n")
        for line in data.split("\n"):
            if line.strip():
                if "," not in line:
                    movie_id = int(line.strip()[:-1])
                    movie_ids += movie_ids_agg
                    user_ids += user_ids_aggs
                    ratings += ratings_aggs
                    dates += dates_aggs
                    movie_ids_agg, user_ids_aggs, ratings_aggs, dates_aggs = [], [], [], []
                else:
                    movie_ids_agg.append(movie_id)
                    rest_data = line.split(",")
                    user_ids_aggs.append(int(rest_data[0]))
                    ratings_aggs.append(int(rest_data[1]))
                    dates_aggs.append(rest_data[2])
                count += 1
                if count % 240000 == 0:
                    progress_handler(count/n_lines*100)
        progress_handler(100)
        del data
        print("Saving to csv")
        df = pd.DataFrame({"movie_id": movie_ids, "user_id": user_ids, "rating": ratings, "date": dates})
        df.to_csv(path + "user_data_" + str(f) + ".csv")
        del df


if __name__ == "__main__":
    process_to_csv()