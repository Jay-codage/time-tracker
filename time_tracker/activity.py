from __future__ import print_function
import pyautogui
from timmer import *
import json
from datetime import datetime,timedelta
import sys
import time
from PIL import Image


global last_move
last_move = time.time()

def user_activity():
    if sys.platform in ['windows', 'win32', 'cygwin']:
        import win32gui
        import uiautomation as auto

    elif sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
        import UIkit
        # from foundation import *
    elif sys.platform in ['linux', 'liunx2']:
        import psutil

    active_window_name = ''
    activity_name = ''
    start_time = datetime.now()
    activeList = ActivityList([])
    first_time = True

    def url_to_name(url):
        straing_list = url.split('/')
        return straing_list[2]

    def get_active_window():
        _active_window_name = None
        if sys.platform in ['windows', 'win32', 'cygwin']:
            window = win32gui.GetForegroundWindow()
            _active_window_name = win32gui.GetWindowText(window)
        elif sys.platform in ['Mac', 'darwin', 'os2']:
            _active_window_name = (UIkit.sharedWorkspace().activeApplication()['NSApplicationName'])

        else:
            print('sys.platform={platform} is not supported.'
                  .format(platform=sys.platform))
            print(sys.version)
        return _active_window_name

    def get_chrome_url():
        if sys.platform in ['windows', 'win32', 'cygwin']:
            window = win32gui.GetForegroundWindow()
            chromeControl = auto.ControlFromHandle(window)
            edit = chromeControl.EditControl()
            return 'https://' + edit.GetValuePattern().Value

        elif sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
            textofmyScript = """tell app "google chrome" to get the url of the active tab of window 1"""
            s = NSAppleScript.initwithSource_(
                NSAppleScript.alloc(), textofmyScript
            )
            results, err = s.executeAndTurnError_(None)
            return results.stringValue()

        else:
            print('sys.platform = {platform} is not supported'
                  .format(platform=sys.platform))
            print(sys.version)
        return _active_window_name

    try:
        activeList.initialize_me()
    except Exception:
        print('No json')

    try:
        i = 1
        while True:
            # print('Taking Screenshot...')
            screenshot = pyautogui.screenshot("E:/screenshots/image-" + str(i) + ".JPEG")
            img = Image.open("E:/screenshots/image-" + str(i) + ".JPEG")
            screenshot_re = img.resize((1000, 500), Image.Resampling.LANCZOS)
            screenshot_re.save("E:/screenshots/image-" + str(i) + ".JPEG", optimize=True, quality=75)
            # print("Screenshot taken...")
            i += 1
            previous_site = ""
            if sys.platform not in ['linux', 'linux2']:
                new_window_name = get_active_window()
                if 'Google Chrome' in new_window_name:
                    new_window_name = url_to_name(get_chrome_url())
            if sys.platform in ['linux', 'linux2']:
                new_window_name = psutil.get_active_window_x()
                if 'Google Chrome' in new_window_name:
                    new_window_name = psutil.get_chrome_url_x()

            if active_window_name != new_window_name:
                print(active_window_name)
                activity_name = active_window_name

                if not first_time:
                    end_time = datetime.now()
                    time_entry = TimeEntry(start_time, end_time, 0, 0, 0, 0, user_end_time)
                    time_entry._get_specific_times()

                    exists = False
                    for activity in activeList.activities:
                        if activity.name == activity_name:
                            exists = True
                            activity.time_entries.append(time_entry)

                    if not exists:
                        activity = Activity(activity_name, [time_entry], )
                        activeList.activities.append(activity)
                    with open('activities.json', 'w') as json_file:
                        json.dump(activeList.serialize(), json_file, indent=4, sort_keys=True)
                        start_time = datetime.now()
                first_time = False
                active_window_name = new_window_name

            time.sleep(1)
            user_end_time = datetime.now()

    except KeyboardInterrupt:
        with open('activities.json', 'w') as json_file:
            json.dump(activeList.serialize(), json_file, indent=4, sort_keys=True)


