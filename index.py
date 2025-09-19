import sys
import logging
from argparse import ArgumentTypeError
from requests import RequestException
from pydantic import ValidationError
 
from hubstaff.api import HubstaffClient
from hubstaff.transformers import agregate_activities, generate_html_table
from helpers.config import read_config, read_args


def main():
    url, login, password, app_token = read_config()
    report_date = read_args()

    client = HubstaffClient(url, login, password, app_token)
    client.autentificate()

    companies = client.get_companies()
    activities = []
    users = []
    projects = []
    for company in companies:
        daily_activities = client.get_activities(company.id, report_date.strftime("%Y-%m-%d"))
        activities += daily_activities.daily_activities
        users += daily_activities.users
        projects += daily_activities.projects

    agregated_activities = agregate_activities(activities)

    report_table = generate_html_table(agregated_activities, users, projects, report_date.strftime("%Y-%m-%d"))

    print(report_table)        

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr, level=logging.WARN)
    logger = logging.getLogger(__name__)
    try:
        main()
    except RequestException as e:
        logger.error(e)
    except ValidationError as e:
        logger.error(e)    
    except EnvironmentError as e:
        logger.error(e)
    except ArgumentTypeError as e:
        logger.error(e)
    except Exception as e:
        logger.exception(e)