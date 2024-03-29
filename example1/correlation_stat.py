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
import numpy as np
import seaborn as sn

def get_redundant_pairs(df):
    '''Get diagonal and lower triangular pairs of correlation matrix'''
    pairs_to_drop = set()
    cols = df.columns
    for i in range(0, df.shape[1]):
        for j in range(0, i+1):
            pairs_to_drop.add((cols[i], cols[j]))
    return pairs_to_drop

def get_top_abs_correlations(df, n=5, ascending=False):
    au_corr = df.corr().unstack()
    labels_to_drop = get_redundant_pairs(df)
    au_corr = au_corr.drop(labels=labels_to_drop).sort_values(ascending=ascending)
    return au_corr[0:n]

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
        "VEGETABLES": 5,
        "FRUITS": 5,
    }

    whitelist = ['VEGETABLES', 'FRUITS', 'MILK', 'CHEESE', 'BEEF', 'CHICKEN',
                 'PORK', 'VEAL', 'MEAT', 'GOOSE', 'LAMB', 'FISH', 'SEAFOOD', 'PROCESSED FOOD']

    reader = core.Data()
    # data = reader.read_data('./data/USDA_Food_Database.csv', columns, merged_groups, generate_label=True)
    data, t, read_columns = reader.read_data('./data/USDA_Food_Database.csv', columns=None, groups=None,
                                             generate_label=False, group_whitelist=None)
    original_data = data
    label_matrix = np.empty([len(read_columns), len(read_columns)], dtype="S20")
    print(len(read_columns))

    for l in range(0, len(read_columns)):
        for k in range(0, len(read_columns)):
            label_matrix[l, k] = ascii(read_columns[l] + "/" + read_columns[k])

    corrcoef = np.corrcoef(data)
    print(np.argwhere(corrcoef > 0.9 ))


    # scaler = MinMaxScaler()
    # data = scaler.fit_transform(data)
    dict = {}
    for l in range(0, len(read_columns)):
        dict[read_columns[l]] = data[:, l]
    #dict["Category"] = t

    frame = pd.DataFrame(dict)

    print("Top positive Correlations")
    print(get_top_abs_correlations(frame, 5, ascending=False))
    print("Top negative Correlations")
    print(get_top_abs_correlations(frame, 5, ascending=True))
    # frame = pd.DataFrame(
    #     {
    #         columns[0]: data[:, 0],  # energy
    #         columns[2]: data[:, 2],  # carbs
    #         columns[6]: data[:, 6],  # sugar
    #         columns[3]: data[:, 3],  # water
    #         columns[4]: data[:, 4],  # salt
    #         columns[5]: data[:, 5],  # zinc
    #         columns[7]: data[:, 7],  # iron
    #         columns[8]: data[:, 8],  # phosphor
    #         columns[1]: data[:, 1],  # protein
    #         "Category": t})

    corrMatrix = frame.corr()


    print(corrMatrix)
    sn.heatmap(corrMatrix, annot=True, linewidth=.5)
    plt.show()

# Water_(g),Energy_(kcal) _ :-0.900532
#  Folic_Acid_(µg) Choline_Tot_ (mg)