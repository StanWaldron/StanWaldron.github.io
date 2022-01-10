import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
from IPython.display import set_matplotlib_formats

# Change matplotlib formats so that the image is clearer

set_matplotlib_formats('svg')
plt.rcParams['figure.dpi'] = 200

# Here we read datasets that I have collected and believe could be interesting

music = pd.read_csv(
    'https://raw.githubusercontent.com/StanWaldron/StanWaldron.github.io/main/Data/test2.csv')

wages = pd.read_csv(
    'https://raw.githubusercontent.com/StanWaldron/StanWaldron.github.io/main/Data/wages.csv')

consumption = pd.read_csv(
    'https://raw.githubusercontent.com/StanWaldron/StanWaldron.github.io/main/Data/h_consumption%20big.csv')

features = ['danceability',	'energy', 'loudness', 'speechiness',
            'instrumentalness',	'liveness',	'valence',	'tempo', 'duration_ms']

# Unused Data

# real_wages = pd.read_csv(
#    r'filepath')

# unemployment = pd.read_csv(
#    r'filepath')

# cons_growth = pd.read_csv(
#    r'filepath')

# This first function creates a dataframe with the data that has been read and teh audio features of the music


def datafinder(inputdata):

    reg_data = pd.DataFrame()

    # Here I convert dates to ordinal dates as it is easier to work with and plot, especially later on when I need to generate more dates so that the dat entries are the same length

    music['rdate_ordinal'] = pd.to_datetime(
        music['album_id']).apply(lambda date: date.toordinal())

    inputdata['year_ordinal'] = pd.to_datetime(
        inputdata['Date']).apply(lambda date: date.toordinal())

    value_organiser = int(
        len(music['rdate_ordinal']) / len(inputdata['year_ordinal']))
    # Here we had to solve the issue of there being quarterly or monthly results for economic indicators, but almost weekly for no.1s
    # So, I make each pieces of data the same size by adding the relative number of days with the same value after each report of the indicator so that they have the same number of values
    # This shouldn't skew the data as the likelihood of these indicators changing drastically in that timeframe, a matter of days, is very small, otherwise they would mesaure it more frequently

    new_dates = []
    new_values = []
    for feature in features:
        reg_data[feature] = music[feature]

    for date in inputdata['year_ordinal']:
        for fill in range(value_organiser):
            new_dates.append(date + fill)

    for value in inputdata['Value']:
        for fill in range(value_organiser):
            new_values.append(value + fill)

    for finalfill in range(len(music[features[0]]) - (len(new_values))):
        # date = random.choice(range(len(new_dates)))
        # value = random.choice(range(len(new_values)))
        new_dates.append(new_dates[len(new_dates) - 1])
        new_values.append(new_values[len(new_values) - 1])

    reg_data['inputdata'] = new_values

    return reg_data

# This function then takes the formatted data from the last function and creates a grid of it plotted against all teh music features


def dataplot(inputdata, xlabel, xticks):

    final_data = datafinder(inputdata)

    # Creates a figure with enough room for 9 subplots in a 3x3 grid.
    fig = plt.subplots(3, 3, sharex=True, figsize=(15, 15))

    # Loop through the figure and insert the relevant graph into that place

    for plot in range(9):
        subfig = plt.subplot(3, 3, plot+1)
        plt.subplots_adjust(left=None, bottom=None, right=None,
                            top=None, wspace=0.2, hspace=0.2)

        sns.regplot(x='inputdata', y=features[plot], data=final_data,
                    scatter_kws={"color": "#555555", "alpha": 0.2},
                    line_kws={"color": '#C40505'})
        subfig.set_xticklabels(xticks)

        # this cleans up waht could otherwise be a very messy graph.

        if plot > 5:
            subfig.set_xlabel(str(xlabel))
            if plot == 8:
                plt.ylim(0, 750000)
                subfig.set_yticklabels(['0', '100k', '200k', '300k', '400k', '500k',
                                        '600k', '700k'])
        else:
            if plot == 4:
                plt.ylim(0, 0.4)
            subfig.set_xlabel('')

    plt.show()

# Here we call the functions for the most interesting datasets


dataplot(wages, '% Growth of Annual Wages',
         ['0', '10', '20', '30', '40', '50'])

dataplot(consumption, 'Consumption', [
         '0', '100k', '200k', '300k', '400k', '500k', '600k'])
