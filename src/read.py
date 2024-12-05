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
with open('/Users/joao/AgenticLoveStory/prompts_per_action.json', 'r') as file:
    prompts = json.load(file)



summary_prompt = prompts["summary_prompt"]
get_main_themes_prompt = prompts["get_main_themes_prompt"]
get_character_development_prompt = prompts["get_character_development_prompt"]
get_conflict_resolution_prompt = prompts["get_conflict_resolution_prompt"]
get_pacing_and_structure_prompt = prompts["get_pacing_and_structure_prompt"]
get_pros_prompt = prompts["get_pros_prompt"]
get_cons_prompt = prompts["get_cons_prompt"]
get_marketability_prompt = prompts["get_marketability_prompt"]

leverage_summary_prompt = prompts["leverage_summary_prompt"]
leverage_main_themes_prompt = prompts["leverage_main_themes_prompt"]
leverage_character_development_prompt = prompts["leverage_character_development_prompt"]
leverage_conflict_resolution_prompt = prompts["leverage_conflict_resolution_prompt"]
leverage_pacing_and_structure_prompt = prompts["leverage_pacing_and_structure_prompt"]
leverage_pros_prompt = prompts["leverage_pros_prompt"]
leverage_cons_prompt = prompts["leverage_cons_prompt"]
leverage_marketability_prompt = prompts["leverage_marketability_prompt"]


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

def load_outputs_placeholder(story_line):
        # Define the path to the JSON file
    json_file_path = 'prompts_per_action.json'

    # Read the JSON file and load the prompts
    with open(json_file_path, 'r') as file:
        prompts_per_action = json.load(file)

    outputs = {action: "" for action in list(prompts_per_action.keys())}
    outputs['story_line'] = story_line

    return outputs


def make_summary(state: ReadState):
    summary = call_model(summary_prompt + state.outputs['story_line'])
    output_state = ReadState(outputs={
        'story_line': state.outputs['story_line'], 
        'summary': summary, 
        'main_themes': "", 
        'character_development': "",
        'conflict_resolution': "",
        'pacing_structure': "",
        'pros': "", 
        'cons': "",
        'marketability': ""
    }, prompts=state.prompts)
    return output_state

def get_main_themes(state: ReadState):
    main_themes = call_model(get_main_themes_prompt + state.outputs['story_line'] 
                             + leverage_summary_prompt + state.outputs['story_line'])
    output_state = ReadState(outputs={
        'story_line': state.outputs['story_line'], 
        'summary': state.outputs['summary'], 
        'main_themes': main_themes, 
        'character_development': "",
        'conflict_resolution': "",
        'pacing_structure': "",
        'pros': "", 
        'cons': "",
        'marketability': ""
    }, prompts=state.prompts)
    return output_state

def get_character_development(state: ReadState):
    character_development = call_model(get_character_development_prompt + state.outputs['story_line'] 
                             + leverage_summary_prompt + state.outputs['story_line'])
    output_state = ReadState(outputs={
        'story_line': state.outputs['story_line'], 
        'summary': state.outputs['summary'], 
        'main_themes': state.outputs['main_themes'], 
        'character_development': character_development,
        'conflict_resolution': "",
        'pacing_structure': "",
        'pros': "", 
        'cons': "",
        'marketability': ""
    }, prompts=state.prompts)
    return output_state

def get_conflict_resolution(state: ReadState):
    conflict_resolution = call_model(get_conflict_resolution_prompt + state.outputs['story_line'] 
                             + leverage_summary_prompt + state.outputs['story_line'])
    output_state = ReadState(outputs={
        'story_line': state.outputs['story_line'], 
        'summary': state.outputs['summary'], 
        'main_themes': state.outputs['main_themes'], 
        'character_development': state.outputs['character_development'],
        'conflict_resolution': conflict_resolution,
        'pacing_structure': "",
        'pros': "", 
        'cons': "",
        'marketability': ""
    }, prompts=state.prompts)
    return output_state

def get_pacing_and_structure(state: ReadState):
    pacing_structure = call_model(get_pacing_and_structure_prompt + state.outputs['story_line'] 
                      + leverage_summary_prompt + state.outputs['summary'] 
                      + leverage_main_themes_prompt + state.outputs['main_themes'])
    output_state = ReadState(outputs={
        'story_line': state.outputs['story_line'], 
        'summary': state.outputs['summary'], 
        'main_themes': state.outputs['main_themes'], 
        'character_development': state.outputs['character_development'],
        'conflict_resolution': state.outputs['conflict_resolution'],
        'pacing_structure': pacing_structure,
        'pros': "", 
        'cons': "",
        'marketability': ""
    }, prompts=state.prompts)
    return output_state

def get_pros(state: ReadState):
    pros = call_model(get_pros_prompt + state.outputs['story_line'] + 
                      leverage_summary_prompt + state.outputs['summary'] + 
                      leverage_main_themes_prompt + state.outputs['main_themes'] +
                      leverage_character_development_prompt + state.outputs['character_development'] +
                      leverage_conflict_resolution_prompt + state.outputs['conflict_resolution'] +
                      leverage_pacing_and_structure_prompt + state.outputs['conflict_resolution'] 
                      )

    output_state = ReadState(outputs={
        'story_line': state.outputs['story_line'], 
        'summary': state.outputs['summary'], 
        'main_themes': state.outputs['main_themes'], 
        'character_development': state.outputs['character_development'],
        'conflict_resolution': state.outputs['conflict_resolution'],
        'pacing_structure': state.outputs['pacing_structure'],
        'pros': pros, 
        'cons': "",
        'marketability': ""
    }, prompts=state.prompts)

    return output_state

def get_cons(state: ReadState):
    cons = call_model(get_cons_prompt + state.outputs['story_line'] + 
                      leverage_summary_prompt + state.outputs['summary'] + 
                      leverage_main_themes_prompt + state.outputs['main_themes'] +
                      leverage_character_development_prompt + state.outputs['character_development'] +
                      leverage_conflict_resolution_prompt + state.outputs['conflict_resolution'] +
                      leverage_pacing_and_structure_prompt + state.outputs['conflict_resolution'] 
                      )
    output_state = ReadState(outputs={
        'story_line': state.outputs['story_line'], 
        'summary': state.outputs['summary'], 
        'main_themes': state.outputs['main_themes'], 
        'character_development': state.outputs['character_development'],
        'conflict_resolution': state.outputs['conflict_resolution'],
        'pacing_structure': state.outputs['pacing_structure'],
        'pros': state.outputs['pros'], 
        'cons': cons,
        'marketability': ""
    }, prompts=state.prompts)
    return output_state

def get_marketability(state: ReadState):

    marketabillity = call_model(get_marketability_prompt + state.outputs['story_line'] + 
                      leverage_summary_prompt + state.outputs['summary'] + 
                      leverage_main_themes_prompt + state.outputs['main_themes'] +
                      leverage_character_development_prompt + state.outputs['character_development'] +
                      leverage_conflict_resolution_prompt + state.outputs['conflict_resolution'] +
                      leverage_pacing_and_structure_prompt + state.outputs['conflict_resolution'] 
                      )

    output_state = ReadState(outputs={
        'story_line': state.outputs['story_line'], 
        'summary': state.outputs['summary'], 
        'main_themes': state.outputs['main_themes'], 
        'character_development': state.outputs['character_development'],
        'conflict_resolution': state.outputs['conflict_resolution'],
        'pacing_structure': state.outputs['pacing_structure'],
        'pros': state.outputs['pros'], 
        'cons': state.outputs['cons'],
        'marketability': ""
    }, prompts=state.prompts)

    return output_state