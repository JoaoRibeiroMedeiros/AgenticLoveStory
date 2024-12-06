from pydantic import BaseModel
from src.prompts import load_prompts, add_task_to_prompts
from model import call_model


class WriteState(BaseModel):
    outputs: dict[str,str]
    prompts: dict[str,str]


state_prompts = load_prompts('write/state')
task_prompts = load_prompts('write/task')

storytelling_prompts = add_task_to_prompts(state_prompts, task_prompts, 'storytelling')
coherence_prompts = add_task_to_prompts(state_prompts, task_prompts, 'coherence')


def load_outputs_placeholder(story_idea, flow_type):

    state_prompts = load_prompts(flow_type +'/state')
    outputs = {}
    outputs['story_idea'] = story_idea

    for action in list(state_prompts.keys()): 
        outputs[action] = ""
    
    return outputs


def get_initial_state(story_idea, flow_type = 'write', task='storytelling'):
    """
    Generates the initial state for writing a story based on the provided story idea and task.

    Args:
        story_idea (str): The initial idea or concept for the story.
        task (str, optional): The specific writing task to be performed. Defaults to 'storytelling'.
    """

    initial_state_outputs_placeholder = load_outputs_placeholder(story_idea, flow_type)

    state_prompts = load_prompts('write/state')
    task_prompts = load_prompts('write/task')
    tasked_state_prompts = add_task_to_prompts(state_prompts, task_prompts, task)

    initial_state = WriteState(prompts=tasked_state_prompts, outputs=initial_state_outputs_placeholder)

    return initial_state


def get_you(state: WriteState):
    you = call_model(state_prompts['you'] + state.outputs['story_idea'])
    state.outputs['you'] = you
    return state

def get_need(state: WriteState):
    need = call_model(storytelling_prompts['need'] + state.outputs['story_idea'] 
                                + coherence_prompts['you'] + state.outputs['you'])
    state.outputs['need'] = need
    return state

def get_go(state: WriteState):
    go = call_model(storytelling_prompts['go'] + state.outputs['story_idea'] 
                                + coherence_prompts['you'] + state.outputs['you']
                                + coherence_prompts['need'] + state.outputs['need'])
    state.outputs['go'] = go
    return state

def get_search(state: WriteState):
    search = call_model(storytelling_prompts['search'] + state.outputs['story_idea'] 
                                + coherence_prompts['you'] + state.outputs['you']
                                + coherence_prompts['need'] + state.outputs['need']
                                + coherence_prompts['go'] + state.outputs['go'])
    state.outputs['search'] = search
    return state

def get_find(state: WriteState):
    find = call_model(storytelling_prompts['find'] + state.outputs['story_idea'] 
                        + coherence_prompts['you'] + state.outputs['you'] 
                        + coherence_prompts['need'] + state.outputs['need']
                        + coherence_prompts['go'] + state.outputs['go']
                        + coherence_prompts['search'] + state.outputs['need'])
    state.outputs['find'] = find
    return state

def get_take(state: WriteState):
    take = call_model(storytelling_prompts['take'] + state.outputs['story_idea'] + 
                        coherence_prompts['you'] + state.outputs['you'] + 
                        coherence_prompts['need'] + state.outputs['need'] +
                        coherence_prompts['go'] + state.outputs['go'] +
                        coherence_prompts['search'] + state.outputs['search'] +
                        coherence_prompts['find'] + state.outputs['find'] 
                        )
    state.outputs['take'] = take
    return state

def get_return(state: WriteState):
    return_ = call_model(storytelling_prompts['return'] + state.outputs['story_idea'] + 
                        coherence_prompts['you'] + state.outputs['you'] + 
                        coherence_prompts['need'] + state.outputs['need'] +
                        coherence_prompts['go'] + state.outputs['go'] +
                        coherence_prompts['search'] + state.outputs['search'] +
                        coherence_prompts['find'] + state.outputs['find'] +
                        coherence_prompts['take'] + state.outputs['take']
                        )
    state.outputs['return'] = return_
    return state

def get_change(state: WriteState):
    change = call_model(storytelling_prompts['change'] + state.outputs['story_idea'] + 
                        coherence_prompts['you'] + state.outputs['you'] + 
                        coherence_prompts['need'] + state.outputs['need'] +
                        coherence_prompts['go'] + state.outputs['go'] +
                        coherence_prompts['search'] + state.outputs['search'] +
                        coherence_prompts['find'] + state.outputs['find'] +
                        coherence_prompts['take'] + state.outputs['take'] +
                        coherence_prompts['return'] + state.outputs['return']
                        )
    state.outputs['change'] = change
    return state
