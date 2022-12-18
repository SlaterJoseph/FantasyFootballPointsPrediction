base_header = ["name", "playerID", "gameID", "season", "week", "team", "teamID", "opponent", "opponentID"]

qb_header = list(base_header)
qb_header.extend(
    ["completions", "passingAttempts", "passingYards", "completionPct", "yardsPerPassAttempt",
     "passingTouchdowns", "interceptions", "longPassing", "sacks", "QBRating", "adjQBR", "rushingAttempts",
     "rushingYards", "yardsPerRushAttempt", "rushingTouchdowns", "longRushing"])

rb_header = list(base_header)
rb_header.extend(
    ["rushingAttempts", "rushingYards", "yardsPerRushAttempt", "rushingTouchdowns", "longRushing", "receptions",
     "receivingTargets", "receivingYards", "yardsPerReception", "receivingTouchdowns", "longReception",
     "fumbles", "fumblesLost"])

wr_header = list(base_header)
wr_header.extend(
    ["receptions", "receivingTargets", "receivingYards", "yardsPerReception", "receivingTouchdowns",
     "longReception", "rushingAttempts", "rushingYards", "yardsPerRushAttempt", "longRushing",
     "rushingTouchdowns", "fumbles", "fumblesLost"])

te_header = list(base_header)
te_header.extend(
    ["receptions", "receivingTargets", "receivingYards", "yardsPerReception", "receivingTouchdowns",
     "longReception", "rushingAttempts", "rushingYards", "yardsPerRushAttempt", "longRushing",
     "rushingTouchdowns", "fumbles", "fumblesLost"])

k_header = list(base_header)
k_header.extend(
    ["fieldGoalsMade1_19-fieldGoalAttempts1_19", "fieldGoalsMade20_29-fieldGoalAttempts20_29",
     "fieldGoalsMade30_39-fieldGoalAttempts30_39", "fieldGoalsMade40_49-fieldGoalAttempts40_49",
     "fieldGoalsMade50-fieldGoalAttempts50", "longFieldGoalMade", "fieldGoalPct",
     "fieldGoalsMade-fieldGoalAttempts", "fieldGoalsMadeYardsAverage", "extraPointsMade-extraPointAttempts",
     "totalKickingPoints"])

def_header = ["team", "teamID", "gameID", "season", "week", "opponent", "opponentID",
              "completions", "passingAttempts", "passingYards", "completionPct", "yardsPerPassAttempt",
              "yardsPerCompletion", "passingTouchdowns", "interceptions", "sacks", "rushingYards", "rushingAttempts",
              "yardsPerRushAttempt", "rushingTouchdowns", "receivingTouchdowns", "fumbles", "fumblesRecovered",
              "fieldGoalsMade1_19", "fieldGoalsMade20_29", "fieldGoalsMade30_39", "fieldGoalsMade40_49",
              "fieldGoalsMade50", "extraPointsMade", "totalKickingPoints"]

headers = {"QB": qb_header, "RB": rb_header, "WR": wr_header, "TE": te_header, "PK": k_header, "DEF": def_header}
