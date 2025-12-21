import requests
import json
from nhlTeamCodes import NHL_TEAM_CODES
from datetime import datetime, timedelta
import csv

schedule_data = []

def get_week_start_and_end(date=None):
    if date is None:
        date = datetime.today()

    # monday = 0 , sunday = 6

    start_of_week = date - timedelta(days=date.weekday())
    end_of_week = start_of_week + timedelta(days=6)    

    return start_of_week.strftime("%Y-%m-%d"), end_of_week.strftime("%Y-%m-%d")


def generate_games_per_day():

    weekStart, weekEnd = get_week_start_and_end()    
  
    
    week_info = {
        "weekStart": weekStart,
        "weekEnd": weekEnd,
        "weekTotal": 0
    }

    games_per_day = {
       "Monday": set(),
        "Tuesday": set(),
        "Wednesday": set(),
        "Thursday": set(),
        "Friday": set(),
        "Saturday": set(),
        "Sunday": set()
    }
    with open("data/schedule.json", "r") as f:
        sd = json.load(f)

    for team in sd:
        team_name = team['team']
        for game in team['games']:
            day = game['day']
            opponent = game['opponent']
            # Use a sorted tuple so (A, B) == (B, A)
            matchup = tuple(sorted([team_name, opponent]))
            games_per_day[day].add(matchup)
    # Convert sets to counts
    games_per_day_count = {day: len(matchups) for day, matchups in games_per_day.items()}
    week_info['weekTotal'] = sum(games_per_day_count.values())
    week_info['gamesPerDay'] = games_per_day_count

    # Save week_info to a separate file or handle as needed
    print("Saving week_info.json...")
    with open("data/week_info.json", "w") as f:
        json.dump(week_info, f, indent=4)
    print("Saved week_info.json!")
                
    with open('data/games_per_day.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Day', 'Number of Games'])
        for day, count in games_per_day.items():
            writer.writerow([day, games_per_day_count[day]])

def convert_json_to_csv(json_data):
    # load the JSON data
    with open("data/schedule.json", "r") as f:
        data = json.load(f)

    # Open CSV for writing
    with open("data/schedule.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["team", "day", "opponent", "homeGame"])
        writer.writeheader()

        for team_entry in data:
            team = team_entry["team"]
            for game in team_entry["games"]:
                writer.writerow({
                    "team": team,
                    "day": game["day"],
                    "opponent": game["opponent"],
                    "homeGame": game["homeGame"]
                })


def get_day_of_week(date):
    #find the day of the week
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    day_of_week = date_obj.strftime("%A")
    return day_of_week


def get_team_schedule(thisTeam, date):
    global schedule_data  # This tells Python to use the global variable

    
    url = f"https://api-web.nhle.com//v1/club-schedule/{thisTeam}/week/{date}"
    # url = f"https://api-web.nhle.com//v1/club-schedule/{team}/week/now"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
       
        total_games = len(data['games'])
        
        team_info = {
            "team": thisTeam, 
            "total": total_games, 
            "games": []
        }
        # loops through all the games this team has this week and sets its details.
        for game in data['games']:

            if game['homeTeam']['abbrev'] == thisTeam: # checks to see if this team is home team to set the homegame boolean
                game_info = {
                    "day": get_day_of_week(game['gameDate']), 
                    "opponent": game['awayTeam']['abbrev'],
                    "homeGame": True
                }
            else:
                game_info = {
                    "day": get_day_of_week(game['gameDate']),
                    "opponent": game['homeTeam']['abbrev'],
                    "homeGame": False
                }
                
            team_info["games"].append(game_info)
    
        schedule_data.append(team_info)
        
    
        
def main():
    global schedule_data
    
    # getting the bounds of the current week to pass to get_team_schedule
    weekStart, weekEnd = get_week_start_and_end()
    
    # Collect all team schedules first
    for team_code in NHL_TEAM_CODES.values():
        get_team_schedule(team_code, weekStart)
    
    # Now write the complete schedule_data to schedule.json once
    with open("data/schedule.json", "w") as f:
        json.dump(schedule_data, f, indent=4)
    
    # Now convert to CSV
    convert_json_to_csv(schedule_data)
    
    # Now generate week_info and games_per_day
    generate_games_per_day()


if __name__ == "__main__":
    main()