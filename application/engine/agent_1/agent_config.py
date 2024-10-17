import pandas as pd
import os
import dotenv

# Load environment variables (e.g., API keys)
dotenv.load_dotenv()

# Import the necessary components from the rakam_systems library
from rakam_systems.components.agents.agents import Agent, Action
from rakam_systems.components.agents.actions import RAGGeneration, GenericLLMResponse
from rakam_systems.components.vector_search.vector_store import VectorStore
from application.engine.agent_1.prompts import PLACEHOLDER_SYS_PROMPT

# Placeholder system prompt

# AGENT and MODEL are set globally
AGENT = None
MODEL = "gpt-4"


# TODO : Define your action functions here
class DummyAction(Action):
    def __init__(self, agent, **kwargs):
        """Dummy action initialization"""
        pass

    def execute(self, **kwargs):
        """Executes the dummy action"""
        return "Dummy Action Executed"


# TODO : Define your agent here
class CustomAgent(Agent):
    def __init__(self, model: str, api_key: str):
        """
        Initialize the agent with the given model and API key.
        Set up all the necessary actions for the agent.
        """
        super().__init__(model)

        # TODO: setup actions
        self.actions = {
            "dummy": DummyAction(self)
            # You can add more actions here, such as RAGGeneration or LLM-based actions
        }

    # TODO : Define your agent « policy function » here to choose the action
    def choose_action(self) -> Action:
        """
        Classifies the query and selects the appropriate action.
        """
        # Example policy logic: always choose the "dummy" action for now
        if True:
            current_action = self.actions.get("dummy", None)
        else:
            current_action = self.actions.get("dummy", None)

        if current_action is None:
            raise ValueError("Action 'dummy' not found in actions dictionary.")

        return current_action


# Initialize the AGENT with the model and API key
AGENT = CustomAgent(model=MODEL, api_key=os.getenv("OPENAI_API_KEY"))

# TODO: You can later use the CustomAgent to choose and execute actions based on the user input
