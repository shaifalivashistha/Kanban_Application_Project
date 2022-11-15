from application.workers import celery
from celery.schedules import crontab

from .send_mail import *


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    dom = 15
    hour = 18
    minute = 27
    sender.add_periodic_task(
        crontab(day_of_month=dom, hour=hour, minute=minute),
        send_summary.s(),
        name="Summary Mail Scheduler",
    )
    sender.add_periodic_task(
        crontab(hour=hour, minute=minute),
        send_reminder.s(),
        name="Daily Reminder",
    )


@celery.task()
def send_summary():
    send()


@celery.task()
def send_reminder():
    remind()


@celery.task()
def trigerred_summary_export(username):
    async_summary_export(username)


@celery.task()
def trigerred_events_export(username, listID):
    async_events_export(username, listID)
