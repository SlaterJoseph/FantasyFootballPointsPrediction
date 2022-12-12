import csv
import requests
import json
import pandas as pd

header = [
    "name", "playerID", "season", "week", "team", "teamID", "opponent", "opponentID",
    "completions", "passingAttempts", "passingYards", "completionPct", "yardsPerPassAttempt", "interceptions",
    "longPassing", "sacks", "QBRating", "adjQBR", "rushingAttempts", "rushingYards", "yardsPerRushAttempt",
    "rushingTouchdowns", "longRushing", "receptions", "receivingTargets", "receivingYards", "yardsPerReception",
    "receivingTouchdowns", "longReception", "fumbles", "fumblesLost",
]


def write_players(items: list) -> None:
    """Function for creating player_data csv"""
    header = ["fullName", "playerID", "teamName", "teamID", "positionName", "positionID", "positionAbbreviation",
              "gameIDs", "headshotURL"]

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

        position_data = pj['position']  # easy reference to team info
        player_id = pj["id"]
        player_info = [pj["fullName"], player_id, tpj["displayName"], tpj["id"], position_data["displayName"],
                       position_data["id"], position_data["abbreviation"], "None",
                       f"https://a.espncdn.com/i/headshots/nfl/players/full/{player_id}.png"]

        print(player_info)  # for progress tracking
        player_info_list.append(player_info)

    writer.writerows(player_info_list)  # add all players to csv


def write_headers() -> None:
    """Function for writing headings for CSVs"""
    qb_writer = csv.writer(open('../CSV Files/QB_data.csv', 'w'))
    rb_writer = csv.writer(open('../CSV Files/RB_data.csv', 'w'))
    wr_writer = csv.writer(open('../CSV Files/WR_data.csv', 'w'))
    te_writer = csv.writer(open('../CSV Files/TE_data.csv', 'w'))

    qb_writer.writerow(header)
    rb_writer.writerow(header)
    wr_writer.writerow(header)
    te_writer.writerow(header)


def write_csv_data(player_data: dict) -> None:
    ffp = {"QB", "WR", "RB", "TE", "K", "DEF"}  # filters out all not used positional players (OLB, LB, CB, S, so on)
    position = player_data["positionAbbreviation"]
    player_id = player_data["playerID"]
    if position not in ffp:
        return  # the filter process

    path = f"../CSV Files/{position}_data.csv"
    writer = csv.writer(open(path, 'a'))

    # Opens the url to find the number of seasons available
    url = f"https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/athletes/{player_id}/gamelog"
    response = requests.get(url)
    parse_json = json.loads(response.text)

    player_stats = dict()  # creates dictionary for player data
    for item in header:
        player_stats[item] = 0
    # Goes over the years to get the data from every game of their career
    for year in parse_json["filters"][1]["options"]:  # gives access to all years of a current players career
        url += f'?season={year["value"]}'
        response = requests.get(url)
        parse_json = json.loads(response.text)

        for week in parse_json['events']:  # individual games
            this_week = dict(player_stats)  # copy of the base dictionary

            # Time & Team Information
            this_week['season'] = year
            this_week['week'] = parse_json['events'][week]['week']
            this_week['team'] = parse_json['events'][week]['team']['abbreviation']
            this_week['teamID'] = parse_json['events'][week]['team']['id']
            this_week['opponent'] = parse_json['events'][week]['opponent']['abbreviation']
            this_week['teamID'] = parse_json['events'][week]['opponent']['id']

    #     header = [
    #     "name", "playerID", "season", "week", "team", "teamID", "opponent", "opponentID",
    #     "completions", "passingAttempts", "passingYards", "completionPct", "yardsPerPassAttempt", "interceptions",
    #     "longPassing", "sacks", "QBRating", "adjQBR", "rushingAttempts", "rushingYards", "yardsPerRushAttempt",
    #     "rushingTouchdowns", "longRushing", "receptions", "receivingTargets", "receivingYards", "yardsPerReception",
    #     "receivingTouchdowns", "longReception", "fumbles", "fumblesLost",
    # ]

    # ?season=2022"
