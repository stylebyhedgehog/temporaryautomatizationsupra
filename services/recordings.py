from external_apis.alfa_requests.fetchers import FetchLesson, FetchCustomer, FetchGroup
from external_apis.zoom.fetchers import FetchRecordings
from utils.date_utils import curr_date, date_seven_days_ago, moscow_to_utc
from utils.string_utils import extract_value_in_brackets


def get_recordings_for_last_week():
    result = []
    current_date = curr_date()
    week_ago_date = date_seven_days_ago()
    lessons = FetchLesson.by_dates(week_ago_date, current_date)
    if lessons:
        for lesson in lessons:
            absent_children_names = []
            for child in lesson.get("details"):
                if child.get("is_attend") == 0:
                    child_id = child.get("customer_id")
                    child_name = FetchCustomer.by_customer_id(child_id)[0].get("name")
                    absent_children_names.append(child_name)
            if len(absent_children_names) > 0:
                lesson_topic = lesson.get("topic")
                group_id = lesson.get("group_ids")[0]
                group_name = FetchGroup.by_group_id(group_id)[0].get("name")
                lesson_room_id = lesson.get("room_id")
                time_from = lesson.get('time_from')
                lesson_date = moscow_to_utc(time_from)
                meetings = FetchRecordings.by_room_id_from_to(lesson_room_id, lesson_date, lesson_date)
                if meetings:
                    recordings= meetings.get("meetings")
                else:
                    continue

                recordings_url_list = []
                for recording in recordings:
                    recording_topic = recording.get('topic')
                    try:
                        recording_group_id = int(extract_value_in_brackets(recording_topic))
                        if recording_group_id == group_id:
                            share_url = recording.get("share_url")
                            passcode = recording.get("recording_play_passcode")
                            recording_url = f"{share_url}?pwd={passcode}"
                            recordings_url_list.append(recording_url)
                    except TypeError as e:
                        print(f"Error in get recordings {e}")
                res_item = {"group_name":group_name,"lesson_date":lesson_date,"lesson_topic":lesson_topic,"children_names":absent_children_names,"recordings_url_list":recordings_url_list}
                result.append(res_item)
    return result



