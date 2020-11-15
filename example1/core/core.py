import csv
from typing import Dict, Any

import numpy as np
import pandas
from pathlib import Path


class Data:
    groups: Dict[str, str]
    columns: []
    data: []
    t: []
    labels: {}
    label_counter = 0

    def __init__(self):
        self.columns = []
        self.data = []
        self.t = []
        self.labels = {}
        self.label_counter = 0
        self.groups = {}
        self.header = []

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


    def read_data_v2(self, filepath, columns):
        return pandas.read_csv( filepath, names=columns)


    def read_data(self, filepath, columns=None, groups=None, generate_label=False, group_whitelist=None,
                  filter_func=None):
        """read the data file"""
        if groups is not None:
            self.label_counter = len(groups)
            self.groups = groups

        filename = Path(filepath)
        if not filename.exists():
            print("Oops, file doesn't exist!")
            return

        print("reading file ... ")
        with open(filepath, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)

            if columns is not None:
                print("columns defined")
                self.columns = columns
                store_columns = False
            else:
                store_columns = True

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

                        if key not in ['No', 'Keyword', 'Name']:
                            if store_columns:
                                self.columns.append(key)

                            if is_not_blank(value):
                                try:
                                    value = float(value)
                                    data_item.append(value)
                                except ValueError:
                                    pass
                            else:
                                data_item.append(np.nan)
                store_columns = False
                label = self.get_label(self.get_label(row['Keyword'], generate_label))

                if group_whitelist and not row['Keyword'] in group_whitelist:
                    # skip entry
                    continue

                if filter_func:
                    label = filter_func(row)
                    if label is None:
                        continue

                self.t.append(label)
                self.data.append(data_item)

        print("[DONE]")
        return np.array(self.data), np.array(self.t), self.columns


def is_not_blank(myString):
    if myString and myString.strip():
        # myString is not None AND myString is not empty or blank
        return True
    # myString is None OR myString is empty or blank
    return False
