from external_apis.alfa_requests.fetchers import FetchLesson, FetchGroup, FetchCustomer, FetchSubject
from utils.date_utils import get_month_name, remove_day, next_month, curr_date, date_15_days_ago


def get_reports_for_last_week():
    current_date = curr_date()
    reports = []
    week_ago_date = date_15_days_ago()
    lessons = FetchLesson.by_dates(week_ago_date, current_date)
    if lessons:
        for lesson in lessons:
            children_list = lesson.get("details")
            if is_children_contains_feedback(children_list):
                group_id = lesson.get("group_ids")[0]

                groups = FetchGroup.by_group_id(group_id)

                if groups is None:
                    continue
                group_name = groups[0].get("name")

                subject_id = lesson.get("subject_id")
                subjects = FetchSubject.by_subject_id(subject_id)
                if subjects is None:
                    continue
                subject_name = ""
                for subject in subjects:
                    if subject.get("id") == subject_id:
                        subject_name = subject.get("name")
                date = lesson.get("date")
                month_name = get_month_name(date)
                date_from = remove_day(date)

                for child_info in children_list:
                    note = child_info.get("note")
                    if len(note)>1 and note.lower().startswith("ос") :
                        child_id = child_info.get("customer_id")
                        customers = FetchCustomer.by_customer_id(child_id)
                        if customers is None:
                            continue
                        customer_info = customers[0]
                        child_name = customer_info.get("name")
                        parent_name = customer_info.get("legal_name")
                        body = form_body(child_id, group_id, date_from)
                        if body is None:
                            continue
                        topic_perf, lessons_amount, attd_lessons_amount, average_attendance, average_grade = body

                        full_text = form_full_report_text(parent_name, child_name, month_name, lessons_amount,
                                                          subject_name,
                                                          average_attendance,
                                                          attd_lessons_amount, topic_perf, note[3:])
                        result = {"group_name": group_name, "child_name": child_name, "parent_name": parent_name,
                                  "date": date,
                                  "full_text": full_text}
                        reports.append(result)
        return reports


def is_children_contains_feedback(details):
    for detail in details:
        note = detail.get("note")
        if len(note)>1 and note.lower().startswith("ос"):
            return True
    return False


def form_body(child_alfa_id, child_group_alfa_id, date_from):
    data = FetchLesson.by_child_id_group_id_period(child_alfa_id, child_group_alfa_id, date_from,
                                                   next_month(date_from))
    if data:
        topic_perf = ""
        lessons_amount = 0
        attd_lessons_amount = 0
        summary_grade = 0
        average_attendance, average_grade = 0, 0
        for lesson_info in data:
            topic = lesson_info.get("topic")

            for child_info in lesson_info.get("details"):
                if child_info.get("customer_id") == child_alfa_id:
                    lessons_amount += 1
                    is_attend = child_info.get("is_attend")
                    if is_attend == 1:
                        attd_lessons_amount += 1
                        grade = child_info.get("grade")
                        if grade is not None:
                            grade = float(grade.replace(",", "."))
                            topic_perf += f"\n▪️{topic} - {grade}%"
                            summary_grade += grade
                    else:
                        topic_perf += f"\n▪️{topic} - Пропущено"
        if lessons_amount > 0:
            average_attendance = int((attd_lessons_amount / lessons_amount) * 100)
        if attd_lessons_amount > 0:
            average_grade = int(summary_grade / attd_lessons_amount)
        return topic_perf, lessons_amount, attd_lessons_amount, average_attendance, average_grade
    return None


def form_full_report_text(parent_name, child_name, month_name, lessons_amount, subject_name, attendance_rate,
                          attendance_amount, topic_perf, teacher_feedback):
    result = f"""
Добрый день! Будем рады поделиться промежуточными результатами обучения за {month_name.lower()}.
"""
    if "АЯ" not in subject_name:
        result+= f"\n📝 У нас прошло {lessons_amount} занятий в рамках курса {subject_name[3:]}."
    else:
        result += f"\n📝 У нас прошло {lessons_amount} занятий."


    result+=f"\n📊 Посещаемость - {attendance_rate}% ({attendance_amount}/{lessons_amount})"


    if "АЯ" not in subject_name:
        result+= "\n\n📖 В рамках блока занятий освоены следующие темы:\n"
        result += topic_perf
    result += f"""
    
Преподаватель отмечает, что {teacher_feedback} 

🏆 Будем благодарны за оценку нашей образовательной услуги в прошлом месяце: от 0 до 10 (где 0 - совсем не понравилось, 10 - все отлично, пожеланий нет).
Мы всегда открыты к вашим вопросам и пожеланиям по процессу обучения! 

С уважением, команда онлайн-академии Supra
         """
    return result