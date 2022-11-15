import os
import csv
import base64
import smtplib
from time import time
from datetime import date

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

from jinja2 import Template
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from weasyprint import HTML
from flask import current_app as app, request

from .models import *


def export():
    fname = f"ExportedSummary_{str(date.today())}.csv"
    user_list = User.query.all()
    # list_header = ["Name", "Date Created", "Description"]
    # for user in user_list:
    #     usr_pth = f"/home/shaifali/Downloads/Mad2_Data/{user.username}"
    #     if not os.path.exists(usr_pth):
    #         os.makedirs(usr_pth)
    #     tIDs = (
    #         UserTaskList.query.with_entities(UserTaskList.tID)
    #         .filter(UserTaskList.uID == user.id)
    #         .all()
    #     )
    #     with open(f"{usr_pth}/{fname}", "w") as file:
    #         myWriter = csv.writer(file)
    #         myWriter.writerow(list_header)
    #         for tid in tIDs:
    #             task_lists = TaskList.query.filter_by(id=tid[0]).first()
    #             myWriter.writerow(
    #                 [
    #                     task_lists.name,
    #                     task_lists.date_created,
    #                     task_lists.description,
    #                 ]
    #             )
    #     file.close()


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
        pdf_pth = f"/home/shaifali/Downloads/Mad2_Data/{user.username}"
        if not os.path.exists(pdf_pth):
            os.makedirs(pdf_pth)
        tIDs = (
            UserTaskList.query.with_entities(UserTaskList.tID)
            .filter(UserTaskList.uID == user.id)
            .all()
        )

        task_list_dict = {}
        for idx, tid in enumerate(tIDs):
            deadlines = {}
            completed = 0
            passed = 0
            task_list = TaskList.query.filter_by(id=tid[0]).first()
            cIDs = (
                ListCards.query.with_entities(ListCards.cID)
                .filter(ListCards.tID == tid[0])
                .all()
            )
            for cid in cIDs:
                myCard = Cards.query.filter_by(id=cid[0]).first()
                if myCard.status:
                    completed += 1
                if myCard.deadline.date() < datetime.now().date():
                    passed += 1
                try:
                    deadlines[myCard.deadline.strftime("%Y-%m-%d")] += 1
                except:
                    deadlines[myCard.deadline.strftime("%Y-%m-%d")] = 1

            img_pth =f'/home/shaifali/Desktop/Kanban_Application_Project/frontend/myapp/src/assets/{user.username}/{task_list.id}.png'

            plt.clf()
            plt.bar(deadlines.keys(), deadlines.values())
            plt.xlabel('Date')
            plt.ylabel('Number of Tasks')
            plt.savefig(img_pth)
            
            task_list_dict[idx] = {
                "id" : task_list.id,
                "name": task_list.name,
                "description": task_list.description,
                "date_created": task_list.date_created,
                "length": len(cIDs),
                "completed": completed,
                "passed": passed
            }
            # print(task_list_dict)

        send_data = {
            "username": user.username,
            "email": user.email,
            "task_list_dict": task_list_dict,
        }
        msg = format_msg(send_data, "Summary")
        # html = HTML(string=msg)
        with open(f'{pdf_pth}/ExportedSummary_{str(date.today())}.html', "w") as f:
            f.write(msg)
        f.close()
        # html.write_pdf(target=f'{pdf_pth}/ExportedSummary_{str(date.today())}.pdf')
        send_mail(
            user.email,
            subject=f"Kanban ToDo: {user.username}'s monthly summary report",
            message=msg,
            attachement=f'{pdf_pth}/ExportedSummary_{str(date.today())}.html',
        )


def remind():
    today = date.today()
    user_list = User.query.all()
    for user in user_list:
        tIDs = (
            UserTaskList.query.with_entities(UserTaskList.tID)
            .filter(UserTaskList.uID == user.id)
            .all()
        )
        flag = True
        deadlines = []
        for tid in tIDs:
            cIDs = (
                ListCards.query.with_entities(ListCards.cID)
                .filter(ListCards.tID == tid[0])
                .all()
            )
            for cid in cIDs:
                myCard = Cards.query.filter_by(id=cid[0]).first()
                cDate = myCard.deadline.date()
                if cDate == today:
                    flag = True
                    deadlines.append(myCard.title)
        if flag:
            send_data = {"username": user.username, "deadlines": deadlines, "date": str(date.today())}
            msg = format_msg(send_data, "Daily")
            send_mail(
                user.email,
                subject=f"Kanban ToDo: Reminder for Deadline of your task",
                message=msg,
            )


def async_summary_export(username):
    fname = f"Summary.csv"
    task_list_header = ["List Name", "Date Created", "Description"]
    usr_pth = f"/home/shaifali/Downloads/Mad2_Data/{username}"
    user = User.query.filter_by(username=username).first()
    if not os.path.exists(usr_pth):
        os.makedirs(usr_pth)
    tIDs = (
        UserTaskList.query.with_entities(UserTaskList.tID)
        .filter(UserTaskList.uID == user.id)
        .all()
    )
    with open(f"{usr_pth}/{fname}", "w") as file:
        myWriter = csv.writer(file)
        myWriter.writerow(task_list_header)
        for tid in tIDs:
            task_list = TaskList.query.filter_by(id=tid[0]).first()
            myWriter.writerow(
                [
                    task_list.name,
                    task_list.date_created,
                    task_list.description,
                ]
            )
    file.close()


def async_events_export(username, listID):
    fname = f"Cards.csv"
    card_header = ["Title", "ListName", "Content", "Deadline", "Status"]
    dir_pth = f"/home/shaifali/Downloads/Mad2_Data/{username}/{listID}"
    if not os.path.exists(dir_pth):
        os.makedirs(dir_pth)
    cIDs = (
        ListCards.query.with_entities(ListCards.cID)
        .filter(ListCards.tID == listID)
        .all()
    )
    with open(f"{dir_pth}/{fname}", "w") as file:
        myWriter = csv.writer(file)
        myWriter.writerow(card_header)
        for cid in cIDs:
            card = Cards.query.filter_by(id=cid[0]).first()
            myWriter.writerow(
                [
                    card.title,
                    card.listName,
                    card.content,
                    card.deadline.date(),
                    card.status,
                ]
            )
    file.close()
