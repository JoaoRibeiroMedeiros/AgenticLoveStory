from src.ai.prompts import load_prompts, add_task_to_prompts
from pydantic import BaseModel

class FlowState(BaseModel):
    outputs: dict[str,str]
    prompts: dict[str,str]

def load_outputs_placeholder(story, flow_type):

    state_prompts = load_prompts(flow_type +'/state')
    
    outputs = {}

    outputs['story'] = story

    for action in list(state_prompts.keys()): 
        outputs[action] = ""
    
    return outputs


def get_initial_state(storyline, flow_type, task):

    initial_state_outputs_placeholder = load_outputs_placeholder(storyline, flow_type)

    state_prompts = load_prompts(flow_type +'/state')
    task_prompts = load_prompts(flow_type +'/task')

    tasked_state_prompts = add_task_to_prompts(state_prompts, task_prompts, task)
    initial_state = FlowState(prompts=tasked_state_prompts, outputs=initial_state_outputs_placeholder)

    return initial_state