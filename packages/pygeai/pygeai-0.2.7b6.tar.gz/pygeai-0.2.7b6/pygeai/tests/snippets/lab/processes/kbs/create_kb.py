from pygeai.lab.managers import AILabManager
from pygeai.lab.models import KnowledgeBase

manager = AILabManager()

knowledge_base = KnowledgeBase(
    name="sample-kb",
    artifact_type_name=["sample-artifact"],
    # artifacts=["artifact-001", "artifact-002"],
    metadata=["issue_id", "priority"]
)

result = manager.create_knowledge_base(
    project_id="2ca6883f-6778-40bb-bcc1-85451fb11107",
    knowledge_base=knowledge_base
)

if isinstance(result, KnowledgeBase):
    print(f"Created knowledge base: {result.name}, ID: {result.id}")
else:
    print("Errors:", result)
