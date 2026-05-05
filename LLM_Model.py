from openai import OpenAI
import os


print("Hello AI Agents");


# from groq import Groq
#
# client = Groq(api_key="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")
#
# response = client.chat.completions.create(
#     model="llama-3.3-70b-versatile",
#     messages=[
#         {"role": "user", "content": "Tell me about Elon Musk"}
#     ]
# )
#
# print(response.choices[0].message.content)


from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()  # reads the .env file

client = Groq(api_key=os.getenv("GROQ_API_KEY"))  # reads GROQ_API_KEY from .env

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": "Tell me about Michael Jackson"}
    ]
)

print(response.choices[0].message.content)