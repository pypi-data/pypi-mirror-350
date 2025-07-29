from pygeai.lab.managers import AILabManager
from pygeai.lab.models import ReasoningStrategy

manager = AILabManager()

result = manager.get_reasoning_strategy(
    project_id="2ca6883f-6778-40bb-bcc1-85451fb11107",
    reasoning_strategy_id="2b757122-3e36-499d-909e-87074c3afc94"
)
if isinstance(result, ReasoningStrategy):
    print(f"Retrieved: {result.name}, ID: {result.id}")
else:
    print("Errors:", result.errors)