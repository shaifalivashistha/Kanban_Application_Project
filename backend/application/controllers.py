from flask_security.utils import hash_password, verify_password
from flask import current_app as app
from flask import (
    request,
    session,
    jsonify,
)

from .models import *
from .tasks import *
from .security import *
from .database import *
from .cache import cache

import os
import base64
import os.path as osp
import time
import matplotlib
matplotlib.use('Agg')
from matplotlib.figure import Figure
from matplotlib import pyplot as plt


@app.before_first_request
def database():
    db.create_all()


@app.route("/")
def home():
    return jsonify({"resp": "ok", "msg": "The Tracker App is Running"})


# -------------------------REGISTER-------------------------#


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        data = request.get_json()

        username, email, pwd = (data["username"], data["email"], data["password"])

        if User.query.filter_by(email=email).first():
            return jsonify(
                {
                    "resp": "not ok",
                    "msg": "Email is already registered",
                }
            )
        elif User.query.filter_by(username=username).first():
            return jsonify(
                {
                    "resp": "not ok",
                    "msg": "Username is already taken",
                }
            )
        else:
            user_datastore.create_user(
                email=email, username=username, password=hash_password(pwd)
            )
            db.session.commit()
            user_fig_dir = f"../frontend/myapp/src/assets/{username}"
            if not osp.exists(user_fig_dir):
                os.makedirs(user_fig_dir)

            return jsonify({"resp": "ok", "msg": "Account created"})
    else:
        return jsonify(
            {
                "resp": "not ok",
                "msg": f"Welcome to Register page ({request.method} request received)",
            }
        )


# -------------------------LOGIN-------------------------#


@app.route("/login_page", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        data = request.get_json()

        user_data = User.query.filter_by(email=data["email"]).first()

        if not user_data:
            return jsonify({"resp": "not ok", "msg": "User does not exists"})

        else:
            pswd = user_data.password
            username = user_data.username
            if verify_password(data["password"], pswd):
                session["email"], session["pwd"], session["username"] = (
                    data["email"],
                    data["password"],
                    username,
                )
                return jsonify(
                    {"resp": "ok", "msg": "Log in success", "stuff": str(username)}
                )
            else:
                return jsonify({"resp": "not ok", "msg": "Incorrect password"})
    else:
        return jsonify(
            {
                "resp": "not ok",
                "msg": f"Welcome to Log in page ({request.method} request received)",
            }
        )


# -------------------------DASHBOARD-------------------------#


@app.route("/dashboard/<string:username>", methods=["GET"])
@cache.memoize()
def dashboard(username):
    time.sleep(3)
    user_data = User.query.filter_by(username=username).first()
    taskObjs = user_data.task_list

    task_list = []
    for taskObj in taskObjs:
        task_list.append(taskObj)
    task_list_dict = {}
    for idx, task in enumerate(task_list):

        card_data_dict= {}
        for key, card in enumerate(task.cards):

            card_data_dict[key] = {
                "id" : card.id,
                "title": card.title,
                "listName": card.listName,
                "content" : card.content,
                "deadline" : card.deadline.strftime("%Y-%m-%d"),
                "status": card.status,
                "checkStatus" : card.checkStatus
            }
        # print(card_data_dict)
        task_list_dict[idx] = {
            "id": task.id,
            "name": task.name,
            "description": task.description,
            "date_created": task.date_created,
            "task_cards_data" : card_data_dict
        }
    

    return jsonify({"resp": "ok", "msg": "Task Lists and Cards parsed", "stuff": task_list_dict})


# -------------------------LOGOUT-------------------------#


@app.route("/logout_page", methods=["GET"])
def logout():
    session.clear()
    cache.clear()
    return jsonify({"resp": "ok", "msg": "Logged out"})


# -------------------------CREATE_TASKLIST-------------------------#


@app.route("/dashboard/<string:username>/create_list", methods=["POST", "GET"])
def create_list(username):
    cache.delete_memoized(cards, username)
    cache.delete_memoized(dashboard, username)
    cache.delete_memoized(summary_page, username)
    if request.method == "POST":

        data = request.get_json()
        # print(data)
        TaskListName, TaskListDescription = (
            data["list_name"],
            data["list_des"],
        )

        newTaskList = TaskList(
            name=TaskListName, description=TaskListDescription
        )

        user = User.query.filter_by(username=username).first()
        user.task_list.append(newTaskList)
        db.session.add(newTaskList)
        db.session.commit()
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)
        axis.set(xlabel="Time Stamp", ylabel="Value")
        fig.savefig(f"../frontend/myapp/src/assets/{username}/{newTaskList.name}.png")
        return jsonify({"resp": "ok", "msg": "task list successfully created"})
    else:
        return jsonify(
            {
                "resp": "not ok",
                "msg": f"Welcome to AddTracker page ({request.method} request received)",
            }
        )


# -------------------------UPDATE_TASK_LIST-------------------------#


