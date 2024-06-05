import requests
from django.conf import settings


class Samplers:
    def __init__(self, api_url=settings.SD_API_URL + "sdapi/v1/samplers"):
        self.api_url = api_url

    def get_samplers(self):
        try:
            response = requests.get(self.api_url, headers={"accept": "application/json"})

            if response.status_code == 200:
                response_data = response.json()
                return response_data
            else:
                print(f"Failed to fetch samplers. Status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None

