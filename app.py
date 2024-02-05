from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request


from insert import add_winners, add_teams, add_standing, fan_season
from live import live_standing, live_team, live_matches, live_match

# Configure application
app = Flask(__name__)
app.secret_key = 'password123'

app.jinja_env.filters["fan"] = fan_season

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///premierleague.db")

c_season = 2023
seasons = [x for x in range(2020,2023)]
types = ["TOTAL", "HOME", "AWAY"]
gameweeks = [x for x in range(1,39)]


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    global c_season
    if request.method == "POST":
        if request.form.get("season") == str(c_season):
            standing = live_standing()
            if request.form.get("type") == "TOTAL":
                redirect("/")
            elif request.form.get("type") == "HOME":
                if len(standing["standing"]) >= 2:
                    return render_template("index.html", standing=standing["standing"][1]["table"], c_season=standing["season"], start=standing["start"], end=standing["end"], seasons=seasons)
                else:
                    flash("There is no Home standing for this season yet", 'warning')
                    return redirect("/")
            else:
                if len(standing["standing"]) >= 3:
                    return render_template("index.html", standing=standing["standing"][2]["table"], c_season=standing["season"], start=standing["start"], end=standing["end"], seasons=seasons)
                else:
                    flash("There is no Away standing for this season yet", 'warning')
                    return redirect("/")
        elif int(request.form.get("season")) in seasons:
            standing = db.execute("SELECT s.*,t.name,t.short_name,t.tla,t.crest FROM ? s JOIN teams t ON s.team_id = t.id WHERE s.type = ?;",
                                  "stand" + str(int(request.form.get("season")) + 1),
                                  request.form.get("type"))
            return render_template("stand.html", standing=standing, c_season=c_season, seasons=seasons, s_season=int(request.form.get("season")), s_type=request.form.get("type"), types=types)

    else:
        standing = live_standing()
        if standing["winner"] and standing["season"] not in seasons:
            add_winners([c_season])
            add_standing([c_season])
            seasons.append(c_season)
        if standing["season"] != c_season:
            c_season = standing["season"]
            add_teams([c_season])
        return render_template("index.html", standing=standing["standing"][0]["table"], c_season=standing["season"], start=standing["start"], end=standing["end"], seasons=seasons, s_season=standing["season"], matchday=standing["matchday"], s_type="TOTAL", types=types)


@app.route("/team=<int:id>")
def team(id):
    team = db.execute("SELECT * FROM teams WHERE id = ?", id)[0]
    l_team = live_team(id)
    return render_template("team.html", team=team, competitions=l_team["competitions"], coach=l_team["coach"], squad=l_team["squad"])


@app.route("/fixtures", methods=["GET", "POST"])
def fixtures():
    if request.method == "POST":
        matches = live_matches()
        gw = int(request.form.get("GW"))
        gw_matches = []
        for i in range(((gw - 1) * 10), (gw * 10)):
            gw_matches.append(matches["matches"][i])
        return render_template("fixtures.html", c_season=matches["season"], start=matches["start"], end=matches["end"], s_GW=gw, gameweeks=gameweeks, gw_matches=gw_matches)
    else:
        matches = live_matches()
        gw = matches["matchday"]
        gw_matches = []
        for i in range(((gw - 1) * 10), (gw * 10)):
            gw_matches.append(matches["matches"][i])
        return render_template("fixtures.html", c_season=matches["season"], start=matches["start"], end=matches["end"], played=matches["played"], s_GW=gw, gameweeks=gameweeks, gw_matches=gw_matches)


@app.route("/match=<int:id>")
def match(id):
    match = live_match(id)
    home_id = match["homeTeam"]["id"]
    stadium = db.execute("SELECT venue FROM teams WHERE id = ?", home_id)[0]["venue"]
    return render_template("match.html", match=match, stadium=stadium)


@app.route("/winners")
def winner():
    winners = db.execute("SELECT w.*,t.short_name,t.crest FROM winners w JOIN teams t ON w.team_id = t.id ORDER BY season DESC;")
    return render_template("winners.html", winners=winners)
