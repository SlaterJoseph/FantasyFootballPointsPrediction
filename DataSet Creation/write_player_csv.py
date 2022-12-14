import requests
import json
import csv
from csv_writer import write_players, write_csv_data
import pandas as pd
from time import sleep
from headers import headers as hd


# First, we need to create the dataset for playerIDs, positionIDs, and teamIDs

def create_players_data() -> None:
    player_list = list()

    for page_num in range(1, 6):  # iterates over all pages of the api for player info
        url = f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/athletes?limit=1000&active=" \
              f"true&page={page_num}"

        response = requests.get(url)
        parse_json = json.loads(response.text)
        items = parse_json["items"]

        for item in items:
            player_list.append(item["$ref"])

    write_players(player_list)


def create_positional_data() -> None:
    df = pd.read_csv('../CSV Files/players_data.csv')
    player_dict = df.to_dict("index")
    ffp = {'C', 'G', 'OT', 'P', 'DT', 'CB', 'P', 'FB', 'LB', 'S', 'DE', 'LS', 'OL', 'DB', '-', 'DL', 'NT'}  # filters out all not used
    # positional players (OLB, LB, CB, S, so on)
    # valid positions are QB, WR, RB, FB, CB, LB, TE, S, PK, DE
    i = 0  # help prevent over calling api adn crashing program

    for num in player_dict:  # Go through players 1 by 1
        player = player_dict[num]
        if player["positionAbbreviation"] not in ffp:  # filters players irrelevant to fantasy football
            ffp.add(player["positionAbbreviation"])  # We have now created the csv, we no longer need to create it
            create_cvs(player["positionAbbreviation"])
            path_to_csv = "../CSV Files/" + player["positionAbbreviation"] + "_data.csv"
            writer = csv.writer(open(path_to_csv, 'w', newline=''))  # write the heading the into csv
            writer.writerow(hd[player['positionAbbreviation']])

        i += 1
        try:
            print(player['fullName'], player['positionAbbreviation'])  # for keeping track of progress
            print('-------------')
            write_csv_data(player)
            if i % 100 == 0:  # Sleep for 1 min to prevent over calling the api
                print('10 sec of Sleep')
                sleep(10)

        except KeyError as ke:
            print('KeyError', ke)
            continue



def create_cvs(pos: str) -> None:
    from xlwt import Workbook
    wb = Workbook()
    sheet1 = wb.add_sheet(pos + "_data")
    wb.save("../CSV Files/" + pos + "_data.csv")  # create a blank csv file


# create_players_data()
create_positional_data()
