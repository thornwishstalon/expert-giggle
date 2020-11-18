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
from kneed import KneeLocator
from sklearn.impute import SimpleImputer

from example1.core import core
import numpy as np
from time import time
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale

import matplotlib.pyplot as plt
import pandas as pd

sample_size = 2000

if __name__ == '__main__':
    print('go go go!')
    # data = pd.read_csv('./data/USDA_Food_Database.csv')
    #columns = ['Protein_(g)', 'Carbohydrt_(g)', 'FA_Sat_(g)', 'Zinc_(mg)',
    #           'Iron_(mg)', 'FA_Sat_(g)', 'Zinc_(mg)', 'Water_(g)', 'Iron_(mg)', 'Phosphorus_(mg)', 'Sugar_Tot_(g)']
    # columns = ['Energy_(kcal)', 'Protein_(g)', 'Carbohydrt_(g)', 'Water_(g)', 'FA_Sat_(g)', 'Zinc_(mg)']
    # columns = [ 'Water_(g)', 'FA_Sat_(g)', 'Zinc_(mg)','Sugar_Tot_(g)']
    #columns = ['Energy_(kcal)', 'Protein_(g)']
    #columns = ['Water_(g)', 'Protein_(g)']

    #columns = ['Folate_Tot_(µg)','Lipid_Tot_(g)']
    # columns = ['Energy_(kcal)', 'Carbohydrt_(g)']
    columns = ['Energy_(kcal)', 'Water_(g)']
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
        "FRUITS": 5,
        "VEGETABLES": 5
    }

    whitelist = [
        'CHEESE',
        'CREAM',
        'MILK',
        'YOGURT',
        'CHICKEN',
        'DUCK',
        'GOAT',
        'VENISON',
        'TURKEY',
        'PORK',
        'GOOSE',
        "MEAT",
        "BEEF",
        "VEAL",
        "LAMB",
        "FISH",
        "SEAFOOD",
        "SNACKS",
        "SWEETS",
        "PROCESSED FOOD",
        "FRUITS",
        "VEGETABLES"
    ]

    reader = core.Data()
    # data = reader.read_data('./data/USDA_Food_Database.csv', columns, merged_groups, generate_label=True)
    # data, t = reader.read_data('./data/USDA_Food_Database.csv', None, None,
    #                        generate_label=True, group_whitelist=whitelist)

    data, t, read_columns = reader.read_data('./data/USDA_Food_Database.csv', columns=columns, groups=None,
                                             generate_label=False, group_whitelist=None)
    imp_mean = SimpleImputer(missing_values=np.nan, strategy='mean')
    imp_mean.fit(data)

    data = imp_mean.transform(data)
    data = scale(data)
    print('generating plots...')

    print(np.unique(t))

    benchmark = False
    # benchmark = True

    n_samples, n_features = data.shape
    # n_groups = len(np.unique(t))
    n_groups = 25
    # n_groups = 5

    print("n_groups: %d, \t n_samples %d, \t n_features %d"
          % (n_groups, n_samples, n_features))

    reduced_components = 2
    pca = PCA(n_components=reduced_components)
    reduced_data = pca.fit_transform(data)

    most_important = [np.abs(pca.components_[i]).argmax() for i in range(reduced_components)]

    initial_feature_names = reader.columns
    # get the names
    most_important_names = [initial_feature_names[most_important[i]] for i in range(reduced_components)]
    print(most_important_names)

    kmeans_kwargs = {
        "n_init": 10,
        "max_iter": 1000,
        "random_state": 42,
        "init": 'k-means++'
    }
    sse = []
    k_range = range(2, 36)
    for k in k_range:
        kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
        kmeans.fit(reduced_data)
        sse.append(kmeans.inertia_)

    kneedle = KneeLocator(
        k_range, sse, curve="convex", direction="decreasing"
    )

    kneedle.plot_knee()

    plt.style.use("fivethirtyeight")
    plt.plot(k_range, sse)
    plt.xticks(k_range)
    plt.xlabel("Number of Clusters")
    plt.ylabel("SSE")

    plt.show()
