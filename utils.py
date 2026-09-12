class Dataset:
    def __init__(self):
        self.Data = []
        self.Count = {}
        self.Mean = {}
        self.Std = {}
        self.Max = {}
        self.Quarter = {}
        self.Half = {}
        self.Three_Quarter = {}
        self.Min = {}

    def set_data(self, data):
        for row in data:
            for key, value in row.items():
                index = 0
                add = False
                for elem in self.Data:
                    if key in elem.keys():
                        self.Data[index][key].append(value)
                        add = True
                    index += 1
                if not add:
                    self.Data.append({key: [value]})

    def set_count(self):
        index = 0
        for row in self.Data:
            for key, _ in row.items():
                self.Count.update({key: len(self.Data[index][key])-1})
            index += 1

    def set_mean(self):
        index = 0
        for row in self.Data:
            for key, _ in row.items():
                valid_number = self._get_valid_numbers(self.Data[index][key])
                self.Mean.update({key: sum(valid_number, 0) /
                                  len(self.Data[index][key])})
            index += 1

    def set_std(self):
        index = 0
        for row in self.Data:
            for key, _ in row.items():
                mean = self.Mean[key]
                valid_numbers = self._get_valid_numbers(self.Data[index][key])
                for i in range(len(valid_numbers)):
                    valid_numbers[i] = (valid_numbers[i] - mean)**2
                std = (sum(valid_numbers, 0)/len(self.Data[index][key]))**0.5
                self.Std.update({key: std})
            index += 1

    def set_min(self):
        for row in self.Data:
            for key, values in row.items():
                self.Min.update({key: self.get_lowest(values)})

    def set_max(self):
        for row in self.Data:
            for key, values in row.items():
                self.Max.update({key: self.get_highest(values)})

    def set_quarter(self):
        for row in self.Data:
            for key, values in row.items():
                numbers = sorted(self._get_valid_numbers(values))
                self.Quarter.update({key: numbers[int(len(values)*0.25)]})

    def set_half(self):
        for row in self.Data:
            for key, values in row.items():
                numbers = sorted(self._get_valid_numbers(values))
                self.Half.update({key: numbers[int(len(values)*0.5)]})

    def set_three_quarter(self):
        for row in self.Data:
            for key, values in row.items():
                numbers = sorted(self._get_valid_numbers(values))
                self.Three_Quarter.update({key:
                                           numbers[int(len(values)*0.75)]})

    def set_all(self, data):
        self.set_data(data)
        self.set_count()
        self.set_mean()
        self.set_std()
        self.set_min()
        self.set_quarter()
        self.set_half()
        self.set_three_quarter()
        self.set_max()

    def _get_valid_numbers(self, lst):
        valid_numbers = []
        for nb in lst:
            try:
                valid_numbers.append(float(nb))
            except Exception:
                valid_numbers.append(0)
        return valid_numbers

    def get_lowest(self, values):
        lowest = values[0]
        for nb in values:
            try:
                if nb == '':
                    continue
                if float(nb) < float(lowest):
                    lowest = nb
            except (ValueError):
                return 0
        if lowest == '':
            return 0
        return float(lowest)

    def get_highest(self, values):
        highest = values[0]
        for nb in values:
            try:
                if nb == '':
                    continue
                if float(nb) > float(highest):
                    highest = nb
            except (ValueError):
                return 0
        if highest == '':
            return 0
        return float(highest)


class Houses:
    def __init__(self, gryff, huffle, raven, slyth):
        self.Gryffindor = gryff
        self.Hufflepuff = huffle
        self.Ravenclaw = raven
        self.Slytherin = slyth


class House:
    def __init__(self, weights, means, stds):
        self.weights = weights
        self.means = means
        self.stds = stds
