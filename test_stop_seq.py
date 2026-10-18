import os, dotenv
import google.genai as genai
from google.genai import types

dotenv.load_dotenv(override=True)
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
config = types.GenerateContentConfig(stop_sequences=['Observation:', '\nObservation:'], temperature=0.1)
prompt = """You are a helpful assistant. Output:
Thought: I will test find_route
Action: find_route
Action Input: {"keyword": "billing"}
Observation: fake observation"""
res = client.models.generate_content(model='gemini-3.5-flash-lite', contents=prompt, config=config)
print('Generated text:\n', res.text)
