import os
from typing import Any

import requests
import logging

from dotenv import load_dotenv


class AlfaApiFetcher:
    @staticmethod
    def _authenticate():
        auth_url = "https://supra.s20.online/v2api/auth/login"
        auth_data = {"email": os.getenv("ALFA_AUTH_EMAIL"), "api_key": os.getenv("ALFA_AUTH_KEY")}

        try:
            response = requests.post(auth_url, json=auth_data)
            response.raise_for_status()
            return response.json()["token"]
        except requests.exceptions.RequestException as e:
            logging.error(f"Authentication failed: {e}")
            return None

    @staticmethod
    def _make_authenticated_request(token, url, json, params):
        headers = {"X-ALFACRM-TOKEN": token}
        try:
            response = requests.post(url, headers=headers, json=json, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                logging.info("Token expired. Re-authenticating...")
                new_token = AlfaApiFetcher._authenticate()
                if new_token:
                    return AlfaApiFetcher._make_authenticated_request(token=new_token, url=url, json=json,
                                                                      params=params)
                else:
                    logging.error(f"Unable to re-authenticate. Exiting.")
                    return None
            else:
                logging.error(f"Request failed: {e}")
                return None

    @staticmethod
    def fetch_paginated_data(url: str, payload: dict = None, params: dict = None) -> list[Any] | None:
        token = AlfaApiFetcher._authenticate()
        data_list = []
        current_count = 0
        page = 0

        while True:
            if payload:
                payload["page"] = page
            else:
                payload = {"page": page}

            response_data = AlfaApiFetcher._make_authenticated_request(token=token, url=url, json=payload,
                                                                       params=params)
            if not response_data:
                logging.error(f"Request failed. Error for unspecified reasons ")
                return None

            data_list.extend(response_data.get("items"))

            current_count += response_data.get("count")
            if current_count >= response_data.get("total"):
                break

            page += 1

        if len(data_list) != 0:
            return data_list
        else:
            return None

    @staticmethod
    def fetch_paginated_data_with_max_pages_constraints(url: str, max_pages, payload: dict = None, params: dict = None) -> list[Any] | None:
        token = AlfaApiFetcher._authenticate()
        data_list = []
        current_count = 0
        page = 0

        while True:
            if payload:
                payload["page"] = page
            else:
                payload = {"page": page}

            response_data = AlfaApiFetcher._make_authenticated_request(token=token, url=url, json=payload,
                                                                       params=params)
            if not response_data:
                logging.error(f"Request failed. Error for unspecified reasons ")
                return None

            data_list.extend(response_data.get("items"))

            current_count += response_data.get("count")
            if current_count >= response_data.get("total") or page >= max_pages:
                break

            page += 1

        if len(data_list) != 0:
            return data_list
        else:
            return None
# from dotenv import load_dotenv
# load_dotenv()
# d = AlfaApiFetcher.fetch_paginated_data(url="https://supra.s20.online/v2api/customer/index",payload={"id": 2324})
# print(d)
