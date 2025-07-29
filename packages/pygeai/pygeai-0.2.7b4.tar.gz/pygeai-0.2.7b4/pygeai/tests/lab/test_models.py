import unittest
from unittest import TestCase
from pygeai.lab.models import (
    FilterSettings, Sampling, LlmConfig, Model, PromptExample, PromptOutput, Prompt, ModelList,
    AgentData, Agent, AgentList, SharingLink, ToolParameter, ToolMessage, Tool, ToolList,
    LocalizedDescription, ReasoningStrategy, ReasoningStrategyList, KnowledgeBase, AgenticActivity,
    ArtifactSignal, UserSignal, Event, SequenceFlow, AgenticProcess, Task, AgenticProcessList,
    TaskList, Variable, VariableList, ProcessInstance, ProcessInstanceList, ArtifactType, ArtifactTypeList
)


class TestLabModels(TestCase):
    """
    python -m unittest pygeai.tests.lab.test_models.TestLabModels
    """

    def test_filter_settings_model_validate(self):
        filter_data = {
            "id": "agent123",
            "name": "test-agent",
            "accessScope": "private",
            "allowDrafts": False,
            "allowExternal": False
        }
        filter_settings = FilterSettings.model_validate(filter_data)
        self.assertEqual(filter_settings.id, filter_data["id"])
        self.assertEqual(filter_settings.name, filter_data["name"])
        self.assertEqual(filter_settings.access_scope, filter_data["accessScope"])
        self.assertEqual(filter_settings.allow_drafts, filter_data["allowDrafts"])
        self.assertIsNone(filter_settings.status)
        self.assertTrue(filter_settings.to_dict() == filter_data)

    def test_sampling_model_validate(self):
        sampling_data = {
            "temperature": 0.7,
            "topK": 40,
            "topP": 0.9
        }
        sampling = Sampling.model_validate(sampling_data)
        self.assertEqual(sampling.temperature, sampling_data["temperature"])
        self.assertEqual(sampling.top_k, sampling_data["topK"])
        self.assertEqual(sampling.top_p, sampling_data["topP"])
        self.assertTrue(sampling.to_dict() == sampling_data)

    def test_llm_config_model_validate(self):
        llm_config_data = {
            "maxTokens": 1000,
            "timeout": 30,
            "sampling": {"temperature": 0.7, "topK": 40, "topP": 0.9}
        }
        llm_config = LlmConfig.model_validate(llm_config_data)
        self.assertEqual(llm_config.max_tokens, llm_config_data["maxTokens"])
        self.assertEqual(llm_config.timeout, llm_config_data["timeout"])
        self.assertEqual(llm_config.sampling.temperature, llm_config_data["sampling"]["temperature"])
        self.assertEqual(llm_config.sampling.top_k, llm_config_data["sampling"]["topK"])
        self.assertEqual(llm_config.sampling.top_p, llm_config_data["sampling"]["topP"])
        self.assertTrue(llm_config.to_dict() == llm_config_data)

    def test_model_model_validate(self):
        model_data = {
            "name": "gpt-4",
            "llmConfig": {"maxTokens": 500, "timeout": 20, "sampling": {"temperature": 0.5, "topK": 30, "topP": 0.8}}
        }
        model = Model.model_validate(model_data)
        self.assertEqual(model.name, model_data["name"])
        self.assertEqual(model.llm_config.max_tokens, model_data["llmConfig"]["maxTokens"])
        self.assertEqual(model.llm_config.timeout, model_data["llmConfig"]["timeout"])
        self.assertEqual(model.llm_config.sampling.temperature, model_data["llmConfig"]["sampling"]["temperature"])
        self.assertIsNone(model.prompt)
        self.assertTrue(model.to_dict() == model_data)

    def test_prompt_example_model_validate(self):
        example_data = {
            "inputData": "Hello world",
            "output": '{"result": "Hi"}'
        }
        prompt_example = PromptExample.model_validate(example_data)
        self.assertEqual(prompt_example.input_data, example_data["inputData"])
        self.assertEqual(prompt_example.output, example_data["output"])
        self.assertTrue(prompt_example.to_dict() == example_data)

    def test_prompt_output_model_validate(self):
        output_data = {
            "key": "summary",
            "description": "Summary of text"
        }
        prompt_output = PromptOutput.model_validate(output_data)
        self.assertEqual(prompt_output.key, output_data["key"])
        self.assertEqual(prompt_output.description, output_data["description"])
        self.assertTrue(prompt_output.to_dict() == output_data)

    def test_prompt_model_validate(self):
        prompt_data = {
            "instructions": "Summarize text",
            "inputs": ["text"],
            "outputs": [{"key": "summary", "description": "Summary of text"}],
            "examples": [{"inputData": "Hello world", "output": '{"summary": "Hi"}'}]
        }
        prompt = Prompt.model_validate(prompt_data)
        self.assertEqual(prompt.instructions, prompt_data["instructions"])
        self.assertEqual(prompt.inputs, prompt_data["inputs"])
        self.assertEqual(prompt.outputs[0].key, prompt_data["outputs"][0]["key"])
        self.assertEqual(prompt.examples[0].input_data, prompt_data["examples"][0]["inputData"])
        self.assertTrue(prompt.to_dict() == prompt_data)

    def test_model_list_model_validate(self):
        model_list_data = [
            {"name": "gpt-4"},
            {"name": "gpt-3.5-turbo"}
        ]
        model_list = ModelList.model_validate({"models": model_list_data})
        self.assertEqual(len(model_list.models), 2)
        self.assertEqual(model_list.models[0].name, model_list_data[0]["name"])
        self.assertEqual(model_list.models[1].name, model_list_data[1]["name"])
        self.assertTrue(model_list.to_dict() == model_list_data)

    def test_agent_data_model_validate(self):
        agent_data_data = {
            "prompt": {"instructions": "Summarize", "inputs": ["text"], "outputs": [{"key": "summary", "description": "Summary"}]},
            "llmConfig": {"maxTokens": 1000, "timeout": 30, "sampling": {"temperature": 0.7, "topK": 40, "topP": 0.9}},
            "models": [{"name": "gpt-4"}]
        }
        agent_data = AgentData.model_validate(agent_data_data)
        self.assertEqual(agent_data.prompt.instructions, agent_data_data["prompt"]["instructions"])
        self.assertEqual(agent_data.llm_config.max_tokens, agent_data_data["llmConfig"]["maxTokens"])
        self.assertEqual(agent_data.models.models[0].name, agent_data_data["models"][0]["name"])
        self.assertTrue(agent_data.to_dict() == agent_data_data)

    def test_agent_model_validate(self):
        agent_data = {
            "id": "agent123",
            "status": "active",
            "name": "TestAgent",
            "isDraft": False,
            "isReadonly": False,
            "accessScope": "public",
            "publicName": "test-agent",
            "agentData": {
                "prompt": {"instructions": "Summarize", "inputs": ["text"], "outputs": [{"key": "summary", "description": "Summary"}]},
                "llmConfig": {"maxTokens": 1000, "timeout": 30, "sampling": {"temperature": 0.7, "topK": 40, "topP": 0.9}},
                "models": [{"name": "gpt-4"}]
            }
        }
        agent = Agent.model_validate(agent_data)
        self.assertEqual(agent.id, agent_data["id"])
        self.assertEqual(agent.name, agent_data["name"])
        self.assertEqual(agent.access_scope, agent_data["accessScope"])
        self.assertEqual(agent.public_name, agent_data["publicName"])
        self.assertEqual(agent.agent_data.prompt.instructions, agent_data["agentData"]["prompt"]["instructions"])
        self.assertTrue(agent.to_dict() == agent_data)

    def test_agent_list_model_validate(self):
        agent_list_data = {
            "agents": [
                {"id": "agent1", "name": "Agent1", "isReadonly": False, "isDraft": True, "accessScope": "private", "status": "active"},
                {"id": "agent2", "name": "Agent2", "isReadonly": False, "isDraft": True, "accessScope": "private", "status": "active"}
            ]
        }
        agent_list = AgentList.model_validate(agent_list_data)
        self.assertEqual(len(agent_list.agents), 2)
        self.assertEqual(agent_list.agents[0].id, agent_list_data["agents"][0]["id"])
        self.assertEqual(agent_list.agents[1].name, agent_list_data["agents"][1]["name"])
        self.assertTrue(agent_list.to_dict() == agent_list_data["agents"])

    def test_sharing_link_model_validate(self):
        sharing_link_data = {
            "agentId": "agent123",
            "apiToken": "token456",
            "sharedLink": "https://example.com/share/agent123"
        }
        sharing_link = SharingLink.model_validate(sharing_link_data)
        self.assertEqual(sharing_link.agent_id, sharing_link_data["agentId"])
        self.assertEqual(sharing_link.api_token, sharing_link_data["apiToken"])
        self.assertEqual(sharing_link.shared_link, sharing_link_data["sharedLink"])
        self.assertTrue(sharing_link.to_dict() == sharing_link_data)

    def test_tool_parameter_model_validate(self):
        param_data = {
            "key": "input",
            "dataType": "String",
            "description": "Input text",
            "isRequired": True,
            "type": "app"
        }
        tool_param = ToolParameter.model_validate(param_data)
        self.assertEqual(tool_param.key, param_data["key"])
        self.assertEqual(tool_param.data_type, param_data["dataType"])
        self.assertEqual(tool_param.description, param_data["description"])
        self.assertEqual(tool_param.is_required, param_data["isRequired"])
        self.assertTrue(tool_param.to_dict() == param_data)

    def test_tool_message_model_validate(self):
        message_data = {
            "description": "Warning: deprecated",
            "type": "warning"
        }
        tool_message = ToolMessage.model_validate(message_data)
        self.assertEqual(tool_message.description, message_data["description"])
        self.assertEqual(tool_message.type, message_data["type"])
        self.assertTrue(tool_message.to_dict() == message_data)

    def test_tool_model_validate(self):
        tool_data = {
            "name": "TextTool",
            "description": "Processes text",
            "scope": "builtin",
            "parameters": [{"key": "input", "dataType": "String", "description": "Input text", "isRequired": True, "type": "app"}],
            "reportEvents": "None"

        }
        tool = Tool.model_validate(tool_data)
        self.assertEqual(tool.name, tool_data["name"])
        self.assertEqual(tool.description, tool_data["description"])
        self.assertEqual(tool.scope, tool_data["scope"])
        self.assertEqual(tool.parameters[0].key, tool_data["parameters"][0]["key"])
        self.assertTrue(tool.to_dict() == tool_data)

    def test_tool_list_model_validate(self):
        tool_list_data = {
            "tools": [
                {"name": "Tool1", "description": "Tool 1", "scope": "builtin", 'reportEvents': 'None'},
                {"name": "Tool2", "description": "Tool 2", "scope": "builtin", 'reportEvents': 'None'}
            ]
        }
        tool_list = ToolList.model_validate(tool_list_data)
        self.assertEqual(len(tool_list.tools), 2)
        self.assertEqual(tool_list.tools[0].name, tool_list_data["tools"][0]["name"])
        self.assertEqual(tool_list.tools[1].description, tool_list_data["tools"][1]["description"])
        self.assertTrue(tool_list.to_dict() == tool_list_data)

    def test_localized_description_model_validate(self):
        localized_data = {
            "language": "english",
            "description": "Test strategy"
        }
        localized_desc = LocalizedDescription.model_validate(localized_data)
        self.assertEqual(localized_desc.language, localized_data["language"])
        self.assertEqual(localized_desc.description, localized_data["description"])
        self.assertTrue(localized_desc.to_dict() == localized_data)

    def test_reasoning_strategy_model_validate(self):
        strategy_data = {
            "name": "TestStrategy",
            "accessScope": "public",
            "type": "addendum",
            "localizedDescriptions": [{"language": "english", "description": "Test strategy"}]
        }
        strategy = ReasoningStrategy.model_validate(strategy_data)
        self.assertEqual(strategy.name, strategy_data["name"])
        self.assertEqual(strategy.access_scope, strategy_data["accessScope"])
        self.assertEqual(strategy.type, strategy_data["type"])
        self.assertEqual(strategy.localized_descriptions[0].language, strategy_data["localizedDescriptions"][0]["language"])
        self.assertTrue(strategy.to_dict() == strategy_data)

    @unittest.skip("Skip for now. Fix later")
    def test_reasoning_strategy_list_model_validate(self):
        strategy_list_data = [
            {"name": "Strategy1", "accessScope": "public", "type": "addendum"},
            {"name": "Strategy2", "accessScope": "private", "type": "base"}
        ]
        strategy_list = ReasoningStrategyList.model_validate(strategy_list_data)
        self.assertEqual(len(strategy_list.strategies), 2)
        self.assertEqual(strategy_list.strategies[0].name, strategy_list_data[0]["name"])
        self.assertEqual(strategy_list.strategies[1].access_scope, strategy_list_data[1]["accessScope"])
        self.assertTrue(strategy_list.to_dict() == strategy_list_data)

    def test_knowledge_base_model_validate(self):
        kb_data = {
            "name": "TestKB",
            "artifactTypeName": ["doc"]
        }
        kb = KnowledgeBase.model_validate(kb_data)
        self.assertEqual(kb.name, kb_data["name"])
        self.assertEqual(kb.artifact_type_name, kb_data["artifactTypeName"])
        self.assertTrue(kb.to_dict() == kb_data)

    def test_agentic_activity_model_validate(self):
        activity_data = {
            "key": "act1",
            "name": "TestActivity",
            "taskName": "TestTask",
            "agentName": "TestAgent",
            "agentRevisionId": 1
        }
        activity = AgenticActivity.model_validate(activity_data)
        self.assertEqual(activity.key, activity_data["key"])
        self.assertEqual(activity.name, activity_data["name"])
        self.assertEqual(activity.task_name, activity_data["taskName"])
        self.assertEqual(activity.agent_name, activity_data["agentName"])
        self.assertEqual(activity.agent_revision_id, activity_data["agentRevisionId"])
        self.assertTrue(activity.to_dict() == activity_data)

    def test_artifact_signal_model_validate(self):
        signal_data = {
            "key": "sig1",
            "name": "TestSignal",
            "handlingType": "C",
            "artifactTypeName": ["text"]
        }
        signal = ArtifactSignal.model_validate(signal_data)
        self.assertEqual(signal.key, signal_data["key"])
        self.assertEqual(signal.name, signal_data["name"])
        self.assertEqual(signal.handling_type, signal_data["handlingType"])
        self.assertEqual(signal.artifact_type_name, signal_data["artifactTypeName"])
        self.assertTrue(signal.to_dict() == signal_data)

    def test_user_signal_model_validate(self):
        user_signal_data = {
            "key": "user1",
            "name": "UserDone"
        }
        user_signal = UserSignal.model_validate(user_signal_data)
        self.assertEqual(user_signal.key, user_signal_data["key"])
        self.assertEqual(user_signal.name, user_signal_data["name"])
        self.assertTrue(user_signal.to_dict() == user_signal_data)

    def test_event_model_validate(self):
        event_data = {
            "key": "evt1",
            "name": "StartEvent"
        }
        event = Event.model_validate(event_data)
        self.assertEqual(event.key, event_data["key"])
        self.assertEqual(event.name, event_data["name"])
        self.assertTrue(event.to_dict() == event_data)

    def test_sequence_flow_model_validate(self):
        flow_data = {
            "key": "flow1",
            "sourceKey": "start",
            "targetKey": "end"
        }
        sequence_flow = SequenceFlow.model_validate(flow_data)
        self.assertEqual(sequence_flow.key, flow_data["key"])
        self.assertEqual(sequence_flow.source_key, flow_data["sourceKey"])
        self.assertEqual(sequence_flow.target_key, flow_data["targetKey"])
        self.assertTrue(sequence_flow.to_dict() == flow_data)

    def test_agentic_process_model_validate(self):
        process_data = {
            "name": "TestProcess",
            "kb": {"name": "TestKB", "artifactTypeName": ["doc"]},
            "agenticActivities": [{"key": "act1", "name": "Act1", "taskName": "Task1", "agentName": "Agent1", "agentRevisionId": 1}]
        }
        process = AgenticProcess.model_validate(process_data)
        self.assertEqual(process.name, process_data["name"])
        self.assertEqual(process.kb.name, process_data["kb"]["name"])
        self.assertEqual(process.agentic_activities[0].key, process_data["agenticActivities"][0]["key"])
        self.assertTrue(process.to_dict() == process_data)

    def test_task_model_validate(self):
        task_data = {
            "name": "TestTask"
        }
        task = Task.model_validate(task_data)
        self.assertEqual(task.name, task_data["name"])
        self.assertIsNone(task.description)
        self.assertTrue(task.to_dict() == task_data)

    def test_agentic_process_list_model_validate(self):
        process_list_data = [
            {"name": "Process1"},
            {"name": "Process2"}
        ]
        process_list = AgenticProcessList.model_validate({"processes": process_list_data})
        self.assertEqual(len(process_list.processes), 2)
        self.assertEqual(process_list.processes[0].name, process_list_data[0]["name"])
        self.assertEqual(process_list.processes[1].name, process_list_data[1]["name"])
        self.assertTrue(process_list.to_dict() == {"processes": process_list_data})

    def test_task_list_model_validate(self):
        task_list_data = [
            {"name": "Task1"},
            {"name": "Task2"}
        ]
        task_list = TaskList.model_validate({"tasks": task_list_data})
        self.assertEqual(len(task_list.tasks), 2)
        self.assertEqual(task_list.tasks[0].name, task_list_data[0]["name"])
        self.assertEqual(task_list.tasks[1].name, task_list_data[1]["name"])
        self.assertTrue(task_list.to_dict() == task_list_data)

    def test_variable_model_validate(self):
        variable_data = {
            "key": "var1",
            "value": "value1"
        }
        variable = Variable.model_validate(variable_data)
        self.assertEqual(variable.key, variable_data["key"])
        self.assertEqual(variable.value, variable_data["value"])
        self.assertTrue(variable.to_dict() == variable_data)

    def test_variable_list_model_validate(self):
        variable_list_data = [
            {"key": "var1", "value": "value1"},
            {"key": "var2", "value": "value2"}
        ]
        variable_list = VariableList.model_validate({"variables": variable_list_data})
        self.assertEqual(len(variable_list.variables), 2)
        self.assertEqual(variable_list.variables[0].key, variable_list_data[0]["key"])
        self.assertEqual(variable_list.variables[1].value, variable_list_data[1]["value"])
        self.assertTrue(variable_list.to_dict() == variable_list_data)

    def test_process_instance_model_validate(self):
        instance_data = {
            "id": "inst123",
            "process": {"name": "TestProcess"},
            "createdAt": "2023-01-01T12:00:00",
            "subject": "TestSubject",
            "variables": [{"key": "var1", "value": "val1"}]
        }
        instance = ProcessInstance.model_validate(instance_data)
        self.assertEqual(instance.id, instance_data["id"])
        self.assertEqual(instance.process.name, instance_data["process"]["name"])
        self.assertEqual(instance.created_at, instance_data["createdAt"])
        self.assertEqual(instance.variables.variables[0].key, instance_data["variables"][0]["key"])
        self.assertTrue(instance.to_dict() == instance_data)

    def test_process_instance_list_model_validate(self):
        instance_list_data = [
            {"id": "inst1", "process": {"name": "Process1"}, "subject": "ProcessSubject"},
            {"id": "inst2", "process": {"name": "Process2"}, "subject": "ProcessSubject"}
        ]
        instance_list = ProcessInstanceList.model_validate({"instances": instance_list_data})
        self.assertEqual(len(instance_list.instances), 2)
        self.assertEqual(instance_list.instances[0].id, instance_list_data[0]["id"])
        self.assertEqual(instance_list.instances[1].process.name, instance_list_data[1]["process"]["name"])
        self.assertTrue(instance_list.to_dict() == instance_list_data)

    def test_filter_settings_instantiation(self):
        
        filter_attr = FilterSettings(id="agent123", name="test-agent", access_scope="private", allow_drafts=False)
        
        filter_dict = FilterSettings(**{
            "id": "agent123",
            "name": "test-agent",
            "accessScope": "private",
            "allowDrafts": False
        })
        self.assertEqual(filter_attr.id, filter_dict.id)
        self.assertEqual(filter_attr.name, filter_dict.name)
        self.assertEqual(filter_attr.access_scope, filter_dict.access_scope)
        self.assertEqual(filter_attr.allow_drafts, filter_dict.allow_drafts)
        self.assertEqual(filter_attr.to_dict(), filter_dict.to_dict())

    def test_sampling_instantiation(self):
        
        sampling_attr = Sampling(temperature=0.7, top_k=40, top_p=0.9)
        
        sampling_dict = Sampling(**{
            "temperature": 0.7,
            "topK": 40,
            "topP": 0.9
        })
        self.assertEqual(sampling_attr.temperature, sampling_dict.temperature)
        self.assertEqual(sampling_attr.top_k, sampling_dict.top_k)
        self.assertEqual(sampling_attr.top_p, sampling_dict.top_p)
        self.assertEqual(sampling_attr.to_dict(), sampling_dict.to_dict())

    def test_llm_config_instantiation(self):
        
        sampling = Sampling(temperature=0.7, top_k=40, top_p=0.9)
        llm_attr = LlmConfig(max_tokens=1000, timeout=30, sampling=sampling)
        
        llm_dict = LlmConfig(**{
            "maxTokens": 1000,
            "timeout": 30,
            "sampling": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.9
            }
        })
        self.assertEqual(llm_attr.max_tokens, llm_dict.max_tokens)
        self.assertEqual(llm_attr.timeout, llm_dict.timeout)
        self.assertEqual(llm_attr.sampling.temperature, llm_dict.sampling.temperature)
        self.assertEqual(llm_attr.to_dict(), llm_dict.to_dict())

    def test_model_instantiation(self):
        
        sampling = Sampling(temperature=0.5, top_k=30, top_p=0.8)
        llm_config = LlmConfig(max_tokens=500, timeout=20, sampling=sampling)
        model_attr = Model(name="gpt-4", llm_config=llm_config)
        
        model_dict = Model(**{
            "name": "gpt-4",
            "llmConfig": {
                "maxTokens": 500,
                "timeout": 20,
                "sampling": {
                    "temperature": 0.5,
                    "topK": 30,
                    "topP": 0.8
                }
            }
        })
        self.assertEqual(model_attr.name, model_dict.name)
        self.assertEqual(model_attr.llm_config.max_tokens, model_dict.llm_config.max_tokens)
        self.assertEqual(model_attr.to_dict(), model_dict.to_dict())

    def test_prompt_instantiation(self):
        
        output = PromptOutput(key="summary", description="Summary of text")
        example = PromptExample(input_data="Hello world", output='{"summary": "Hi"}')
        prompt_attr = Prompt(instructions="Summarize text", inputs=["text"], outputs=[output], examples=[example])
        
        prompt_dict = Prompt(**{
            "instructions": "Summarize text",
            "inputs": ["text"],
            "outputs": [{"key": "summary", "description": "Summary of text"}],
            "examples": [{"inputData": "Hello world", "output": '{"summary": "Hi"}'}]
        })
        self.assertEqual(prompt_attr.instructions, prompt_dict.instructions)
        self.assertEqual(prompt_attr.inputs, prompt_dict.inputs)
        self.assertEqual(prompt_attr.outputs[0].key, prompt_dict.outputs[0].key)
        self.assertEqual(prompt_attr.examples[0].input_data, prompt_dict.examples[0].input_data)
        self.assertEqual(prompt_attr.to_dict(), prompt_dict.to_dict())

    def test_model_list_instantiation(self):
        
        model = Model(name="gpt-4")
        model_list_attr = ModelList(models=[model])
        
        model_list_dict = ModelList(**{
            "models": [{"name": "gpt-4"}]
        })
        self.assertEqual(len(model_list_attr.models), len(model_list_dict.models))
        self.assertEqual(model_list_attr.models[0].name, model_list_dict.models[0].name)
        self.assertEqual(model_list_attr.to_dict(), model_list_dict.to_dict())

    def test_agent_data_instantiation(self):
        
        output = PromptOutput(key="summary", description="Summary")
        prompt = Prompt(instructions="Summarize", inputs=["text"], outputs=[output])
        sampling = Sampling(temperature=0.7, top_k=40, top_p=0.9)
        llm_config = LlmConfig(max_tokens=1000, timeout=30, sampling=sampling)
        model_list = ModelList(models=[Model(name="gpt-4")])
        agent_data_attr = AgentData(prompt=prompt, llm_config=llm_config, models=model_list)
        
        agent_data_dict = AgentData(**{
            "prompt": {
                "instructions": "Summarize",
                "inputs": ["text"],
                "outputs": [{"key": "summary", "description": "Summary"}]
            },
            "llmConfig": {
                "maxTokens": 1000,
                "timeout": 30,
                "sampling": {"temperature": 0.7, "topK": 40, "topP": 0.9}
            },
            "models": [{"name": "gpt-4"}]
        })
        self.assertEqual(agent_data_attr.prompt.instructions, agent_data_dict.prompt.instructions)
        self.assertEqual(agent_data_attr.llm_config.max_tokens, agent_data_dict.llm_config.max_tokens)
        self.assertEqual(agent_data_attr.models.models[0].name, agent_data_dict.models.models[0].name)
        self.assertEqual(agent_data_attr.to_dict(), agent_data_dict.to_dict())

    def test_agent_instantiation(self):
        
        output = PromptOutput(key="summary", description="Summary")
        prompt = Prompt(instructions="Summarize", inputs=["text"], outputs=[output])
        sampling = Sampling(temperature=0.7, top_k=40, top_p=0.9)
        llm_config = LlmConfig(max_tokens=1000, timeout=30, sampling=sampling)
        model_list = ModelList(models=[Model(name="gpt-4")])
        agent_data = AgentData(prompt=prompt, llm_config=llm_config, models=model_list)
        agent_attr = Agent(id="agent123", name="TestAgent", access_scope="public", public_name="test-agent", agent_data=agent_data)
        
        agent_dict = Agent(**{
            "id": "agent123",
            "name": "TestAgent",
            "accessScope": "public",
            "publicName": "test-agent",
            "agentData": {
                "prompt": {
                    "instructions": "Summarize",
                    "inputs": ["text"],
                    "outputs": [{"key": "summary", "description": "Summary"}]
                },
                "llmConfig": {
                    "maxTokens": 1000,
                    "timeout": 30,
                    "sampling": {"temperature": 0.7, "topK": 40, "topP": 0.9}
                },
                "models": [{"name": "gpt-4"}]
            }
        })
        self.assertEqual(agent_attr.id, agent_dict.id)
        self.assertEqual(agent_attr.name, agent_dict.name)
        self.assertEqual(agent_attr.access_scope, agent_dict.access_scope)
        self.assertEqual(agent_attr.public_name, agent_dict.public_name)
        self.assertEqual(agent_attr.agent_data.prompt.instructions, agent_dict.agent_data.prompt.instructions)
        self.assertEqual(agent_attr.to_dict(), agent_dict.to_dict())

    def test_tool_instantiation(self):
        
        param = ToolParameter(key="input", data_type="String", description="Input text", is_required=True)
        tool_attr = Tool(name="TextTool", description="Processes text", scope="builtin", parameters=[param])
        
        tool_dict = Tool(**{
            "name": "TextTool",
            "description": "Processes text",
            "scope": "builtin",
            "parameters": [
                {"key": "input", "dataType": "String", "description": "Input text", "isRequired": True}
            ]
        })
        self.assertEqual(tool_attr.name, tool_dict.name)
        self.assertEqual(tool_attr.description, tool_dict.description)
        self.assertEqual(tool_attr.scope, tool_dict.scope)
        self.assertEqual(tool_attr.parameters[0].key, tool_dict.parameters[0].key)
        self.assertEqual(tool_attr.to_dict(), tool_dict.to_dict())

    def test_agentic_process_instantiation(self):
        
        activity = AgenticActivity(key="act1", name="Act1", task_name="Task1", agent_name="Agent1", agent_revision_id=1)
        start_event = Event(key="start1", name="Start")
        flow = SequenceFlow(key="flow1", source_key="start1", target_key="act1")
        process_attr = AgenticProcess(name="TestProcess", agentic_activities=[activity], start_event=start_event, sequence_flows=[flow])
        
        process_dict = AgenticProcess(**{
            "name": "TestProcess",
            "agenticActivities": [
                {"key": "act1", "name": "Act1", "taskName": "Task1", "agentName": "Agent1", "agentRevisionId": 1}
            ],
            "startEvent": {"key": "start1", "name": "Start"},
            "sequenceFlows": [
                {"key": "flow1", "sourceKey": "start1", "targetKey": "act1"}
            ]
        })
        self.assertEqual(process_attr.name, process_dict.name)
        self.assertEqual(process_attr.agentic_activities[0].key, process_dict.agentic_activities[0].key)
        self.assertEqual(process_attr.start_event.key, process_dict.start_event.key)
        self.assertEqual(process_attr.sequence_flows[0].key, process_dict.sequence_flows[0].key)
        self.assertEqual(process_attr.to_dict(), process_dict.to_dict())

    def test_task_instantiation(self):
        
        output = PromptOutput(key="summary", description="Summary")
        prompt = Prompt(instructions="Summarize", inputs=["text"], outputs=[output])
        artifact = ArtifactType(name="document", usage_type="input")
        artifact_list = ArtifactTypeList(artifact_types=[artifact])
        task_attr = Task(name="TestTask", prompt_data=prompt, artifact_types=artifact_list)
        
        task_dict = Task(**{
            "name": "TestTask",
            "promptData": {
                "instructions": "Summarize",
                "inputs": ["text"],
                "outputs": [{"key": "summary", "description": "Summary"}]
            },
            "artifactTypes": [
                {"name": "document", "usageType": "input"}
            ]
        })
        self.assertEqual(task_attr.name, task_dict.name)
        self.assertEqual(task_attr.prompt_data.instructions, task_dict.prompt_data.instructions)
        self.assertEqual(task_attr.artifact_types.artifact_types[0].name, task_dict.artifact_types.artifact_types[0].name)
        self.assertEqual(task_attr.to_dict(), task_dict.to_dict())