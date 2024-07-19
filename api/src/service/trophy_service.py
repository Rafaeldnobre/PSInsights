import requests
import json
from pandas import json_normalize
import pandas as pd
from api.src.auth import get_authentication_token
from api.constants.api_constants import TROPHY_BASE

class TrophyService():
    """
    Class to manage all of the trophy api related services
    """
    def __init__(self, npsso, user_id) -> None:
        self.npsso = npsso
        self.user_id = user_id
        self.get_auth()

    def get_auth(self):
        self.token = get_authentication_token(self.npsso)

    def get_trophies(self):
        """
        Gets trophy for the user_id

        Args:
            user_id str: psn username that will have the trophies request
        """
        my_trophies_url = TROPHY_BASE + self.user_id + '/trophyTitles'

        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.get(my_trophies_url, headers=headers)
        return response

    def trophies_to_df(self):
        trophies = self.get_trophies()
        trophies_json = trophies.json()
        with open('response_json','w') as file:
            json.dump(trophies_json, file, indent=4)

        trophies_df = json_normalize(
            trophies_json['trophyTitles']
            )
        
        desired_columns = [
            'trophyTitleName', 
            'trophyGroupCount', 
            'progress', 
            'definedTrophies.bronze', 
            'definedTrophies.silver', 
            'definedTrophies.gold', 
            'definedTrophies.platinum', 
            'earnedTrophies.bronze', 
            'earnedTrophies.silver', 
            'earnedTrophies.gold', 
            'earnedTrophies.platinum'
            ]
        trophies_df = trophies_df[desired_columns]
        return trophies_df