def get_off_days(weekinfo):
    games_per_day = weekinfo["gamesPerDay"]

    # Filter out days with zero games
    non_zero_days = {day: count for day, count in games_per_day.items() if count > 0}

    # Sort remaining days by game count ascending
    sorted_days = sorted(non_zero_days.items(), key=lambda x: x[1])

    # Pick the 3 lowest-volume days (or fewer if week is weird)
    off_days = [day for day, count in sorted_days[:3]]

    return off_days



def count_offday_games(schedule, off_days):
    """
    schedule: list of team entries from schedule.json
    off_days: list of strings like ["Monday", "Wednesday", "Friday"]

    Returns a list of dicts:
    [
        { "team": "ANA", "offdayGames": 3, "totalGames": 4 },
        { "team": "BOS", "offdayGames": 1, "totalGames": 4 },
        ...
    ]
    """
    results = []

    for team_entry in schedule:
        team = team_entry["team"]
        games = team_entry["games"]

        # Count how many games fall on off-days
        offday_count = sum(1 for g in games if g["day"] in off_days)

        results.append({
            "team": team,
            "offdayGames": offday_count,
            "totalGames": team_entry["total"]
        })

    return results

def rank_teams_by_offdays(results):
    """
    Sort teams by number of off-day games (descending).
    results: list of dicts like:
        { "team": "ANA", "offdayGames": 2, "totalGames": 4 }

    Returns a sorted list.
    """
    return sorted(results, key=lambda x: x["offdayGames"], reverse=True)

def analyze_offday_value(weekinfo, schedule):
    """
    Combine all steps:
    1. Determine off-days from weekinfo
    2. Count off-day games for each team
    3. Rank teams by off-day value

    Returns a JSON-ready dict.
    """
    off_days = get_off_days(weekinfo)
    results = count_offday_games(schedule, off_days)
    ranked = rank_teams_by_offdays(results)

    return {
        "offDays": off_days,
        "rankedTeams": ranked
    }
