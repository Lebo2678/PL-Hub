# Premier League Hub

#### Video Demo: https://youtu.be/Nonr6AWM6HA

#### Description:
This is a web application that provides information about the Premier League, including team standings, fixtures, and match details. The application is built using the Flask web framework and SQLite database. It utilizes live data to display current standings, match schedules, and other related information.

## Project Overview

At its core, the Premier League Web Application offers a user-friendly interface for accessing essential Premier League information. The application provides several key functionalities:

- **Main Page:** The index route (`/`) serves as the main page of the application. It displays the current standings of the Premier League, upcoming fixtures, and basic season information. Users can quickly get an overview of how their favorite teams are performing and which matches are on the horizon.

- **Team Details:** The team route (`/team=<int:id>`) provides comprehensive details about a specific team. This includes information about the competitions the team is participating in, the coach leading the team, and the squad members who make up the team's roster.

- **Upcoming Fixtures:** The fixtures route (`/fixtures`) presents users with a list of upcoming fixtures. Users can also select a specific gameweek to view the matches scheduled for that week. This feature allows fans to plan their match-watching schedules ahead of time.

- **Match Details:** The match route (`/match=<int:id>`) offers users detailed information about a specific match. This includes the teams competing, the scores, the stadium where the match is played, and the referees overseeing the game.

- **Past Winners:** The winners route (`/winners`) displays a list of past Premier League season winners, along with information about their respective teams. This feature provides users with historical context about the league's most successful teams.

## Files and Functionality

### `templates/`: HTML templates for different views.

### `static/`: CSS and JavaScript files for styling and interactivity.

### `app.py`
This is the main application file that serves as the core of the web application. It includes the Flask routes to handle various functionalities.

- **Index Route (`/`):** Displays the main page with current standings, upcoming fixtures, and basic season information.

- **Team Route (`/team=<int:id>`):** Displays details about a specific team, including competitions, coach, and squad information.

- **Fixtures Route (`/fixtures`):** Displays a list of upcoming fixtures or allows users to select a specific gameweek to view its matches.

- **Match Route (`/match=<int:id>`):** Displays detailed information about a specific match, including teams, scores, and stadium.

- **Winners Route (`/winners`):** Displays a list of past season winners along with their team information.

### `insert.py`
This file contains functions to insert data into the SQLite database, including teams, standings, winners, and more.

- **`add_teams(list)`:** Adds teams to the database for the specified seasons. Fetches team information using the Football Data API and populates the 'teams' table.

- **`add_standing(list)`:** Adds standings data to the database for the specified seasons. Fetches standings information using the Football Data API and populates the corresponding 'stand' tables.

- **`add_winners(list)`:** Adds winners of each season to the database. Fetches winner information using the Football Data API and adds them to the 'winners' table.

- **`premier_winners()`:** Adds historical winners of the Premier League seasons to the database. Manually adds the first winner and uses the Football Data API to populate the rest.

- **`fan_season(season)`:** A custom filter to format the season into the "fan" style (e.g., "2020/2021").

- **`__main__`:** Calls the necessary functions to populate the database with team, standings, and winner data for specific seasons.

This `insert.py` file is crucial for initializing and updating the data in your database. It fetches information from the Football Data API and populates the necessary tables to ensure your web application has accurate and up-to-date data for teams, standings, and winners.

### `live.py`
Contains functions to fetch live data related to standings, teams, matches, and match details.

- **`live_standing()`:** Fetches and returns live standing data for the Premier League. Retrieves information such as the current season, start and end dates, winner, current matchday, and standings for teams.

- **`live_matches()`:** Retrieves live match data for the Premier League. Retrieves details such as the current season, number of played matches, current matchday, start and end dates of the match data, and a list of upcoming matches.

- **`live_team(team)`:** Fetches live data for a specific team. Provides details such as the team's running competitions, coach information, and squad members.

- **`live_match(match)`:** Fetches detailed live data for a specific match. Retrieves information about the match's date, status, matchday, teams playing, scores, and referees.

These functions utilize the Football Data API to provide real-time information to your web application users, ensuring that they are always presented with the latest standings, match schedules, team details, and match specifics.

## Design Choices

- The application is built using Flask, providing a lightweight and efficient web framework.
- SQLite is used as the database to store data about teams, standings, and winners.
- Live data fetching functions are implemented in `live.py` to ensure up-to-date information for users.
- The application employs user-friendly routes to navigate between different sections of the website.

## Usage

1. The home page provides an overview of the current season's standings.
2. Use the dropdown menus to select a specific season, type of standing (total, home, away), and gameweek to view relevant data.
3. Navigate to team pages to learn more about a specific team, including squad and competitions.
4. Check the fixtures page to see upcoming match fixtures and details.
5. Access match pages to view specific match details and venue information.
6. The winners page displays a list of teams that have won the Premier League in past seasons.

## Technologies Used

- Python
- Flask
- SQLite
- CS50 Library
- HTML/CSS
- Jinja2 (templating engine)

## Future Enhancements

- Additional pages for detailed player statistics and historical data.
- User authentication to allow personalized experiences, such as saving favorite teams.
- Enhanced styling and user interface improvements.

Feel free to explore the code and the various routes to understand how the application works. If you have any questions or suggestions, please feel free to reach out!

## Acknowledgments

This project is inspired by the passion for the Premier League and the desire to create a user-friendly platform for fans to access relevant information.
