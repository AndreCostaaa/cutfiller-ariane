import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from scipy import stats
import os
import math
from matplotlib.ticker import PercentFormatter

BASE_DIR = "Csv/Merge"
IMAGES_DIR = "Contours"


def get_files_from_dir(dir):
    return [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]


def plot_df(df, file):
    # plt.plot(df["width"].tolist(), df["height"].tolist(), 'ro')
    max_lst = []

    for i in range(len(df["width_mm"].tolist())):
        if i >= len(df["height_mm"].tolist()):
            break
        max_lst.append(max(df["width_mm"].tolist()[i], df["height_mm"].tolist()[i]))

    maximum = max(max_lst)

    plt.hist(max_lst, math.trunc(maximum) - 7, weights=np.ones(len(max_lst)) / len(max_lst))

    plt.xlabel("Width")
    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
    plt.title(file + " - " + str(len(df)) + " observations")
    plt.axis((0., 100., 0., .1))
    return max_lst


def create_buckets(lst):
    buckets = {}
    for i in lst:
        key = int(i)
        if key in buckets:
            buckets[key].append(i)
        else:
            buckets[key] = [i]
    return buckets


def filter_df(df):
    df = df[(np.abs(stats.zscore(df)) < 3).all(axis=1)]
    df = df.loc[(df != 0).any(axis=1)]
    return df


def max_lst(df):
    res = []

    for k in range(len(df["width_mm"].tolist())):
        if k >= len(df["height_mm"].tolist()):
            break
        res.append(max(df["width_mm"].tolist()[k], df["height_mm"].tolist()[k]))
    return res


def main():
    files = get_files_from_dir(BASE_DIR)
    fig = plt.figure(figsize=(15, 8))
    j = 1
    width = 0.2

    df_ch = filter_df(pd.read_csv(os.path.join(BASE_DIR, "merged_data_ch.csv")))
    df_pl = filter_df(pd.read_csv(os.path.join(BASE_DIR, "merged_data_pl.csv")))
    lst_ch = max_lst(df_ch)
    lst_pl = max_lst(df_pl)

    ch_buckets = create_buckets(lst_ch)
    pl_buckets = create_buckets(lst_pl)

    ch_buckets_percentage = {key: len(l) / len(lst_ch) * 100 for key, l in ch_buckets.items()}
    pl_buckets_percentage = {key: len(l) / len(lst_pl) * 100 for key, l in pl_buckets.items()}

    keys = list(ch_buckets_percentage.keys())
    keys.sort()
    ch_values = [ch_buckets_percentage[x] for x in keys]
    keys = list(pl_buckets_percentage.keys())
    keys.sort()
    pl_values = [pl_buckets_percentage[x] for x in keys]
    print(len(ch_values), len(pl_values))
    r = np.arange(len(keys))
    print(ch_values, pl_values)
    plt.bar(r - width * .5, ch_values, color="g", width=width, edgecolor="black", label="Switzerland")
    plt.bar(r + width * .5, pl_values, color="b", width=width, edgecolor="black", label="Poland")
    row_labels = [f"{key} - {key + 1 - .1}" for key in keys]
    plt.title("Ariane Sticks - Tobacco Branch Length Comparison")
    plt.xticks(r, row_labels)
    plt.ylabel("[%]")
    plt.xlabel("[mm]")
    plt.legend()
    cell_text = [[f"{ch_values[i]:.2f}", f"{pl_values[i]:.2f}"] for i in range(len(ch_values))]

    plt.table(cellText=cell_text,
              rowLabels=[x + " [mm]" for x in row_labels],
              colLabels=["CH [%]", "PL [%]"],
              loc='center right',
              colWidths=[0.1, 0.1])

    fig.tight_layout()
    plt.savefig(os.path.join("plots", "Ariane Sticks - CH PL.png"))
    plt.close(fig)


if __name__ == "__main__":
    main()
