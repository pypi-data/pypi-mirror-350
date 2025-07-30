from pygeai.lab.managers import AILabManager
from pygeai.lab.models import Agent

manager = AILabManager()

result = manager.publish_agent_revision(
    project_id="2ca6883f-6778-40bb-bcc1-85451fb11107",
    agent_id="9716a0a1-5eab-4cc9-a611-fa2c3237c511",
    revision="6"
)

if isinstance(result, Agent):
    print(f"Published agent: {result.name}, ID: {result.id}")
    print(f"Revision: {result.revision}, Draft: {result.is_draft}")
else:
    print("Errors:", result.errors)