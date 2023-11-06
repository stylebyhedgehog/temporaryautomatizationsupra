from datetime import datetime, timezone, timedelta
from datetime import datetime


def get_month_name(date_str):
    # Convert the string to a datetime object
    date_object = datetime.strptime(date_str, '%Y-%m-%d')

    # Get the month number
    month_number = date_object.month

    # Map the month number to the month name in English
    months = {
        1: 'Январь',
        2: 'Февраль',
        3: 'Март',
        4: 'Апрель',
        5: 'Май',
        6: 'Июнь',
        7: 'Июль',
        8: 'Август',
        9: 'Сентябрь',
        10: 'Октябрь',
        11: 'Ноябрь',
        12: 'Декабрь'
    }

    # Return the month name
    return months.get(month_number)


def next_month(date_str):
    current_date = datetime.strptime(date_str, "%Y-%m")
    next_month_date = current_date + timedelta(days=32)
    next_month_date = next_month_date.replace(day=1)
    return next_month_date.strftime("%Y-%m")


def remove_day(date_str):
    y, m, d = date_str.split("-")
    return y + "-" + m


def curr_date():
    current_date = datetime.now()
    formatted_date = current_date.strftime('%Y-%m-%d')
    return formatted_date


def date_15_days_ago():
    current_date = datetime.now()
    seven_days_ago = current_date - timedelta(days=15)
    formatted_date = seven_days_ago.strftime('%Y-%m-%d')
    return formatted_date


def moscow_to_utc(moscow_date):
    moscow_datetime = datetime.strptime(moscow_date, '%Y-%m-%d %H:%M:%S')

    moscow_timezone = timezone(timedelta(hours=3))
    moscow_datetime = moscow_datetime.replace(tzinfo=moscow_timezone)

    utc_datetime = moscow_datetime.astimezone(timezone.utc)

    utc_date = utc_datetime.strftime('%Y-%m-%d')

    return utc_date
