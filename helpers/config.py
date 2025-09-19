import os
import argparse
from dotenv import load_dotenv
from datetime import datetime, timedelta
from helpers.validators import validate_date 
from typing import Tuple

def read_config() -> Tuple[str,str,str,str]:
    load_dotenv()
    url = os.getenv('HUBSTAFF_API_URL')
    login = os.getenv('HUBSTAFF_EMAIL')
    password = os.getenv('HUBSTAFF_PASSWORD')
    app_token = os.getenv('HUBSTAFF_APP_TOKEN')

    if not all([url, login, password, app_token]):
        raise EnvironmentError("Error: Missing required environment variables HUBSTAFF_API_URL, HUBSTAFF_EMAIL, HUBSTAFF_PASSWORD, HUBSTAFF_APP_TOKEN")
    
    return url, login, password, app_token

# click might be more elegant but for a single action script looks like overkill
def read_args() -> datetime:
    today = datetime.now().date()

    yesterday = today - timedelta(days=1)

    parser = argparse.ArgumentParser(description="Script that accepts date and datetime parameters, with yesterday as default for a date.")

    parser.add_argument(
        "--report_date",
        type=validate_date,
        default=yesterday,
        help="Date for the report in YYYY-MM-DD format"
    )
    args = parser.parse_args()

    return args.report_date