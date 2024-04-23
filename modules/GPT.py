import openai
from openai import OpenAI

class ChatGPT:
    gpt_model = "gpt-3.5-turbo"

    def __init__(self, key, system_prompt):
        self.key = key
        self.system_prompt = system_prompt
        self.client = OpenAI(api_key=key)
    
    
    def get_response(self, message):
        completion = self.client.chat.completions.create(
            model=self.gpt_model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": message}
            ]
        )
        return completion
    