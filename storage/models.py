import datetime
import json

from google.appengine.ext import ndb
from google.appengine.api import users

# difficult-to-find but useful cheat-sheet on ndb can be found here:
# https://docs.google.com/document/d/1AefylbadN456_Z7BZOpZEXDq8cR8LYu7QgI7bt5V0Iw/edit

# more documentation can be found at https://cloud.google.com/appengine/docs/python/ndb/queries

class Node(ndb.Model):
  children = ndb.IntegerProperty(repeated=True)
  parent_node = ndb.KeyProperty(kind='Node')
  name = ndb.StringProperty(required=True)
  description = ndb.StringProperty(required=True)

  def to_json(self):
    return json.dumps(self.to_dict())

  def to_dict(self):
    return {'children': self.children,
          'parent_node': self.parent_node,
          'name': self.name,
          'description': self.description}


class Workflow(ndb.Model):
  name = ndb.StringProperty()
  description = ndb.StringProperty()
  components = ndb.IntegerProperty(repeated=True)

  def to_json(self):
    return json.dumps(
        {'name': self.name,
         'description': self.description,
         'components': self.components})

class Task(ndb.Model):
  name = ndb.StringProperty(required=True)
  workflow = ndb.StringProperty()
  active_nodes = ndb.IntegerProperty(repeated=True)
  metadata = ndb.StringProperty()

  def to_json(self):
    return json.dumps(
        {'name': self.name,
         'workflow': self.workflow,
         'active_nodes':
            [Node.get_by_id(node_id).to_dict() for node_id in self.active_nodes],
         'metadata': self.metadata})

