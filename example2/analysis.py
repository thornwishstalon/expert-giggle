import pandas as pd
import sqlite3 as sql
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from bioinfokit.analys import stat, get_data
import scipy.stats as stats
import os.path

pd.set_option('display.max_rows', 1500)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sql.connect(db_file)
    except sql.Error as e:
        print(e)

    return conn


def createCSVFile():
    print("Hello World!")
    connection = create_connection('switrs.sqlite')
    query = '''SELECT * FROM collisions where collision_date IS NOT NULL and latitude is not null and longitude is not null and road_surface is not null and road_condition_1 is not null and lighting is not null '''

    collisions = pd.read_sql_query(query, connection, parse_dates=["collision_date"])
    connection.close()

    print(collisions.head())
    collisions.to_csv('input/collisions.csv', index=False)


def main4(options):
    # createCSVFile()
    wrapData(options, False)
    # plot stuff
    data = STATSlookIntoCauses(options)

    data = data.set_index('pcf_violation_category')
    data = data.groupby(['pcf_violation_category'])
    max_cols = 2
    fig, axs = plt.subplots(3, max_cols, sharex=True, sharey=True)
    labels = {1: "wrong side of road", 2: "automobile right of way", 3: "improper turning", 4: "speeding",
              5: "traffic signals and signs", 6: "dui"}
    row = -1
    i = 0
    for k in range(1, 7):
        if i % max_cols == 0:
            row += 1
        axs[row][i % max_cols].hist(x=data.get_group(labels[k])['hour'], bins=25)
        axs[row][i % max_cols].set_title(labels[k])
        axs[row][i % max_cols].axvline(6, color='black', linestyle='--')
        axs[row][i % max_cols].axvline(9, color='black', linestyle='--')
        axs[row][i % max_cols].axvline(15, color='black', linestyle='--')
        axs[row][i % max_cols].axvline(18, color='black', linestyle='--')
        axs[row][i % max_cols].axvline(21, color='black', linestyle='--')
        axs[row][i % max_cols].axhline(1000, color='black', linestyle='--')
        axs[row][i % max_cols].axhline(2000, color='black', linestyle='--')
        axs[row][i % max_cols].axhline(3000, color='black', linestyle='--')
        axs[row][i % max_cols].axhline(4000, color='black', linestyle='--')
        i += 1

    P = np.empty([6, 6])
    list = []

    for k in range(1, 7):
        list_item = []
        for l in range(1, 7):
            if l < k or l == k:
                P[k - 1][l - 1] = np.NaN
                continue

            print('k:%s, l:%s' % (k, l))
            stat, p = stats.mannwhitneyu(data.get_group(labels[k])['hour'], data.get_group(labels[l])['hour'])
            print('stat={:.3f}, p={:.5f}'.format(stat, p))
            P[k - 1][l - 1] = p
            list_item.append('stat={:.3f}, p={:.5f}'.format(stat, p))
            if (p < 0.05):
                pass
        list.append(list_item)
    print(list)

    plt.figure()
    sns.heatmap(P, vmin=0, vmax=0.05)


def main3(options):
    # createCSVFile()
    wrapData(options, False)
    # plot stuff
    data = STATSlookIntoCauses(options)
    plt.figure()
    plt.hist(x=data['hour'], bins=25)
    plt.title('at what hour, does bicycle accidents occur?')

    data.set_index(['month'], inplace=True)
    data = data.groupby(['month'])

    print(data.get_group(1).head())
    max_cols = 3
    fig, axs = plt.subplots(4, max_cols, sharex=True, sharey=True)
    labels = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August",
              9: "September", 10: "October", 11: "November", 12: "December"}
    row = -1
    i = 0
    for k in range(1, 13):
        if i % max_cols == 0:
            row += 1
        axs[row][i % max_cols].hist(x=data.get_group(k)['hour'], bins=25)
        axs[row][i % max_cols].set_title(labels[k])
        axs[row][i % max_cols].axvline(6, color='black', linestyle='--')
        axs[row][i % max_cols].axvline(9, color='black', linestyle='--')
        axs[row][i % max_cols].axvline(15, color='black', linestyle='--')
        axs[row][i % max_cols].axvline(18, color='black', linestyle='--')
        axs[row][i % max_cols].axvline(21, color='black', linestyle='--')
        axs[row][i % max_cols].axhline(1000, color='black', linestyle='--')
        axs[row][i % max_cols].axhline(1500, color='black', linestyle='--')
        i += 1

    P = np.empty([12, 12])
    list = []

    for k in range(1, 13):
        list_item = []
        for l in range(1, 13):
            if l < k or l == k:
                P[k - 1][l - 1] = np.NaN
                continue

            print('k:%s, l:%s' % (k, l))
            stat, p = stats.ttest_ind(data.get_group(k)['hour'], data.get_group(l)['hour'], equal_var=False)
            print('stat={:.3f}, p={:.5f}'.format(stat, p))
            P[k - 1][l - 1] = p
            list_item.append('stat={:.3f}, p={:.5f}'.format(stat, p))
            if (p < 0.05):
                pass
        list.append(list_item)
    print(list)

    plt.figure()
    sns.heatmap(P, vmin=0, vmax=0.1)


