import requests, re
from bs4 import BeautifulSoup
import csv

with open('name_fields.csv', 'w') as name_file:
    csv_writer = csv.writer(name_file)

    csv_writer.writerow(['name', 'long_name'])

    url_lists = open('final_url_list.csv')
    csv_reader_urls = csv.reader(url_lists)

    for line in csv_reader_urls:

        line = line[0]
        line = line.replace("marktwertverlauf", "profil")

        r = requests.get(line, headers = {'User-Agent':'Mozilla/5.0'})

        soup_r = BeautifulSoup(r.text, "lxml")
        og_name_container = soup_r.find('div', class_="dataName")
        og_name = og_name_container.h1.text
        name = og_name.strip(" ")

        try:
            long_name_container = soup_r.find('div', class_="spielerdaten")
            long_name = long_name_container.td.text

            if re.search(r'\d', long_name):
                long_name = name
            else:
                long_name = long_name.strip(" ")

            csv_writer.writerow([name, long_name])

        except:
            long_name = "nan"
            pass

            csv_writer.writerow([name, long_name])