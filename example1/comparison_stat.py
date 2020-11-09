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
import numpy as np
from sklearn.preprocessing import scale

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

    # whitelist = ['VEGETABLES', 'FRUITS', 'MILK', 'CHEESE', 'BEEF', 'CHICKEN',
    #             'PORK', 'VEAL', 'MEAT', 'GOOSE', 'LAMB', 'FISH', 'SEAFOOD', 'PROCESSED FOOD']
    #whitelist = ['BEEF', 'PORK', 'VENISON', 'VEAL']
    #whitelist = ['CHEESE', 'CREAM', 'MILK', 'YOGURT']
    whitelist = ['FISH', 'SEAFOOD', 'CHICKEN', 'TURKEY']

    reader = core.Data()
    # data = reader.read_data('./data/USDA_Food_Database.csv', columns, merged_groups, generate_label=True)
    data, t, read_columns = reader.read_data('./data/USDA_Food_Database.csv', columns=None, groups=None,
                                             generate_label=False, group_whitelist=whitelist)

    # data = scale(data)
    print(len(data))
    print('generating plots...')
    print(len(read_columns))

    dict = {}
    for l in range(0, len(read_columns)):
        dict[read_columns[l]] = data[:, l]
    dict["Category"] = t

    frame = pd.DataFrame(dict)

    boxplot_data = []
    max_cols = 9
    fig, ax = plt.subplots( 5, max_cols, sharex=True)

    row = -1
    i = 0
    for k in range(0, len(read_columns)):
        frame = pd.DataFrame({"Value": data[:, k], "Category": t})

        if i % max_cols == 0:
            row += 1

        groups = frame.groupby("Category")
        group_data = []
        labels = []
        for name, group in groups:
            labels.append(name)
            group_data.append((group['Value']))

        ax[row][i % max_cols].set_title(read_columns[k])
        ax[row][i % max_cols].boxplot(group_data)

        # plt.close()
        i += 1
    fig.suptitle('(1){0} (2){1} (3){2} (4){3}'.format(labels[0],labels[1],labels[2],labels[3]), fontsize=12)
    #plt.xticks([0, 1, 2], labels)
    plt.show()
