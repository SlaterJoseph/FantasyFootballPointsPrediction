import csv
import requests
import json
from headers import headers as hd
from time import sleep


# header = [
#     "name", "playerID", "gameID", "season", "week", "team", "teamID", "opponent", "opponentID",
#     "completions", "passingAttempts", "passingYards", "completionPct", "yardsPerPassAttempt", "interceptions",
#     "longPassing", "sacks", "QBRating", "adjQBR", "rushingAttempts", "rushingYards", "yardsPerRushAttempt",
#     "rushingTouchdowns", "longRushing", "receptions", "receivingTargets", "receivingYards", "yardsPerReception",
#     "receivingTouchdowns", "longReception", "fumbles", "fumblesLost",
# ]


def write_players(items: list) -> None:
    """Function for creating player_data csv"""
    header = ["fullName", "playerID", "teamName", "teamID", "positionName", "positionID", "positionAbbreviation",
              "gameIDs", "headshotURL"]

    writer = csv.writer(open('../CSV Files/players_data.csv', 'w', newline=''))

    writer.writerow(header)
    i = 0

    writer = csv.writer(open('../CSV Files/players_data.csv', 'a', newline=''))
    for entry in items:  # looping through players
        i += 1

        if i % 250 == 0:
            print('100 Seconds Sleep')  # to prevent calling the API to often and being locked out
            sleep(100)

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

        print(i, player_info)  # for progress tracking
        # player_info_list.append(player_info)
        writer.writerow(player_info)

    # writer.writerows(player_info_list)  # add all players to csv


def write_csv_data(player_data: dict) -> None:
    ffp = {"QB", "WR", "RB", "TE", "PK", "DEF"}  # filters out all not used positional players (OLB, LB, CB, S, so on)
    not_ffp = {'C', 'G', 'OT', 'P', 'DT', 'CB', 'P', 'FB', 'LB', 'S', 'DE', 'LS'}
    position = player_data["positionAbbreviation"]
    player_id = player_data["playerID"]

    if position not in ffp:
        return  # the filter process

    if position in not_ffp:
        return  # the filter process part 2

    header = hd[position]

    path = f"../CSV Files/{position}_data.csv"
    writer = csv.writer(open(path, 'a', newline=''))

    # Opens the url to find the number of seasons available
    url = f"https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/athletes/{player_id}/gamelog?league=nfl"
    response = requests.get(url)
    parse_json = json.loads(response.text)

    player_stats = dict()  # creates dictionary for player data
    for item in header:  # is some values do not exist we want them to be null
        player_stats[item] = 0

    # Goes over the years to get the data from every game of their career
    try:
        for year in parse_json["filters"][1]["options"]:  # gives access to all years of a current players career
            print(year['value'])
            url += f'&season={year["value"]}'
            response = requests.get(url)
            parse_json = json.loads(response.text)

            game_stats = dict()
            # we need to set up our player statistics to correlate to gameIDs
            try:
                for entry in parse_json['seasonTypes']:  # gameStats
                    for part in entry['categories']:
                        for game in part['events']:
                            game_stats[game['eventId']] = game['stats']

                stat_values = parse_json['names']  # stats value's correlating category

                for week in parse_json['events']:  # individual games
                    this_week = dict(player_stats)  # copy of the base dictionary

                    # Non Player Statistic Information
                    this_week["name"] = player_data["fullName"]
                    this_week["playerID"] = player_data["playerID"]
                    this_week['gameID'] = week
                    this_week['season'] = year['value']
                    this_week['week'] = parse_json['events'][week]['week']
                    this_week['team'] = parse_json['events'][week]['team']['abbreviation']
                    this_week['teamID'] = parse_json['events'][week]['team']['id']
                    this_week['opponent'] = parse_json['events'][week]['opponent']['abbreviation']
                    this_week['opponentID'] = parse_json['events'][week]['opponent']['id']

                    this_game_stats = game_stats[week]
                    for i in range(len(stat_values)):
                        this_week[stat_values[i]] = this_game_stats[i]

                    # create a dictionary connecting stat categories to statistic values
                    # print(week['stats'])
                    #     print(this_week)
                    #     print("----------")
                    row = [this_week[x] for x in header]
                    writer.writerow(row)

            except KeyError as ke:
                print('KeyError', ke)
                continue

            url = f"https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/athletes/{player_id}/gamelog?league=nfl"
    except IndexError as ie:
        print('Index Error', ie)
        return
