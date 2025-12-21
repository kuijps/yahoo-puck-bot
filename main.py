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
    # get team roster and make it look nicer
    # Prepare data for tabulate
    # table = [
    #     [
    #         p['name'],
    #         p['selected_position'],
    #         ', '.join(p['eligible_positions']),
    #         p['status']
    #     ]
    #     for p in players
    # ]

    # print("Team Roster:" )
    players = team.roster()
    return players


def main():
    lg = get_league()
    tms = lg.teams()

    # Get current date and time and create filename with timestamp
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M")


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
    
   


        # print(f"Roster for team {team_key}:")
        # print(tabulate(roster_table, headers=['Name', 'Selected', 'Eligible', 'Status']))
        # print("\n")

    # use this line later for reporting team names
    # print("Team keys and names:")
    # for k, v in tms.items():
         #print(f"{k}: {v['name']}")
        



    # myteam = get_team(lg)
    
    # # get team roster and make it look nicer
    # players = team.roster()
    # # Prepare data for tabulate
    # table = [
    #     [
    #         p['name'],
    #         p['selected_position'],
    #         ', '.join(p['eligible_positions']),
    #         p['status']
    #     ]
    #     for p in players
    # ]

    # print("Team Roster:" )
    # print(tabulate(table, headers=['Name', 'Selected', 'Eligible', 'Status']))

    # # Find players who are NOT in 'IR' but are in 'IR+'
    # ir_plus_players = [
    #     p for p in players
    # if p['selected_position'] == 'IR+' and 'IR+' not in p['eligible_positions']
    # ]

    # if ir_plus_players:
    #     print("\nPlayers in IR+ that are not eligible!:")
    #     print(tabulate(
    #         [
    #             [
    #                 p['name'],
    #                 p['selected_position'],
    #                 ', '.join(p['eligible_positions']),
    #                 p['status']
    #             ]
    #             for p in ir_plus_players
    #         ],
    #         headers=['Name', 'Selected', 'Eligible', 'Status']
    #     ))
    # else:
    #     print("\All players in IR+ are eligible.")
if __name__ == "__main__": 
    main()