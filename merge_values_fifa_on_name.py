import pandas as pd


# each yearly table needs to be run individually; comment out other tables and change all df placeholders between lines 14-68 in script with current table (ie fifa_16, etc.)

# fifa_15 = pd.read_csv('/Users/rp/PycharmProjects/FIFA Project/fifa-20-complete-player-dataset/players_15.csv')
fifa_16 = pd.read_csv('/Users/rp/PycharmProjects/FIFA Project/fifa-20-complete-player-dataset/players_16.csv')
# fifa_17 = pd.read_csv('/Users/rp/PycharmProjects/FIFA Project/fifa-20-complete-player-dataset/players_17.csv')
# fifa_18 = pd.read_csv('/Users/rp/PycharmProjects/FIFA Project/fifa-20-complete-player-dataset/players_18.csv')
# fifa_19 = pd.read_csv('/Users/rp/PycharmProjects/FIFA Project/fifa-20-complete-player-dataset/players_19.csv')
# fifa_20 = pd.read_csv('/Users/rp/PycharmProjects/FIFA Project/fifa-20-complete-player-dataset/players_20.csv')


del_col_list = ['sofifa_id','player_url', 'dob', 'value_eur', 'wage_eur', 'real_face', 'release_clause_eur', 'contract_valid_until','team_jersey_number', 'nation_jersey_number', 'player_positions', 'passing', 'ls', 'st', 'rs',
       'lw', 'lf', 'cf', 'rf', 'rw', 'lam', 'cam', 'ram', 'lm', 'lcm', 'cm',
       'rcm', 'rm', 'lwb', 'ldm', 'cdm', 'rdm', 'rwb', 'lb', 'lcb', 'cb',
       'rcb', 'rb']

fifa_16.drop(del_col_list, axis = 1, inplace=True)

data_table = pd.read_csv('/Users/rp/PycharmProjects/FIFA Project/scripts/values_2.csv')
names_fields = pd.read_csv('/Users/rp/PycharmProjects/FIFA Project/scripts/name_fields.csv')

# spot check changes for big name players that will not be caught by name match seeking logic

names_fields.loc[names_fields["long_name"] == "Lionel Andrés Messi Cuccitini", "long_name" ] = "Lionel Andrés Messi Cuccittini"
names_fields.loc[names_fields["long_name"] == "Neymar da Silva Santos Júnior", "long_name" ] = "Neymar da Silva Santos Junior"
names_fields.loc[names_fields["long_name"] == "Kylian Mbappe Lottin", ['long_name']] = "Kylian Mbappé"
names_fields.loc[names_fields["long_name"] == "Mohamed  Salah Ghaly", ['long_name']] = "Mohamed Salah"

# end of spot check changes

values_table = pd.merge(data_table, names_fields, on="name")

names = values_table['long_name']
names_2 = values_table['name']
long_names = fifa_16['long_name']

for i in range(len(names)):
    found = False
    name0_list = names[i].split()
    name_list = [x.lower() for x in name0_list]
    name0_list_2 = names_2[i].split()
    name_list_2 = [y.lower() for y in name0_list_2]
    for j in range(len(long_names)):
        long0_name_list = long_names[j].split()
        long_name_list = [z.lower() for z in long0_name_list]
        if set(name_list).issubset(long_name_list) or set(long_name_list).issubset(name_list):
            fifa_16.loc[j, "long_name"] = values_table.loc[i, "name"]
            found = True
    if not found:
        for j in range(len(long_names)):
            long0_name_list = long_names[j].split()
            long_name_list = [z.lower() for z in long0_name_list]
            if set(name_list_2).issubset(long_name_list) and len(name_list_2)>1:
                fifa_16.loc[j, "long_name"] = values_table.loc[i, "name"]
                found = True
        if not found:
            for j in range(len(long_names)):
                long0_name_list = long_names[j].split()
                long_name_list = [z.lower() for z in long0_name_list]
                if set(names_2).issubset(long_name_list):
                    fifa_16.loc[j, "long_name"] = values_table.loc[i, "name"]


fifa_16.rename(columns={'long_name': 'name'}, inplace=True)
resulting_table = pd.merge(fifa_16, values_table["name"], on='name')
fifa_16.to_csv(r'/Users/rp/PycharmProjects/FIFA Project/merged data/merged_df.csv')

# following code is to find players not in the high-value tables:
# comment out all dataframes except fifa_20 above, comment out above block, and run code block below to find new players without values

# resulting_table = pd.merge(fifa_16, values_table["name"], on='name', how="outer", indicator=True)
# resulting_table = resulting_table[resulting_table["_merge"] == 'left_only']
# resulting_table = resulting_table.drop(columns= '_merge')
# resulting_table.to_csv(r'/Users/rp/PycharmProjects/FIFA Project/merged data/new_players_20.csv')