
from langchain_core.messages.ai import AIMessage
from langchain_openai import ChatOpenAI
import json
import os


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