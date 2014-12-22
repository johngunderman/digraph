import datetime
from google.appengine.ext import db
from google.appengine.api import users


class Node(db.Model):
  children = db.ListProperty(int)
  parent_node = db.SelfReferenceProperty()
  name = db.StringProperty(required=True)
  description = db.StringProperty(required=True)

class Workflow(db.Model):
  name = db.StringProperty()
  description = db.StringProperty()
  components = db.ListProperty(int)

class Task(db.Model):
  name = db.StringProperty(int, required=True)
  active_nodes = db.ListProperty(int, required=True)
  metadata = db.StringProperty()

