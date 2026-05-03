from openai import OpenAI
import os


print("Hello AI Agents");


print("test");


from openai import OpenAI

client = OpenAI(
    api_key="?"
)

response = client.responses.create(
    model="gpt-4.1-mini",
    input="Write a one-line joke about AI"
)

print(response.output[0].content[0].text)