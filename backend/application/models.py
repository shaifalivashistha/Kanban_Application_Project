from flask_security import UserMixin, RoleMixin
from datetime import datetime
from .database import db


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    task_list = db.relationship(
        "TaskList", secondary="UserTaskList", backref="User", cascade="all,delete"
    )
    roles = db.relationship(
        "Role", secondary="roles_users", backref=db.backref("User", lazy=True)
    )


class TaskList(db.Model):
    __tablename__ = "task_list"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(300), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.now)
    cards = db.relationship(
        "Cards", secondary="List_Cards", backref="task_list", cascade="all,delete"
    )


class Cards(db.Model):
    __tablename__ = "cards"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    listName = db.Column(db.Integer, nullable=False, unique=True)
    title = db.Column(db.String(300), nullable=False)
    content = db.Column(db.String(300), nullable=False)
    deadline = db.Column(db.DateTime(300), nullable=True)
    status = db.Column(db.String(300), nullable=False)


class UserTaskList(db.Model):
    __tablename__ = "UserTaskList"
    UserTaskListID = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    uID = db.Column(db.Integer(), db.ForeignKey("user.id"))
    tID = db.Column(db.Integer(), db.ForeignKey("task_list.id"))


class ListCards(db.Model):
    __tablename__ = "List_Cards"
    List_CardsID = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    tID = db.Column(db.Integer(), db.ForeignKey("task_list.id"))
    cID = db.Column(db.Integer(), db.ForeignKey("cards.id"))


class Role(db.Model, RoleMixin):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(300))


class RolesUsers(db.Model):
    __tablename__ = "roles_users"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column("user_id", db.Integer(), db.ForeignKey("user.id"))
    role_id = db.Column("role_id", db.Integer(), db.ForeignKey("role.id"))
