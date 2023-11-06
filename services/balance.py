from external_apis.alfa_requests.fetchers import FetchGroup, FetchCustomer, FetchLesson
from utils.date_utils import curr_date, date_15_days_ago


def get_balance_info_for_last_week():
    current_date = curr_date()
    balance_info = []
    week_ago_date = date_15_days_ago()
    lessons = FetchLesson.by_dates(week_ago_date, current_date)
    unique_child_ids = set()
    if lessons:
        for lesson in lessons:
            lesson_date = lesson.get("date")
            group_id = lesson.get("group_ids")[0]
            group_name = FetchGroup.by_group_id(group_id)[0].get("name")
            for child in lesson.get("details"):
                child_id = child.get("customer_id")
                if not child_id in unique_child_ids:
                    unique_child_ids.add(child_id)
                    child_info = FetchCustomer.by_customer_id(child_id)[0]
                    balance, paid_count, child_name = child_info.get("balance"), child_info.get(
                        "paid_count"), child_info.get(
                        "name")
                    if int(paid_count) <= 1:
                        res = {"group_name": group_name, "lesson_date": lesson_date, "child_name": child_name,
                               "paid_count": paid_count, "balance": balance}
                        balance_info.append(res)
    return balance_info
