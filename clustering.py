import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import os

BASE_DIR = "Csv"
def get_files_from_dir(dir):
    return [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]

def main():
    files = get_files_from_dir(BASE_DIR)

    for file in files:
        file_path = os.path.join(BASE_DIR, file)
        if "csv" not in os.path.splitext(file)[1]:
            continue
        df = pd.read_csv(file_path)
        for k in [3,5,7,9]:
            kmeans = KMeans(n_clusters=k).fit(df)
            centroids = kmeans.cluster_centers_
            print(centroids)

            plt.scatter(df['width'], df['height'])#, c=kmeans.labels_.astype(float), s=50, alpha=0.5)
            plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)
            plt.show()

if __name__ == "__main__":
    main()