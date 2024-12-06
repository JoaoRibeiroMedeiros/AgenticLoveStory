from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel
from langchain_core.messages.ai import AIMessage
import json
import os


class ReadState(BaseModel):
    outputs: dict[str,str]
    prompts: dict[str,str]


# Load prompts from JSON file
with open('/Users/joao/AgenticLoveStory/prompts/read/get_prompts.json', 'r') as file:
    prompt_get = json.load(file)

with open('/Users/joao/AgenticLoveStory/prompts/read/leverage_prompts.json', 'r') as file:
    prompt_leverage = json.load(file)

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

    
os.environ["OPEN_API_KEY"] = config["OPENAI_API_SECRET_KEY"]

model = ChatOpenAI(model="gpt-4o",
                   max_tokens=2000,
                   temperature=0,
                   top_p=1,
                   api_key= os.environ["OPEN_API_KEY"])


def call_model(field):
    response = model.invoke(field)
    if isinstance(response, AIMessage):
        response_content = response.content  # Adjust this based on the actual property
    else:
        response_content = str(response)
    return response_content

def load_outputs_placeholder(storyline):
        # Define the path to the JSON file
    json_file_path = 'get_prompts.json'

    # Read the JSON file and load the prompts
    with open(json_file_path, 'r') as file:
        prompts_per_action = json.load(file)

    outputs = {}
    
    outputs['storyline'] = storyline

    for action in list(prompts_per_action.keys()): 
        outputs[action] = ""
    
    return outputs


def get_initial_state(storyline):

    initial_state_outputs_placeholder = load_outputs_placeholder(storyline)

    with open('get_prompts.json', 'r') as file:
        get_prompts = json.load(file)

    initial_state =  ReadState(prompts = get_prompts, outputs = initial_state_outputs_placeholder)

    return initial_state


def make_summary(state: ReadState):
    summary = call_model(prompt_get['summary'] + state.outputs['storyline'])
    state.outputs['summary'] = summary
    return state

def get_main_themes(state: ReadState):
    main_themes = call_model(prompt_get['main_themes'] + state.outputs['storyline'] 
                             + prompt_leverage['summary'] + state.outputs['storyline'])
    state.outputs['main_themes'] = main_themes
    return state

def get_character_development(state: ReadState):
    character_development = call_model(prompt_get['character_development'] + state.outputs['storyline'] 
                             + prompt_leverage['summary'] + state.outputs['storyline'])
    state.outputs['character_development'] = character_development
    return state

def get_conflict_resolution(state: ReadState):
    conflict_resolution = call_model(prompt_get['conflict_resolution'] + state.outputs['storyline'] 
                             + prompt_leverage['summary'] + state.outputs['storyline'])
    state.outputs['conflict_resolution'] = conflict_resolution
    return state

def get_pacing_and_structure(state: ReadState):
    pacing_and_structure = call_model(prompt_get['pacing_and_structure'] + state.outputs['storyline'] 
                      + prompt_leverage['summary'] + state.outputs['summary'] 
                      + prompt_leverage['main_themes'] + state.outputs['main_themes'])
    state.outputs['pacing_and_structure'] = pacing_and_structure
    return state

def get_pros(state: ReadState):
    pros = call_model(prompt_get['pros'] + state.outputs['storyline'] + 
                      prompt_leverage['summary'] + state.outputs['summary'] + 
                      prompt_leverage['main_themes'] + state.outputs['main_themes'] +
                      prompt_leverage['character_development'] + state.outputs['character_development'] +
                      prompt_leverage['conflict_resolution'] + state.outputs['conflict_resolution'] +
                      prompt_leverage['pacing_and_structure'] + state.outputs['conflict_resolution'] 
                      )
    state.outputs['pros'] = pros
    return state

def get_cons(state: ReadState):
    cons = call_model(prompt_get['cons'] + state.outputs['storyline'] + 
                      prompt_leverage['summary'] + state.outputs['summary'] + 
                      prompt_leverage['main_themes'] + state.outputs['main_themes'] +
                      prompt_leverage['character_development'] + state.outputs['character_development'] +
                      prompt_leverage['conflict_resolution'] + state.outputs['conflict_resolution'] +
                      prompt_leverage['pacing_and_structure'] + state.outputs['conflict_resolution'] 
                      )
    state.outputs['cons'] = cons
    return state

def get_marketability(state: ReadState):

    marketability = call_model(prompt_get['marketability'] + state.outputs['storyline'] + 
                      prompt_leverage['summary'] + state.outputs['summary'] + 
                      prompt_leverage['main_themes'] + state.outputs['main_themes'] +
                      prompt_leverage['character_development'] + state.outputs['character_development'] +
                      prompt_leverage['conflict_resolution'] + state.outputs['conflict_resolution'] +
                      prompt_leverage['pacing_and_structure'] + state.outputs['conflict_resolution'] 
                      )
    state.outputs['marketability'] = marketability
    return state