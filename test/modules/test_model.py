import unittest

from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed

from storage.models import Node, Workflow, Task


class ModelTestCase(unittest.TestCase):

    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def testModelNode_to_json(self):
        node = Node(name='test',
                    description='test node',
                    parent_node=None,
                    # TODO: test that nodes cannot be their own children
                    children=[ndb.Key('Node', 2)])
        node.put()
        node.to_json()

    def testModelWorkflow_to_json(self):
        workflow = Workflow(name='test',
                            description='foo',
                            components=[ndb.Key('Node', 1)])
        workflow.put()
        workflow.to_json()

    def testModelTask_to_json(self):
        task = Task(name='test',
                    workflow='test workflow',
                    active_nodes=[ndb.Key('Node', 1)],
                    metadata='test metadata')

if __name__ == '__main__':
    unittest.main()
