import os

from swarm_models.popular_llms import Fireworks

# Initialize the model
llm = Fireworks(
    temperature=0.2,
    max_tokens=3500,
    openai_api_key=os.getenv("FIREWORKS_API_KEY"),
)

# Run the model
response = llm("What is the meaning of life?")
print(response)
