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
import numpy as np
from time import time
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import scale

import matplotlib.pyplot as plt
import pandas as pd

sample_size = 2000


def bench_k_means(estimator, name, data):
    t0 = time()
    estimator.fit(data)
    print('%-9s\t%.2fs\t%i\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f'
          % (name, (time() - t0), estimator.inertia_,
             metrics.homogeneity_score(labels, estimator.labels_),
             metrics.completeness_score(labels, estimator.labels_),
             metrics.v_measure_score(labels, estimator.labels_),
             metrics.adjusted_rand_score(labels, estimator.labels_),
             metrics.adjusted_mutual_info_score(labels, estimator.labels_),
             metrics.silhouette_score(data, estimator.labels_,
                                      metric='euclidean',
                                      sample_size=sample_size)))


if __name__ == '__main__':
    print('go go go!')
    # data = pd.read_csv('./data/USDA_Food_Database.csv')
    #columns = ['Protein_(g)', 'Carbohydrt_(g)', 'FA_Sat_(g)', 'Zinc_(mg)',
    #           'Iron_(mg)', 'FA_Sat_(g)', 'Zinc_(mg)', 'Water_(g)', 'Iron_(mg)', 'Phosphorus_(mg)', 'Sugar_Tot_(g)']
    # columns = ['Energy_(kcal)', 'Protein_(g)', 'Carbohydrt_(g)', 'Water_(g)', 'FA_Sat_(g)', 'Zinc_(mg)']
    #columns = ['Water_(g)', 'Protein_(g)']
    #columns = ['Energy_(kcal)','Water_(g)']

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
    n_groups = 7
    # n_groups = 5

    labels = t
    print("n_groups: %d, \t n_samples %d, \t n_features %d"
          % (n_groups, n_samples, n_features))

    if benchmark:
        print(82 * '_')
        print('init\t\ttime\tinertia\thomo\tcompl\tv-meas\tARI\tAMI\tsilhouette')

        bench_k_means(KMeans(init='k-means++', n_clusters=n_groups, n_init=10),
                      name="k-means++", data=data)

        bench_k_means(KMeans(init='random', n_clusters=n_groups, n_init=10),
                      name="random", data=data)

        # in this case the seeding of the centers is deterministic, hence we run the
        # kmeans algorithm only once with n_init=1
        pca = PCA(n_components=n_groups).fit(data)
        bench_k_means(KMeans(init=pca.components_, n_clusters=n_groups, n_init=1),
                      name="PCA-based",
                      data=data)
        print(82 * '_')

    reduced_components = 2
    pca = PCA(n_components=reduced_components)
    reduced_data = pca.fit_transform(data)

    most_important = [np.abs(pca.components_[i]).argmax() for i in range(reduced_components)]

    initial_feature_names = reader.columns
    # get the names
    most_important_names = [initial_feature_names[most_important[i]] for i in range(reduced_components)]
    print(most_important_names)

    reduced_data = data
    kmeans = KMeans(init='k-means++', n_clusters=n_groups, n_init=10)
    kmeans.fit(reduced_data)

    # Step size of the mesh. Decrease to increase the quality of the VQ.
    h = .05  # point in the mesh [x_min, x_max]x[y_min, y_max].

    # Plot the decision boundary. For that, we will assign a color to each
    x_min, x_max = reduced_data[:, 0].min() - 1, reduced_data[:, 0].max() + 1
    y_min, y_max = reduced_data[:, 1].min() - 1, reduced_data[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

    # Obtain labels for each point in mesh. Use last trained model.
    Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.figure(1)
    plt.clf()
    plt.imshow(Z, interpolation='nearest',
               extent=(xx.min(), xx.max(), yy.min(), yy.max()),
               cmap=plt.cm.Paired,
               aspect='auto', origin='lower',
               alpha=0.5
               )

    frame = pd.DataFrame(
        {"X Value": reduced_data[:, 0], "Y Value": reduced_data[:, 1], "Category": t})

    groups = frame.groupby("Category")
    for name, group in groups:
        plt.scatter(group["X Value"], group["Y Value"], marker="o", label=name, alpha=0.2, zorder=-5)

    plt.legend()
    # plt.plot(reduced_data[:, 0], reduced_data[:, 1], 'k.', markersize=2)
    # Plot the centroids as a white X
    centroids = kmeans.cluster_centers_
    plt.scatter(centroids[:, 0], centroids[:, 1],
                marker='o', s=100, linewidths=1,
                color='r', zorder=10, alpha=1)
    plt.scatter(centroids[:, 0], centroids[:, 1],
                marker='x', s=80, linewidths=2,
                color='black', zorder=10, alpha=1)

    #plt.title('K-means clustering on the scaled and reduced dataset (PCA)\n')
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.xlabel(most_important_names[0])
    plt.ylabel(most_important_names[1])
    plt.xticks(())
    plt.yticks(())

    plt.show()
