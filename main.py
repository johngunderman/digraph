from flask import Flask, render_template, request, flash
from cgi import escape
import json

from storage.models import Node, Workflow, Task

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.
app = Flask(__name__, static_url_path="/static")
app.config['DEBUG'] = True
# TODO: configure this via flag
app.secret_key = 'test-secret'


@app.route('/', methods=['GET'])
def handle_index():
    """Return a friendly HTTP greeting."""
    return render_template("index.html")


@app.route('/task', methods=['GET'])
def handle_task():
    return render_template("task.html")


@app.route('/workflow', methods=['GET'])
def handle_workflow():
    return render_template("workflow.html")


@app.route('/tasks', methods=['GET'])
def handle_tasks():
    tasks = Task.query().fetch(100)
    return render_template("tasks.html", tasks=tasks)


@app.route('/workflows', methods=['GET'])
def handle_workflows():
    return render_template("workflows.html")


# JSON API BELOW

@app.route('/tasks/json', methods=['GET'])
def handle_tasks_json():
    return json.dumps(
        [task.to_json() for task in Task.query().fetch(100)])


# POST METHODS BELOW

@app.route('/task', methods=['POST'])
def handle_task_post():
    # TODO: needs to check for existence in request
    # TODO: needs to check for uniqueness in name (for this user)
    task = Task()
    task.name = request.form['name']
    task.workflow = request.form['workflow']
    task.metadata = request.form['extra_info']
    nodes = Node.query(Node.workflow == task.workflow,
                       Node.parent_node == None).fetch(100)
    if len(nodes) < 1:
        flash("No valid root nodes found for this workflow."
              + " Are you sure this workflow exists?")
        return "error"
    if len(nodes) > 1:
        flash("More than one root node exists for this workflow."
              + " Something has gone terribly wrong somewhere...")
        return "error"
    root_node = nodes[0]
    task.active_nodes.append(root_node)
    # TODO: figure out what the return value is here and check it
    task.put()
    return "success"


@app.route('/workflow', methods=['POST'])
def handle_workflow_post():
    # TODO: verify everything before committing anything
    #      eg. validate workflow before creating nodes
    workflow_json = request.get_json()
    node_lookup_names = []
    # table of node names to node objects
    node_table = {}
    for json_node in workflow_json.nodelist:
        node = Node()
        node.name = json_node.name
        node.description = json_node.description
        # this will probably break horribly in the future if the
        # user posts nodes in the wrong order, as it expects that parent
        # nodes have already been committed.
        # possibly enforce this in JS and not worry about it here?
        if json_node.parent is not "":
            # support multiple comma separated parents
            for parent in node.split(','):
                try:
                    node.parent_nodes.append(node_table[parent.strip()])
                except KeyError:
                    flash("The step " + escape(parent) +
                          " is out of order or does not exist.")
                    return "error"
        node.put()
        node_table[node.name] = node.key()

    workflow = Workflow()
    workflow.name = workflow_json.name
    workflow.description = workflow.description
    workflow.active_nodes = node_table.values()
    workflow.metadata = workflow_json.extra_info
    workflow.put()
    return "success"


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
