from pygeai.core.base.responses import EmptyResponse
from pygeai.lab.managers import AILabManager

manager = AILabManager(api_key="your-api-key")


result = manager.delete_tool(
    project_id="2ca6883f-6778-40bb-bcc1-85451fb11107",
    tool_id="affd8ede-97c6-4083-b1f6-2b463ad4891e"
)

if isinstance(result, EmptyResponse):
    print("Tool deleted successfully")
else:
    print("Errors:", result.errors)

result = manager.delete_tool(
    project_id="2ca6883f-6778-40bb-bcc1-85451fb11107",
    tool_name="sample tool V5"
)

if isinstance(result, EmptyResponse):
    print("Tool deleted successfully")
else:
    print("Errors:", result.errors)