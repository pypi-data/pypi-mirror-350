from pygeai.core.base.responses import EmptyResponse
from pygeai.lab.managers import AILabManager

manager = AILabManager()

agent_id = "3c06e604-26a9-485c-b84e-8eba3ff9a218"

result = manager.delete_agent(
    project_id="2ca6883f-6778-40bb-bcc1-85451fb11107",
    agent_id=agent_id
)

if isinstance(result, EmptyResponse):
    print(f"Agent deleted successfully")
else:
    print("Errors:", result.errors)
