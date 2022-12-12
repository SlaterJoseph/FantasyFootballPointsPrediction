import requests
import json
from csv_writer import write_players, write_csv_data

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

def create_positional_data(player_data: list, ) -> None:
    pass