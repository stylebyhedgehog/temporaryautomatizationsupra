from external_apis.alfa_requests.template import AlfaApiFetcher


class FetchCustomer:
    @staticmethod
    def by_customer_id(customer_id, with_groups=True):
        url = "https://supra.s20.online/v2api/customer/index"
        payload = {"id": customer_id, "removed": 1, "withGroups": with_groups}

        data = AlfaApiFetcher.fetch_paginated_data(url=url, payload=payload)
        return data


class FetchGroup:
    @staticmethod
    def by_group_id(group_id):
        url = "https://supra.s20.online/v2api/group/index"
        payload = {"id": group_id, "removed": 3}
        data = AlfaApiFetcher.fetch_paginated_data(url=url, payload=payload)
        return data

    @staticmethod
    def all():
        url = "https://supra.s20.online/v2api/group/index"
        payload = {"removed": 3, "status_id": 2}
        data = AlfaApiFetcher.fetch_paginated_data(url=url, payload=payload)
        return data


class FetchLesson:
    @staticmethod
    def by_child_id_group_id_period(child_alfa_id, group_alfa_id, date_from, date_to):
        url = "https://supra.s20.online/v2api/lesson/index"
        payload = {"group_id": group_alfa_id, "customer_id": child_alfa_id,
                   "date_from": date_from, "date_to": date_to}
        data = AlfaApiFetcher.fetch_paginated_data(url=url, payload=payload)
        return data

    @staticmethod
    def by_lesson_id(lesson_id):
        url = "https://supra.s20.online/v2api/lesson/index"
        payload = {"id": lesson_id}

        data = AlfaApiFetcher.fetch_paginated_data(url=url, payload=payload)
        return data

    @staticmethod
    def by_dates(date_from, date_to):
        url = "https://supra.s20.online/v2api/lesson/index"
        payload = {"date_from": date_from, "date_to": date_to, "lesson_type_id": 2, "status": 3}

        data = AlfaApiFetcher.fetch_paginated_data(url=url, payload=payload)
        return data

    @staticmethod
    def by_pages_amount(pages_amount):
        url = "https://supra.s20.online/v2api/lesson/index"

        data = AlfaApiFetcher.fetch_paginated_data_with_max_pages_constraints(url=url, max_pages=pages_amount)

        return data


class FetchSubject:
    @staticmethod
    def by_subject_id(subject_id):
        url = "https://supra.s20.online/v2api/subject/index"
        payload = {"id": subject_id, "active": False}

        data = AlfaApiFetcher.fetch_paginated_data(url=url, payload=payload)
        return data

class FetchRoom:
    @staticmethod
    def all():
        url = "https://supra.s20.online/v2api/room/index"

        data = AlfaApiFetcher.fetch_paginated_data(url=url)
        return data


    @staticmethod
    def get_room_num_by_id(room_id):
        data = FetchRoom.all()
        for room in data:
            if room.get("id") == room_id:
                return int(room.get("name")[1:])
