from datetime import datetime

def write_log(user, action, target):
    with open("logs/activity.log", "a") as f:
        f.write(f"{datetime.now()} | {user} | {action} | {target}\n")
