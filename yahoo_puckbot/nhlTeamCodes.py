# nhl_team_codes.py

NHL_TEAM_CODES = {
    "Anaheim": "ANA",
    "Boston": "BOS",
    "Buffalo": "BUF",
    "Calgary": "CGY",
    "Carolina": "CAR",
    "Chicago": "CHI",
    "Colorado": "COL",
    "Columbus": "CBJ",
    "Dallas": "DAL",
    "Detroit": "DET",
    "Edmonton": "EDM",
    "Florida": "FLA",
    "Los Angeles": "LAK",
    "Minnesota": "MIN",
    "Montreal": "MTL",
    "Nashville": "NSH",
    "New Jersey": "NJ",
    "NY Islanders": "NYI",
    "NY Rangers": "NYR",
    "Ottawa": "OTT",
    "Philadelphia": "PHI",
    "Pittsburgh": "PIT",
    "San Jose": "SJ",
    "Seattle": "SEA",
    "St. Louis": "STL",
    "Tampa Bay": "TB",
    "Toronto": "TOR",
    "Utah": "UTA",
    "Vancouver": "VAN",
    "Vegas": "VGK",
    "Washington": "WSH",
    "Winnipeg": "WPG"
}

NHL_CODE_TO_TEAM = {code: team for team, code in NHL_TEAM_CODES.items()}

def get_team_code(team_name):
    return NHL_TEAM_CODES.get(team_name)

def get_team_name(team_code):
    return NHL_CODE_TO_TEAM.get(team_code)  