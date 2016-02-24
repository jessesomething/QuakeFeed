import json
import bs4
import requests

url = "http://earthquake-report.com/feeds/recent-eq?json"
r = requests.get(url)
data = r.text

soup = bs4.BeautifulSoup(data, "html.parser")
print(soup)


#
# for event in soup.find_all('magnitude'):
#     print(event)

quakes = json.loads(data)

for events in quakes:
    print(events['location'] + "\nLat: " + events['latitude'] + "\nLong: " + events['longitude'] + "\nMagnitude: " + events['magnitude'] + "\n")
# print '"location":', result['magnitude']

# print '"networkdiff":', result['getpoolstatus']['data']['networkdiff']

# print(soup)
