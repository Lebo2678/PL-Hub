import requests

api_key = '2e2dc554678d49a6a4d4cfef085986ec'
headers = {'X-Auth-Token': api_key}

base_url = 'https://api.football-data.org/v4'

def live_standing():
    endpoint = "/competitions/PL/standings"
    response = requests.get(base_url + endpoint, headers=headers)
    if response.status_code == 200:
        season = int(response.json()["filters"]["season"])
        start = response.json()["season"]["startDate"]
        end = response.json()["season"]["endDate"]
        winner = response.json()["season"]["winner"]
        matchday = response.json()["season"]["currentMatchday"]
        standing = response.json()["standings"]
        return {
            "season": season,
            "start": start,
            "end": end,
            "winner": winner,
            "matchday": matchday,
            "standing": standing
            }


def live_matches():
    endpoint = "/competitions/PL/matches"
    response = requests.get(base_url + endpoint, headers=headers)
    if response.status_code == 200:
        season = int(response.json()["filters"]["season"])
        played = response.json()["resultSet"]["played"]
        matchday = response.json()["matches"][0]["season"]["currentMatchday"]
        start = response.json()["resultSet"]["first"]
        end = response.json()["resultSet"]["last"]
        matches = response.json()["matches"]
        return {
            "season": season,
            "played": played,
            "matchday": matchday,
            "start": start,
            "end": end,
            "matches": matches
        }


def live_team(team):
    endpoint = f"/teams/{team}"
    response = requests.get(base_url + endpoint, headers=headers)
    if response.status_code == 200:
        competitions = response.json()["runningCompetitions"]
        coach = response.json()["coach"]
        squad = response.json()["squad"]
        return {
            "competitions": competitions,
            "coach": coach,
            "squad": squad
        }


def live_match(match):
    endpoint = f"/matches/{match}"
    response = requests.get(base_url + endpoint, headers=headers)
    if response.status_code == 200:
        date = response.json()["utcDate"]
        status = response.json()["status"]
        matchday = response.json()["matchday"]
        homeTeam = response.json()["homeTeam"]
        awayTeam = response.json()["awayTeam"]
        score = response.json()["score"]
        referees = response.json()["referees"]
        return {
            "date": date,
            "status": status,
            "matchday": matchday,
            "homeTeam": homeTeam,
            "awayTeam": awayTeam,
            "score": score,
            "referees": referees,
        }
