from pygeai.lab.managers import AILabManager
from pygeai.lab.models import SharingLink

manager = AILabManager()


result = manager.create_sharing_link(
    project_id="2ca6883f-6778-40bb-bcc1-85451fb11107",
    agent_id="9716a0a1-5eab-4cc9-a611-fa2c3237c511"
)


if isinstance(result, SharingLink):
    print(f"Sharing link created for agent ID: {result.agent_id}")
    print(f"API Token: {result.api_token}")
    print(f"Shared Link: {result.shared_link}")
else:
    print("Errors:", result.errors)