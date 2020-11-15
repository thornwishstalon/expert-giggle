######
# Task example3: Comparison
# In this task you will have to compare different groups in the data. You will have to select three groups and find out the differences among them. Every food type has a keyword assigned which defines its membership to a certain group. The following groups are available in the data:
# These are some suggestions for group comparisons, but you can also select others:
#
# BEEF vs. PORK
# BEEF vs. VEAL
# BEEF vs. VENISON
# BEVERAGES vs. ALCOHOLIC BEVERAGES
# FISH vs. SEAFOOD
# CHICKEN vs. TURKEY
# ANIMAL FAT vs. VEGETABLE FAT
# You may also further filter the groups (e.g., use only cereals in the GRAIN group) if you think that the groups are too heterogeneous, or do in-groups comparisons (e.g., compare food from restaurants against food from fast food chains in the PROCESSED FOOD group). The selected groups do not have to be of the same size.
#
# Statistical analysis: Use the Python functionalities to identify differences.
# Visualization: Use radar charts, or any other visualization you would prefer, to identify differences. Use the Python plotting functionalities, for example pyplot.
#
# Please answer the following questions in the final report:
#
# Which groups did you use and why?
# Describe the differences among the three groups.
# Which Python functionalities did you employ for the statistical analysis and which visualization type did you use?
# Was it easier to do the comparison with statistical analysis only, or by employing visualization?

######

from example1.core import core

import matplotlib.pyplot as plt
import pandas as pd
from math import pi

import re
import numpy as np
from sklearn.preprocessing import scale


def filterfunc(data_array):
    txt = data_array['Name']
    x = re.search(".*MCDONALD'S.*", txt)
    if x:
        return "MCDONALD'S"
    x = re.search(".*WENDY'S.*", txt)
    if x:
        return "WENDY'S"
    x = re.search(".*BURGER KING.*", txt)
    if x:
        return "BURGER KING"
    x = re.search(".*BURGER KING.*", txt)
    if x:
        return "BURGER KING"
    x = re.search(".*TACO BELL.*", txt)
    if x:
        return "TACO BELL"
    x = re.search(".*PIZZA HUT.*", txt)
    if x:
        return "PIZZA HUT"
    x = re.search(".*DOMINO'S.*", txt)
    if x:
        return "DOMINO'S"
    x = re.search(".*SUBWAY.*", txt)
    if x:
        return "SUBWAY"

    return None


if __name__ == '__main__':
    print('go go go!')
    # data = pd.read_csv('./data/USDA_Food_Database.csv')
    columns = ['Energy_(kcal)', 'Protein_(g)', 'Carbohydrt_(g)', 'Water_(g)', 'FA_Sat_(g)', 'Zinc_(mg)',
               'Sugar_Tot_(g)', 'Iron_(mg)', 'Phosphorus_(mg)']
    # columns = ['Energy_(kcal)', 'Protein_(g)', 'Carbohydrt_(g)', 'Water_(g)', 'FA_Sat_(g)', 'Zinc_(mg)']
    # columns = ['Riboflavin_(mg)', 'Energy_(kcal)']

    # columns = ['Energy_(kcal)', 'Carbohydrt_(g)']
    # columns = ['Energy_(kcal)', 'Water_(g)']
    # columns = ['Energy_(kcal)', 'FA_Sat_(g)']
    labels = {
        1: "milk products",
        2: "meats",
        3: "fish etc",
        4: "processed etc",
    }
    merged_groups = {
        'CHEESE': 1,
        'CREAM': 1,
        'MILK': 1,
        'YOGURT': 1,
        'CHICKEN': 2,
        'DUCK': 2,
        'GOAT': 2,
        'VENISON': 2,
        'TURKEY': 2,
        'PORK': 2,
        'GOOSE': 2,
        "MEAT": 2,
        "BEEF": 2,
        "VEAL": 2,
        "LAMB": 2,
        "FISH": 3,
        "SEAFOOD": 3,
        "SNACKS": 4,
        "SWEETS": 4,
        "PROCESSED FOOD": 4,
    }

    # data = reader.read_data('./data/USDA_Food_Database.csv', columns, merged_groups, generate_label=True)
    whitelist = ['PROCESSED FOOD']

    reader = core.Data()
    data, t, read_columns = reader.read_data('./data/USDA_Food_Database.csv', columns=None, groups=None,
                                             generate_label=False, group_whitelist=whitelist, filter_func=filterfunc)
    print(read_columns)
    data = scale(data)
    print('generating plots...')

    dict = {}
    for l in range(0, len(read_columns)):
        dict[read_columns[l]] = data[:, l]
    dict["Category"] = t

    frame = pd.DataFrame(dict)
    groups = frame.groupby("Category")

    N = len(read_columns) - 1
    group_id = 0
    for name, group in groups:
        # values
        fig = plt.figure()
        ax = plt.subplot(polar=True)
        values_data = group.to_numpy()[:, 0:-1]
        c_data = len(values_data)
        plt.title(name + " (n={})".format(c_data))
        for i in range(c_data):
            # print(values)
            values = values_data[i, :]
            values += values[:1]  # repeat first value to close poly
            # calculate angle for each category
            K = len(values)
            # calculate angle for each category
            angles = [n / float(N) * 2 * pi for n in range(N)]
            angles += angles[:1]  # repeat first angle to close poly
            # plot
            plt.polar(angles, values, marker='.', alpha=0.1, color='red')  # lines
            #plt.fill(angles, values, alpha=0.1)  # area

            # xticks
            plt.xticks(angles, read_columns)
            # yticks
            ax.set_rlabel_position(0)  # yticks position
            plt.yticks([-2, 0, 2, 4, 6, 8, 10], color="grey", size=6)
            # plt.ylim(0, 30)

    plt.show()
