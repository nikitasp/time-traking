import requests
import time 
from requests.exceptions import RequestException
from hubstaff.models import ActivityData, CompanysData, Company

class HubstaffSession(requests.Session):
    def __init__(self, max_retries=3):
        super().__init__()
        self.max_retries = max_retries

    def request(self, method, url, **kwargs):
        retries = 0
        while retries < self.max_retries:
            response = super().request(method, url, **kwargs)
            if response.status_code == 200:
                return response
            elif response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 60))
                time.sleep(retry_after)
                retries += 1
            else:
                response.raise_for_status()
        raise RequestException(f"Max retries exceeded for endpoint '{url}'")
    
class HubstaffClient:
    def __init__(self, url: str, login: str, password: str, app_token: str):

        self.base_url = url
        self.login = login
        self.password = password
        self.headers = {
            'AppToken': app_token
        }

        self.session = HubstaffSession()

    def autentificate(self):
        # POST
        # email formData
        # password formData
        # AppToken header
        response = self.session.post(f'{self.base_url}/employee/auth', headers=self.headers, data={
            'email': self.login,
            'password': self.password,
        })

        self.auth_token = response.json()['auth_token']

    def get_companies(self) -> list[Company]:
        # GET
        #PageStartId (header) Default value : 0
        #page_limit () The default page size
        companies = []
        response = self.session.get(f'{self.base_url}/company', headers=self.headers, params={'auth_token': self.auth_token})

        response_json = response.json()
        companies = response_json

        while 'pagination' in response_json:
            headers = self.headers | {"PageStartId": response_json['pagination']['next_page_start_id']}
            response = self.session.get(f'{self.base_url}/company', headers=headers, params={'auth_token': self.auth_token})
            response_json = response.json()
            companies['organizations'] += response_json['organizations']

        companys_data = CompanysData(**companies)

        return companys_data.organizations

    def get_activities(self, company_id: str | int, date: str) -> ActivityData:
        # GET
        #PageStartId (header) Default value : 0
        #page_limit (query) The default page size
	    #*date[start] (query)
        #*DateStop  (header) Start date (ISO 8601)
        #UserIds array[integer] (header) 
        #task_ids array[integer] (query)
        #project_ids array[integer] (query)
        #include array[string] (query) users, projects, tasks
        #*organization_id (path)
        headers = self.headers | {"DateStop": date}

        activities = {}
        response = self.session.get(
            f'{self.base_url}/company/{company_id}/working/day', 
            headers=headers, 
            params={'auth_token': self.auth_token, 'date[start]': date, 'include': 'users,projects,tasks'}
        )
        response_json = response.json()
        activities = response_json

        while 'pagination' in response_json:
            headers = headers | {"PageStartId": response_json['pagination']['next_page_start_id']}
            response = self.session.get(f'{self.base_url}/company', headers=headers, params={'auth_token': self.auth_token})
            response_json = response.json()
            activities['daily_activities'] += response_json['daily_activities']
            activities['users'] += response_json['users']
            activities['projects'] += response_json['projects']

        return ActivityData(**activities)