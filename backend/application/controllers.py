from flask_security.utils import hash_password, verify_password
from flask import current_app as app
from flask import (
    request,
    redirect,
    url_for,
    flash,
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
from matplotlib.figure import Figure


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
# @cache.memoize()
def dashboard(username):
    time.sleep(1)
    user_data = User.query.filter_by(username=username).first()
    taskObjs = user_data.task_list

    task_list = []
    for taskObj in taskObjs:
        task_list.append(taskObj)
    task_list_dict = {}
    for idx, task in enumerate(task_list):
        print(task)
        print(task.cards)

        task_list_dict[idx] = {
            "id": task.id,
            "name": task.name,
            "description": task.description,
            "date_created": task.date_created,
            "task_cards_data" : task.cards
        }

    
    return jsonify({"resp": "ok", "msg": "Tasks parsed", "stuff": task_list_dict})


# -------------------------LOGOUT-------------------------#


@app.route("/logout_page", methods=["GET"])
def logout():
    session.clear()
    # cache.clear()
    return jsonify({"resp": "ok", "msg": "Logged out"})


# -------------------------CREATE_TASKLIST-------------------------#


@app.route("/dashboard/<string:username>/create_list", methods=["POST", "GET"])
def create_list(username):
    # cache.delete_memoized(dashboard, username)
    if request.method == "POST":

        data = request.get_json()
        print(data)
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
        fig.savefig(f"../frontend/myapp/src/assets/{username}/{newTaskList.id}.png")
        return jsonify({"resp": "ok", "msg": "task list successfully created"})
    else:
        return jsonify(
            {
                "resp": "not ok",
                "msg": f"Welcome to AddTracker page ({request.method} request received)",
            }
        )


# -------------------------UPDATE_TASK_LIST-------------------------#


@app.route("/<string:username>/<int:listID>/update", methods=["POST"])
def update(username, listID):
    # cache.delete_memoized(dashboard, username)
    task_list = TaskList.query.filter_by(id=listID).first()
    data = request.get_json()
    if task_list:
        task_list.name, task_list.description = data["list_name"], data["list_des"]
        db.session.commit()
        return jsonify({"resp": "ok", "msg": "List updated successfully"})


# -------------------------CREATE_CARDS-------------------------#


@app.route("/<string:username>/<int:listID>/create_card", methods=["GET"])
# @cache.memoize()
def cards(username, listID):
    parent_list = TaskList.query.filter_by(id=listID).first()
    if request.method == "GET":
        time.sleep(1)
        all_cards = parent_list.cards
        img_pth = f"../frontend/myapp/src/assets/{username}/{listID}.png"
        card_list = []
        for card in all_cards:
            card_list.append(card)
        data = {}

        taskList = []
        all_lists = TaskList.query.all()
        print(all_lists)
        for task in all_lists:
            taskList.append(task.name)
            print(task.name)
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)
        axis.plot(data.keys(), data.values())
        axis.set(xlabel="Time Stamp", ylabel="Value")
        fig.savefig(img_pth)
        with open(img_pth, "rb") as image_file:
            encodedImage = str(base64.b64encode(image_file.read()).decode("utf-8"))

        card_dict = {}
        for idx, card in enumerate(card_list):
            Dcard = {
                "listName": card.listName,
                "cardID": card.id,
                "title": card.Title,
                "content": card.content,
                "deadline": card.deadline,
                "status" : card.status
            }
            card_dict[idx] = Dcard
        print(taskList)
        return jsonify(
            {
                "resp": "ok",
                "stuff": {"taskList":taskList,"cardData": card_dict, "encodedImage": encodedImage},
            }
        )


# -------------------------BONCE_CARD_CACHE-------------------------#


@app.route("/<string:username>/<int:listID>/bounce_card_cache", methods=["POST"])
def bounce_log_cache(username, listID):
    # cache.delete_memoized(log, username, listID)
    parent_list = TaskList.query.filter_by(id=listID).first()
    img_pth = f"../frontend/myapp/src/assets/{username}/{listID}.png"
    data = request.get_json()

    new_card = Cards(
        ListName=data["ListName"], title=data["title"], content=data["content"], deadline=data["deadline"], status=data["status"]
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
            "title": mycard.Title,
            "cardID": mycard.cardID,
            "content": mycard.content,
            "deadline": mycard.deadline,
            "status": mycard.status,
        }
        card_dict[idx] = Dcard
    return jsonify(
        {
            "resp": "ok",
            "msg": "new log added and log cache cleared successfully",
            "stuff": {"logData": card_dict, "encodedImage": encodedImage},
        }
    )


# -------------------------DELETE_TASK_LIST-------------------------#


@app.route("/<string:username>/<int:listID>/delete", methods=["GET"])
def delete(username, listID):
    print("delete request at backend")
    # cache.delete_memoized(dashboard, username)
    targetTaskList = TaskList.query.get_or_404(listID)
    try:
        db.session.delete(targetTaskList)
        db.session.commit()
        return jsonify({"resp": "ok", "msg": "List deleted successfully."})
    except:

        return jsonify(
            {
                "resp": "not ok",
                "msg": "Problem encountered while trying to delete tracker",
            }
        )


# -------------------------DELETE_CARDS-------------------------#


@app.route("/<string:username>/<int:listID>/<int:cardID>/delete", methods=["GET"])
def delete_card(username, listID, cardID):
    # cache.delete_memoized(log, username, trackerID)
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


@app.route("/<string:username>/<int:listID>/<int:cardID>/update", methods=["POST"])
def update_card(username, listID, cardID):
    # cache.delete_memoized(log, username, trackerID)
    myCard= Cards.query.filter_by(id=cardID).first()
    data = request.get_json()
    if myCard:
        myCard.title, myCard.lsitName, myCard.content, myCard.deadline, myCard.status = data["title"], data["taskList"], data["content"], data["deadline"], data["status"]
        db.session.commit()
        return jsonify({"resp": "ok", "msg": "log updated successfully"})


# -------------------------TASK_LIST_EXPORT-------------------------#


@app.route("/<string:username>/export_task_lists", methods=["GET", "POST"])
def export_task_lists(username):
    if request.method == "POST":
        job = trigerred_summary_export(username)
        return jsonify(
            {"resp": "ok", "msg": f"{str(job)}. Exported successfully. Status: 200"}
        )
    else:
        return jsonify({"resp": "not ok", "msg": "GET request received"})


@app.route("/<string:username>/<int:trackerID>/export_events", methods=["GET", "POST"])
def export_events(username, trackerID):
    if request.method == "POST":
        job = trigerred_events_export(username, trackerID)
        return jsonify(
            {"resp": "ok", "msg": f"{str(job)}. Exported successfully. Status: 200"}
        )
    else:
        return jsonify({"resp": "not ok", "msg": "GET request received"})
