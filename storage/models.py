import datetime
from google.appengine.ext import db
from google.appengine.api import users


class Node(db.Model):
  children = db.ListProperty(int)
  parent = db.SelfReferenceProperty()
  name = db.StringProperty(required=True)
  description = db.StringProperty(required=True)

class Task(db.Model):
  active_nodes = db.ListProperty(required=True, int)
  metadata = db.StringProperty(required=True)

