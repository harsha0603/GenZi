import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Retrieve API key from environment variables
api_key = os.getenv("API_KEY")

# Initialize the OpenAI client
client = openai.OpenAI(api_key=api_key)

# Test chat completion request
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello, how are you?"}],
    max_tokens=50
)

# Print the response
print(response.choices[0].message.content.strip())
