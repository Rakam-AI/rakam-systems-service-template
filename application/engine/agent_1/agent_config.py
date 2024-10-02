import pandas as pd

from application.engine.agent_1.prompts import PLACEHOLDER_SYS_PROMPT

import os
import dotenv
dotenv.load_dotenv()

from rakam_systems.generation.agents import Agent, Action
from rakam_systems.generation.agents import RAGGeneration, VectorStores

AGENT = None
MODEL = "gpt-4o"

# TODO : Define your action functions here
class DummyAction(Action):
    def __init__(self, agent, **kwargs):
        pass

    def execute(self, **kwargs):

        return "Dummy"

# TODO : Define your agent here
class CustomAgent(Agent):
    def __init__(
        self,
        model: str,
        api_key: str
    ):
        super().__init__(model, api_key)
        
        # TODO: setup actions
        self.actions = {
            "dummy": DummyAction(self)
        }


    # TODO : Define your agent « policy function» here to choose the action
    def choose_action(self) -> Action:
        """
        Classifies the query and selects the appropriate action
        RAGGeneration instance for either commercial or informative responses.
        """   

        if True : 
            current_action = self.actions.get("dummy", None)
        else : 
            current_action = self.actions.get("dummy", None)

        if current_action is None:
            raise ValueError("Action 'dummy' not found in actions dictionary.")

        return current_action

#------

AGENT = CustomAgent(model=MODEL, api_key=os.getenv("OPENAI_API_KEY"))