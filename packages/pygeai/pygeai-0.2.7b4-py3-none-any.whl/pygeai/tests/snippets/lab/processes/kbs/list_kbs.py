from pygeai.lab.managers import AILabManager
from pygeai.lab.models import KnowledgeBaseList

manager = AILabManager()

result = manager.list_knowledge_bases(
    project_id="2ca6883f-6778-40bb-bcc1-85451fb11107",
    start=0,
    count=10
)

if isinstance(result, KnowledgeBaseList):
    print(f"Retrieved {len(result.knowledge_bases)} knowledge bases:")
    for kb in result.knowledge_bases:
        print(f"- Name: {kb.name}, ID: {kb.id}")
        print(f"  Artifacts: {kb.artifacts}")
        print(f"  Metadata: {kb.metadata}")
        print(f"  Artifact Types: {kb.artifact_type_name}")
else:
    print("Errors:", result.errors)

result = manager.list_knowledge_bases(
    project_id="2ca6883f-6778-40bb-bcc1-85451fb11107",
    name="sample-kb",
    start=0,
    count=5
)

if isinstance(result, KnowledgeBaseList):
    print(f"Retrieved {len(result.knowledge_bases)} knowledge bases with name 'sample-kb':")
    for kb in result.knowledge_bases:
        print(f"- Name: {kb.name}, ID: {kb.id}")
        print(f"  Artifacts: {kb.artifacts}")
        print(f"  Metadata: {kb.metadata}")
        print(f"  Artifact Types: {kb.artifact_type_name}")
else:
    print("Errors:", result.errors)