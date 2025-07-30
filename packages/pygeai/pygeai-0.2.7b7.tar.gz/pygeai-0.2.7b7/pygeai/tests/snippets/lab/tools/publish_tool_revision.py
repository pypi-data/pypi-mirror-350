from pygeai.lab.managers import AILabManager
from pygeai.lab.models import Tool

manager = AILabManager()

result = manager.publish_tool_revision(
    project_id="2ca6883f-6778-40bb-bcc1-85451fb11107",
    tool_id="affd8ede-97c6-4083-b1f6-2b463ad4891e",
    revision="1"
)

if isinstance(result, Tool):
    print(f"Published tool: {result.name}, ID: {result.id}, Revision: {result.revision}")
else:
    print("Errors:", result.errors)