import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv(
    'https://raw.githubusercontent.com/StanWaldron/StanWaldron.github.io/main/Data/unis_table.csv')

ax = sns.regplot(data=data, x=data['Ranking'], y=data['Graduate Prospects in %'], scatter_kws={
                "color": "seagreen"}, line_kws={"color": "black"})

plt.show()
