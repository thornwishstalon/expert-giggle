import csv
from typing import Dict, Any

import numpy as np
from pathlib import Path


class Data:
    groups: Dict[str, str]
    columns: []
    data: []
    labels: {}
    label_counter = 0

    def __init__(self):
        self.columns = []
        self.data = []
        self.labels = {}
        self.label_counter = 0
        self.groups = {}

    def get_label(self, key, generate_label=False):
        if self.groups is not None:
            if key in self.groups:
                return self.groups[key]

        if generate_label is True:
            if key in self.labels:
                return self.labels[key]
            else:
                self.labels[key] = self.label_counter
                self.label_counter += 1
                return self.labels[key]
        else:
            return key

    def read_data(self, filepath, columns=None, groups=None, generate_label=False):
        """read the data file"""
        if groups is not None:
            self.label_counter = len(groups)
            self.groups = groups

        filename = Path(filepath)
        if not filename.exists():
            print("Oops, file doesn't exist!")
            return

        print("reading file ... ")
        with open(filepath, newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            if columns is not None:
                print("columns defined")
                self.columns = columns

            for row in reader:
                data_item = []
                if columns is not None:
                    for column in columns:
                        value = row[column].strip()
                        if is_not_blank(value):
                            data_item.append(float(value))
                        else:
                            data_item.append(float(-1.0))
                else:
                    for key, value in row.items():
                        if key not in ['No', 'Keyword', 'Name'] and value is not value:
                            data_item.append(float(value))

                label = self.get_label(self.get_label(row['Keyword'], generate_label))

                data_item.append(label)
                self.data.append(data_item)

        print("[DONE]")
        return np.array(self.data)


def is_not_blank(myString):
    if myString and myString.strip():
        # myString is not None AND myString is not empty or blank
        return True
    # myString is None OR myString is empty or blank
    return False
