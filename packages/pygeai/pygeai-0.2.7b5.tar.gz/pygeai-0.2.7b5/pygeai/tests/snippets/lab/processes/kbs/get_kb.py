from pygeai.lab.managers import AILabManager
from pygeai.lab.models import KnowledgeBase

manager = AILabManager()

kb_id = "c6af1295-3ea6-4823-8ae4-730337b278c6"
result = manager.get_knowledge_base(
    project_id="2ca6883f-6778-40bb-bcc1-85451fb11107",
    kb_id=kb_id
)

if isinstance(result, KnowledgeBase):
    print(f"Retrieved knowledge base: {result.name}, ID: {result.id}")
    print(f"Artifacts: {result.artifacts}")
    print(f"Metadata: {result.metadata}")
    print(f"Artifact Types: {result.artifact_type_name}")
else:
    print("Errors:", result)

kb_name = "sample-kb"
result = manager.get_knowledge_base(
    project_id="2ca6883f-6778-40bb-bcc1-85451fb11107",
    kb_name=kb_name
)

if isinstance(result, KnowledgeBase):
    print(f"Retrieved knowledge base: {result.name}, ID: {result.id}")
    print(f"Artifacts: {result.artifacts}")
    print(f"Metadata: {result.metadata}")
    print(f"Artifact Types: {result.artifact_type_name}")
else:
    print("Errors:", result.errors)
