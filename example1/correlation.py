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
from sklearn.preprocessing import normalize
from sklearn.preprocessing import MinMaxScaler
from matplotlib import cm

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
        "VEGETABLES": 5,
        "FRUITS": 5,
    }

    whitelist = ['VEGETABLES', 'FRUITS', 'MILK', 'CHEESE', 'BEEF', 'CHICKEN',
                 'PORK', 'VEAL', 'MEAT', 'GOOSE', 'LAMB', 'FISH', 'SEAFOOD', 'PROCESSED FOOD']

    reader = core.Data()
    # data = reader.read_data('./data/USDA_Food_Database.csv', columns, merged_groups, generate_label=True)
    data, t = reader.read_data('./data/USDA_Food_Database.csv', columns=columns, groups=None,
                               generate_label=False, group_whitelist=None)

    scaler = MinMaxScaler()
    data = scaler.fit_transform(data)
    frame = pd.DataFrame(
        {
         columns[0]: data[:, 0], # energy
         columns[2]: data[:, 2], # carbs
         columns[6]: data[:, 6], # sugar
         columns[3]: data[:, 3], # water
         columns[4]: data[:, 4], # salt
         columns[5]: data[:, 5], # zinc
         columns[7]: data[:, 7], # iron
         columns[8]: data[:, 8], # phosphor
         columns[1]: data[:, 1], # protein
         "Category": t})


    pd.plotting.parallel_coordinates(frame, "Category", colormap=cm.get_cmap('tab20'))
    #pd.plotting.parallel_coordinates(frame, "Category", colormap=None)
    plt.show()


