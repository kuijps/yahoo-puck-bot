import logging
from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
import json
from tabulate import tabulate
import csv
import datetime
import os

# Global Variables
league_id = "465.l.34586"

log_path = '/root/yahoo-puckBot/data/log'
os.makedirs(log_path, exist_ok=True)


# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s',
    #filename='data/log/puckBot.log',      # Log file in project folder
    filename=os.path.join(log_path, 'puckBot.log'),
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
    lg = gm.to_league(league_id)
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

def main():
    # get the yahoo league and teams in league
    lg = get_league()
    tms = lg.teams()

    # Get current date and time and create filename with timestamp
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M")

    get_ir_cheese(lg,tms,timestamp)

       
    

if __name__ == "__main__": 
    main()