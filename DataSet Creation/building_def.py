import pandas as pd
import csv
from headers import def_header as header
from write_player_csv import create_cvs


def build_def() -> None:
    csvs = ["../CSV Files/QB_data.csv", "../CSV Files/RB_data.csv", "../CSV Files/WR_data.csv",
            "../CSV Files/TE_data.csv", "../CSV Files/PK_data.csv"]  # All of our player csvs
    create_cvs('DEF')
    teams = dict()

    for pos in csvs:
        position = pos.split('/')[2].split('_')[0]  # Splitting to find our players position
        print(position)
        df = pd.read_csv(pos)

        for index, row in df.iterrows():
            team = row['opponent']
            season = row['season']
            week = row['week']


            if team not in teams:  # Adding the teams
                teams[team] = dict()
            if season not in teams[team]:  # Adding the season
                teams[team][season] = dict()
            if week not in teams[team][season]:  # Adding the week
                teams[team][season][week] = create_def_dict()

            stats = teams[team][season][week]
            stats['team'] = team
            stats['teamID'] = row['teamID']
            stats['season'] = season
            stats['week'] = week
            stats['opponent'] = row['opponent']
            stats['opponentID'] = row['opponentID']
            stats['gameID'] = row['gameID']

            if position == 'QB':  # Adding all relevant QB stats to the DEF
                # print('In QB')
                stats['completions'] = row['completions']
                stats['passingAttempts'] = row['passingAttempts']
                stats['passingYards'] = row['passingYards']
                stats['completionPct'] = row['completionPct']
                stats['interceptions'] = row['interceptions']
                stats['sacks'] = row['sacks']
                stats['yardsPerPassAttempt'] = row['yardsPerPassAttempt']
                try:
                    stats['yardsPerCompletion'] = round(row['passingYards'] / row['completions'], 2)
                except ZeroDivisionError:
                    stats['yardsPerCompletion'] = 0

                stats['passingTouchdowns'] = row['passingTouchdowns']
                add_rushing(row, stats)

            if position == 'RB' or position == 'WR' or position == 'TE':  # Adding all relevant RB, WR or TE stats
                # print('In RB, WR or TE')
                add_rushing(row, stats)
                if row['receivingTouchdowns'] == '-':  # testing null values
                    row['receivingTouchdowns'] = 0
                stats['receivingTouchdowns'] += int(row['receivingTouchdowns'])
                if row['fumbles'] == '-':  # testing null values
                    row['fumbles'] = 0
                stats['fumbles'] += int(row['fumbles'])
                if row['fumblesLost'] == '-':  # testing null values
                    row['fumblesLost'] = 0
                stats['fumblesRecovered'] += int(row['fumblesLost'])

            if position == 'PK':  # Adding all relevant PK stats
                # print('In PK')
                stats["fieldGoalsMade1_19"] = row["fieldGoalsMade1_19-fieldGoalAttempts1_19"].split('-')[0]
                stats["fieldGoalsMade20_29"] = row["fieldGoalsMade20_29-fieldGoalAttempts20_29"].split('-')[0]
                stats["fieldGoalsMade30_39"] = row["fieldGoalsMade30_39-fieldGoalAttempts30_39"].split('-')[0]
                stats["fieldGoalsMade40_49"] = row["fieldGoalsMade40_49-fieldGoalAttempts40_49"].split('-')[0]
                stats["fieldGoalsMade50"] = row["fieldGoalsMade50-fieldGoalAttempts50"].split('-')[0]
                stats["extraPointsMade"] = row["extraPointsMade-extraPointAttempts"].split('-')[0]
                stats["totalKickingPoints"] = row["totalKickingPoints"]

            stats['pointsGivenUp'] = ((stats['rushingTouchdowns'] + stats['receivingTouchdowns']) * 6) + \
                                       stats['totalKickingPoints']

    writer = csv.writer(open('../CSV Files/DEF_data.csv', 'w', newline=''))
    writer.writerow(header)

    for team in teams:

        for season in teams[team]:
            for week in teams[team][season]:
                stats = teams[team][season][week]
                writer.writerow(stats.values())


def create_def_dict() -> dict:  # creating our empty dict
    week_stats = dict()
    for item in header:
        week_stats[item] = 0
    return week_stats


def add_rushing(row: pd.Series, stats: dict) -> None:
    if row['rushingYards'] == '-':  # testing for null values
        row['rushingYards'] = 0
    if row['rushingAttempts'] == '-':
        row['rushingAttempts'] = 0
    if row['rushingTouchdowns'] == '-':
        row['rushingTouchdowns'] = 0

    stats['rushingYards'] += float(row['rushingYards'])  # adding for rushing stats
    stats['rushingAttempts'] += int(row['rushingAttempts'])
    try:
        stats['yardsPerRushAttempt'] = round(stats['rushingYards'] / stats['rushingAttempts'], 2)
    except ZeroDivisionError:
        stats['yardsPerRushAttempt'] = 0

    stats['rushingTouchdowns'] += int(row['rushingTouchdowns'])


build_def()
