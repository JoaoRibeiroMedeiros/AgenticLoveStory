
from src.ai.prompts import load_prompts, add_task_to_prompts
from src.ai.model import call_model
from src.ai.utils import FlowState


state_prompts = load_prompts('read/state')
task_prompts = load_prompts('read/task')

story_analysis_prompts = add_task_to_prompts(state_prompts, task_prompts, 'story_analysis')
consistency_prompts = add_task_to_prompts(state_prompts, task_prompts, 'consistency')


def get_summary(state: FlowState):
    summary = call_model(story_analysis_prompts['summary'] + state.outputs['story'])
    state.outputs['summary'] = summary
    return state

def get_main_themes(state: FlowState):
    main_themes = call_model(story_analysis_prompts['main_themes'] + state.outputs['story'] 
                             +consistency_prompts['summary'] + state.outputs['story'])
    state.outputs['main_themes'] = main_themes
    return state

def get_character_development(state: FlowState):
    character_development = call_model(story_analysis_prompts['character_development'] + state.outputs['story'] 
                             +consistency_prompts['summary'] + state.outputs['story'])
    state.outputs['character_development'] = character_development
    return state

def get_conflict_resolution(state: FlowState):
    conflict_resolution = call_model(story_analysis_prompts['conflict_resolution'] + state.outputs['story'] 
                             +consistency_prompts['summary'] + state.outputs['story'])
    state.outputs['conflict_resolution'] = conflict_resolution
    return state

def get_pacing_and_structure(state: FlowState):
    pacing_and_structure = call_model(story_analysis_prompts['pacing_and_structure'] + state.outputs['story'] )
    state.outputs['pacing_and_structure'] = pacing_and_structure
    return state

def get_pros(state: FlowState):
    pros = call_model(story_analysis_prompts['pros'] + state.outputs['story'] + 
                     consistency_prompts['summary'] + state.outputs['summary'] + 
                     consistency_prompts['main_themes'] + state.outputs['main_themes'] +
                     consistency_prompts['character_development'] + state.outputs['character_development'] +
                     consistency_prompts['conflict_resolution'] + state.outputs['conflict_resolution'] +
                     consistency_prompts['pacing_and_structure'] + state.outputs['conflict_resolution'] 
                      )
    state.outputs['pros'] = pros
    return state

def get_cons(state: FlowState):
    cons = call_model(story_analysis_prompts['cons'] + state.outputs['story'] + 
                     consistency_prompts['summary'] + state.outputs['summary'] + 
                     consistency_prompts['main_themes'] + state.outputs['main_themes'] +
                     consistency_prompts['character_development'] + state.outputs['character_development'] +
                     consistency_prompts['conflict_resolution'] + state.outputs['conflict_resolution'] +
                     consistency_prompts['pacing_and_structure'] + state.outputs['conflict_resolution'] 
                      )
    state.outputs['cons'] = cons
    return state

def get_marketability(state: FlowState):

    marketability = call_model(story_analysis_prompts['marketability'] + state.outputs['story'] + 
                     consistency_prompts['summary'] + state.outputs['summary'] + 
                     consistency_prompts['main_themes'] + state.outputs['main_themes'] +
                     consistency_prompts['character_development'] + state.outputs['character_development'] +
                     consistency_prompts['conflict_resolution'] + state.outputs['conflict_resolution'] +
                     consistency_prompts['pacing_and_structure'] + state.outputs['conflict_resolution'] 
                      )
    state.outputs['marketability'] = marketability
    return state