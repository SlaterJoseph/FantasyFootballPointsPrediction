import requests
import json
from csv_writer import write_csv, write_players

# First, we need to create the dataset for playerIDs, positionIDs, and teamIDs
player_list = list()

for page_num in range(1, 6):
    url = f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/athletes?limit=1000&active=" \
          f"true&page={page_num}"

    response = requests.get(url)
    parse_json = json.loads(response.text)
    items = parse_json["items"]

    for item in items:
        player_list.append(item["$ref"])

write_players(player_list)
# url = player_list[0]
# response = requests.get(url)
# pj = json.loads(response.text)
#
# print(pj["headshot"]["href"])