import csv
from utils import Dataset


def load_datasets(path):
    data = []
    with open(path) as f:
        for row in csv.DictReader(f):
            data.append(row)
    return data


def print_headers(row_to_print):
    first_column_width = 8

    headers = []
    for key in row_to_print:
        if key == "Index":
            continue

        try:
            float(row_to_print[key])
        except ValueError:
            continue

        if len(key) > 12:
            headers.append(key[:12] + "...")
        else:
            headers.append(key)

    width = 15

    print(" " * first_column_width, end="")
    for header in headers:
        print(f"{header:>{width}}", end=" ")
    print()


def print_table(row_to_print, data, data_name):
    first_column_width = 8
    width = 15

    print(f"{data_name:<{first_column_width}}", end="")
    for key in row_to_print:
        if key == "Index":
            continue

        try:
            float(row_to_print[key])
        except ValueError:
            continue

        print(f"{round(data[key], 2):>{width}}", end=" ")
    print()


def main():
    dataset = Dataset()
    data = load_datasets("./datasets/dataset_test.csv")
    dataset.set_all(data)
    print_headers(data[0])
    print_table(data[0], dataset.Count, "Count")
    print_table(data[0], dataset.Mean, "Mean")
    print_table(data[0], dataset.Std, "Std")
    print_table(data[0], dataset.Min, "Min")
    print_table(data[0], dataset.Quarter, "25%")
    print_table(data[0], dataset.Half, "50%")
    print_table(data[0], dataset.Three_Quarter, "75%")
    print_table(data[0], dataset.Max, "Max")


if __name__ == "__main__":
    main()
