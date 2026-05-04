from openai import OpenAI
import os


print("Hello AI Agents");


print("test");

from anthropic import Anthropic

client = Anthropic(api_key="?")  # your key

response = client.messages.create(
    model="claude-sonnet-4-6",  # ✅ updated model
    max_tokens=50,
    messages=[
        {"role": "user", "content": "Write a one-line joke about AI"}
    ]
)

print(response.content[0].text)