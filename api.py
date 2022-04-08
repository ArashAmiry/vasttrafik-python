import base64
import json
import requests
from global_url import *

def fetch_token(key,secret):
    # Every client using the api needs to pass a valid authentication key in every request.
    # How to generate token: https://developer.vasttrafik.se/portal/#/guides/oauth2

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic " + base64.b64encode((AUTH_KEY + ":" + AUTH_SECRET).encode()).decode()
    }

    data = {
        'grant_type': 'client_credentials'
    }

    serverData = requests.post(TOKEN_URL, data=data, headers=headers)

    # decode data to readable dictionary
    serverData = json.loads(serverData.content.decode('UTF-8'))
    return serverData["access_token"]

class API:

    def __init__(self):
        self.__authentication = fetch_token(AUTH_KEY, AUTH_SECRET)
        self.__format = "&format=json"

    def requestHTTP(self, location, querys=None):
        # Requests can only be made with GET

        headers = {
            "Authorization": "Bearer " + self.__authentication
        }

        url = BASE_URL + location

        if "?" not in url:
            url += "?"

        if querys is not None:
            for queryKey in querys:
                url += "&" + queryKey + "=" + str(querys[queryKey])

        url += "&" + self.__format

        response = requests.get(url, headers=headers)
        response = json.loads(response.content.decode('UTF-8'))
        return response
