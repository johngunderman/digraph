from flask import Flask, render_template
from google.appengine.ext import db

from storage import models

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.
app = Flask(__name__, static_url_path="/static")
app.config['DEBUG'] = True


@app.route('/', methods = ['GET'])
def handle_index():
    """Return a friendly HTTP greeting."""
    return render_template("index.html")

@app.route('/task', methods = ['GET'])
def handle_task():
    return render_template("task.html")

@app.route('/workflow', methods = ['GET'])
def handle_workflow():
    return render_template("workflow.html")

@app.route('/tasks', methods = ['GET'])
def handle_tasks():
    tasks = db.GqlQuery("SELECT * FROM Task")
    return render_template("tasks.html", tasks=tasks)

@app.route('/workflows', methods = ['GET'])
def handle_workflows():
    return render_template("workflows.html")

@app.route('/task', methods = ['POST'])
def handle_task():
    #TODO: needs to check for existence in request
    task = models.Task()
    task.name = request.post['name']
    task.workflow = request.post['workflow']
    task.metadata = request.post['extra_info']
    query_string = ("SELECT * FROM Node WHERE Node.workflow = @1" +
                    "AND Node.parent_node = null ")



@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
