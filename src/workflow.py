from langgraph.graph import END, START, StateGraph
import os

from src.read import (
    make_summary,
    get_main_themes,
    get_character_development,
    get_conflict_resolution,
    get_pacing_and_structure,
    get_cons,
    get_pros,
    get_marketability,
    ReadState
)

class WorkflowManager:

    def __init__(self):
        self.workflow = StateGraph(ReadState)

        self.workflow.add_node('make_summary', make_summary)
        self.workflow.add_node('get_main_themes', get_main_themes)
        self.workflow.add_node('get_character_development', get_character_development)
        self.workflow.add_node('get_conflict_resolution', get_conflict_resolution)
        self.workflow.add_node('get_pacing_and_structure', get_pacing_and_structure)
        self.workflow.add_node('get_cons', get_cons)
        self.workflow.add_node('get_pros', get_pros)
        self.workflow.add_node('get_marketability', get_marketability)

        self.workflow.add_edge(START, 'make_summary')
        self.workflow.add_edge('make_summary', 'get_main_themes')
        self.workflow.add_edge('get_main_themes', 'get_character_development')
        self.workflow.add_edge('get_character_development', 'get_conflict_resolution')
        self.workflow.add_edge('get_conflict_resolution', 'get_pacing_and_structure')
        self.workflow.add_edge('get_pacing_and_structure', 'get_cons')
        self.workflow.add_edge('get_cons', 'get_pros')
        self.workflow.add_edge('get_pros', 'get_marketability')
        self.workflow.add_edge('get_marketability',  END)
        
        self.app = self.workflow.compile()

    def invoke(self, initial_state: ReadState):
        output = self.app.invoke(input = initial_state)
        return output
