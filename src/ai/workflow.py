from langgraph.graph import END, START, StateGraph
from IPython.display import Markdown, display
import os
import json

from src.ai.read import (
    get_summary,
    get_main_themes,
    get_character_development,
    get_conflict_resolution,
    get_pacing_and_structure,
    get_cons,
    get_pros,
    get_marketability,
    ReadState
)

from src.ai.write import (
    get_you,
    get_need,
    get_go,
    get_search,
    get_find,
    get_take,
    get_return,
    get_change,
    WriteState
)

class ReadflowManager:

    def __init__(self):
        self.workflow = StateGraph(ReadState)

        self.workflow.add_node('get_summary', get_summary)
        self.workflow.add_node('get_main_themes', get_main_themes)
        self.workflow.add_node('get_character_development', get_character_development)
        self.workflow.add_node('get_conflict_resolution', get_conflict_resolution)
        self.workflow.add_node('get_pacing_and_structure', get_pacing_and_structure)
        self.workflow.add_node('get_cons', get_cons)
        self.workflow.add_node('get_pros', get_pros)
        self.workflow.add_node('get_marketability', get_marketability)

        self.workflow.add_edge(START, 'get_summary')
        self.workflow.add_edge('get_summary', 'get_main_themes')
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
    

class WriteflowManager:

    def __init__(self):
        self.workflow = StateGraph(ReadState)

        self.workflow.add_node('you', get_you)
        self.workflow.add_node('need', get_need)
        self.workflow.add_node('go', get_go)
        self.workflow.add_node('search', get_search)
        self.workflow.add_node('find', get_find)
        self.workflow.add_node('take', get_take)
        self.workflow.add_node('return', get_return)
        self.workflow.add_node('change', get_change)

        self.workflow.add_edge(START, 'you')
        self.workflow.add_edge('you', 'need')
        self.workflow.add_edge('need', 'go')
        self.workflow.add_edge('go', 'search')
        self.workflow.add_edge('search', 'find')
        self.workflow.add_edge('find', 'take')
        self.workflow.add_edge('take', 'return')
        self.workflow.add_edge('return', 'change')
        self.workflow.add_edge('change', END)
        
        self.app = self.workflow.compile()

    def invoke(self, initial_state: ReadState):
        output = self.app.invoke(input = initial_state)
        return output


def display_outputs(workflow):

    for key in list(workflow['outputs'].keys()):
        display(Markdown(f"### {key.replace('_', ' ').capitalize()}"))
        display(Markdown(workflow['outputs'][key]))

def display_output(title, text):

    display(Markdown(f"### {title.replace('_', ' ').capitalize()}"))
    display(Markdown(text))

def save_outputs(workflow, tracking_index):

    output_path = os.path.join(os.getcwd(), 'data/experiments/'+ tracking_index + '_workflow_outputs.json')

    with open(output_path, 'w') as f:
        json.dump(workflow['outputs'], f, indent=4)


def load_outputs( tracking_index):

    output_path = os.path.join(os.getcwd(), 'data/experiments/'+ tracking_index + '_workflow_outputs.json')

    with open(output_path, 'r') as f:
        outputs = json.load(f)

    return outputs


def load_joined_outputs( tracking_index):

    output_path = os.path.join(os.getcwd(), 'data/experiments/'+ tracking_index + '_workflow_outputs.json')

    with open(output_path, 'r') as f:
        outputs = json.load(f)

    final = ' \n\n '.join(outputs.values())

    return final

