import csv
import requests
import json

def write_csv(pos: str, data: list) -> None:
    writer = csv.writer(open('../CSV Files/' + pos + "_data.csv", 'w'))

    header = ["Name", "Position", "Season", "Week", "Team", "Opponent", "Activated", "Played", "Started"]

    if pos == 'k':  # Kicker specific header
        header.extend(["FieldGoalsAttempted", "FieldGoalsMade", "FieldGoalsLongestMade", "ExtraPointsMade"])

    header.extend(["PassingAttempts", "PassingCompletions", "PassingYards", "PassingTouchdowns", "RushingAttempts",
                   "RushingYards", "RushingYardsPerAttempt", "RushingTouchdowns", "ReceivingTargets", "Receptions",
                   "ReceivingYards", "ReceivingYardsPerReception", "ReceivingTouchdowns", "ReceivingLong", "Fumbles"])

    writer.writerow(header)
    writer.writerows(data)


def write_players(items: list) -> None:
    header = ["fullName", "playerID", "teamName", "teamID", "positionName", "positionID", "positionAbbreviation",
              "gameIDs"]

    writer = csv.writer(open('../CSV Files/players_data.csv', 'w'))

    writer.writerow(header)
    player_info_list = list()
    for entry in items:  # looping through players
        url = entry
        response = requests.get(url)
        pj = json.loads(response.text)

        # getting the team's info through another api call
        team_url = pj["team"]["$ref"]
        team_response = requests.get(team_url)
        tpj = json.loads(team_response.text)

        position_data = pj['position']

        player_info = [pj["fullName"], pj["id"], tpj["displayName"], tpj["id"], position_data["displayName"],
                       position_data["id"], position_data["abbreviation"], "None"]

        print(pj["fullName"])
        # for entry in player_info:
        #     print(entry)
        player_info_list.append(player_info)

    writer.writerows(player_info_list)
# def get_player_info(s)

