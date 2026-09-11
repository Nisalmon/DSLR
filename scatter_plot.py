import csv
from utils import Dataset
import matplotlib.pyplot as plt


def load_datasets(path):
    data = []
    with open(path) as f:
        for row in csv.DictReader(f):
            data.append(row)
    return data


def get_valid_keys(data: list):
    valid_keys = []
    for row in data:
        for key, values in row.items():
            if key == "Index":
                continue
            valid = False
            try:
                _ = float(values)
                valid = True
            except ValueError:
                continue
            if valid and key not in valid_keys:
                valid_keys.append(key)
    return valid_keys


def correlation(x, y):
    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)

    numerator = 0
    sum_x = 0
    sum_y = 0

    for i in range(len(x)):
        diff_x = x[i] - mean_x
        diff_y = y[i] - mean_y

        numerator += diff_x * diff_y
        sum_x += diff_x ** 2
        sum_y += diff_y ** 2

    denominator = (sum_x * sum_y)**0.5

    return numerator / denominator


def get_valid_values(values_a, values_b):
    valid_a = []
    valid_b = []

    for value_a, value_b in zip(values_a, values_b):
        try:
            value_a = float(value_a)
            value_b = float(value_b)
        except ValueError:
            continue

        valid_a.append(value_a)
        valid_b.append(value_b)

    return valid_a, valid_b


def compare(features, data):
    correlation_result = []
    for i in range(len(features)):
        if i+1 == len(features):
            break
        feature_a = features[i]
        feature_b = features[i + 1]
        values_a = []
        values_b = []
        for row in data:
            values_a.append(row[feature_a])
            values_b.append(row[feature_b])
        values_a, values_b = get_valid_values(values_a, values_b)
        correlation_result.append((feature_a, feature_b,
                                   correlation(values_a, values_b)))
    return correlation_result


def get_highest_score(correlations: list[tuple]):
    curr = correlations[0]
    for corr in correlations:
        if abs(corr[2]) > abs(curr[2]):
            curr = corr
    return curr


def main():
    dataset = Dataset()
    data = load_datasets("./datasets/dataset_train.csv")
    features = get_valid_keys(data)
    dataset.set_all(data)
    corr = compare(features, data)
    highest_corr = get_highest_score(corr)
    values_a = []
    values_b = []
    for row in data:
        values_a.append(row[highest_corr[0]])
        values_b.append(row[highest_corr[1]])
    values_a, values_b = get_valid_values(values_a, values_b)
    plt.scatter(values_a, values_b)
    plt.xlabel(highest_corr[0])
    plt.ylabel(highest_corr[1])
    plt.title(f"{highest_corr[0]}-{highest_corr[1]}")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    try:
        main()
    except (Exception, KeyboardInterrupt) as e:
        print(e)
