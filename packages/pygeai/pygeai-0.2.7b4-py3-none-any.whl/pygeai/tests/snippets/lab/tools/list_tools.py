from pygeai.lab.managers import AILabManager
from pygeai.lab.models import FilterSettings

manager = AILabManager()

filter_settings = FilterSettings(
    id="",
    count="100",
    access_scope="public",
    allow_drafts=True,
    scope="builtin",
    allow_external=True
)


result = manager.list_tools(
    project_id="2ca6883f-6778-40bb-bcc1-85451fb11107",
    filter_settings=filter_settings
)


if isinstance(result, list):
    print(f"Found {len(result)} tools:")
    for tool in result:
        print(f"Tool: {tool.name}, ID: {tool.id}, Scope: {tool.scope}")
else:
    print("Errors:", result.errors)