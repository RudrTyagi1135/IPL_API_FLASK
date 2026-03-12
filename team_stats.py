import json
from data_loader import matches


def teamsAPI():
    teams = sorted(list(set(matches['Team1']).union(set(matches['Team2']))))
    return {'teams': teams}


def teamVteamAPI(team1, team2):

    valid_teams = teamsAPI()['teams']

    if team1 not in valid_teams or team2 not in valid_teams:
        return {'message': 'Invalid team name'}

    temp_df = matches[
        ((matches['Team1'] == team1) & (matches['Team2'] == team2)) |
        ((matches['Team1'] == team2) & (matches['Team2'] == team1))
    ]

    total_matches = temp_df.shape[0]

    matches_won_team1 = temp_df['WinningTeam'].value_counts().get(team1, 0)
    matches_won_team2 = temp_df['WinningTeam'].value_counts().get(team2, 0)

    draws = total_matches - (matches_won_team1 + matches_won_team2)

    return {
        'total_matches': total_matches,
        team1: matches_won_team1,
        team2: matches_won_team2,
        'draws': draws
    }


def team1vsteam2(team, team2):

    df = matches[
        ((matches['Team1'] == team) & (matches['Team2'] == team2)) |
        ((matches['Team2'] == team) & (matches['Team1'] == team2))
    ]

    mp = df.shape[0]
    won = df[df.WinningTeam == team].shape[0]
    nr = df[df.WinningTeam.isnull()].shape[0]
    loss = mp - won - nr

    return {
        'matchesplayed': mp,
        'won': won,
        'loss': loss,
        'noResult': nr
    }


def allRecord(team):

    df = matches[(matches['Team1'] == team) | (matches['Team2'] == team)]

    mp = df.shape[0]
    won = df[df.WinningTeam == team].shape[0]
    nr = df[df.WinningTeam.isnull()].shape[0]
    loss = mp - won - nr

    nt = df[(df.MatchNumber == 'Final') & (df.WinningTeam == team)].shape[0]

    return {
        'matchesplayed': mp,
        'won': won,
        'loss': loss,
        'noResult': nr,
        'title': nt
    }


def team_record_API(team):

    self_record = allRecord(team)

    TEAMS = matches.Team1.unique()

    against = {team2: team1vsteam2(team, team2) for team2 in TEAMS}

    data = {
        team: {
            'overall': self_record,
            'against': against
        }
    }

    return json.dumps(data)