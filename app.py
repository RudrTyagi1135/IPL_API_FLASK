from flask import Flask, jsonify, request
import json

import team_stats
import player_stats

app = Flask(__name__)


@app.route('/')
def home():
    return "IPL Analytics API Running"


@app.route('/api/teams')
def teams():
    return jsonify(team_stats.teamsAPI())


@app.route('/api/teamvteam')
def teamvteam():

    team1 = request.args.get('team1')
    team2 = request.args.get('team2')

    if not team1 or not team2:
        return jsonify({"error": "Please provide team1 and team2"}), 400

    response = team_stats.teamVteamAPI(team1, team2)

    return jsonify(response)


@app.route('/api/team-record')
def team_record():

    team_name = request.args.get('team')

    if not team_name:
        return jsonify({"error": "Please provide team name"}), 400

    response = json.loads(team_stats.team_record_API(team_name))

    return jsonify(response)


@app.route('/api/batting-record')
def batting_record():

    batsman = request.args.get('batsman')

    if not batsman:
        return jsonify({"error": "Provide batsman name"}), 400

    response = json.loads(player_stats.batsmanAPI(batsman))

    return jsonify(response)


@app.route('/api/bowling-record')
def bowling_record():

    bowler = request.args.get('bowler')

    if not bowler:
        return jsonify({"error": "Provide bowler name"}), 400

    response = json.loads(player_stats.bowlerAPI(bowler))

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)