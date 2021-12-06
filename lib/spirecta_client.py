import requests
import urllib.parse

class SpirectaClient:
    SPIRECTA_BASE_URL = "https://api.spirecta.com/"
    SPIRECTA_BASE_API_URL = SPIRECTA_BASE_URL + "api/v1/"
    SPIRECTA_TOKEN_URL = SPIRECTA_BASE_URL + "oauth/token"

    def __init__(self, username, password, client_id, client_secret):
        payload = {
            'username': username,
            'password': password,
            'grant_type': 'password',
            'client_id': client_id,
            'client_secret': client_secret}

        response = requests.post(self.SPIRECTA_TOKEN_URL, data = payload)
        response_json = response.json()

        if not response.status_code == 200:
            print(response.content)
            assert(False)
        self.__access_token = response_json['access_token']
        self.__refresh_token = response_json['refresh_token']

    def touch(self):
        self._post_call("me/touch")
        
    def monthly_result_report(self):
        endpoint = "reports/results"
        # Hard-coded range for now..
        vars = {'current_start_date': '2021-11-01',
                'current_end_date': '2021-11-30',
                'previous_start_date': '2020-11-01',
                'previous_end_date': '2020-11-30',
                'locale': 'sv-SE'}
        report = self._get_call(endpoint, vars)
        return report

    def _post_call(self, endpoint):
        endpoint_url = self.SPIRECTA_BASE_API_URL + endpoint

        headers = {'Authorization': 'Bearer {}'.format(self.__access_token)}
        response = requests.post(endpoint_url, headers=headers)
        
        if not response.status_code == 200:
            print(response.content)
            assert(False)

        return response.json()

    def _get_call(self, endpoint, vars = {}):
        vars_url = urllib.parse.urlencode(vars)
        endpoint_url = self.SPIRECTA_BASE_API_URL + endpoint + "?" + vars_url

        headers = {'Authorization': 'Bearer {}'.format(self.__access_token)}
        response = requests.get(endpoint_url, headers=headers)
        
        if not response.status_code == 200:
            print(response.content)
            assert(False)

        return response.json()
