# load some fake data (TEST ONLY)
# run this in the admin console to populate app.
node = Node(name='foo',
            description='test node')
node.put()
workflow = Workflow(name="test workflow",
                    description="test only workflow",
                    components=[node.key.integer_id()])
workflow.put()
task = Task(name='order 1',
            workflow='test workflow',
            active_nodes=[node.key.integer_id()],
            metadata='test task')
task.put()
