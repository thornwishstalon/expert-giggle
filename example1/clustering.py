######
# Task example1: Clustering
# In this task you will have to cluster the food types according to two nutrition elements. The following combinations are suggestions, you can also find your own preferred combination of nutrition elements:
#
# Energy_(kcal) and Protein_(g)
# Energy_(kcal) and Carbohydrt_(g)
# Energy_(kcal) and Water_(g)
# Energy_(kcal) and FA_Sat_(g)
# Water_(g) and Zinc_(mg)
# Water_(g) and Iron_(mg)
# Water_(g) and Phosphorus_(mg)
# Water_(g) and Sugar_(g)
# Sugar_(g) and Protein_(mg)
#
# Statistical analysis: Use the Python functionalities, for example sklearn.cluster, to cluster the data.
# Visualization: Use a 2D scatter plot, or any other visualization you would prefer, to identify the clusters. Use the Python plotting functionalities, for example pyplot.
#
# Please answer the following questions in the final report:
#
# Why did you select the specific combination of nutrition elements?
# How did you find out how many clusters need to be formed to describe the data best?
# Which Python functionality did you use for the statistical analysis and which visualization type did you employ?
# Which aspects of the task (e.g., identifying the number of clusters) where easier to solve by using statistical analysis, and which by using visualization?
######

from example1.core import core

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import scale

if __name__ == '__main__':
    print('go go go!')
    # data = pd.read_csv('./data/USDA_Food_Database.csv')
    columns = ['Energy_(kcal)', 'Protein_(g)', 'Carbohydrt_(g)', 'Water_(g)', 'FA_Sat_(g)', 'Zinc_(mg)',
               'Sugar_Tot_(g)','Iron_(mg)', 'Phosphorus_(mg)']
    # columns = ['Energy_(kcal)', 'Protein_(g)', 'Carbohydrt_(g)', 'Water_(g)', 'FA_Sat_(g)', 'Zinc_(mg)']
    #columns = ['Riboflavin_(mg)', 'Energy_(kcal)']

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

    whitelist = ['VEGETABLES', 'FRUITS', 'MILK', 'CHEESE', 'BEEF', 'CHICKEN',
                 'PORK', 'VEAL', 'MEAT', 'GOOSE', 'LAMB', 'FISH', 'SEAFOOD', 'PROCESSED FOOD']

    reader = core.Data()
    # data = reader.read_data('./data/USDA_Food_Database.csv', columns, merged_groups, generate_label=True)
    data, t, read_columns = reader.read_data('./data/USDA_Food_Database.csv', columns=columns, groups=None,
                               generate_label=True, group_whitelist=None)

    #data = scale(data)
    print(t)
    print('generating plots...')

    for k in range(0, len(columns)):
        for l in range(0, len(columns)):

            if k < l and not k == l:
                frame = pd.DataFrame(
                    {"X Value": data[:, k], "Y Value": data[:, l], "Category": t})

                plt.figure()
                groups = frame.groupby("Category")
                for name, group in groups:
                    plt.scatter(group["X Value"], group["Y Value"], marker="o", label=name, alpha=0.2)

                plt.title("{0} v.s. {1}".format(columns[k], columns[l]))
                plt.legend()

    # Plot
    # plt.scatter(data.data[example1:100, 0], data.data[example1:100, example1], alpha=0.5)
    # plt.scatter(data.data[example1:1000, 0], data.data[example1:1000, example1], alpha=0.5)
    # plt.scatter(data.data[:, 0], data.data[:, example1], alpha=0.5)

    plt.show()
