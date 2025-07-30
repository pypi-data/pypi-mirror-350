import os

from swarm_models import OpenAIChat

# Get the OpenAI API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Create an instance of the OpenAIChat class
model = OpenAIChat(openai_api_key=api_key, model_name="gpt-4o-mini")

# Query the model with a question
out = model(
    "What is the best state to register a business in the US for the least amount of taxes?"
)

# Print the model's response
print(out)
