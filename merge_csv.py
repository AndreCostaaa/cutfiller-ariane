import os
from pprint import pprint

FOLDER = "Csv"
OUTPUT_FOLDER = "Csv/Merge"


def read_csv(file_path):
    return parse_csv(read_lines(file_path))


def parse_csv(lines, sep=",", start_line=0):
    headers = lines[start_line].split(sep)
    return [
        {headers[i]: line.split(sep)[i] for i in range(len(headers))}
        for line in lines[start_line + 1:]
        if len(line.split(sep)) == len(headers)
    ]


def read_lines(file_path):
    return [line.rstrip() for line in open(file_path)]


def add_img_and_location(entry, file):
    return entry
    entry["img"] = file.split('.')[0]
    entry["img_index"] = index(file)
    entry["location"] = "PL" if index(file) >= 14 else "CH"
    return entry


def index(file):
    return int(file.split('.')[0][3:])


def output_csv(data: list[dict], file_path):
    if len(data) < 1:
        raise RuntimeError("Not enough data to export csv file")
    headers = list(data[0].keys())

    with open(file_path, "w+") as f:
        f.write(",".join(headers))
        f.write('\n')
        for x in data:
            f.write(",".join([str(x) for x in x.values()]))
            f.write('\n')


def main():
    files = [x for x in os.listdir(FOLDER) if x.lower().endswith('.csv')]
    ch_data = []
    pl_data = []
    for file in files:
        file_path = os.path.join(FOLDER, file)
        if index(file) >= 14:
            pl_data += [add_img_and_location(x, file) for x in read_csv(file_path)]
        else:
            ch_data += [add_img_and_location(x, file) for x in read_csv(file_path)]

    #ch_data.sort(key=lambda x: int(x["img_index"]))
    #pl_data.sort(key=lambda x: int(x["img_index"]))
    output_csv(ch_data, os.path.join(OUTPUT_FOLDER, "merged_data_ch.csv"))
    output_csv(pl_data, os.path.join(OUTPUT_FOLDER, "merged_data_pl.csv"))


if __name__ == "__main__":
    main()