@app.route("/<string:username>/update_task_list", methods=["POST"])
def update(username):
    cache.delete_memoized(cards, username)
    cache.delete_memoized(dashboard, username)
    cache.delete_memoized(summary_page, username)
    data = request.get_json()
    # print(data)
    task_list = TaskList.query.filter_by(id=data["listID"]).first()
    if task_list:
        task_list.name, task_list.description = data["listName"], data["listDescription"]
        db.session.commit()
        return jsonify({"resp": "ok", "msg": "List updated successfully"})


# -------------------------CREATE_CARDS-------------------------#


@app.route("/<string:username>/create_card", methods=["GET"])
@cache.memoize()
def cards(username):
    # cache.delete_memoized(dashboard, username)
    # parent_list = TaskList.query.filter_by(id=listID).first()
    if request.method == "GET":
        time.sleep(3)
        
        # all_cards = parent_list.cards

        # img_pth = f"../frontend/myapp/src/assets/{username}/{listID}.png"
        # card_list = []
        # for card in all_cards:
        #     card_list.append(card)
        # data = {}

        taskDict = {}
        all_lists = TaskList.query.all()
        # print(all_lists)
        for idx, task in enumerate(all_lists):
            taskDict[idx] = {"id": task.id,"listName":task.name}
            # print(taskDict)
        # fig = Figure()
        # axis = fig.add_subplot(1, 1, 1)
        # axis.plot(data.keys(), data.values())
        # axis.set(xlabel="Time Stamp", ylabel="Value")
        # fig.savefig(img_pth)
        # with open(img_pth, "rb") as image_file:
        #     encodedImage = str(base64.b64encode(image_file.read()).decode("utf-8"))

        # card_dict = {}
        # for idx, card in enumerate(card_list):
        #     Dcard = {
        #         "listName": card.listName,
        #         "cardID": card.id,
        #         "title": card.title,
        #         "content": card.content,
        #         "deadline": card.deadline,
        #         "status" : card.status
        #     }
        #     card_dict[idx] = Dcard
        # print(taskList)
        return jsonify(
            {
                "resp": "ok",
                "stuff": {"taskDict":taskDict}
                # "stuff": {"taskList":taskList,"cardData": card_dict, "encodedImage": encodedImage},
            }
        )


# -------------------------BONCE_CARD_CACHE-------------------------#


@app.route("/<string:username>/<int:listID>/bounce_card_cache", methods=["POST"])
def bounce_card_cache(username, listID):
    cache.delete_memoized(cards, username)
    cache.delete_memoized(dashboard, username)
    cache.delete_memoized(summary_page, username)
    data = request.get_json()
    parent_list = TaskList.query.filter_by(id=listID).first()
    img_pth = f"../frontend/myapp/src/assets/{username}/{listID}.png"

    # print(data)
    new_card = Cards(
        listName=data["listName"], title=data["title"], content=data["content"], deadline=datetime.strptime(data["deadline"], '%Y-%m-%d').date(), status=data["status"], checkStatus=data["checkStatus"]
    )
    parent_list.cards.append(new_card)
    db.session.add(new_card)
    db.session.commit()

    with open(img_pth, "rb") as image_file:
        encodedImage = str(base64.b64encode(image_file.read()).decode("utf-8"))

    all_cards = parent_list.cards
    card_list = []
    for mycard in all_cards:
        card_list.append(mycard)
    card_dict = {}
    for idx, mycard in enumerate(card_list):
        Dcard = {
            "listName":mycard.listName,
            "title": mycard.title,
            "cardID": mycard.id,
            "content": mycard.content,
            "deadline": mycard.deadline,
            "status": mycard.status,
        }
        card_dict[idx] = Dcard
    return jsonify(
        {
            "resp": "ok",
            "msg": "new card added and card cache cleared successfully",
            "stuff": {"cardData": card_dict, "encodedImage": encodedImage},
        }
    )


# -------------------------DELETE_TASK_LIST-------------------------#


@app.route("/<string:username>/<int:listID>/delete", methods=["GET"])
def delete(username, listID):
    # print("delete request at backend")
    cache.delete_memoized(dashboard, username)
    cache.delete_memoized(summary_page, username)
    cache.delete_memoized(cards, username)
    targetTaskList = TaskList.query.get_or_404(listID)
    try:
        db.session.delete(targetTaskList)
        db.session.commit()
        return jsonify({"resp": "ok", "msg": "TaskList deleted successfully."})
    except:

        return jsonify(
            {
                "resp": "not ok",
                "msg": "Problem encountered while trying to delete Task list",
            }
        )


# -------------------------DELETE_CARDS-------------------------#


@app.route("/<string:username>/<int:listID>/<int:cardID>/delete", methods=["GET"])
def delete_card(username, listID, cardID):
    cache.delete_memoized(cards, username)
    cache.delete_memoized(dashboard, username)
    cache.delete_memoized(summary_page, username)
    myCard= Cards.query.get_or_404(cardID)
    try:
        db.session.delete(myCard)
        db.session.commit()
        return jsonify({"resp": "ok", "msg": "Card deleted succesfully"})
    except:
        return jsonify(
            {
                "resp": "not ok",
                "msg": "Problem encountered while trying to delete event",
            }
        )


