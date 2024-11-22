

import boto3
from botocore.exceptions import ClientError
from langchain.llms import BaseLLM

import boto3
from botocore.exceptions import ClientError
import os
from langchain.llms import BaseLLM

class BedrockLLM(BaseLLM):
    def __init__(self, model_id, aws_access_key_id, aws_secret_access_key):
        self.model_id = model_id
        self.client = boto3.client(
            "bedrock-runtime",
            region_name="us-east-1",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

    def _call(self, prompt):
        conversation = [
            {
                "role": "user",
                "content": [{"text": prompt}],
            }
        ]
        
        try:
            response = self.client.converse(
                modelId=self.model_id,
                messages=conversation,
                inferenceConfig={"maxTokens": 512, "temperature": 0.5, "topP": 0.9},
            )
            response_text = response["output"]["message"]["content"][0]["text"]
            return response_text
        except ClientError as e:
            raise ValueError(f"An error occurred: {e}")

    def _generate(self, prompts):
        # Convert prompts to a single prompt string for Bedrock
        results = []
        for prompt in prompts:
            results.append(self._call(prompt))
        return results

    @property
    def _llm_type(self):
        return "bedrock"