import platform
import time
from datetime import datetime
from datetime import timedelta

from click import echo
from click import style


def convert_time_to_epoch(time_str, eod=True):
    if time_str in ("None", None):
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


def convert_epoch_to_date(epoch_time):
    if epoch_time == 0:
        return "None"
    try:
        date_obj = datetime.fromtimestamp(epoch_time)
        return date_obj.strftime("%d-%m-%Y")
    except Exception as e:
        return e.__str__()


def convert_epoch_to_datetime(epoch_time):
    if epoch_time == 0:
        return "None"
    try:
        date_obj = datetime.fromtimestamp(epoch_time)
        return date_obj.strftime("%H:%M, %-d/%-m/%Y")
    except Exception:
        return "invalid"


def convert_seconds_delta_to_time(seconds):
    seconds = int(seconds)
    hrs = seconds // 3600
    mins = (seconds % 3600) // 60
    secs = seconds % 60
    parts = []
    if hrs > 0:
        parts.append(f"{hrs} hrs")
    if mins > 0:
        parts.append(f"{mins} mins")
    if secs > 0 or not parts:
        parts.append(f"{secs} secs")
    return ", ".join(parts)


def sanitize_text(text):
    return text.strip().replace("'", '"')


def generate_migration_error():
    display_error_message(
        "Have You Run Migrations? Run 'devcord init --migrate' to run migrations",
    )


def display_error_message(message: str):
    """
    Display an error message in red style with an error prefix.
    """
    echo(
        style(
            f"Error: {message}",
            fg="red",
        ),
    )


def display_info_message(message: str):
    """
    Display an informational message in green style with an info prefix.
    """
    echo(
        style(
            f"Info: {message}",
            fg="yellow",
        ),
    )


def display_success_message(message: str):
    """
    Display a success message in green style with a success prefix.
    """
    echo(
        style(
            f"Success: {message}",
            fg="green",
        ),
    )


def sanitize_table_name(table_name: str) -> (str, bool):  # type: ignore
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


def get_relative_date_string(relative_days: int) -> str:
    """
    Get the date string for today + relative_days.

    Args:
        relative_days (int): Number of days relative to today. Can be positive or negative.

    Returns:
        str: Date string in the format "dd-mm-yyyy".
    """
    target_date = datetime.now() + timedelta(days=relative_days)
    return target_date.strftime("%d-%m-%Y")


def check_if_relative_deadline(deadline: str) -> str:
    if deadline[0] == "+" or deadline[0] == "-":
        if deadline[1:].isdigit():
            deadline = get_relative_date_string(int(deadline))
        else:
            display_error_message("Example: '+4'")
            return False
    return deadline


def get_os():
    system = platform.system()
    if system == "Linux":
        return "Linux"
    elif system == "Darwin":
        return "MacOS"
    elif system == "Windows":
        return "Windows"
    else:
        return "Unknown"
