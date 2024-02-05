from openai import OpenAI
from dotenv import find_dotenv, load_dotenv
from scripts import read_or_create_assistant
import os

load_dotenv()
client = OpenAI()  # por default, pega OPENAI_API_KEY do .env
assistant_id = read_or_create_assistant() # reusa ou cria um assistente criativo


thread = client.beta.threads.create(
  messages=[
    {
      "role": "assistant_id",
      "content": "Comece com um tópico. Qual o tema da startup que você deseja criar?"
    }
  ]
)

run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant_id
)