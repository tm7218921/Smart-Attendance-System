import schedule
import time
import datetime

def job():
    import BACKEND_LOGIC

def run_on_weekdays():
    if datetime.datetime.today().weekday() < 5:
        job()

schedule.every().day.at("10:15").do(run_on_weekdays)
schedule.every().day.at("10:30").do(run_on_weekdays)
schedule.every().day.at("10:45").do(run_on_weekdays)
schedule.every().day.at("11:15").do(run_on_weekdays)
schedule.every().day.at("11:30").do(run_on_weekdays)
schedule.every().day.at("11:45").do(run_on_weekdays)
schedule.every().day.at("13:15").do(run_on_weekdays)
schedule.every().day.at("13:30").do(run_on_weekdays)
schedule.every().day.at("13:45").do(run_on_weekdays)

while True:
    now = datetime.datetime.now()

    if now.hour >= 14:
        print("It's after 2:00 PM, stopping the scheduler for today.")
        break

    schedule.run_pending()

    time.sleep(60)
