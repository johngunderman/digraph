from flask import Flask, render_template
from google.appengine.ext import db

from storage import models

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.
app = Flask(__name__, static_url_path="/static")
app.config['DEBUG'] = True


@app.route('/')
def handle_index():
    """Return a friendly HTTP greeting."""
    return render_template("index.html")

@app.route('/task')
def handle_task():
    return render_template("task.html")

@app.route('/workflow')
def handle_workflow():
    return render_template("workflow.html")

@app.route('/tasks')
def handle_tasks():
    tasks = db.GqlQuery("SELECT * FROM Task")
    return render_template("tasks.html", tasks=tasks)

@app.route('/workflows')
def handle_workflows():
    return render_template("workflows.html")


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
