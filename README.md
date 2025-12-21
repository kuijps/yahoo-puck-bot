# yahoo-puck-bot 
this is a blueprint i used to connect to my NHL yahoo fantasy league to do various functions relevant to me and automate decisions I made daily. 

## what it does not have:
- oauth2.json file (you will need to create one in the project folder) : see the yahoo-fantasy-api (Authentication) documentation for setup: https://yahoo-fantasy-api.readthedocs.io/en/latest/authentication.html | Repo: https://github.com/spilchen/yahoo_fantasy_api
- a wrapper or UI: I suggest creating something to run this in a useful way to you. Create a webapp to display the data on load or wrapper that runs it on a schedule. Initailly I chose to wrap the python scripts and use a smtp server to email info daily to help manage my team and strean FAs

## what it does
- gets the nhl scedule for the week and stores in a json and csv format
- connects to your league and runs different functions like get ir cheese and FAs for the week depending on schedule (in progress)

## files

### main.py
This script connects to the Yahoo Fantasy Sports API to analyze and manage NHL fantasy league data. It identifies players improperly placed in the "IR+" position and logs the results.

Key Features:
Yahoo API Integration: Authenticates and retrieves league and team data.
Roster Analysis: Checks if players are incorrectly placed in the "IR+" position.
CSV Output: Saves flagged players to IR-Cheese.csv with details like team name, player name, and status.
Logging: Logs activity to puckBot.log.
Usage:
Run the script to analyze your fantasy league:

### nhlShedule.py 
- gets all games per day on the week - useful for streaming FAs to maximize you're games in a head-to-head league

This file is responsible for fetching, processing, and analyzing NHL team schedules for the current week. It uses the NHL team codes from nhlTeamCodes.py to retrieve and organize schedule data. The script interacts with an NHL API to gather data and generates various outputs for further use.

Key Features:
Fetch Weekly Schedules:

Retrieves the weekly schedule for all NHL teams using the NHL API.
Processes the data to determine game details such as opponents, game days, and whether the game is a home game.
Generate Weekly Insights:

Calculates the total number of games for the week.
Breaks down the number of games played each day of the week.
Data Outputs:

Saves the full weekly schedule in JSON format (schedule.json).
Converts the schedule data into a CSV file (schedule.csv).
Generates a summary of games per day and saves it as a CSV file (games_per_day.csv).
Creates a week_info.json file containing weekly statistics, such as the total number of games and a breakdown of games per day.
Utility Functions:

get_week_start_and_end: Determines the start and end dates of the current week.
get_day_of_week: Converts a date into the corresponding day of the week.
get_team_schedule: Fetches and processes the schedule for a specific team.

Example Usage:
Run the script to fetch and process the current week's NHL schedule:



### nhlTeamCodes.py 
-This file contains a dictionary, NHL_TEAM_CODES, which maps the full names of NHL teams to their corresponding three-letter abbreviations
