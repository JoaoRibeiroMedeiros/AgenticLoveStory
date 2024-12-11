from pydantic import BaseModel
from src.ai.prompts import load_prompts, add_task_to_prompts
from src.ai.model import call_model


class ReadState(BaseModel):
    outputs: dict[str,str]
    prompts: dict[str,str]

state_prompts = load_prompts('read/state')
task_prompts = load_prompts('read/task')

story_analysis_prompts = add_task_to_prompts(state_prompts, task_prompts, 'story_analysis')
consistency_prompts = add_task_to_prompts(state_prompts, task_prompts, 'consistency')


def load_outputs_placeholder(storyline, flow_type):

    state_prompts = load_prompts(flow_type +'/state')
    outputs = {}
    outputs['storyline'] = storyline

    for action in list(state_prompts.keys()): 
        outputs[action] = ""
    
    return outputs


def get_initial_state(storyline, flow_type = 'read', task='story_analysis'):

    initial_state_outputs_placeholder = load_outputs_placeholder(storyline, flow_type)

    state_prompts = load_prompts(flow_type +'/state')
    task_prompts = load_prompts(flow_type +'/task')
    tasked_state_prompts = add_task_to_prompts(state_prompts, task_prompts, task)

    initial_state = ReadState(prompts=tasked_state_prompts, outputs=initial_state_outputs_placeholder)

    return initial_state


def get_summary(state: ReadState):
    summary = call_model(story_analysis_prompts['summary'] + state.outputs['storyline'])
    state.outputs['summary'] = summary
    return state

def get_main_themes(state: ReadState):
    main_themes = call_model(story_analysis_prompts['main_themes'] + state.outputs['storyline'] 
                             +consistency_prompts['summary'] + state.outputs['storyline'])
    state.outputs['main_themes'] = main_themes
    return state

def get_character_development(state: ReadState):
    character_development = call_model(story_analysis_prompts['character_development'] + state.outputs['storyline'] 
                             +consistency_prompts['summary'] + state.outputs['storyline'])
    state.outputs['character_development'] = character_development
    return state

def get_conflict_resolution(state: ReadState):
    conflict_resolution = call_model(story_analysis_prompts['conflict_resolution'] + state.outputs['storyline'] 
                             +consistency_prompts['summary'] + state.outputs['storyline'])
    state.outputs['conflict_resolution'] = conflict_resolution
    return state

def get_pacing_and_structure(state: ReadState):
    pacing_and_structure = call_model(story_analysis_prompts['pacing_and_structure'] + state.outputs['storyline'] )
    state.outputs['pacing_and_structure'] = pacing_and_structure
    return state

def get_pros(state: ReadState):
    pros = call_model(story_analysis_prompts['pros'] + state.outputs['storyline'] + 
                     consistency_prompts['summary'] + state.outputs['summary'] + 
                     consistency_prompts['main_themes'] + state.outputs['main_themes'] +
                     consistency_prompts['character_development'] + state.outputs['character_development'] +
                     consistency_prompts['conflict_resolution'] + state.outputs['conflict_resolution'] +
                     consistency_prompts['pacing_and_structure'] + state.outputs['conflict_resolution'] 
                      )
    state.outputs['pros'] = pros
    return state

def get_cons(state: ReadState):
    cons = call_model(story_analysis_prompts['cons'] + state.outputs['storyline'] + 
                     consistency_prompts['summary'] + state.outputs['summary'] + 
                     consistency_prompts['main_themes'] + state.outputs['main_themes'] +
                     consistency_prompts['character_development'] + state.outputs['character_development'] +
                     consistency_prompts['conflict_resolution'] + state.outputs['conflict_resolution'] +
                     consistency_prompts['pacing_and_structure'] + state.outputs['conflict_resolution'] 
                      )
    state.outputs['cons'] = cons
    return state

def get_marketability(state: ReadState):

    marketability = call_model(story_analysis_prompts['marketability'] + state.outputs['storyline'] + 
                     consistency_prompts['summary'] + state.outputs['summary'] + 
                     consistency_prompts['main_themes'] + state.outputs['main_themes'] +
                     consistency_prompts['character_development'] + state.outputs['character_development'] +
                     consistency_prompts['conflict_resolution'] + state.outputs['conflict_resolution'] +
                     consistency_prompts['pacing_and_structure'] + state.outputs['conflict_resolution'] 
                      )
    state.outputs['marketability'] = marketability
    return state