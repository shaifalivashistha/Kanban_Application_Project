from application.workers import celery
from celery.schedules import crontab

from .send_mail import *


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    dom = 30
    hour = 23
    minute = 30
    sender.add_periodic_task(
        crontab(day_of_month=dom, hour=hour, minute=minute),
        celery_summary_export.s(),
        name="Create A Report",
    )
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
def celery_summary_export():
    export()


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
