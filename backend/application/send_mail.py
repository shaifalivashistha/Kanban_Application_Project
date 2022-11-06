import os
import csv
import smtplib
from time import time
from datetime import date

from jinja2 import Template
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from weasyprint import HTML
from flask import current_app as app

from .models import Logs, TrackerLog, User, Tracker, UserTracker


def export():
    fname = f"ExportedSummary_{str(date.today())}.csv"
    user_list = User.query.all()
    tracker_header = ["Name", "Date Created", "Description", "Type"]
    for user in user_list:
        usr_pth = f"/home/shaifali/Downloads/Mad2_Data/{user.username}"
        if not os.path.exists(usr_pth):
            os.makedirs(usr_pth)
        tIDs = (
            UserTracker.query.with_entities(UserTracker.tID)
            .filter(UserTracker.uID == user.id)
            .all()
        )
        with open(f"{usr_pth}/{fname}", "w") as file:
            myWriter = csv.writer(file)
            myWriter.writerow(tracker_header)
            for tid in tIDs:
                tracker = Tracker.query.filter_by(id=tid[0]).first()
                myWriter.writerow(
                    [
                        tracker.name,
                        tracker.date_created,
                        tracker.description,
                        tracker.type,
                    ]
                )
        file.close()


def format_msg(data, mType="Daily"):
    template_pth = "reminder"
    if mType == "Summary":
        template_pth = "mail"
    with open(f"./templates/{template_pth}_template.html", "r") as msg_file:
        template = Template(msg_file.read())
        msg = template.render(data=data)
    return msg


def send_mail(to_address, subject, message, attachement=None):
    msg = MIMEMultipart()
    msg["From"] = app.config["SENDER_ADDRESS"]
    msg["To"] = to_address
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "html"))

    if attachement:
        with open(attachement, "rb") as attachement_file:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachement_file.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachement; filename= {attachement.split('/')[-1]}",
        )
        msg.attach(part)

    s = smtplib.SMTP(
        host=app.config["SMTP_SERVER_HOST"], port=app.config["SMTP_SERVER_PORT"]
    )
    s.login(app.config["SENDER_ADDRESS"], app.config["SENDER_PASSWORD"])
    s.send_message(msg)
    s.quit()
    return True


def send():
    user_list = User.query.all()

    for user in user_list:
        attachement_pth = f"/home/shaifali/Downloads/Mad2_Data/{user.username}/ExportedSummary_{str(date.today())}.pdf"
        tIDs = (
            UserTracker.query.with_entities(UserTracker.tID)
            .filter(UserTracker.uID == user.id)
            .all()
        )

        tracker_data = []
        for tid in tIDs:
            tracker = Tracker.query.filter_by(id=tid[0]).first()
            temp_dict = {
                "name": tracker.name,
                "description": tracker.description,
                "timestamp": tracker.date_created,
                "type": tracker.type,
            }
            tracker_data.append(temp_dict)

        send_data = {
            "username": user.username,
            "email": user.email,
            "tracker_data": tracker_data,
        }
        msg = format_msg(send_data, "Summary")
        html = HTML(string=msg)
        html.write_pdf(target=attachement_pth)
        send_mail(
            user.email,
            subject=f"The Self Tracker app: {user.username}'s monthly summary report",
            message=msg,
            attachement=attachement_pth,
        )


def remind():
    today = date.today()
    user_list = User.query.all()
    for user in user_list:
        tIDs = (
            UserTracker.query.with_entities(UserTracker.tID)
            .filter(UserTracker.uID == user.id)
            .all()
        )
        flag = True
        for tid in tIDs:
            lIDs = (
                TrackerLog.query.with_entities(TrackerLog.lID)
                .filter(TrackerLog.tID == tid[0])
                .all()
            )
            for lid in lIDs:
                mylog = Logs.query.filter_by(id=lid[0]).first()
                lDate = mylog.timestamp.date()
                if lDate == today:
                    flag = False
                    break
        if flag:
            send_data = {"username": user.username, "date": str(date.today())}
            msg = format_msg(send_data, "Daily")
            send_mail(
                user.email,
                subject=f"The Self Tracker: Reminder for logging your data",
                message=msg,
            )


def async_summary_export(username):
    fname = f"Summary.csv"
    tracker_header = ["Name", "Date Created", "Description", "Type"]
    usr_pth = f"/home/shaifali/Downloads/Mad2_Data/{username}"
    user = User.query.filter_by(username=username).first()
    if not os.path.exists(usr_pth):
        os.makedirs(usr_pth)
    tIDs = (
        UserTracker.query.with_entities(UserTracker.tID)
        .filter(UserTracker.uID == user.id)
        .all()
    )
    with open(f"{usr_pth}/{fname}", "w") as file:
        myWriter = csv.writer(file)
        myWriter.writerow(tracker_header)
        for tid in tIDs:
            tracker = Tracker.query.filter_by(id=tid[0]).first()
            myWriter.writerow(
                [
                    tracker.name,
                    tracker.date_created,
                    tracker.description,
                    tracker.type,
                ]
            )
    file.close()


def async_events_export(username, trackerID):
    fname = f"Logs.csv"
    log_header = ["Log", "TimeStamp", "Value", "Note"]
    dir_pth = f"/home/shaifali/Downloads/Mad2_Data/{username}/{trackerID}"
    if not os.path.exists(dir_pth):
        os.makedirs(dir_pth)
    lIDs = (
        TrackerLog.query.with_entities(TrackerLog.lID)
        .filter(TrackerLog.tID == trackerID)
        .all()
    )
    with open(f"{dir_pth}/{fname}", "w") as file:
        myWriter = csv.writer(file)
        myWriter.writerow(log_header)
        for lid in lIDs:
            log = Logs.query.filter_by(id=lid[0]).first()
            myWriter.writerow(
                [
                    log.log,
                    log.timestamp,
                    log.value,
                    log.note,
                ]
            )
    file.close()
