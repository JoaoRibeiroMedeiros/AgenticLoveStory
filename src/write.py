from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from langchain_core.messages.ai import AIMessage
import json
import os


class WriteState(BaseModel):
    outputs: dict[str,str]
    prompts: dict[str,str]


# Load prompts from JSON file
with open('/Users/joao/AgenticLoveStory/prompts/write/get_prompts.json', 'r') as file:
    prompt_get = json.load(file)

with open('/Users/joao/AgenticLoveStory/prompts/write/leverage_prompts.json', 'r') as file:
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

def load_outputs_placeholder(story_idea):

        # Define the path to the JSON file
    json_file_path = 'get_prompts.json'

    # Read the JSON file and load the prompts
    with open(json_file_path, 'r') as file:
        prompts_per_action = json.load(file)

    outputs = {}
    
    outputs['story_idea'] = story_idea

    for action in list(prompts_per_action.keys()): 
        outputs[action] = ""
    
    return outputs


def get_initial_state(story_idea):

    initial_state_outputs_placeholder = load_outputs_placeholder(story_idea)

    with open('get_prompts.json', 'r') as file:
        get_prompts = json.load(file)

    initial_state =  WriteState(prompts = get_prompts, outputs = initial_state_outputs_placeholder)

    return initial_state

def get_you(state: WriteState):
    you = call_model(prompt_get['you'] + state.outputs['story_idea'])
    state.outputs['you'] = you
    return state

def get_need(state: WriteState):
    need = call_model(prompt_get['need'] + state.outputs['story_idea'] 
                                + prompt_leverage['you'] + state.outputs['you'])
    state.outputs['need'] = need
    return state

def get_go(state: WriteState):
    go = call_model(prompt_get['go'] + state.outputs['story_idea'] 
                                + prompt_leverage['you'] + state.outputs['you']
                                + prompt_leverage['need'] + state.outputs['need'])
    state.outputs['go'] = go
    return state

def get_search(state: WriteState):
    search = call_model(prompt_get['search'] + state.outputs['story_idea'] 
                                + prompt_leverage['you'] + state.outputs['you']
                                + prompt_leverage['need'] + state.outputs['need']
                                + prompt_leverage['go'] + state.outputs['go'])
    state.outputs['search'] = search
    return state

def get_find(state: WriteState):
    find = call_model(prompt_get['find'] + state.outputs['story_idea'] 
                        + prompt_leverage['you'] + state.outputs['you'] 
                        + prompt_leverage['need'] + state.outputs['need']
                        + prompt_leverage['go'] + state.outputs['go']
                        + prompt_leverage['search'] + state.outputs['need'])
    state.outputs['find'] = find
    return state

def get_take(state: WriteState):
    take = call_model(prompt_get['take'] + state.outputs['story_idea'] + 
                        prompt_leverage['you'] + state.outputs['you'] + 
                        prompt_leverage['need'] + state.outputs['need'] +
                        prompt_leverage['go'] + state.outputs['go'] +
                        prompt_leverage['search'] + state.outputs['search'] +
                        prompt_leverage['find'] + state.outputs['find'] 
                        )
    state.outputs['take'] = take
    return state

def get_return(state: WriteState):
    return_ = call_model(prompt_get['return'] + state.outputs['story_idea'] + 
                        prompt_leverage['you'] + state.outputs['you'] + 
                        prompt_leverage['need'] + state.outputs['need'] +
                        prompt_leverage['go'] + state.outputs['go'] +
                        prompt_leverage['search'] + state.outputs['search'] +
                        prompt_leverage['find'] + state.outputs['find'] +
                        prompt_leverage['take'] + state.outputs['take']
                        )
    state.outputs['return'] = return_
    return state

def get_change(state: WriteState):
    change = call_model(prompt_get['change'] + state.outputs['story_idea'] + 
                        prompt_leverage['you'] + state.outputs['you'] + 
                        prompt_leverage['need'] + state.outputs['need'] +
                        prompt_leverage['go'] + state.outputs['go'] +
                        prompt_leverage['search'] + state.outputs['search'] +
                        prompt_leverage['find'] + state.outputs['find'] +
                        prompt_leverage['take'] + state.outputs['take'] +
                        prompt_leverage['return'] + state.outputs['return']
                        )
    state.outputs['change'] = change
    return state
