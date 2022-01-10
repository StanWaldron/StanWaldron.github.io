import requests
import pandas as pd
import json
import numpy as np


url = 'https://raw.githubusercontent.com/StanWaldron/StanWaldron.github.io/main/Data/CrystalPalace.csv'
html = requests.get(url)
json_data = html.json()
json_data

df = pd.DataFrame(json_data['data'])

df2 = df[['match_start', 'home_team', 'away_team', 'stats']]

home = []
away = []
palace = [home, away]

for i in range(392):
    if (df2['home_team'][i]['team_id'] == 2515):
        palace[0].append(int(1))
    else:
        palace[0].append(int(0))

for i in range(392):
    if (df2['away_team'][i]['team_id'] == 2515):
        palace[1].append(int(1))
    else:
        palace[1].append(int(0))

df2.sort_values(by='palace_away')

df2_home_matches = {}
df2_home_matches = df2[df2['palace_home'] == 1]

df2_away_matches = {}
df2_away_matches = df2[df2['palace_away'] == 1]

awaygames = pd.DataFrame(df2_away_matches)
homegames = pd.DataFrame(df2_home_matches)

awayscores = []
oppawayscores = []
for agames in awaygames['stats']:
    awayscores.append(agames['away_score'])
    oppawayscores.append(agames['home_score'])

homescores = []
opphomescores = []
for hgames in homegames['stats']:
    homescores.append(hgames['home_score'])
    opphomescores.append(hgames['away_score'])

homegames['homescore'] = homescores
awaygames['awayscore'] = awayscores
homegames['opphomescore'] = opphomescores
awaygames['oppawayscore'] = oppawayscores

awaygames
x = 0
cumaway = []
oppcumaway = []
cumhome = []
oppcumhome = []
for x in awaygames['awayscore']:
    cumaway.append(x)

for q in awaygames['oppawayscore']:
    oppcumaway.append(q)

for w in homegames['homescore']:
    cumhome.append(w)

for o in homegames['opphomescore']:
    cumhome.append(o)

cumaway = np.cumsum(cumaway)
cumhome = np.cumsum(cumhome)
oppcumaway = np.cumsum(oppcumaway)
oppcumhome = np.cumsum(oppcumhome)
cumaway
cumhome

finalaway = pd.DataFrame()
finalhome = pd.DataFrame()

finalaway['Date'] = awaygames['match_start']
away_gd = []

agd = np.subtract(awaygames['awayscore'], awaygames['oppawayscore'])
fagd = np.cumsum(agd)
hgd = np.subtract(homegames['homescore'], homegames['opphomescore'])
fhgd = np.cumsum(hgd)
finalaway['Away_GD'] = fagd
finalhome['Home_GD'] = fhgd
finalhome['Date'] = homegames['match_start']
final = pd.DataFrame(pd.concat([finalhome, finalaway]))
final.sort_values(by='Date')

final.to_csv(r'/content/drive/MyDrive/ColabNotebooks/final.csv', index=False)
