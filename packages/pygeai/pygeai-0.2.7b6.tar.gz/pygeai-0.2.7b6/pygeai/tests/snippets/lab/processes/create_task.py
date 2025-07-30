from pygeai.lab.managers import AILabManager
from pygeai.lab.models import Task

manager = AILabManager()
task = Task(name="basic-task-4", description="Basic task for process", title_template="Basic Task")
result = manager.create_task(project_id="2ca6883f-6778-40bb-bcc1-85451fb11107", task=task, automatic_publish=True)
if isinstance(result, Task):
    print(f"Created task: {result.name}, ID: {result.id}")
else:
    print("Errors:", result.errors)