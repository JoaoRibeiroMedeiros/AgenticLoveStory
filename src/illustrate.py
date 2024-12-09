import openai
import json
import os

# Load configuration from a JSON file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Set API key
os.environ["OPENAI_API_KEY"] = config["OPENAI_API_SECRET_KEY"]

# Configure OpenAI with the API key
openai.api_key = os.environ["OPENAI_API_KEY"]

def generate_image(prompt):
    try:
        # Call the image generation API
        response = openai.images.generate(
            prompt=prompt,
            n=1,  # number of images to generate
            size="1024x1024"  # image size; modify as needed
        )

        # Extract the URL of the generated image
        image_url = response.data[0].url
        return image_url

    except Exception as e:
        return f"An error occurred: {e}"
    


def get_illustration_per_stage(writing_outputs):

    story_stages = list(writing_outputs.keys()).copy()
    story_stages.remove('story_idea')

    img_url_per_stage = {}

    for stage in story_stages:

        img_url = generate_image(stage)
        img_url_per_stage[stage] = img_url

    return img_url_per_stage