def main2(options):
    # createCSVFile()
    wrapData(options, False)
    # plot stuff
    data = lookIntoMissingPosition(options)

    plt.figure()
    plt.hist(x=data['deaths'], bins='auto')
    plt.title('killed victims')
    plt.figure()
    plt.hist(x=data['injured'], bins='auto')
    plt.title('injuries')
    print(data.head())
    plt.figure()
    plotMissingPositions(data)
    data = STATSlookIntoMissingPosition(options)
    doStats(data)


def main(options):
    # createCSVFile()
    wrapData(options)
    # plot stuff
    causes = lookIntoCauses(options)
    print(causes)
    plotCausesTrend(causes)


def plotMissingPositions(data):
    sns.lineplot(data=data, x="year", y='deaths', hue="has_spatial_data")
    plt.title('killed victims total')
    plt.figure()
    sns.lineplot(data=data, x="year", y='injured', hue="has_spatial_data")
    plt.title('injured victims total')


def lookIntoMissingPosition(options):
    yearly_causes = []
    keys = []

    for item in options:
        collisions = pd.read_csv('input/{}_collisions.csv'.format(item['label']), parse_dates=["collision_date"],
                                 dtype={
                                     'killed_victims': 'Int64',
                                     'injured_victims': 'Int64',
                                     'bicyclist_injured_count': 'Int64',
                                     'bicyclist_killed_count': 'Int64',
                                     'bicycle_collision': 'Int64',
                                     'party_count': 'Int64',
                                     'pcf_violation_code': 'str',
                                     'pcf_violation_category': 'str',
                                     'latitude': 'float',
                                     'longitude': 'float'
                                 })
        collisions['killed_victims'].fillna(0)
        collisions['injured_victims'].fillna(0)

        collisions['has_spatial_data'] = collisions['latitude']
        collisions['has_spatial_data'] = collisions['has_spatial_data'].apply(lambda x: 'n' if pd.isnull(x) else 'y')

        data = (collisions.groupby(
            ['has_spatial_data'])
                .agg(count=('case_id', 'count'),
                     bicycle_deaths=('bicyclist_killed_count', 'sum'),
                     bicycle_injured=('bicyclist_injured_count', 'sum'),
                     deaths=('killed_victims', 'sum'),
                     deaths_avg=('killed_victims', np.mean),
                     deaths_sd=('killed_victims', np.var),
                     injured=('injured_victims', 'sum'),
                     injured_avg=('injured_victims', np.mean),
                     injured_sd=('injured_victims', np.var),
                     # sum_engagement=('Engagement', 'sum'),
                     )
                .reset_index()
                )

        data['year'] = item['label']

        yearly_causes.append(data.reset_index().set_index(['year', 'has_spatial_data']))
        keys.append(item['label'])

    return pd.concat(yearly_causes)


def doStats(data):
    # data = data.groupby('has_spatial_data')
    a = data.query('has_spatial_data == "y"')
    b = data.query('has_spatial_data == "n"')

    print(a.head())
    n1, n2 = len(a), len(b)
    print('lenght %s, %s' % (n1, n2))
    stat, p = stats.kruskal(a['killed_victims'], b['killed_victims'], equal_var=True)
    print('killed:  stat=%.3f, p=%.5f' % (stat, p))
    if p > 0.05:
        print('Probably the same distribution')
    else:
        print('Probably different distributions')

    stat, p = stats.kruskal(a['injured_victims'], b['injured_victims'], equal_var=True)
    print('injury: stat=%.3f, p=%.5f' % (stat, p))
    if p > 0.05:
        print('Probably the same distribution')
    else:
        print('Probably different distributions')


