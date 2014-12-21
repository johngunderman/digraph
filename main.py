from flask import Flask, render_template
#from flask_bootstrap import Bootstrap

app = Flask(__name__, static_url_path="/static")
#Bootstrap(app)
app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

@app.route('/')
def handle_index():
    """Return a friendly HTTP greeting."""
    return render_template("index.html")

@app.route('/task')
def handle_task():
    pass

@app.route('/node')
def handle_node():
    pass

@app.route('/tasks')
def handle_tasks():
    pass

@app.route('/nodes')
def handle_nodes():
    pass


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
