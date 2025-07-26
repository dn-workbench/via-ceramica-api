from apscheduler.schedulers.background import BackgroundScheduler
from parser import parse_xml

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(parse_xml, 'interval', minutes=5)
    scheduler.start()
