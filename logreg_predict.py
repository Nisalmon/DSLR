import csv
from utils import House, Houses
import sys
import math


def load_weights(path):
    data = []
    with open(path) as f:
        for row in csv.DictReader(f):
            data.append(row)
    return data


def load_data(path):
    data = []
    with open(path) as f:
        for row in csv.DictReader(f):
            data.append(row)
    return data


def get_houses(house_data):
    houses = {}
    for house in house_data:
        houses.update({house["House"]: House(
            weights=eval(house["Weights"]),
            means=eval(house["Means"]),
            stds=eval(house["Stds"])
        )})
    return houses
    

def sigmoid(z):
    return 1 / (1 + math.exp(-z))


def predict(X, weights):
    predictions = []
    for row in X:
        z = weights[0]
        for j in range(len(row)):
            z += weights[j + 1] * row[j]
        predictions.append(sigmoid(z))
    return predictions


def get_x(data, features):
    X = []
    valid_data = []

    for row in data:
        values = []
        valid = True
        for feature in features:
            try:
                values.append(float(row[feature]))
            except Exception:
                valid = False
                break
        if valid:
            X.append(values)
            valid_data.append(row)
    return X, valid_data


def normalize(X, means, stds):
    normalized_X = []

    for row in X:
        normalized_row = []

        for j, value in enumerate(row):
            normalized_value = (value - means[j]) / stds[j]
            normalized_row.append(normalized_value)

        normalized_X.append(normalized_row)

    return normalized_X


def create_houses_predictions(X, models):
    predictions = []

    for row in X:
        best_house = None
        best_probability = -1

        for name, values in models.items():
            probability = predict([row], values.weights)[0]

            if probability > best_probability:
                best_probability = probability
                best_house = name

        predictions.append(best_house)

    return predictions


def save_predictions(data, predictions, path="houses.csv"):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)

        writer.writerow([
            "Index",
            "Hogwarts House"
        ])

        for row, house in zip(data, predictions):
            writer.writerow([
                row["Index"],
                house
            ])


def get_values(houses):
    means = None
    stds = None
    for _, values in houses.items():
        means = values.means
        stds = values.stds
        break
    return means, stds


def main():
    if len(sys.argv) != 3:
        print("Erreur. Pour lancer ce programme veillez a lui remettre le fichier genere par le programme 'logreg_train.py' et le fichier suivant 'dataset_test.csv'")
        return
    all_weights = load_weights(sys.argv[1])
    data = load_data(sys.argv[2])
    FEATURES = [
        "Ancient Runes",
        "Herbology"
    ]
    HOUSES = get_houses(all_weights)
    X, valid_data = get_x(data, FEATURES)
    means, stds = get_values(HOUSES)
    X = normalize(X, means, stds)
    predictions = create_houses_predictions(
        X,
        HOUSES
    )
    save_predictions(
        valid_data,
        predictions
    )


if __name__ == "__main__":
    try:
        main()
    except (Exception, KeyboardInterrupt) as e:
        print(e)
