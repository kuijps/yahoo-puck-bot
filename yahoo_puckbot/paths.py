from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent

SECRETS_PATH = PACKAGE_ROOT / "secrets" / "oauth2.json"

DATA_DIR = PACKAGE_ROOT / "data"
LOG_DIR = DATA_DIR / "log"
LOG_FILE = LOG_DIR / "puckbot.log"

IR_CHEESE_FILE = DATA_DIR / "IR-Cheese.csv"
GAMES_PER_DAY_FILE = DATA_DIR / "games_per_day.csv"
OFFDAY_ANALYSIS_FILE = DATA_DIR / "offday_analysis.csv"
OFFDAYS_FILE = DATA_DIR / "offdays.json"
WEEK_INFO_FILE = DATA_DIR / "week_info.json"
SCHEDULE_FILE = DATA_DIR / "schedule.csv"
SCHEDULE_DATA_FILE = DATA_DIR / "schedule.json"

# Ensure directories exist
LOG_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

