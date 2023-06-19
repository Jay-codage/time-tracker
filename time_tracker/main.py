import requests
import json
from datetime import datetime, timedelta
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
import time
from activity import user_activity
import threading

global total_start_time
total_start_time = datetime.now()

global last_move
last_move = time.time()


def on_press(key):
    global last_move
    last_move = time.time()


def on_move(x, y):
    global last_move
    last_move = time.time()


# global list

inactive_time_slot = []
inactive_time_dic = []


def time_tracker():
    while True:
        if time.time() - last_move > 3:
            start_time = datetime.now()
            print("system is not working")
            while time.time() - last_move > 3:
                time.sleep(0.1)
            print("System is working")

            # inactive_time_slot

            end_time = datetime.now()
            total_time = end_time - start_time
            time1 = datetime.strptime(str(start_time), "%Y-%m-%d %H:%M:%S.%f")
            time2 = datetime.strptime(str(end_time), "%Y-%m-%d %H:%M:%S.%f")
            total_user_time = time2 - timedelta(hours=time1.hour, minutes=time1.minute, seconds=time1.second)
            step_inactive = total_user_time.strftime("%H:%M:%S")
            # print(step_inactive)

            # convert in json

            time_slot = {
                'inactive_start_time': start_time.strftime("%Y-%m-%d %H:%M:%S"),
                'inactive_end_time': end_time.strftime("%Y-%m-%d %H:%M:%S"),
                'inactive_time': step_inactive,
            }

            inactive_time_slot.append(step_inactive)
            time_slot.update()
            inactive_time_dic.append(time_slot)
            inactive = inactive_time_dic
            save_file = open('inactive_time_slot.json', 'w')
            json.dump(inactive, save_file, indent=2)
            save_file.close()
            # print(inactive_time_slot)

            # inactive time

            totalsec = 0
            for tm in inactive_time_slot:
                timeparts = [int(s) for s in tm.split(':')]
                totalsec += (timeparts[0] * 60 + timeparts[1] * 60 + timeparts[2])
            totalsec, sec = divmod(totalsec, 60)
            hr, min = divmod(totalsec, 60)
            total_inactive_time = (("%d:%02d:%02d") % (hr, min, sec))

            # total_time

            total_end_time = datetime.now()
            time3 = datetime.strptime(str(total_start_time), "%Y-%m-%d %H:%M:%S.%f")
            time4 = datetime.strptime(str(total_end_time), "%Y-%m-%d %H:%M:%S.%f")
            total_user_time = time4 - timedelta(hours=time3.hour, minutes=time3.minute, seconds=time3.second)
            total_time_spend = total_user_time.strftime("%H:%M:%S")

            # active time

            time5 = datetime.strptime(str(total_inactive_time), "%H:%M:%S")
            time6 = datetime.strptime(str(total_time_spend), "%H:%M:%S")
            total_user_time = time6 - timedelta(hours=time5.hour, minutes=time5.minute, seconds=time5.second)
            total_active_time = total_user_time.strftime("%H:%M:%S")

            # json data

            user_time_slot = {
                'start_time': total_start_time.strftime("%Y-%m-%d %H:%M:%S"),
                'end_time': total_end_time.strftime("%Y-%m-%d %H:%M:%S"),
                'total_time': total_time_spend,
                'total_inactive_time': total_inactive_time,
                'total_active_time': total_active_time,
            }

            save_files = open('user_time.json', 'w')
            json.dump(user_time_slot, save_files, indent=2)
            save_files.close()


last_move = time.time()

keyboard_listener = KeyboardListener(on_press=on_press)
mouse_listener = MouseListener(on_move=on_move)

keyboard_listener.start()
mouse_listener.start()

main = threading.Thread(target=time_tracker)
timmer = threading.Thread(target=user_activity)
main.start()
timmer.start()

keyboard_listener.join()
mouse_listener.join()
