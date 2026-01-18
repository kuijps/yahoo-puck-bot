import logging
from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
import json
from tabulate import tabulate
from config import LEAGUE_ID
from config import LOG_PATH
import csv
import datetime
import os
from analysis.offday_analysis import analyze_offday_value
from nhlSchedule import get_weekly_schedule
from nhlSchedule import generate_games_per_day


os.makedirs(LOG_PATH, exist_ok=True)


# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s',
    #filename='data/log/puckBot.log',      # Log file in project folder
    filename=os.path.join(LOG_PATH, 'puckBot.log'),
    filemode='a'                   # Append to the log file
)
logger = logging.getLogger(__name__)

def get_league():
    #connect to yahoo api
    sc = OAuth2(None, None, from_file='data/oauth2.json')
    logger.info("Connected to Yahoo API")
    #get game object 
    gm = yfa.Game(sc, 'nhl')
    # uncomment the below 3 lines to get league ids printed to the console - use these for getting the league object
    #leagues = gm.league_ids()
    #print(leagues)
    #exit()
   
    # get the league object
    lg = gm.to_league(LEAGUE_ID)
    return lg

def get_myteam(lg):
    #get my team key and create the team object
    teamkey = lg.team_key()
    team = lg.to_team(teamkey)
    return team
  

def get_Roster(team):

    players = team.roster()
    return players

def get_ir_cheese(lg,tms,timestamp):
    with open('data/IR-Cheese.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write header row
        writer.writerow(['Team Name', 'Player Name', 'Selected Position', 'Eligible Positions', 'Status','Date'])

        for team_key in tms.keys():
            team = lg.to_team(team_key)
            roster = get_Roster(team)
            
            for player in roster:
                if player['selected_position'] == 'IR+' and 'IR+' not in player['eligible_positions']:
                    writer.writerow([
                        tms[team_key]['name'],
                        player['name'],
                        player['selected_position'],
                        player['eligible_positions'],
                        'CHEESED',
                        timestamp
                    ])  
                else:
                    print(f"{player['name']} is correctly placed in {player['selected_position']} and status is {player['status']}")

def get_best_free_agents():
    
    '''
    
    generate_games_per_day()

    with open("data/week_info.json") as f:
        weekinfo = json.load(f)

    #print(weekinfo)
    '''
    schedule = get_weekly_schedule()
    weekinfo = generate_games_per_day(schedule)
    
    analysis = analyze_offday_value(weekinfo, schedule)

    print(json.dumps(analysis, indent=4))
    
    # create offday top availablility teams csv report
    with(open('data/offday_analysis.csv', 'w', newline='') as csvfile):
        writer = csv.writer(csvfile)
        # Write header row
        writer.writerow(['Team', 'Offday Games', 'Total Games'])

        for entry in analysis['rankedTeams']:
            writer.writerow([entry["team"], entry["offdayGames"], entry["totalGames"]])

    # create offdays csv report
    with(open('data/offdays.csv', 'w', newline='') as csvfile):
        writer = csv.writer(csvfile)
        # Write header row
        writer.writerow(['Off Days'])

        for day in analysis['offDays']:
            writer.writerow([day])





def main():
    # get the yahoo league and teams in league
    lg = get_league()
    tms = lg.teams()

    # Get current date and time and create filename with timestamp
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M")

    get_ir_cheese(lg,tms,timestamp)
    
    get_best_free_agents()
      
    

if __name__ == "__main__": 
    main()