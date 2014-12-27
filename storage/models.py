import datetime
import json

from google.appengine.ext import ndb
from google.appengine.api import users

# difficult-to-find but useful cheat-sheet on ndb can be found here:
# https://docs.google.com/document/d/1AefylbadN456_Z7BZOpZEXDq8cR8LYu7QgI7bt5V0Iw/edit

# more documentation can be found at
# https://cloud.google.com/appengine/docs/python/ndb/queries


class Node(ndb.Model):
    children = ndb.KeyProperty(kind='Node', repeated=True)
    parent_node = ndb.KeyProperty(kind='Node')
    name = ndb.StringProperty(required=True)
    description = ndb.StringProperty(required=True)

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        # requires two get() calls per node, so far less than ideal
        # TODO: fix this, pull it into a separate method?
        parent = None if self.parent_node is None or self.parent_node.get() is None \
            else self.parent_node.get().to_dict()
        children = [None if key is None or key.get() is None
                    else key.get().to_dict() for key in self.children]
        return {'children': children,
                'parent_node': parent,
                'name': self.name,
                'description': self.description}


class Workflow(ndb.Model):
    name = ndb.StringProperty()
    description = ndb.StringProperty()
    components = ndb.KeyProperty(kind='Node', repeated=True)

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        components = [None if key is None or key.get() is None
                      else key.get().to_dict() for key in self.components]
        return {'name': self.name,
                'description': self.description,
                'components': components}


class Task(ndb.Model):
    name = ndb.StringProperty(required=True)
    workflow = ndb.StringProperty()
    active_nodes = ndb.KeyProperty(kind='Node', repeated=True)
    metadata = ndb.StringProperty()

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        active_nodes = [None if key is None or key.get() is None
                        else key.get().to_dict() for key in self.active_nodes]
        return {'name': self.name,
                'workflow': self.workflow,
                'active_nodes': active_nodes,
                'metadata': self.metadata}
