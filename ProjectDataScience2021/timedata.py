import pandas as pd
import numpy as np
import datetime as dt

#Load in data

consumption = pd.read_csv(
    'https://raw.githubusercontent.com/StanWaldron/StanWaldron.github.io/main/Data/h_consumption%20big.csv')

music = pd.read_csv(
    'https://raw.githubusercontent.com/StanWaldron/StanWaldron.github.io/main/Data/test2.csv')

# Convert dates into ordinal dates so that they are easier to work with when selecting time periods

music['year_ordinal'] = pd.to_datetime(
    music['album_id']).apply(lambda date: date.toordinal())

consumption['year_ordinal'] = pd.to_datetime(
    consumption['Date']).apply(lambda date: date.toordinal())

features = ['danceability',	'energy', 'loudness', 'speechiness',
            'instrumentalness',	'liveness',	'valence',	'tempo', 'duration_ms']

# This function takes the average of teh consumption and then works out what every musical feature needs to be multiplied by so they all look somewhat similar on one graph

def get_relative_values():

    # Find the mean of consumption

    averages = []
    multipliers = []
    reg_data = pd.DataFrame()
    con_average = (np.sum(consumption['Value']) / len(consumption['Value']))

    # Loop through for all audio features and work out their multipliers

    for feature in features:
        average = (np.sum(music[feature]) / len(music[feature]))
        averages.append(average)
        multiplier = (con_average / average)
        multipliers.append(multiplier)
        reg_data[feature] = music[feature]

    # Apply these multipliers

    for x in range(len(features)):
        reg_data[features[x]] = multipliers[x] * music[features[x]]

    reg_data['Date'] = music['album_id']

    return reg_data

# This function takes your start and finish dates, as well as the y value you are measuring and returns all of the data in that timeframe. Limits have to be ordinal.


def time_data(data, start, finish, y):
    timeframe = pd.DataFrame()

    new_dates = []
    new_values = []

    # Loop and find all dates within specified period and then create arrays with new dates and values

    for i in range(len(data['year_ordinal'])):
        if data['year_ordinal'][i] in range(start, finish):
            new_dates.append(data['year_ordinal'][i])
            new_values.append(data[y][i])

    timeframe['Date'] = new_dates
    timeframe['Value'] = new_values
    print(len(new_dates))
    return timeframe

# Take the converted values and make the dates ordinal

converted_music = get_relative_values()

converted_music['year_ordinal'] = pd.to_datetime(
    converted_music['Date']).apply(lambda date: date.toordinal())

# Here we get the consumption, no need to loop as it is on its own

cons3 = time_data(consumption, 726468, 735243, 'Value')
cons3['Date'] = cons3['Date'].apply(dt.datetime.fromordinal)
new_dates = []
new_values = []

# Here we loop through for the respective data on audio features adn then save the results
# I could have put this all in one dataframe, but the way I wanted the data to be presented, it wouldn't have worked

base_file = r'C:/Users/Stan/Desktop/Data Science/Project/{}.csv'
for feature in features:
    filepath = base_file.format(feature)
    featureinfo = time_data(converted_music, 726468, 735243, feature)
    featureinfo['Date'] = featureinfo['Date'].apply(dt.datetime.fromordinal)
    featureinfo.to_csv(filepath)


cons3.to_csv(r'C:/Users/Stan/Desktop/Data Science/Project/cons90-14.csv')
