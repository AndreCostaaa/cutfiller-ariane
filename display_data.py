
import pandas as pd
import pylab as plt
import matplotlib.image as mpimg
import numpy as np
from scipy import stats
import os
import math
from matplotlib.ticker import PercentFormatter
BASE_DIR = "Csv"
IMAGES_DIR = "Contours"


def get_files_from_dir(dir):
    return [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]


def plot_df(df, file):



    #plt.plot(df["width"].tolist(), df["height"].tolist(), 'ro')
    max_lst = []

    for i in range(len(df["width"].tolist())):
        if i >= len(df["height"].tolist()):
            break
        max_lst.append(max(df["width"].tolist()[i], df["height"].tolist()[i]))

    maximum = max(max_lst)

    plt.hist(max_lst, math.trunc(maximum) - 7, weights=np.ones(len(max_lst)) / len(max_lst))
    plt.xlabel("Width")
    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
    plt.title(file + " " + str(len(df)))
    #plt.axis([-5, 100, -5, 100])


def main():
    files = get_files_from_dir(BASE_DIR)

    for file in files:
        file_path = os.path.join(BASE_DIR, file)
        if "csv" not in os.path.splitext(file)[1]:
            continue
        df = pd.read_csv(file_path)
        file_name_no_ext = os.path.splitext(file)[0]
        img_path = os.path.join(IMAGES_DIR, file_name_no_ext + '.jpeg')

        img = np.uint8(mpimg.imread(img_path))
        df = df[(np.abs(stats.zscore(df)) < 3).all(axis=1)]
        df = df.loc[(df != 0).any(axis=1)]

        fig = plt.figure(figsize=(15, 8))
        subplot = 121
        fig.add_subplot(subplot)
        plot_df(df, file)
        subplot += 1
        fig.add_subplot(subplot)
        plt.title("image")
        plt.imshow(img)
        subplot += 1
        #plt.show()
        plt.savefig(file.split('.')[0] + ".png",)


if __name__ == "__main__":
    main()
