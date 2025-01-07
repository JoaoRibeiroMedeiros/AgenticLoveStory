import yaml

def load_prompts(prompt_type):

    yaml_file_path = 'prompts/'+prompt_type+'_prompts.yaml'
    with open(yaml_file_path, 'r') as file:
        prompts = yaml.safe_load(file)

    return prompts

def add_task_to_prompts(state_prompts, task_prompts, task):
    # TODO there coud also be a model call here for merging task with prompt

    tasked_state_prompts = {}
    
    for i, (key, prompt) in enumerate(list(state_prompts.items())):

        tasked_prompt = prompt + task_prompts[task]
        tasked_state_prompts[key] = "Part " + str(i) + " " + tasked_prompt
    
    return tasked_state_prompts