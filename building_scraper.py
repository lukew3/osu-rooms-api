from bs4 import BeautifulSoup
import re
import requests
import csv

data = {
    'sort': 'letter',
    'Submit': 'Sort Buildings',
}

response = requests.post('https://www.osu.edu/map/buildingindex.php', data=data)


# parse results into a beautifulsoup object
soup = BeautifulSoup(response.text, 'html.parser')

# go inside div id: buildingIndex and extract all the li tags
building_index = soup.find(id="buildingIndex")
lis = building_index.find_all("li")

# store the building names into a list
building_names = []
building_numbers = []
building_urls = []

for li in lis:
    # get the building number
    number = li.find_all("strong")[1].text
    number = re.search(r"\((\d+)\)", number).group(1)
    building_numbers.append(number)

    # get the building url
    url = 'www.osu.edu/map/building/' + number
    building_urls.append(url)

    # get the building name
    a = li.find("a")
    a.span.decompose()
    building_names.append(a.text.rstrip())


# results
# print(len(building_names))
# print(len(building_numbers))
# print(len(building_urls))
# print(building_urls)


# save the building names, numbers, and urls into a csv file
with open('buildings.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['number', 'name', 'url'])
    for i in range(len(building_names)):
        writer.writerow([building_numbers[i], building_names[i], building_urls[i]])

