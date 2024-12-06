import json

def load_prompts(prompt_type):

    json_file_path = 'prompts/'+prompt_type+'_prompts.json'
    with open(json_file_path, 'r') as file:
        prompts = json.load(file)

    return prompts

def add_task_to_prompts(state_prompts, task_prompts, task):

    tasked_state_prompts = {}
    
    for i, (key, prompt) in enumerate(list(state_prompts.items())):

        tasked_prompt = prompt + task_prompts[task]
        tasked_state_prompts[key] = "Part " + str(i) + " of the story: " + tasked_prompt
    
    return tasked_state_prompts