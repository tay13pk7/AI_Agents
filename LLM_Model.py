from openai import OpenAI
import os


print("Hello AI Agents");


print("test");

# // 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

from openai import OpenAI

client = OpenAI(
    api_key="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"   # 👈 paste your key directly
)

response = client.responses.create(
    model="gpt-4.1-mini",
    input="Write a one-line joke about AI"
)

print(response.output[0].content[0].text)