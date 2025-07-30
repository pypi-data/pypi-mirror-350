import unittest
from unittest.mock import Mock, patch
from io import StringIO

from pygeai.core.base.models import Error
from pygeai.migration.strategies import (
    ProjectMigrationStrategy,
    AgentMigrationStrategy,
    ToolMigrationStrategy,
    AgenticProcessMigrationStrategy,
    TaskMigrationStrategy,
)
from pygeai.core.models import Project
from pygeai.core.base.responses import ErrorListResponse
from pygeai.organization.managers import OrganizationManager
from pygeai.lab.managers import AILabManager
from pygeai.lab.models import Agent, Tool, AgenticProcess, Task


class TestMigrationStrategies(unittest.TestCase):
    """
    python -m unittest pygeai.tests.migration.test_strategies.TestMigrationStrategies
    """

    def setUp(self):
        self.from_api_key = "from_key"
        self.from_instance = "http://from.instance"
        self.to_api_key = "to_key"
        self.to_instance = "http://to.instance"
        self.from_project_id = "proj_123"
        self.to_project_id = "proj_456"
        self.to_project_name = "New Project"
        self.admin_email = "admin@example.com"
        self.agent_id = "agent_123"
        self.tool_id = "tool_123"
        self.process_id = "process_123"
        self.task_id = "task_123"

    @patch('pygeai.migration.strategies.OrganizationManager')
    def test_project_migration_strategy_init(self, mock_org_manager):
        strategy = ProjectMigrationStrategy(
            from_api_key=self.from_api_key,
            from_instance=self.from_instance,
            to_api_key=self.to_api_key,
            to_instance=self.to_instance,
            from_project_id=self.from_project_id,
            to_project_name=self.to_project_name,
            admin_email=self.admin_email
        )
        self.assertEqual(strategy.from_api_key, self.from_api_key)
        self.assertEqual(strategy.from_instance, self.from_instance)
        self.assertEqual(strategy.to_api_key, self.to_api_key)
        self.assertEqual(strategy.to_instance, self.to_instance)
        self.assertEqual(strategy.from_project_id, self.from_project_id)
        self.assertEqual(strategy.to_project_name, self.to_project_name)
        self.assertEqual(strategy.admin_email, self.admin_email)
        mock_org_manager.assert_any_call(api_key=self.from_api_key, base_url=self.from_instance)
        mock_org_manager.assert_any_call(api_key=self.to_api_key, base_url=self.to_instance)

    @patch('pygeai.migration.strategies.OrganizationManager')
    @patch('sys.stdout', new_callable=StringIO)
    def test_project_migration_success(self, mock_stdout, mock_org_manager):
        mock_source = Mock()
        mock_destination = Mock()
        mock_org_manager.side_effect = [mock_source, mock_destination]

        mock_project = Mock(spec=Project, name="Old Project", email="old@example.com")
        mock_new_project = Mock(spec=Project, name=self.to_project_name, email=self.admin_email)
        mock_response = Mock(project=mock_new_project)

        mock_source.get_project_data.return_value = Mock(project=mock_project)
        mock_destination.create_project.return_value = mock_response

        strategy = ProjectMigrationStrategy(
            from_api_key=self.from_api_key,
            from_instance=self.from_instance,
            to_api_key=self.to_api_key,
            to_instance=self.to_instance,
            from_project_id=self.from_project_id,
            to_project_name=self.to_project_name,
            admin_email=self.admin_email
        )
        strategy.migrate()

        mock_source.get_project_data.assert_called_with(project_id=self.from_project_id)
        mock_destination.create_project.assert_called_with(mock_project)
        self.assertIn(f"Migrated project: \n{mock_response}", mock_stdout.getvalue())

    @patch('pygeai.migration.strategies.OrganizationManager')
    @patch('sys.stdout', new_callable=StringIO)
    def test_project_migration_error(self, mock_stdout, mock_org_manager):
        mock_source = Mock()
        mock_destination = Mock()
        mock_org_manager.side_effect = [mock_source, mock_destination]

        mock_error_response = ErrorListResponse(errors=[Error(id="1", description="Migration failed")])
        mock_source.get_project_data.return_value = mock_error_response

        strategy = ProjectMigrationStrategy(
            from_api_key=self.from_api_key,
            from_instance=self.from_instance,
            to_api_key=self.to_api_key,
            to_instance=self.to_instance,
            from_project_id=self.from_project_id,
            to_project_name=self.to_project_name,
            admin_email=self.admin_email
        )
        result = strategy.migrate()

        self.assertEqual(mock_stdout.getvalue(), "")

    @patch('pygeai.migration.strategies.AILabManager')
    def test_agent_migration_strategy_init(self, mock_lab_manager):
        strategy = AgentMigrationStrategy(
            from_api_key=self.from_api_key,
            from_instance=self.from_instance,
            to_api_key=self.to_api_key,
            to_instance=self.to_instance,
            from_project_id=self.from_project_id,
            to_project_id=self.to_project_id,
            agent_id=self.agent_id
        )
        self.assertEqual(strategy.from_api_key, self.from_api_key)
        self.assertEqual(strategy.from_instance, self.from_instance)
        self.assertEqual(strategy.to_api_key, self.to_api_key)
        self.assertEqual(strategy.to_instance, self.to_instance)
        self.assertEqual(strategy.from_project_id, self.from_project_id)
        self.assertEqual(strategy.to_project_id, self.to_project_id)
        self.assertEqual(strategy.agent_id, self.agent_id)
        mock_lab_manager.assert_any_call(api_key=self.from_api_key, base_url=self.from_instance)
        mock_lab_manager.assert_any_call(api_key=self.to_api_key, base_url=self.to_instance)

    @patch('pygeai.migration.strategies.AILabManager')
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    def test_agent_migration_success(self, mock_stderr, mock_stdout, mock_lab_manager):
        mock_source = Mock()
        mock_destination = Mock()
        mock_lab_manager.side_effect = [mock_source, mock_destination]

        mock_agent = Mock(spec=Agent)
        mock_source.get_agent.return_value = mock_agent
        mock_destination.create_agent.return_value = mock_agent

        strategy = AgentMigrationStrategy(
            from_api_key=self.from_api_key,
            from_instance=self.from_instance,
            to_api_key=self.to_api_key,
            to_instance=self.to_instance,
            from_project_id=self.from_project_id,
            to_project_id=self.to_project_id,
            agent_id=self.agent_id
        )
        strategy.migrate()

        mock_source.get_agent.assert_called_with(project_id=self.from_project_id, agent_id=self.agent_id)
        mock_destination.create_agent.assert_called_with(project_id=self.to_project_id, agent=mock_agent)
        self.assertIn(f"New agent detail: \n{mock_agent}", mock_stdout.getvalue())
        self.assertEqual(mock_stderr.getvalue(), "")

    @patch('pygeai.migration.strategies.AILabManager')
    @patch('sys.stderr', new_callable=StringIO)
    def test_agent_migration_error(self, mock_stderr, mock_lab_manager):
        mock_source = Mock()
        mock_destination = Mock()
        mock_lab_manager.side_effect = [mock_source, mock_destination]

        mock_source.get_agent.side_effect = ValueError("Unable to retrieve requested agent.")

        strategy = AgentMigrationStrategy(
            from_api_key=self.from_api_key,
            from_instance=self.from_instance,
            to_api_key=self.to_api_key,
            to_instance=self.to_instance,
            from_project_id=self.from_project_id,
            to_project_id=self.to_project_id,
            agent_id=self.agent_id
        )
        strategy.migrate()

        self.assertIn("Agent migration failed: Unable to retrieve requested agent.", mock_stderr.getvalue())

    @patch('pygeai.migration.strategies.AILabManager')
    def test_tool_migration_strategy_init(self, mock_lab_manager):
        strategy = ToolMigrationStrategy(
            from_api_key=self.from_api_key,
            from_instance=self.from_instance,
            to_api_key=self.to_api_key,
            to_instance=self.to_instance,
            from_project_id=self.from_project_id,
            to_project_id=self.to_project_id,
            tool_id=self.tool_id
        )
        self.assertEqual(strategy.from_api_key, self.from_api_key)
        self.assertEqual(strategy.from_instance, self.from_instance)
        self.assertEqual(strategy.to_api_key, self.to_api_key)
        self.assertEqual(strategy.to_instance, self.to_instance)
        self.assertEqual(strategy.from_project_id, self.from_project_id)
        self.assertEqual(strategy.to_project_id, self.to_project_id)
        self.assertEqual(strategy.tool_id, self.tool_id)
        mock_lab_manager.assert_any_call(api_key=self.from_api_key, base_url=self.from_instance)
        mock_lab_manager.assert_any_call(api_key=self.to_api_key, base_url=self.to_instance)

    @patch('pygeai.migration.strategies.AILabManager')
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    def test_tool_migration_success(self, mock_stderr, mock_stdout, mock_lab_manager):
        mock_source = Mock()
        mock_destination = Mock()
        mock_lab_manager.side_effect = [mock_source, mock_destination]

        mock_tool = Mock(spec=Tool)
        mock_source.get_tool.return_value = mock_tool
        mock_destination.create_tool.return_value = mock_tool

        strategy = ToolMigrationStrategy(
            from_api_key=self.from_api_key,
            from_instance=self.from_instance,
            to_api_key=self.to_api_key,
            to_instance=self.to_instance,
            from_project_id=self.from_project_id,
            to_project_id=self.to_project_id,
            tool_id=self.tool_id
        )
        strategy.migrate()

        mock_source.get_tool.assert_called_with(project_id=self.from_project_id, tool_id=self.tool_id)
        mock_destination.create_tool.assert_called_with(project_id=self.to_project_id, tool=mock_tool)
        self.assertIn(f"New tool detail: \n{mock_tool}", mock_stdout.getvalue())
        self.assertEqual(mock_stderr.getvalue(), "")

    @patch('pygeai.migration.strategies.AILabManager')
    @patch('sys.stderr', new_callable=StringIO)
    def test_tool_migration_error(self, mock_stderr, mock_lab_manager):
        mock_source = Mock()
        mock_destination = Mock()
        mock_lab_manager.side_effect = [mock_source, mock_destination]

        mock_source.get_tool.side_effect = ValueError("Unable to retrieve requested tool.")

        strategy = ToolMigrationStrategy(
            from_api_key=self.from_api_key,
            from_instance=self.from_instance,
            to_api_key=self.to_api_key,
            to_instance=self.to_instance,
            from_project_id=self.from_project_id,
            to_project_id=self.to_project_id,
            tool_id=self.tool_id
        )
        strategy.migrate()

        self.assertIn("Tool migration failed: Unable to retrieve requested tool.", mock_stderr.getvalue())

    @patch('pygeai.migration.strategies.AILabManager')
    def test_process_migration_strategy_init(self, mock_lab_manager):
        strategy = AgenticProcessMigrationStrategy(
            from_api_key=self.from_api_key,
            from_instance=self.from_instance,
            to_api_key=self.to_api_key,
            to_instance=self.to_instance,
            from_project_id=self.from_project_id,
            to_project_id=self.to_project_id,
            process_id=self.process_id
        )
        self.assertEqual(strategy.from_api_key, self.from_api_key)
        self.assertEqual(strategy.from_instance, self.from_instance)
        self.assertEqual(strategy.to_api_key, self.to_api_key)
        self.assertEqual(strategy.to_instance, self.to_instance)
        self.assertEqual(strategy.from_project_id, self.from_project_id)
        self.assertEqual(strategy.to_project_id, self.to_project_id)
        self.assertEqual(strategy.process_id, self.process_id)
        mock_lab_manager.assert_any_call(api_key=self.from_api_key, base_url=self.from_instance)
        mock_lab_manager.assert_any_call(api_key=self.to_api_key, base_url=self.to_instance)

    @patch('pygeai.migration.strategies.AILabManager')
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    def test_process_migration_success(self, mock_stderr, mock_stdout, mock_lab_manager):
        mock_source = Mock()
        mock_destination = Mock()
        mock_lab_manager.side_effect = [mock_source, mock_destination]

        mock_process = Mock(spec=AgenticProcess)
        mock_source.get_process.return_value = mock_process
        mock_destination.create_process.return_value = mock_process

        strategy = AgenticProcessMigrationStrategy(
            from_api_key=self.from_api_key,
            from_instance=self.from_instance,
            to_api_key=self.to_api_key,
            to_instance=self.to_instance,
            from_project_id=self.from_project_id,
            to_project_id=self.to_project_id,
            process_id=self.process_id
        )
        strategy.migrate()

        mock_source.get_process.assert_called_with(project_id=self.from_project_id, process_id=self.process_id)
        mock_destination.create_process.assert_called_with(project_id=self.to_project_id, process=mock_process)
        self.assertIn(f"New process detail: \n{mock_process}", mock_stdout.getvalue())
        self.assertEqual(mock_stderr.getvalue(), "")

    @patch('pygeai.migration.strategies.AILabManager')
    @patch('sys.stderr', new_callable=StringIO)
    def test_process_migration_error(self, mock_stderr, mock_lab_manager):
        mock_source = Mock()
        mock_destination = Mock()
        mock_lab_manager.side_effect = [mock_source, mock_destination]

        mock_source.get_process.side_effect = ValueError("Unable to retrieve requested process.")

        strategy = AgenticProcessMigrationStrategy(
            from_api_key=self.from_api_key,
            from_instance=self.from_instance,
            to_api_key=self.to_api_key,
            to_instance=self.to_instance,
            from_project_id=self.from_project_id,
            to_project_id=self.to_project_id,
            process_id=self.process_id
        )
        strategy.migrate()

        self.assertIn("Process migration failed: Unable to retrieve requested process.", mock_stderr.getvalue())

    @patch('pygeai.migration.strategies.AILabManager')
    def test_task_migration_strategy_init(self, mock_lab_manager):
        strategy = TaskMigrationStrategy(
            from_api_key=self.from_api_key,
            from_instance=self.from_instance,
            to_api_key=self.to_api_key,
            to_instance=self.to_instance,
            from_project_id=self.from_project_id,
            to_project_id=self.to_project_id,
            task_id=self.task_id
        )
        self.assertEqual(strategy.from_api_key, self.from_api_key)
        self.assertEqual(strategy.from_instance, self.from_instance)
        self.assertEqual(strategy.to_api_key, self.to_api_key)
        self.assertEqual(strategy.to_instance, self.to_instance)
        self.assertEqual(strategy.from_project_id, self.from_project_id)
        self.assertEqual(strategy.to_project_id, self.to_project_id)
        self.assertEqual(strategy.task_id, self.task_id)
        mock_lab_manager.assert_any_call(api_key=self.from_api_key, base_url=self.from_instance)
        mock_lab_manager.assert_any_call(api_key=self.to_api_key, base_url=self.to_instance)

    @patch('pygeai.migration.strategies.AILabManager')
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    def test_task_migration_success(self, mock_stderr, mock_stdout, mock_lab_manager):
        mock_source = Mock()
        mock_destination = Mock()
        mock_lab_manager.side_effect = [mock_source, mock_destination]

        mock_task = Mock(spec=Task)
        mock_source.get_task.return_value = mock_task
        mock_destination.create_task.return_value = mock_task

        strategy = TaskMigrationStrategy(
            from_api_key=self.from_api_key,
            from_instance=self.from_instance,
            to_api_key=self.to_api_key,
            to_instance=self.to_instance,
            from_project_id=self.from_project_id,
            to_project_id=self.to_project_id,
            task_id=self.task_id
        )
        strategy.migrate()

        mock_source.get_task.assert_called_with(project_id=self.from_project_id, task_id=self.task_id)
        mock_destination.create_task.assert_called_with(project_id=self.to_project_id, task=mock_task)
        self.assertIn(f"New task detail: \n{mock_task}", mock_stdout.getvalue())
        self.assertEqual(mock_stderr.getvalue(), "")

    @patch('pygeai.migration.strategies.AILabManager')
    @patch('sys.stderr', new_callable=StringIO)
    def test_task_migration_error(self, mock_stderr, mock_lab_manager):
        mock_source = Mock()
        mock_destination = Mock()
        mock_lab_manager.side_effect = [mock_source, mock_destination]

        mock_source.get_task.side_effect = ValueError("Unable to retrieve requested task.")

        strategy = TaskMigrationStrategy(
            from_api_key=self.from_api_key,
            from_instance=self.from_instance,
            to_api_key=self.to_api_key,
            to_instance=self.to_instance,
            from_project_id=self.from_project_id,
            to_project_id=self.to_project_id,
            task_id=self.task_id
        )
        strategy.migrate()

        self.assertIn("Task migration failed", mock_stderr.getvalue())

