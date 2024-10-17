from django.test import TestCase
from application.engine.agent_1.agent_config import AGENT, DummyAction

class CustomAgentTestCase(TestCase):
    def setUp(self):

        pass

    def test_choose_action_executes_dummy_action(self):
        # Choose the action using the AGENT
        action = AGENT.choose_action()

        # Ensure the action is an instance of DummyAction
        self.assertIsInstance(action, DummyAction)

        # Execute the action and check the result
        result = action.execute()
        self.assertEqual(result, "Dummy Action Executed")