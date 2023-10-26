import base64
import os

import requests


class ZoomApiFetcher:
    TOKEN = ""
    @staticmethod
    def _authenticate():
        auth_url = "https://zoom.us/oauth/token"
        params = {"grant_type": "account_credentials", "account_id":os.getenv("ZOOM_ACCOUNT_ID")}
        username = os.getenv("ZOOM_CLIENT_ID")
        password = os.getenv("ZOOM_CLIENT_SECRET")
        auth_string = f"{username}:{password}"
        base64_auth_string = base64.b64encode(auth_string.encode()).decode('utf-8')

        headers = {
            'Authorization': f'Basic {base64_auth_string}',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        print("Zoom auth call")
        response = requests.post(auth_url, params=params, headers=headers)
        response.raise_for_status()
        token = response.json()["access_token"]
        ZoomApiFetcher.TOKEN = token
        return token

    @staticmethod
    def make_authenticated_request(url, params, token=None):
        if token:
            headers = {"Authorization": f"Bearer {token}"}
        else:
            headers = {"Authorization": f"Bearer {ZoomApiFetcher.TOKEN}"}
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                new_token = ZoomApiFetcher._authenticate()
                if new_token:
                    return ZoomApiFetcher.make_authenticated_request(token=new_token, url=url, params=params)
                else:
                    return None
            else:
                return None