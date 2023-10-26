from external_apis.zoom.template import ZoomApiFetcher


class FetchRecordings:
    @staticmethod
    def by_room_id_from_to(room_id,date_from,date_to):
        url = f"https://api.zoom.us/v2/users/supra.{room_id}@supraschool.ru/recordings"
        params = {"from": date_from, "to":date_to}

        data = ZoomApiFetcher.make_authenticated_request(url=url, params=params)
        return data