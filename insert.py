import requests
from cs50 import SQL

db = SQL("sqlite:///premierleague.db")

db.execute("CREATE TABLE IF NOT EXISTS teams (id INTEGER PRIMARY KEY,name TEXT NOT NULL,short_name TEXT NOT NULL,tla TEXT NOT NULL,crest TEXT NOT NULL,address TEXT NOT NULL,website TEXT NOT NULL,founded INTEGER,colors TEXT NOT NULL,venue TEXT NOT NULL,country TEXT);")
db.execute("CREATE TABLE IF NOT EXISTS winners (team_id INTEGER,name TEXT NOT NULL,season INTEGER,FOREIGN KEY (team_id) REFERENCES teams(id));")
db.execute("CREATE INDEX IF NOT EXISTS id_index ON teams (id);")


api_key = '2e2dc554678d49a6a4d4cfef085986ec'
headers = {'X-Auth-Token': api_key}

base_url = 'https://api.football-data.org/v4/competitions/PL'


def add_standing(list):
    for year in list:
        endpoint = "/standings?season=" + str(year)
        response = requests.get(base_url + endpoint, headers=headers)
        if response.status_code == 200:
            fanseason = str(year + 1)
            db.execute("CREATE TABLE IF NOT EXISTS ? (team_id INTEGER,position INTEGER,played INTEGER,won INTEGER,draw INTEGER,lost INTEGER,form TEXT,goalsFor INTEGER,goalsAgainst INTEGER,goalDifference INTEGER,points INTEGER,type TEXT,FOREIGN KEY (team_id) REFERENCES teams(id));",
                       f"stand{fanseason}")
            lines = db.execute("SELECT * FROM ?", f"stand{fanseason}")
            if len(lines) != 0:
                db.execute("DELETE FROM ?", f"stand{fanseason}")
            stand = response.json()["standings"]
            for x in stand:
                type = x["type"]
                for team in x["table"]:
                    db.execute("INSERT INTO ? (team_id,position,played,won,draw,lost,form,goalsFor,goalsAgainst,goalDifference,points,type) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                               f"stand{fanseason}",
                               team["team"]["id"],
                               team["position"],
                               team["playedGames"],
                               team["won"],
                               team["draw"],
                               team["lost"],
                               team["form"],
                               team["goalsFor"],
                               team["goalsAgainst"],
                               team["goalDifference"],
                               team["points"],
                               type)

            print("Data written")
        else:
            print("Error:", response.status_code)
            continue


def add_teams(list):
    for year in list:
        endpoint = "/teams?season=" + str(year)
        response = requests.get(base_url + endpoint, headers=headers)
        if response.status_code == 200:
            teams = response.json()["teams"]
            for team in teams:
                lines = db.execute("SELECT * FROM teams WHERE id = ?", team["id"])
                if len(lines) == 0:
                    db.execute("INSERT INTO teams (id,name,short_name,tla,crest,address,website,founded,colors,venue,country) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                               team["id"],
                               team["name"],
                               team["shortName"],
                               team["tla"],
                               team["crest"],
                               team["address"],
                               team["website"],
                               team["founded"],
                               team["clubColors"],
                               team["venue"],
                               team["area"]["name"])
                else:
                    continue

            print("Data written")
        else:
            print("Error:", response.status_code)
            continue


def add_winners(list):
    for year in list:
        endpoint = "/standings?season=" + str(year)
        response = requests.get(base_url + endpoint, headers=headers)
        if response.status_code == 200:
            lines = db.execute("SELECT * FROM winners WHERE season = ?", year + 1)
            if len(lines) != 0:
                continue
            country = response.json()["area"]["name"]
            winner = response.json()["season"]["winner"]
            if winner:
                if len(db.execute("SELECT * FROM teams WHERE id = ?", winner["id"])) == 1:
                    db.execute("INSERT INTO winners (team_id,name,season) VALUES (?,?,?)",
                            winner["id"],
                            winner["name"],
                            year + 1)
                else:
                    db.execute("INSERT INTO teams (id,name,short_name,tla,crest,address,website,founded,colors,venue,country) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                               winner["id"],
                               winner["name"],
                               winner["shortName"],
                               winner["tla"],
                               winner["crest"],
                               winner["address"],
                               winner["website"],
                               winner["founded"],
                               winner["clubColors"],
                               winner["venue"],
                               country)
                    db.execute("INSERT INTO winners (team_id,name,season) VALUES (?,?,?)",
                            winner["id"],
                            winner["name"],
                            year + 1)

            print("Data written")
        else:
            print("Error:", response.status_code)
            continue


def premier_winners():
    response = requests.get(base_url, headers=headers)
    if response.status_code == 200:
        # to add first premier league winner manually
        db.execute("INSERT INTO winners (team_id,name,season) VALUES (?,?,?)", 66, "Manchester United FC", 1993)
        seasons = response.json()["seasons"]
        for i in range(30, 0, -1):
            year = int(seasons[i]["endDate"].split("-")[0])
            winner = seasons[i]["winner"]
            if len(db.execute("SELECT * FROM teams WHERE id = ?", winner["id"])) == 1:
                    db.execute("INSERT INTO winners (team_id,name,season) VALUES (?,?,?)",
                            winner["id"],
                            winner["name"],
                            year)
            else:
                db.execute("INSERT INTO teams (id,name,short_name,tla,crest,address,website,founded,colors,venue,country) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                            winner["id"],
                            winner["name"],
                            winner["shortName"],
                            winner["tla"],
                            winner["crest"],
                            winner["address"],
                            winner["website"],
                            winner["founded"],
                            winner["clubColors"],
                            winner["venue"],
                            "England")
                db.execute("INSERT INTO winners (team_id,name,season) VALUES (?,?,?)",
                        winner["id"],
                        winner["name"],
                        year)

            print("Data written")
    else:
        print("Error:", response.status_code)


def fan_season(season):
    season = int(season)
    fan = str(season) + "/" + str(season + 1)
    return fan


if __name__ == "__main__":
    add_teams([x for x in range(2020,2024)])
    premier_winners()
    add_standing([x for x in range(2020,2023)])