def STATSlookIntoCauses(options):
    yearly_causes = []
    keys = []

    for item in options:
        collisions = pd.read_csv('input/{}_collisions.csv'.format(item['label']), parse_dates=["collision_date"],
                                 dtype={
                                     'case_id': 'str',
                                     'killed_victims': 'Int64',
                                     'injured_victims': 'Int64',
                                     'bicyclist_injured_count': 'Int64',
                                     'bicyclist_killed_count': 'Int64',
                                     'bicycle_collision': 'Int64',
                                     'party_count': 'Int64',
                                     'pcf_violation_code': 'str',
                                     'pcf_violation_category': 'str',
                                     'latitude': 'float',
                                     'longitude': 'float'
                                 })
        collisions.dropna(subset=['collision_date', 'collision_time'], inplace=True)
        collisions['killed_victims'] = collisions['killed_victims'].fillna(0)
        collisions['injured_victims'] = collisions['injured_victims'].fillna(0)

        collisions['has_spatial_data'] = collisions['latitude']
        collisions['has_spatial_data'] = collisions['has_spatial_data'].apply(lambda x: 'n' if pd.isnull(x) else 'y')
        collisions['hour'] = pd.DatetimeIndex(collisions['collision_time']).hour
        collisions['month'] = pd.DatetimeIndex(collisions['collision_date']).month
        # using dictionary to convert specific columns
        convert_dict = {'hour': int,
                        'month': int
                        }
        collisions = collisions.astype(convert_dict)
        collisions['year'] = item['label']

        yearly_causes.append(collisions.reset_index().set_index('case_id'))
        keys.append(item['label'])

    return pd.concat(yearly_causes)


def STATSlookIntoMissingPosition(options):
    yearly_causes = []
    keys = []

    for item in options:
        collisions = pd.read_csv('input/{}_collisions.csv'.format(item['label']), parse_dates=["collision_date"],
                                 dtype={
                                     'case_id': 'str',
                                     'killed_victims': 'Int64',
                                     'injured_victims': 'Int64',
                                     'bicyclist_injured_count': 'Int64',
                                     'bicyclist_killed_count': 'Int64',
                                     'bicycle_collision': 'Int64',
                                     'party_count': 'Int64',
                                     'pcf_violation_code': 'str',
                                     'pcf_violation_category': 'str',
                                     'latitude': 'float',
                                     'longitude': 'float'
                                 })
        collisions['killed_victims'] = collisions['killed_victims'].fillna(0)
        collisions['injured_victims'] = collisions['injured_victims'].fillna(0)

        collisions['has_spatial_data'] = collisions['latitude']
        collisions['has_spatial_data'] = collisions['has_spatial_data'].apply(lambda x: 'n' if pd.isnull(x) else 'y')
        collisions['hour'] = pd.DatetimeIndex(collisions['collision_time']).hour
        collisions['month'] = pd.DatetimeIndex(collisions['collision_time']).hour
        collisions['year'] = item['label']

        yearly_causes.append(collisions.reset_index().set_index('case_id'))
        keys.append(item['label'])

    return pd.concat(yearly_causes)


def lookIntoCauses(options, daily=False, yearly=True, showPie=False):
    yearly_causes = []
    keys = []

    for item in options:
        collisions = pd.read_csv('input/{}_collisions.csv'.format(item['label']), parse_dates=["collision_date"],
                                 dtype={
                                     'killed_victims': 'Int64',
                                     'injured_victims': 'Int64',
                                     'bicyclist_injured_count': 'Int64',
                                     'bicyclist_killed_count': 'Int64',
                                     'bicycle_collision': 'Int64',
                                     'party_count': 'Int64',
                                     'pcf_violation_code': 'str',
                                     'pcf_violation_category': 'str',
                                     'latitude': 'float',
                                     'longitude': 'float'
                                 })
        data = collisions
        if daily is True:
            # daily things
            data = (collisions.groupby(
                [pd.Grouper(key='collision_date', freq='7T'),  # replace 5T by D to get daily agggregation
                 'pcf_violation_category'])
                    .agg(count=('pcf_violation_category', 'count')  # ,
                         # sum_shares=('Shares', 'sum'),
                         # sum_comments=('Comments', 'sum'),
                         # sum_engagement=('Engagement', 'sum'),
                         )
                    .reset_index()
                    )
            # print(data.head(25))
            plt.figure()
            sns.lineplot(data=data, x="collision_date", y='count', hue="pcf_violation_category",
                         style="pcf_violation_category")
            plt.title(item['label'])

        if yearly is True:
            data = (collisions.groupby(
                ['pcf_violation_category'])
                    .agg(count=('pcf_violation_category', 'count'),
                         bicycle_deaths=('bicyclist_killed_count', 'sum'),
                         bicycle_injured=('bicyclist_injured_count', 'sum'),
                         deaths=('killed_victims', 'sum'),
                         deaths_avg=('killed_victims', np.mean),
                         deaths_sd=('killed_victims', np.var),
                         injured=('injured_victims', 'sum'),
                         injured_avg=('injured_victims', np.mean),
                         injured_sd=('injured_victims', np.var),
                         )
                    .reset_index()
                    )
            data = data.sort_values(['count'], ascending=False)

        data['year'] = item['label']
        data.set_index('pcf_violation_category', inplace=True)
        data.reset_index().set_index(['year', 'pcf_violation_category'])

        # print(data.head())
        if showPie is True:
            data.plot.pie(y='count', legend=None)
            plt.title(item['label'])

        yearly_causes.append(data)
        keys.append(item['label'])

    return pd.concat(yearly_causes)


