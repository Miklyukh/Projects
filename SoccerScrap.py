import requests
from bs4 import BeautifulSoup

URL = "https://www.uslleaguetwo.com/stats/league_instance/134228?subseason=731558"
r = requests.get(URL)

soup = BeautifulSoup(r.content, 'html5lib')
table = soup.find("table", attrs={"class": "dataTable statTable theme-stat-table"})
table_data = table.tbody.find_all("tr")
heading = []
print(table.text)