from pydantic import BaseModel
from src.ai.prompts import load_prompts, add_task_to_prompts
from src.ai.model import call_model
from src.ai.utils import FlowState


state_prompts = load_prompts('write/state')
task_prompts = load_prompts('write/task')

storytelling_prompts = add_task_to_prompts(state_prompts, task_prompts, 'storytelling')
coherence_prompts = add_task_to_prompts(state_prompts, task_prompts, 'coherence')


def get_you(state: FlowState):
    you = call_model(state_prompts['you'] + state.outputs['story'])
    state.outputs['you'] = you
    return state

def get_need(state: FlowState):
    need = call_model(storytelling_prompts['need'] + state.outputs['story'] 
                                + coherence_prompts['you'] + state.outputs['you'])
    state.outputs['need'] = need
    return state

def get_go(state: FlowState):
    go = call_model(storytelling_prompts['go'] + state.outputs['story'] 
                                + coherence_prompts['you'] + state.outputs['you']
                                + coherence_prompts['need'] + state.outputs['need'])
    state.outputs['go'] = go
    return state

def get_search(state: FlowState):
    search = call_model(storytelling_prompts['search'] + state.outputs['story'] 
                                + coherence_prompts['you'] + state.outputs['you']
                                + coherence_prompts['need'] + state.outputs['need']
                                + coherence_prompts['go'] + state.outputs['go'])
    state.outputs['search'] = search
    return state

def get_find(state: FlowState):
    find = call_model(storytelling_prompts['find'] + state.outputs['story'] 
                        + coherence_prompts['you'] + state.outputs['you'] 
                        + coherence_prompts['need'] + state.outputs['need']
                        + coherence_prompts['go'] + state.outputs['go']
                        + coherence_prompts['search'] + state.outputs['need'])
    state.outputs['find'] = find
    return state

def get_take(state: FlowState):
    take = call_model(storytelling_prompts['take'] + state.outputs['story'] + 
                        coherence_prompts['you'] + state.outputs['you'] + 
                        coherence_prompts['need'] + state.outputs['need'] +
                        coherence_prompts['go'] + state.outputs['go'] +
                        coherence_prompts['search'] + state.outputs['search'] +
                        coherence_prompts['find'] + state.outputs['find'] 
                        )
    state.outputs['take'] = take
    return state

def get_return(state: FlowState):
    return_ = call_model(storytelling_prompts['return'] + state.outputs['story'] + 
                        coherence_prompts['you'] + state.outputs['you'] + 
                        coherence_prompts['need'] + state.outputs['need'] +
                        coherence_prompts['go'] + state.outputs['go'] +
                        coherence_prompts['search'] + state.outputs['search'] +
                        coherence_prompts['find'] + state.outputs['find'] +
                        coherence_prompts['take'] + state.outputs['take']
                        )
    state.outputs['return'] = return_
    return state

def get_change(state: FlowState):
    change = call_model(storytelling_prompts['change'] + state.outputs['story'] + 
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
