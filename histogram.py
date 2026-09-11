from utils import Dataset
import csv


def load_datasets(path):
    data = []
    with open(path) as f:
        for row in csv.DictReader(f):
            data.append(row)
    return data


def get_lowest_std(data: dict, keys: dict):
    valid_keys = get_valid_keys(keys)
    values = []
    for key in valid_keys:
        values.append((key, data[key]))
    current_lowest = values[0][1]
    lowest, second, third = "", "", ""
    for courses in values:
        if courses[1] < current_lowest:
            third = second
            second = lowest
            lowest = courses[0]
            current_lowest = courses[1]
    return lowest, second, third


def get_valid_keys(data: list):
    valid_keys = []
    for row in data:
        for key, values in row.items():
            if key == "Index":
                continue
            valid = False
            try:
                # if key == "First Name":
                #     print(values)
                _ = float(values)
                valid = True
            except ValueError:
                continue
            if valid and key not in valid_keys:
                valid_keys.append(key)
    return valid_keys


def main():
    dataset = Dataset()
    data = load_datasets("./datasets/dataset_test.csv")
    dataset.set_all(data)
    lowest, second, third = get_lowest_std(dataset.Std, data)
    print("Here is the top 3 courses with the most homogeneous score "
          "distribution between all four houses.\n\n")
    print(f"In third place:\n\t{third}. with a derivation "
          f"of {dataset.Std[third]}")
    print(f"In second place:\n\t{second}. with a derivation "
          f"of {dataset.Std[second]}")
    print(f"And in first place:\n\t{lowest}. with a derivation "
          f"of {dataset.Std[lowest]}")


if __name__ == "__main__":
    main()
