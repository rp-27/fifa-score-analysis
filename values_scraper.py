import requests, re, ast
from bs4 import BeautifulSoup
import pandas as pd
import csv


i = 1

url_list = []

while True:

    try:
        page = requests.get('https://www.transfermarkt.us/spieler-statistik/wertvollstespieler/marktwertetop' + str(i), headers = {'User-Agent':'Mozilla/5.0'}).text

    except requests.exceptions.Timeout:
        sys.exit(1)

    parsed_page = BeautifulSoup(page,'lxml')

    all_links = []
    for link in parsed_page.find_all('a', href=True):
        link = str(link['href'])
        all_links.append(link)

    r = re.compile('.*profil/spieler.*')
    player_links = list(filter(r.match, all_links))

    for plink in range(0,25):
        url_list.append('https://www.transfermarkt.us' + player_links[plink])

    i += 1

    if i > 20:
        break


with open('final_url_list.csv', 'w') as final_url_file:
    csv_writer = csv.writer(final_url_file)

    for i in url_list:

        try:
            int_page = requests.get(i, headers = {'User-Agent':'Mozilla/5.0'}).text

        except requests.exceptions.Timeout:
            sys.exit(1)

        parsed_int_page = BeautifulSoup(int_page,'lxml')
        graph_container = parsed_int_page.find('div', class_='large-7 columns small-12 marktwertentwicklung-graph')

        try:
            graph_a = graph_container.find('a')
            graph_link = graph_a.get('href')
            final_link = 'https://www.transfermarkt.us' + graph_link
            final_url_list.append(final_link)

            csv_writer.writerow([final_link])

        except AttributeError:
            pass
            print("Graph error:" + i)


with open('values_2.csv', 'w') as test_file:

    csv_writer = csv.writer(test_file)
    csv_writer.writerow(['name', '2014', '2015', '2016', '2017', '2018', '2019'])

    for url in final_url_list:

        try:
            r = requests.get(url, headers = {'User-Agent':'Mozilla/5.0'})
        except requests.exceptions.Timeout:
            sys.exit(1)

        soup_r = BeautifulSoup(r.text, "lxml")
        name_container = soup_r.find('div', class_="dataName")
        full_name = name_container.h1.text

        first_name = full_name.strip(" ")

        p = re.compile(r"'data':(.*)}\],")
        s = p.findall(r.text)[0]
        s = s.encode().decode('unicode_escape')

        try:
            data = ast.literal_eval(s)

            values = pd.DataFrame.from_records(data, columns = ['datum_mw', 'mw'])
            new_values = values[values.datum_mw.str.contains('.*201[4-9]')].copy()
            new_values['mw'] = new_values['mw'].str.strip("$")
            new_values['mw'] = new_values['mw'].str.replace(r'(k|m)', r' \1')
            split = new_values['mw'].str.split(r'(k|m)', expand = True)
            new_values['value'] = split[0]
            new_values['multiplier'] = split[1]
            new_values.drop(columns =['mw'], inplace = True)

            new_values['value'] = new_values['value'].apply(pd.to_numeric, errors='coerce')
            new_values.loc[new_values['multiplier'] == 'k', 'value'] = new_values.loc[new_values['multiplier'] == 'k', 'value'].apply(lambda x: ((x * 1000) / 1000000))
            new_values['datum_mw'] = pd.to_datetime(new_values['datum_mw'])
            new_values['datum_mw'] = new_values['datum_mw'].dt.year
            avg_value_per_year = round(new_values.groupby('datum_mw')['value'].mean().to_frame(), 4)

            if 2014 in avg_value_per_year.index:
                value_2014 = avg_value_per_year.loc[2014].item()
            else:
                value_2014 = float("NaN")
            if 2015 in avg_value_per_year.index:
                value_2015 = avg_value_per_year.loc[2015].item()
            else:
                value_2015 = float("NaN")
            if 2016 in avg_value_per_year.index:
                value_2016 = avg_value_per_year.loc[2016].item()
            else:
                value_2016 = float("NaN")
            if 2017 in avg_value_per_year.index:
                value_2017 = avg_value_per_year.loc[2017].item()
            else:
                value_2017 = float("NaN")
            if 2018 in avg_value_per_year.index:
                value_2018 = avg_value_per_year.loc[2018].item()
            else:
                value_2018 = float("NaN")
            if 2019 in avg_value_per_year.index:
                value_2019 = avg_value_per_year.loc[2019].item()
            else:
                value_2019 = float("NaN")

            csv_writer.writerow([first_name, value_2014, value_2015, value_2016, value_2017, value_2018, value_2019])

        except:
            print(url)
            pass


