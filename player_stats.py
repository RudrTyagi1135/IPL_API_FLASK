import pandas as pd
import numpy as np
import json
from data_loader import matches, balls


class NpEncoder(json.JSONEncoder):

    def default(self, obj):

        if isinstance(obj, np.integer):
            return int(obj)

        if isinstance(obj, np.floating):
            return float(obj)

        if isinstance(obj, np.ndarray):
            return obj.tolist()

        return super().default(obj)


ball_withmatch = balls.merge(matches, on='ID', how='inner').copy()

ball_withmatch['BowlingTeam'] = ball_withmatch.Team1 + ball_withmatch.Team2

ball_withmatch['BowlingTeam'] = ball_withmatch[['BowlingTeam', 'BattingTeam']].apply(
    lambda x: x.values[0].replace(x.values[1], ''), axis=1
)

batter_data = ball_withmatch[np.append(balls.columns.values, ['BowlingTeam', 'Player_of_Match'])]


def batsmanRecord(batsman, df):

    df = df[df['batter'] == batsman]

    out = df[df.player_out == batsman].shape[0]
    inngs = df.ID.unique().shape[0]
    runs = df.batsman_run.sum()

    fours = df[(df.batsman_run == 4) & (df.non_boundary == 0)].shape[0]
    sixes = df[(df.batsman_run == 6) & (df.non_boundary == 0)].shape[0]

    avg = runs / out if out else np.inf

    nballs = df[~(df.extra_type == 'wides')].shape[0]
    strike_rate = runs / nballs * 100 if nballs else 0

    gb = df.groupby('ID').sum(numeric_only=True)

    fifties = gb[(gb.batsman_run >= 50) & (gb.batsman_run < 100)].shape[0]
    hundreds = gb[gb.batsman_run >= 100].shape[0]

    highest_score = gb.batsman_run.max()

    not_out = inngs - out

    mom = df[df.Player_of_Match == batsman].drop_duplicates('ID').shape[0]

    return {
        'innings': inngs,
        'runs': runs,
        'fours': fours,
        'sixes': sixes,
        'avg': avg,
        'strikeRate': strike_rate,
        'fifties': fifties,
        'hundreds': hundreds,
        'highestScore': highest_score,
        'notOut': not_out,
        'mom': mom
    }


def batsmanVsTeam(batsman, team, df):

    df = df[df.BowlingTeam == team]

    return batsmanRecord(batsman, df)


def batsmanAPI(batsman):

    df = batter_data[batter_data.innings.isin([1, 2])]

    self_record = batsmanRecord(batsman, df)

    TEAMS = matches.Team1.unique()

    against = {team: batsmanVsTeam(batsman, team, df) for team in TEAMS}

    data = {
        batsman: {
            'all': self_record,
            'against': against
        }
    }

    return json.dumps(data, cls=NpEncoder)


bowler_data = batter_data.copy()


def bowlerRun(x):

    if x[0] in ['penalty', 'legbyes', 'byes']:
        return 0

    return x[1]


bowler_data['bowler_run'] = bowler_data[['extra_type', 'total_run']].apply(bowlerRun, axis=1)


def bowlerWicket(x):

    if x[0] in ['caught', 'caught and bowled', 'bowled', 'stumped', 'lbw', 'hit wicket']:
        return x[1]

    return 0


bowler_data['isBowlerWicket'] = bowler_data[['kind', 'isWicketDelivery']].apply(bowlerWicket, axis=1)


def bowlerRecord(bowler, df):

    df = df[df['bowler'] == bowler]

    inngs = df.ID.unique().shape[0]

    nballs = df[~(df.extra_type.isin(['wides', 'noballs']))].shape[0]

    runs = df['bowler_run'].sum()

    eco = runs / nballs * 6 if nballs else 0

    wicket = df.isBowlerWicket.sum()

    avg = runs / wicket if wicket else np.inf

    strike_rate = nballs / wicket if wicket else np.nan

    gb = df.groupby('ID').sum(numeric_only=True)

    w3 = gb[(gb.isBowlerWicket >= 3)].shape[0]

    best_wicket = gb.sort_values(
        ['isBowlerWicket', 'bowler_run'],
        ascending=[False, True]
    )[["isBowlerWicket", "bowler_run"]].head(1).values

    best_figure = f"{best_wicket[0][0]}/{best_wicket[0][1]}" if best_wicket.size else np.nan

    mom = df[df.Player_of_Match == bowler].drop_duplicates('ID').shape[0]

    return {
        'innings': inngs,
        'wicket': wicket,
        'economy': eco,
        'average': avg,
        'strikeRate': strike_rate,
        'best_figure': best_figure,
        '3+W': w3,
        'mom': mom
    }


def bowlerVsTeam(bowler, team, df):

    df = df[df.BattingTeam == team]

    return bowlerRecord(bowler, df)


def bowlerAPI(bowler):

    df = bowler_data[bowler_data.innings.isin([1, 2])]

    self_record = bowlerRecord(bowler, df)

    TEAMS = matches.Team1.unique()

    against = {team: bowlerVsTeam(bowler, team, df) for team in TEAMS}

    data = {
        bowler: {
            'all': self_record,
            'against': against
        }
    }

    return json.dumps(data, cls=NpEncoder)