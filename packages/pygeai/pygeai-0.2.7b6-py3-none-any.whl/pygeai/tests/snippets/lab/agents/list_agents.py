from pygeai.lab.managers import AILabManager
from pygeai.lab.models import FilterSettings, AgentList

ai_lab_manager = AILabManager()

project_id = "2ca6883f-6778-40bb-bcc1-85451fb11107"
filter_settings = FilterSettings(
    allow_external=False,
    allow_drafts=True
)

result = ai_lab_manager.get_agent_list(
    project_id=project_id,
    filter_settings=filter_settings
)

if isinstance(result, AgentList):
    for agent in result.agents:
        print(f"Agent: {agent.name}, ID: {agent.id}")
else:
    print("Errors occurred:", result.errors)
