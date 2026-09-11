import sys
import csv
import math


def load_datasets(path):
    data = []
    with open(path) as f:
        for row in csv.DictReader(f):
            data.append(row)
    return data


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


def get_y(data):
    y = []
    for row in data:
        y.append(row["Hogwarts House"])
    return y


def create_binary_y(y, house):
    binary_y = []
    for value in y:
        if value == house:
            binary_y.append(1)
        else:
            binary_y.append(0)
    return binary_y


def normalize(X):
    means = []
    stds = []

    for j in range(len(X[0])):
        column = [row[j] for row in X]
        means.append(sum(column) / len(column))

    for j in range(len(X[0])):
        column = [row[j] for row in X]

        variance = sum(
            (value - means[j]) ** 2
            for value in column
        ) / len(column)

        stds.append(variance ** 0.5)

    normalized_X = []

    for row in X:
        normalized_row = []

        for j, value in enumerate(row):
            normalized_value = (value - means[j]) / stds[j]
            normalized_row.append(normalized_value)

        normalized_X.append(normalized_row)

    return normalized_X, means, stds


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


def compute_loss(y, predictions):
    total_loss = 0
    low_nb = 1*10**-15

    for i in range(len(y)):
        p = predictions[i]
        p = max(min(p, 1 - low_nb), low_nb)
        total_loss += (
            y[i] * math.log(p) + (1 - y[i]) * math.log(1 - p)
        )
    return -total_loss / len(y)


def compute_gradient(X, y, predictions):
    gradients = [0] * (len(X[0]) + 1)

    for i in range(len(X)):
        error = predictions[i] - y[i]

        gradients[0] += error

        for j in range(len(X[i])):
            gradients[j + 1] += error * X[i][j]

    for j in range(len(gradients)):
        gradients[j] /= len(X)

    return gradients


def gradient_descent(X, y, learning_rate=0.01, iterations=1000):
    weights = [0] * (len(X[0]) + 1)

    for _ in range(iterations):
        predictions = predict(X, weights)

        gradients = compute_gradient(
            X,
            y,
            predictions
        )

        for j in range(len(weights)):
            weights[j] -= learning_rate * gradients[j]

    return weights


def train_models(X, y, houses):
    models = {}

    for house in houses:
        binary_y = create_binary_y(y, house)

        weights = gradient_descent(
            X,
            binary_y
        )

        models[house] = weights

    return models


def save_weights(models, means, stds, path="weights.csv"):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)

        writer.writerow(["House", "Weights", "Means", "Stds"])

        for house, weights in models.items():
            writer.writerow([
                house,
                weights,
                means,
                stds
            ])


def main(argv):
    if len(argv) != 2:
        print("Erreur. Pour lancer ce programme veillez "
              "a ne donner qu'un parametre.")
        return
    FEATURES = [
        "Ancient Runes",
        "Herbology"
    ]
    data = load_datasets(sys.argv[1])
    houses = [
        "Gryffindor",
        "Hufflepuff",
        "Ravenclaw",
        "Slytherin"
    ]
    X, valid_data = get_x(data, FEATURES)
    X, means, stds = normalize(X)
    y = get_y(valid_data)
    models = train_models(X, y, houses)
    save_weights(models, means, stds)


if __name__ == "__main__":
    main(sys.argv)
