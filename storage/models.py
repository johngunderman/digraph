import datetime
from google.appengine.ext import ndb
from google.appengine.api import users


class Node(ndb.Model):
  children = ndb.ListProperty(int)
  workflow = ndb.StringProperty()
  parent_node = ndb.SelfReferenceProperty()
  name = ndb.StringProperty(required=True)
  description = ndb.StringProperty(required=True)

class Workflow(ndb.Model):
  name = ndb.StringProperty()
  description = ndb.StringProperty()
  components = ndb.ListProperty(int)

class Task(ndb.Model):
  name = ndb.StringProperty(int, required=True)
  workflow = ndb.StringProperty()
  active_nodes = ndb.ListProperty(int, required=True)
  metadata = ndb.StringProperty()

