import os

from swarm_models.models import Anthropic

model = Anthropic(anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"))

task = "What is quantum field theory? What are 3 books on the field?"

print(model(task))
