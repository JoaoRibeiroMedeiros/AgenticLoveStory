import openai
import json
import os

from IPython.display import Image, display
import requests

from src.workflow import display_output

# Load configuration from a JSON file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Set API key
os.environ["OPENAI_API_KEY"] = config["OPENAI_API_SECRET_KEY"]

# Configure OpenAI with the API key
openai.api_key = os.environ["OPENAI_API_KEY"]

def generate_image(prompt, style):

    # insert length threshold (1000 characters)
    with open('prompts/illustrate/style.json', 'r') as config_file:
        style_prompts = json.load(config_file)

    style_prompt = style_prompts[style]
    prompt_with_style = prompt[0:900] + style_prompt

    try:
        # Call the image generation API
        response = openai.images.generate(
            prompt=prompt_with_style,
            n=1,  # number of images to generate
            size="512x512"  # image size; modify as needed
        )

        # Extract the URL of the generated image
        image_url = response.data[0].url
        return image_url

    except Exception as e:
        return f"An error occurred: {e}"

def get_illustration_per_stage(writing_outputs, style):

    story_stages = list(writing_outputs.keys()).copy()
    story_stages.remove('story_idea')

    img_url_per_stage = {}

    for stage in story_stages:
        
        img_url = generate_image(writing_outputs[stage], style)
        img_url_per_stage[stage] = img_url

    return img_url_per_stage

def display_image_from_url(url):
    # Fetch the image from the URL
    response = requests.get(url)
    if response.status_code == 200:
        # Display the image in the notebook
        display(Image(url=url))
    else:
        print("Failed to retrieve image")


def display_illustration_for_all_stages(writing_outputs, img_url_per_stage):

    story_stages = list(writing_outputs.keys()).copy()
    story_stages.remove('story_idea')

    for stage in story_stages:
        display_output(stage, writing_outputs[stage])
        if 'https'in img_url_per_stage[stage]:
            display_image_from_url(img_url_per_stage[stage])