import os
from dotenv import load_dotenv
from openai import OpenAI
from prompts import sys_prompt, user_prompt

load_dotenv()

GROQ_BASE_URL="https://api.groq.com/openai/v1"

client = OpenAI(
    base_url=GROQ_BASE_URL,
    api_key= os.getenv('GROQ_API_KEY')
)

question = input("Please enter your question: ")

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "system", "content": sys_prompt(question)},
        {"role": "user", "content": user_prompt(question)}
    ],
    stream=True
)

res = ""

for chunk in response:
    if chunk.choices and chunk.choices[0].delta:
        content = chunk.choices[0].delta.content
        if content:
            print(content, end="", flush=True)
            res += content