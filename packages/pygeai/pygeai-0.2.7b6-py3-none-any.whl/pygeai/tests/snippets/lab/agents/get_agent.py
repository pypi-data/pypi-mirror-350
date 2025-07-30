from pygeai.lab.managers import AILabManager
from pygeai.lab.models import FilterSettings, Agent


manager = AILabManager()


result = manager.get_agent(
    project_id="2ca6883f-6778-40bb-bcc1-85451fb11107",
    agent_id="9716a0a1-5eab-4cc9-a611-fa2c3237c511"
)

if isinstance(result, Agent):
    print(f"Retrieved agent: {result.to_dict()}")
else:
    print("Errors:", result.errors)


filter_settings = FilterSettings(
    revision="0",
    version="0",
    allow_drafts=False
)
result = manager.get_agent(
    project_id="2ca6883f-6778-40bb-bcc1-85451fb11107",
    agent_id="9716a0a1-5eab-4cc9-a611-fa2c3237c511",
    filter_settings=filter_settings
)

if isinstance(result, Agent):
    print(f"Retrieved agent: {result.to_dict()}")
else:
    print("Errors:", result.errors)
