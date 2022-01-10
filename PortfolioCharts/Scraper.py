from bs4 import BeautifulSoup
import pandas as pd
import requests
url = "https://www.thecompleteuniversityguide.co.uk/league-tables/rankings"
html = requests.get(url)
soup = BeautifulSoup(html.content, 'html.parser')

soup.findAll('div')

table = soup.find('li', id="colOne")
print(table)

unis = table.findAll('a', class_='uni_lnk')
finalunis = [x.text for x in unis]
finalunis
rankings = []
for ranking in range(len(finalunis)):
    rankings.append(ranking + 1)


unis_table = pd.DataFrame()
unis_table['Ranking'] = rankings
unis_table['University'] = finalunis

unis_table
grad_score = []
grad = soup.find_all('div', class_='segtxt')
for g in grad:
    grad_score.append(str(g.text.replace('\n', '').replace('%', '')))


finalgradscore = []
for z in range(len(grad_score)):
    if z >= 520:
        finalgradscore.append(int(grad_score[int(z)]))

unis_table['Graduate Prospects in %'] = finalgradscore

unis_table.to_csv(
  r'/content/drive/MyDrive/ColabNotebooks/unis_table.csv', index=False)
