import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

claimant_count = pd.DataFrame()
claimant_count = pd.read_csv(
    'https://raw.githubusercontent.com/StanWaldron/StanWaldron.github.io/main/Data/Claimant%20count%202020.csv')

plot = sns.lineplot(x='Period', y='UK_claimant',
                    data=claimant_count, legend=False)

locator = mdates.MonthLocator(bymonthday=1, interval=1)
plot.xaxis.set_major_locator(locator)

plot.set(ylabel='No. Claimants in the UK', xlabel='Date')

plt.show()

### Rendering Plot in Html
# figfile = io.BytesIO()
# plt.savefig(figfile, format='png')
# figfile.seek(0)
# figdata_png = base64.b64encode(figfile.getvalue())
# esult = str(figdata_png)[2:-1]

# Could potentially add hours worked to prove point:
# https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/bulletins/uklabourmarket/january2021
