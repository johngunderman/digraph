from flask import Flask, render_template, request

from storage.models import Node, Workflow, Task

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
    tasks = Task.query().fetch(100)
    return render_template("tasks.html", tasks=tasks)

@app.route('/workflows', methods = ['GET'])
def handle_workflows():
    return render_template("workflows.html")

@app.route('/task', methods = ['POST'])
def handle_task_post():
    #TODO: needs to check for existence in request
    task = Task()
    task.name = request.form['name']
    task.workflow = request.form['workflow']
    task.metadata = request.form['extra_info']
    nodes = Node.query(Node.workflow == task.workflow,
                       Node.parent_node == None).fetch(100)
    # make these return an actual error code
    if len(nodes) < 1:
        return "No valid root nodes found for this workflow." \
            + " Are you sure this workflow exists?"
    if len(nodes) > 1:
        return "More than one root node exists for this workflow." \
            + " Something has gone terribly wrong somewhere..."
    root_node = nodes[0]
    task.active_nodes.append(root_node)
    #TODO: figure out what the return value is here and check it
    task.put()
    return ""


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
