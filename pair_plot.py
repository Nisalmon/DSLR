import csv
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
            if key == "Index" or key == "First Name":
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


def get_valid_values(data, feature_x, feature_y):
    values_x = []
    values_y = []
    houses = []

    for row in data:
        try:
            value_x = float(row[feature_x])
            value_y = float(row[feature_y])
        except ValueError:
            continue

        values_x.append(value_x)
        values_y.append(value_y)
        houses.append(row["Hogwarts House"])
    return values_x, values_y, houses


def main():
    data = load_datasets("./datasets/dataset_train.csv")
    features = get_valid_keys(data)

    fig, axes = plt.subplots(
        len(features),
        len(features),
        figsize=(20, 20)
    )
    colors = {
        "Gryffindor": "red",
        "Slytherin": "green",
        "Ravenclaw": "blue",
        "Hufflepuff": "yellow"
    }

    i = 0
    for features_y in features:
        j = 0
        for features_x in features:
            if j > i:
                axes[i][j].axis("off")
                j += 1
                continue
            values_x, values_y, houses = get_valid_values(data,
                                                          features_x,
                                                          features_y)
            for house in colors:
                house_x = []
                house_y = []
                for x, y, student_house in zip(values_x, values_y, houses):
                    if student_house == house:
                        house_x.append(x)
                        house_y.append(y)
                axes[i][j].scatter(house_x, house_y,
                                   color=colors[house], label=house)
            if i == len(features) - 1:
                axes[i][j].set_xlabel(features_x[:12])
            if j == 0:
                axes[i][j].set_ylabel(features_y[:12], rotation=0)
            j += 1
        i += 1
    plt.show()


if __name__ == "__main__":
    try:
        main()
    except (Exception, KeyboardInterrupt) as e:
        print(e)
