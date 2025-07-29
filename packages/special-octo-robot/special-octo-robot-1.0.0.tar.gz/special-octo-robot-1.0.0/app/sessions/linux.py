import json
import os
import signal
import sys
import tempfile
from datetime import datetime
from multiprocessing import Process

from ewmh import EWMH
from Xlib import display
from Xlib import X
from Xlib.protocol.event import PropertyNotify


def start_logging(file_handle: str):

    # Dictionary to store window name and active time
    activity = {}

    def trim_spaces_from_list(lst):
        return [item.strip() for item in lst if item.strip()]

    # Connect to the X server
    disp = display.Display()
    root = disp.screen().root
    ewmh = EWMH(disp)

    # Listen for property changes on the root window
    root.change_attributes(event_mask=X.PropertyChangeMask)

    # Key to get active window event
    NET_ACTIVE_WINDOW = disp.intern_atom("_NET_ACTIVE_WINDOW")

    last_window = ewmh.getActiveWindow()
    last_window_name = ewmh.getWmName(last_window)
    if isinstance(last_window_name, bytes):
        last_window_name = last_window_name.decode("utf-8")
    last_window_id = last_window.id
    last_switch_time = datetime.now()
    activity[last_window.id] = {
        "time": 0,
        "name_list": trim_spaces_from_list(list(last_window_name.split("-"))),
    }

    def add_time_to_current_window():
        current_time = datetime.now()
        name_list = trim_spaces_from_list(list(last_window_name.split("-")))
        if activity.get(last_window_id, None):
            activity[last_window_id]["time"] += (
                current_time - last_switch_time
            ).total_seconds()
            new_name_list = []
            for item in activity[last_window_id]["name_list"]:
                if item in name_list:
                    new_name_list.append(item)
            activity[last_window_id]["name_list"] = new_name_list
        else:
            activity[last_window_id] = {
                "time": (current_time - last_switch_time).total_seconds(),
                "name_list": name_list,
            }

    def handle_exit(signum, frame):
        try:
            add_time_to_current_window()
            with open(file_handle, "w+") as f:
                json.dump(activity, f, indent=4)
            print(f"Successfully captured session data.")
        except Exception as e:
            print(f"Failed to capturing session data: {e}")
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    while True:
        event = disp.next_event()
        if isinstance(event, PropertyNotify) and event.atom == NET_ACTIVE_WINDOW:

            active_window = ewmh.getActiveWindow()
            window_name = ewmh.getWmName(active_window)
            if isinstance(window_name, bytes):
                window_name = window_name.decode("utf-8")

            if active_window and active_window.id > 0 and window_name:
                add_time_to_current_window()
                if (datetime.now() - last_switch_time).total_seconds() > 30:
                    with open(file_handle, "w+") as f:
                        json.dump(activity, f, indent=4)

                last_window = active_window
                last_window_name = ewmh.getWmName(last_window)
                if isinstance(last_window_name, bytes):
                    last_window_name = last_window_name.decode("utf-8")
                last_window_id = last_window.id
                last_switch_time = datetime.now()


def session_start():
    # Create and start a process for start_logging
    tmp = tempfile.NamedTemporaryFile(delete=False)
    logging_process = Process(target=start_logging, args=(tmp.name,))
    logging_process.start()
    return logging_process.pid, tmp.name  # Return the process ID


def session_end(pid):
    try:
        os.kill(pid, signal.SIGTERM)
        return True, ""
    except ProcessLookupError:
        return False, None
    except Exception as e:
        return False, str(e)
