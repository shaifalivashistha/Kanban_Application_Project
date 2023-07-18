<h1 align="center">

**<u>KanBan To Do</u>**
</h1>

<p align="center">
KanBan To Do is a web application that gives the user analytical results of work, deadlines, schedule, and helps the user to track and manage his/her schedule on the base of that analysis. Learn more about working of KanBan To Do by reading the documentation below.
</p>

#### Index

- [What's included](#whats-included)
- [How To Run "KanBan To Do"](#how-to-run-kanban-to-do)
- [Backend Application contents](#backend-application-contents)
- [Backend Application Python Files](#backend-application-python-files)
- [Developer](#developer)
- [Thanks](#thanks)

## What's included

Within the application folder you'll find the following directories and files. You'll see something like this:

```text
project/
│
├── backend/
│   │
│   ├── application/
│   │   ├── __init__.py
│   │   ├── cache.py
│   │   ├── config.py
│   │   ├── controllers.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── security.py
│   │   ├── send_mail.py
│   │   ├── task.py
│   │   └── workers.py
│   │
│   ├── templates/
│   │   ├── mail_template.html
│   │   └── reminder_template.html
│   │   
│   ├── trackerdb.sqlite3
│   └── main.py
│
│
├── frontend/myapp/
│   │
│   ├── public/
│   │   └── img/icons
│   │       └── index.html
│   │
│   ├── src/
│   │   ├── assets/
│   │   │   └── Kanban1.jpg
│   │   │   
│   │   ├── components/
│   │   │   ├── DashboardPage.vue
│   │   │   ├── HomePage.vue
│   │   │   ├── LoginPage.vue
│   │   │   ├── RegisterPage.vue
│   │   │   ├── createTaskCard.vue
│   │   │   ├── createTaskList.vue 
│   │   │   ├── summaryPage.vue
│   │   │   ├── updateCardPage.vue
│   │   │   └── updateListPage.vue
│   │   │  
│   │   │  
│   │   ├── router/
│   │   │   └── index.js
│   │   │  
│   │   ├── views/
│   │   │   ├── AboutView.vue 
│   │   │   ├── DashboardView.vue
│   │   │   ├── HomeView.vue
│   │   │   ├── LoginView.vue
│   │   │   ├── RegisterView.vue
│   │   │   ├── createCardView.vue 
│   │   │   ├── createTskView.vue
│   │   │   ├── summaryView.vue 
│   │   │   ├── updateCardView.vue
│   │   │   └── updateListView.vue 
│   │   │ 
│   │   ├── App.vue/
│   │   │ 
│   │   │ 
│   │   └── main.js/
│   │ 
│   ├── babel.config.js
│   ├── jsconfig.json
│   ├── package-lock.json
│   ├── package.json
│   └── vue.config.js
│
├── Report.pdf
│
├── tracker.sqlite3
│
└── README.md  
```

## How To Run "KanBan To Do":
One can run Run "KanBan To Do" using localhost command by running.  Below is the general command to run the application:

	http://127.0.0.1:5000/

## Backend Application contents
Below are the contents of the Backend Application code-

- [Python Libraries](#python-libraries)

#### Python Libraries

1. **<u>Flask:</u>**
    Flask is used for developing web applications using python, implemented on Jinja2. We used diffrent flask decorators and functions in the application for better handling here we used  **route,before_first_request decorator, redirect and render_template functions, Flask class and request, session, flash as others objects.**
    Here, *route* is used to to bind a function with a specific url where in some function we used route with variable section also and *before_app_request( )* registers a function that runs before the view function, no matter what URL is requested. *redirect( )* fuction is used to redirect a user to another endpoint. *render_template( )* function is used to render html templates stored in templates folder. *Request* is a flask object used to retrieve the data at the server side using its attributes. *Flask* is class used to create class instance in which __ __name__ __ is passed as argument which represents the name of the application package. *Flask-Session* is an extension for Flask that support Server-side Session to the application. The Session is the time between the client logs in to the server and logs out of the server. *flash( )* method of the flask module passes the message to the next request which is an HTML template.

2. <u>**Flask SqlAlchemy:**</u>
    Flask-SQLAlchemy is an extension to Flask that aims to simplify using SQLAlchemy with Flask by providing defaults and helpers to accomplish common tasks. One of the most sought after helpers being the handling of a database connection across the app. In KanBan To Do, We used flask-sqlalchemy to create database schema and tables.

3. <u>**Flask Security:**</u>
    Flask-Security is an extension to Flask which adds basic security and authentication features to your Flask apps quickly and easily. In the KanBan To Do application the flask security is used for hashing password, user vreification and authentication.

4. <u>**Flask CORS:**</u>
    Flask-CORS is an extension to Flask for handling Cross Origin Resource Sharing (CORS), making cross-origin AJAX possible. In KanBan To Do application this module is used to allow fetch requests from Vue js frontend and send back data in response of the request.

5. <u>**Flask Caching:**</u>
    Flask-Caching is an extension to Flask that adds caching support for backends to any Flask application. In our application it is used to cache the user data such as tracker details, events and graphs logged by the user under any tracker.

6. <u>**Celery:**</u>
    Celery is an open-source Python library which is used to run the tasks asynchronously. It is a task queue that holds the tasks and distributes them to the workers in a proper manner. In the KanBan To Do appliation the jobs handled by celery are: to export trackers list and logged events to a CSV file, to send monthly pdf reports by emails to the client that uses crontab for a scheduled event of celery, and send Daily reminders by emailing the user only if the user has not logged during the daytime.

7. <u>**Redis:**</u>
    Redis is an in-memory data store that can be used as either a high-performance key-value store or as a caching storage database. In our application the user data, tracker details along with logged events and trendline graphs are stored in the database as cache.

8. <u>**Datetime:**</u>
    Datetime is a python module which supplies classes to work with date and time. These classes provide a number of functions to deal with dates, times and time intervals. In the KanBan To Do, we used datetime module to get timestamp in the application.

9. **<u>matplotlib.pyplot:</u>**
    **matplotlib.pyplot** is a collection of functions. Each pyplot function makes some change to a figure: e.g., creates a figure, creates a plotting area in a figure, plots some lines in a plotting area, decorates the plot with labels, etc. In matplotlib.



## Backend Application Python Files

Below is the description of backend application python files and their functions:

- [main_py](#main_py)
- [config_py](#config_py)
- [controllers_py](#controllers_py)
- [database_py](#database_py)
- [models_py](#models_py)
- [security_py](#security_py)
- [send_mail_py](#send_mail_py)
- [task_py](#task_py)
- [workers_py](#workers_py)



#### main_py: 
In this file, a we have several imports of various libraries and files from the application folder . Under this file a function named **create_app** is defined which returns app, api and celery instance mounted with configurations that are assigned in the config.py file and is imported in current file. This is the main file that runs the backend server using commandline.

#### config_py: 
In this file, all the configurations related to the application such as database configurations, security configurations, Celery configurations, etc are assigned for local development of the application. 

#### controllers_py: 

In this file, all the routes that receives fetch request to the backend server from the frontend and send responses in result to a request are defined here.

#### database_py: 

In this file, the flask_sqlalchemy database instance is defined.

#### models_py: 
In this file, all the raw structure of database models that are to be used and queried in the application is written in the form of classes(tables).

#### security_py: 
In this file, a security instance is defined on User model and db instance  using flask_security.

#### send_mail_py: 
In this file, 7 functions are defined **export, format_msg, send_mail, send, remind, async_summary_export, async_event_export** which functions together to create CSV and pdf files as per requirement and email the pdf and csv reports and summary respectively to the user in both scheduled manner or whenever the user wants to get the CSV summary.

#### task_py: 
In this file, one celery scheduler **setup_periodic_tasks** and 5 celery tasks **celer_summary_export, send_summary, send_reminder, triggered_summary_export, triggered_events_export** are defined out of which **celer_summary_export, send_summary** are monthly scheduled and **send_reminder** is daily scheduled event.

#### workers_py: 
In this file, a celery instance is defined for the application jobs.


## Developer

- **Name : Shaifali Vashistha**
- **Roll Number : 21f1003257**
- **Student Email : 21f1003257@student.onlinedegree.iitm.ac.in**
- **Contact Email : shaifalivashistha@gmail.com**
- **Linked-In : https://www.linkedin.com/in/shaifali-vashistha-420082226/**
- **GitHub : https://github.com/shaifalivashistha**

##  Thanks

I am thankful to IIT Madras for giving me the opportunity to develop such an interesting web application!