# -------------------------UPDATE_CARDS-------------------------#


@app.route("/<string:username>/update_card", methods=["POST"])
def update_card(username):
    cache.delete_memoized(cards, username)
    cache.delete_memoized(dashboard, username)
    cache.delete_memoized(summary_page, username)
    data = request.get_json()

    myCard= Cards.query.filter_by(id=data["cardID"]).first()
    # print(myCard)
    # print(data)
    # print(data["listName"])
    if myCard:
        db.session.delete(myCard)
        db.session.commit()
        parent_list = TaskList.query.filter_by(name=data["listName"]).first()
        new_card = Cards(
        listName=data["listName"], title=data["title"], content=data["content"], deadline=datetime.strptime(data["deadline"], '%Y-%m-%d').date(), status=data["status"], checkStatus=data["checkStatus"]
        )
        parent_list.cards.append(new_card)
        db.session.add(new_card)
        db.session.commit()
        # print(last_parent_list.cards)
        # last_parent_list = TaskList.query.filter_by(name=myCard.listName).first()
        # last_parent_list.cards.remove(myCard)
        # db.session.commit()
        # print(last_parent_list.cards)
        # myCard.id = data["cardID"]
        # myCard.title, myCard.listName, myCard.content, myCard.deadline, myCard.status = data["title"], data["listName"], data["content"], datetime.strptime(data["deadline"], '%Y-%m-%d').date(), data["status"]
        # db.session.commit()
        # parent_list = TaskList.query.filter_by(name=data["listName"]).first()
        # parent_list.cards.append(myCard)
        # db.session.commit()

        return jsonify({"resp": "ok", "msg": "log updated successfully"})


# -------------------------TASK_LIST_EXPORT-------------------------#


@app.route("/<string:username>/export_summary", methods=["GET", "POST"])
def export_task_lists(username):
    if request.method == "POST":
        job = trigerred_summary_export(username)
        return jsonify(
            {"resp": "ok", "msg": f"{str(job)}. Exported successfully. Status: 200"}
        )
    else:
        return jsonify({"resp": "not ok", "msg": "GET request received"})


# -------------------------CARDS_EXPORT-------------------------#

@app.route("/<string:username>/<int:listID>/export_card", methods=["GET", "POST"])
def export_cards(username, listID):
    if request.method == "POST":
        job = trigerred_events_export(username, listID)
        return jsonify(
            {"resp": "ok", "msg": f"{str(job)}. Exported successfully. Status: 200"}
        )
    else:
        return jsonify({"resp": "not ok", "msg": "GET request received"})


# -------------------------SUMMARY_PAGE-------------------------#

@app.route("/<string:username>/summary_page", methods=["GET"])
@cache.memoize()
def summary_page(username):
    time.sleep(3)
    user_data = User.query.filter_by(username=username).first()
    taskObjs = user_data.task_list

    task_list = []
    for taskObj in taskObjs:
        task_list.append(taskObj)

    task_list_dict = {}
    for idx, task in enumerate(task_list):

        card_data_dict= {}
        deadlines = {}
        completed = 0
        passed = 0
        for key, card in enumerate(task.cards):

            card_data_dict[key] = {
                "id" : card.id,
                "title": card.title,
                "listName": card.listName,
                "content" : card.content,
                "deadline" : card.deadline.strftime("%Y-%m-%d"),
                "status": card.status
            }
            if card.status:
                completed += 1
            if card.deadline.date() < datetime.now().date():
                passed += 1
            try:
                deadlines[card_data_dict[key]["deadline"]] += 1
            except:
                deadlines[card_data_dict[key]["deadline"]] = 1

        # img_pth =f'/home/shaifali/Downloads/Mad2_Data/{username}/{task.name}.png'
        img_pth =f'/home/shaifali/Desktop/Kanban_Application_Project/frontend/myapp/src/assets/{username}/{task.name}.png'


        # f1 = plt.figure()
        plt.clf()
        plt.bar(deadlines.keys(), deadlines.values())
        plt.xlabel('Date')
        plt.ylabel('Number of Tasks')
        plt.savefig(img_pth)
        with open(img_pth, "rb") as image_file:
            encoded_img = str(base64.b64encode(image_file.read()).decode("utf-8"))
            
        # print(card_data_dict)
        task_list_dict[idx] = {
            "id": task.id,
            "name": task.name,
            "description": task.description,
            "date_created": task.date_created,
            "task_cards_data" : card_data_dict,
            "encoded_img": encoded_img,
            "completed": completed,
            "passed": passed
        }

    return jsonify({"resp": "ok", "msg": "Task Lists and Cards parsed", "stuff": task_list_dict})