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

if __name__ == '__main__':
    print('go go go!')
    # data = pd.read_csv('./data/USDA_Food_Database.csv')
    columns = ['Energy_(kcal)', 'Protein_(g)']
    # columns = ['Energy_(kcal)', 'Carbohydrt_(g)']
    #columns = ['Energy_(kcal)', 'Water_(g)']
    # columns = ['Energy_(kcal)', 'FA_Sat_(g)']
    labels = {
        1: "milk products",
        2: "meats",
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
    }

    reader = core.Data()
    #data = reader.read_data('./data/USDA_Food_Database.csv', columns, merged_groups, generate_label=True)
    data = reader.read_data('./data/USDA_Food_Database.csv', columns, None, generate_label=True)
    frame = pd.DataFrame({"X Value": data[:, 0], "Y Value": data[:, 1], "Category": data[:, 2]})

    groups = frame.groupby("Category")
    for name, group in groups:
        plt.plot(group["X Value"], group["Y Value"], marker="o", linestyle="", label=name)
    plt.legend()

    # Plot
    # plt.scatter(data.data[example1:100, 0], data.data[example1:100, example1], alpha=0.5)
    # plt.scatter(data.data[example1:1000, 0], data.data[example1:1000, example1], alpha=0.5)
    # plt.scatter(data.data[:, 0], data.data[:, example1], alpha=0.5)

    plt.show()
