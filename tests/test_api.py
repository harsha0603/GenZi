from app.core.llm_processor import generate_gpt4_response

prompt = "Hello, how can I help you today?"
response = generate_gpt4_response(prompt)
print("GPT-4 Response:", response)
