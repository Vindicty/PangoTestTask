import os
from pathlib import Path

BASE_DIR = Path(os.getenv("BASE_DIR", Path(__file__).resolve().parent.parent.parent))


# Config file location
CONFIG_FILE = BASE_DIR / "automation_framework" / "config" / "config.ini"

# APK file location
APK_PATH = BASE_DIR / "automation_framework" / "mobile_apps" / "OpenWeather_1.1.7_APKPure.apk"

# DB location
DB_PATH = BASE_DIR / "automation_framework" / "db" / "data.db"

# Test reports location
TEST_REPORTS_PATH = BASE_DIR / "automation_framework" / "tests" / "logs"
