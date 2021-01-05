import requests, re
from bs4 import BeautifulSoup
import csv

url_list = []

i = 0

while True:

    x = i*60

    try:
        page = requests.get('https://sofifa.com/teams?offset=' + str(x), headers={'User-Agent': 'Mozilla/5.0'}).text

    except requests.exceptions.Timeout:
        sys.exit(1)

    parsed_page = BeautifulSoup(page, 'lxml')

    team_containers = parsed_page.find_all('div', class_='bp3-text-overflow-ellipsis')

    found_links = []
    for indv_team_container in team_containers:
        indv_team_links = indv_team_container.find_all('a', href=True)
        for a in range(len(indv_team_links)):
            link = indv_team_links[a]
            link_container = str(link['href'])
            found_links.append(link_container)

    pattern = re.compile('.team.')

    team_link = list(filter(pattern.match, found_links))

    for url in team_link:
        url_list.append(url)


    i += 1

    if i > 16:
        break

with open('team_id.csv', 'w') as team_id_file:
    csv_writer = csv.writer(team_id_file)
    csv_writer.writerow(['team_id', 'club'])

    for url in url_list:

        try:
            page = requests.get('https://sofifa.com' + url, headers={'User-Agent': 'Mozilla/5.0'}).text

        except requests.exceptions.Timeout:
            sys.exit(1)

        team_page = BeautifulSoup(page, 'lxml')
        name_id_container = team_page.find('div', class_= "info").h1.text
        name_id_pair = name_id_container[:-20]
        name_id_list = name_id_pair.split(" (")
        name = name_id_list[0].strip()

        id_uncleaned = name_id_list[1]

        found = re.search('ID: (\d*)', id_uncleaned)
        if found:
            team_id = found.group(1)

        csv_writer.writerow([team_id, name])
