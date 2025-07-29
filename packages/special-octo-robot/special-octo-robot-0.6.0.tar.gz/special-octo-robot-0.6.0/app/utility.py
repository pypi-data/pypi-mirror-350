import time
from datetime import datetime
from datetime import timedelta

from click import echo
from click import style


def convert_time_to_epoch(time_str, eod=True):
    if time_str == "None":
        return 0
    separator_list = [":", ".", "-", "/", "\\", "|", "_", ","]
    for separator in separator_list:
        if separator in time_str:
            date_list = time_str.split(separator)
            break
    else:
        return "No separator found"
    if len(date_list) != 3:
        return "Length not 3"

    if len(date_list[0]) != 4:
        date_list = date_list[::-1]

    if eod == True:
        hr = 23
        minute = 59
        sec = 59
    else:
        hr = 0
        minute = 0
        sec = 0

    try:
        date_obj = datetime(
            int(date_list[0]),
            int(date_list[1]),
            int(date_list[2]),
            hour=hr,
            minute=minute,
            second=sec,
        )
        epoch_time = int(time.mktime(date_obj.timetuple()))
        return epoch_time
    except Exception as e:
        return e.__str__()


def convert_epoch_to_time(epoch_time):
    if epoch_time == 0:
        return "None"
    try:
        date_obj = datetime.fromtimestamp(epoch_time)
        return date_obj.strftime("%d-%m-%Y")
    except Exception as e:
        return e.__str__()


def sanitize_text(text):
    return text.strip().replace("'", '"')


def generate_migration_error():
    echo(
        style(
            "Have You Run Migrations? Run 'devcord init --migrate' to run migrations",
            fg="red",
        ),
    )


def sanitize_table_name(table_name: str) -> (str, bool):
    for ch in table_name:
        if ch.isalnum() or ch == " " or ch == "_":
            continue
        else:
            return "", False

    return table_name.replace(" ", "_"), True


def get_weekend() -> str:
    """
    Get the date of the current week's end (Sunday).
    """
    today = datetime.now()
    days_until_sunday = 6 - today.weekday()
    sunday = today + timedelta(days=days_until_sunday)
    return sunday.strftime("%d-%m-%Y")


def get_week_start() -> str:
    """
    Get the date of the current week's start (Monday).
    """
    today = datetime.now()
    days_since_monday = today.weekday()
    monday = today - timedelta(days=days_since_monday)
    return monday.strftime("%d-%m-%Y")
