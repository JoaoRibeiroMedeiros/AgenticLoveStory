from langgraph import StateGraph
from src.read import (
    make_summary,
    get_main_themes,
    get_character_themes,
    get_conflict_resolution,
    get_pacing_and_structure,
    get_cons,
    get_pros,
    get_marketability,
    leverage_summary,
    leverage_main_themes,
    leverage_pros,
    leverage_character_themes,
    leverage_conflict_resolution,
    leverage_pacing_and_structure,
    leverage_cons,
    leverage_marketability,
    ReadState
)

class WorkflowManager:
    def __init__(self):
        self.workflow = StateGraph(ReadState)
        self.workflow.add_node('make_summary', make_summary)
        self.workflow.add_node('get_main_themes', get_main_themes)
        self.workflow.add_node('get_character_themes', get_character_themes)
        self.workflow.add_node('get_conflict_resolution', get_conflict_resolution)
        self.workflow.add_node('get_pacing_and_structure', get_pacing_and_structure)
        self.workflow.add_node('get_cons', get_cons)
        self.workflow.add_node('get_pros', get_pros)
        self.workflow.add_node('get_marketability', get_marketability)
        self.workflow.add_node('leverage_summary', leverage_summary)
        self.workflow.add_node('leverage_main_themes', leverage_main_themes)
        self.workflow.add_node('leverage_pros', leverage_pros)
        self.workflow.add_node('leverage_character_themes', leverage_character_themes)
        self.workflow.add_node('leverage_conflict_resolution', leverage_conflict_resolution)
        self.workflow.add_node('leverage_pacing_and_structure', leverage_pacing_and_structure)
        self.workflow.add_node('leverage_cons', leverage_cons)
        self.workflow.add_node('leverage_marketability', leverage_marketability)
        self.app = self.workflow.compile()

    def invoke(self, initial_state: ReadState):
        output = app.invoke(input = initial_state)

