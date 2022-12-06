import requests
import json
from csv_writer import write_csv

# The only free seasons for use are 2021 and 2022, so those weeks will make up the dataset
# Set the API endpoint URL
url = "https://api.sportsdata.io/v3/nfl/stats/json/PlayerGameStatsByWeek/2021/1"

# Set the API key
api_key = "be646eda27c1403d866308a91602848f"

# Set the request headers
headers = {
    "Ocp-Apim-Subscription-Key": api_key
}

# Send the request to the API endpoint
response = requests.get(url, headers=headers)
parse_json = json.loads(response.text)

# Testing to make sure that the api call works correctly
# for item in parse_json:
#     print(item["Name"])

for item in parse_json:
    ff_pos = {"QB", "RB", "WR", "TE", "K"}

    # ignoring players not a part of fantasy football
    if item["Position"] not in ff_pos:
        continue

    write_csv(item["Position"], item["Name"])
