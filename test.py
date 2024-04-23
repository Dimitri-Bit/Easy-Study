import os
from modules.GPT import ChatGPT
from dotenv import load_dotenv

load_dotenv()

key = os.environ.get("OPENAI_API_KEY")
gpt = ChatGPT(key, "You are a large langauge model AI. Answer any given questions/inquries with the bets of your abilities.")

response = gpt.get_response("Write me a poem about brawl stars.")
print(f"Response: {response.choices[0].message.content}")