def wrapData(options, overwrite=False):
    connection = create_connection('switrs.sqlite')
    for item in options:
        filename = 'input/{}_collisions.csv'.format(item['label'])
        if not os.path.isfile(filename) or overwrite:
            print(item['label'])
            query = '''SELECT * FROM collisions where 
                    collision_date IS NOT NULL and {} and bicycle_collision = 1'''  #
            collisions = pd.read_sql_query(query.format(item['value']), connection, parse_dates=["collision_date"])
            collisions.to_csv(filename, index=False)
    connection.close()


def plotCausesTrend(causes):
    # Pivot table:
    pivot_table = causes.pivot_table(index='pcf_violation_category', columns='year', values='count')

    print(pivot_table.head())
    # Chi-square Test for independence
    res = stat()
    res.chisq(df=pivot_table)
    print(res.summary)

    sns.lineplot(data=causes, x="year", y='count', hue="pcf_violation_category", style="pcf_violation_category")
    plt.legend(bbox_to_anchor=(0.95, 1), loc='upper left')

    plt.figure()
    sns.lineplot(data=causes, x="year", y='injured', hue="pcf_violation_category", style="pcf_violation_category")
    plt.legend(bbox_to_anchor=(0.95, 1), loc='upper left')

    plt.figure()
    sns.lineplot(data=causes, x="year", y='deaths', hue="pcf_violation_category", style="pcf_violation_category")
    plt.legend(bbox_to_anchor=(0.95, 1), loc='upper left')

    plt.figure()
    sns.lineplot(data=causes, x="year", y='bicycle_deaths', hue="pcf_violation_category",
                 style="pcf_violation_category")
    plt.legend(bbox_to_anchor=(0.95, 1), loc='upper left')

    plt.figure()
    sns.lineplot(data=causes, x="year", y='bicycle_injured', hue="pcf_violation_category",
                 style="pcf_violation_category")
    plt.legend(bbox_to_anchor=(0.95, 1), loc='upper left')


if __name__ == "__main__":
    options = [
        {'label': '2001', 'value': 'collision_date between "2001-01-01" and "2001-12-31"'},
        {'label': '2002', 'value': 'collision_date between "2002-01-01" and "2002-12-31"'},
        {'label': '2003', 'value': 'collision_date between "2003-01-01" and "2003-12-31"'},
        {'label': '2004', 'value': 'collision_date between "2004-01-01" and "2004-12-31"'},
        {'label': '2005', 'value': 'collision_date between "2005-01-01" and "2005-12-31"'},
        {'label': '2006', 'value': 'collision_date between "2006-01-01" and "2006-12-31"'},
        {'label': '2007', 'value': 'collision_date between "2007-01-01" and "2007-12-31"'},
        {'label': '2008', 'value': 'collision_date between "2008-01-01" and "2008-12-31"'},
        {'label': '2009', 'value': 'collision_date between "2009-01-01" and "2009-12-31"'},
        {'label': '2010', 'value': 'collision_date between "2010-01-01" and "2010-12-31"'},
        {'label': '2011', 'value': 'collision_date between "2011-01-01" and "2011-12-31"'},
        {'label': '2012', 'value': 'collision_date between "2012-01-01" and "2012-12-31"'},
        {'label': '2013', 'value': 'collision_date between "2013-01-01" and "2013-12-31"'},
        {'label': '2014', 'value': 'collision_date between "2013-12-31" and "2015-01-01"'},
        {'label': '2015', 'value': 'collision_date between "2014-12-31" and "2016-01-01"'},
        {'label': '2016', 'value': 'collision_date between "2015-12-31" and "2017-01-01"'},
        {'label': '2017', 'value': 'collision_date between "2016-12-31" and "2018-01-01"'},
        {'label': '2018', 'value': 'collision_date between "2017-12-31" and "2019-01-01"'},
        {'label': '2019', 'value': 'collision_date between "2018-12-31" and "2020-01-01"'},
        {'label': '2020', 'value': 'collision_date between "2019-12-31" and "2021-01-01"'}
    ]

    # main()
    # main()
    # main3(options)
    main4(options)

    plt.show()
