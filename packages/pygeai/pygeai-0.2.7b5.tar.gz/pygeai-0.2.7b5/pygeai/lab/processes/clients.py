from json import JSONDecodeError
from typing import Any, Union, List

from pygeai import logger
from pygeai.core.base.clients import BaseClient
from pygeai.lab.processes.endpoints import CREATE_PROCESS_V2, UPDATE_PROCESS_V2, UPSERT_PROCESS_V2, GET_PROCESS_V2, \
    LIST_PROCESSES_V2, LIST_PROCESS_INSTANCES_V2, DELETE_PROCESS_V2, PUBLISH_PROCESS_REVISION_V2, CREATE_TASK_V2, \
    UPDATE_TASK_V2, UPSERT_TASK_V2, GET_TASK_V2, LIST_TASKS_V2, DELETE_TASK_V2, PUBLISH_TASK_REVISION_V2, \
    START_INSTANCE_V2, ABORT_INSTANCE_V2, GET_INSTANCE_V2, GET_INSTANCE_HISTORY_V2, GET_THREAD_INFORMATION_V2, \
    SEND_USER_SIGNAL_V2, CREATE_KB_V1, GET_KB_V1, LIST_KBS_V1, DELETE_KB_V1, LIST_JOBS_V1


class AgenticProcessClient(BaseClient):

    def create_process(
            self,
            project_id: str,
            key: str,
            name: str,
            description: str = None,
            kb: dict = None,
            agentic_activities: list = None,
            artifact_signals: list = None,
            user_signals: list = None,
            start_event: dict = None,
            end_event: dict = None,
            sequence_flows: list = None,
            variables: list = None,
            automatic_publish: bool = False
    ):
        """
        Creates a new process in the specified project.

        :param project_id: str - Unique identifier of the project.
        :param key: str - Unique key for the process.
        :param name: str - Name of the process.
        :param description: str, optional - Description of the process.
        :param kb: dict, optional - Knowledge base configuration.
        :param agentic_activities: list, optional - List of agentic activity definitions.
        :param artifact_signals: list, optional - List of artifact signal definitions.
        :param user_signals: list, optional - List of user signal definitions.
        :param start_event: dict, optional - Start event definition.
        :param end_event: dict, optional - End event definition.
        :param sequence_flows: list, optional - List of sequence flow definitions.
        :param variables: list, optional - Updated list of variables.
        :param automatic_publish: bool - Whether to publish the process after creation. Defaults to False.
        :return: dict or str - JSON response with the created process details if successful, otherwise raw text.
        """
        endpoint = CREATE_PROCESS_V2
        if automatic_publish:
            endpoint = f"{endpoint}?automaticPublish=true"

        headers = {
            "Authorization": self.api_service.token,
            "ProjectId": project_id,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        data = {
            "processDefinition": {
                "key": key,
                "name": name
            }
        }
        if description:
            data["processDefinition"]["description"] = description
        if kb:
            data["processDefinition"]["kb"] = kb
        if agentic_activities:
            data["processDefinition"]["agenticActivities"] = agentic_activities
        if artifact_signals:
            data["processDefinition"]["artifactSignals"] = artifact_signals
        if user_signals:
            data["processDefinition"]["userSignals"] = user_signals
        if start_event:
            data["processDefinition"]["startEvent"] = start_event
        if end_event:
            data["processDefinition"]["endEvent"] = end_event
        if sequence_flows:
            data["processDefinition"]["sequenceFlows"] = sequence_flows
        if variables:
            data["processDefinition"]["variables"] = variables

        logger.debug(f"Creating agentic process with data: {data}")

        response = self.api_service.post(endpoint=endpoint, headers=headers, data=data)
        try:
            result = response.json()
        except JSONDecodeError:
            result = response.text

        return result

    def update_process(
            self,
            project_id: str,
            process_id: str = None,
            name: str = None,
            key: str = None,
            description: str = None,
            kb: dict = None,
            agentic_activities: list = None,
            artifact_signals: list = None,
            user_signals: list = None,
            start_event: dict = None,
            end_event: dict = None,
            sequence_flows: list = None,
            variables: list = None,
            automatic_publish: bool = False,
            upsert: bool = False
    ):
        """
        Updates an existing process in the specified project or upserts it if specified.

        :param project_id: str - Unique identifier of the project.
        :param process_id: str, optional - Unique identifier of the process to update.
        :param name: str, optional - Name of the process to update (used if process_id is not provided).
        :param key: str, optional - Updated unique key for the process.
        :param description: str, optional - Updated description of the process.
        :param kb: dict, optional - Updated knowledge base configuration.
        :param agentic_activities: list, optional - Updated list of agentic activity definitions.
        :param artifact_signals: list, optional - Updated list of artifact signal definitions.
        :param user_signals: list, optional - Updated list of user signal definitions.
        :param start_event: dict, optional - Updated start event definition.
        :param end_event: dict, optional - Updated end event definition.
        :param sequence_flows: list, optional - Updated list of sequence flow definitions.
        :param variables: list, optional - Updated list of variables.
        :param automatic_publish: bool - Whether to publish the process after updating. Defaults to False.
        :param upsert: bool - Whether to insert the process if it does not exist. Defaults to False.
        :return: dict or str - JSON response with the updated process details if successful, otherwise raw text.
        :raises ValueError: If neither process_id nor name is provided.
        """
        if not (process_id or name):
            raise ValueError("Either process_id or name must be provided.")

        identifier = process_id if process_id else name
        endpoint = UPSERT_PROCESS_V2 if upsert else UPDATE_PROCESS_V2
        endpoint = endpoint.format(processId=identifier)

        if automatic_publish:
            endpoint = f"{endpoint}?automaticPublish=true"

        headers = {
            "Authorization": self.api_service.token,
            "ProjectId": project_id,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        data = {
            "processDefinition": {}
        }
        if key is not None:
            data["processDefinition"]["key"] = key
        if name is not None:
            data["processDefinition"]["name"] = name
        if description is not None:
            data["processDefinition"]["description"] = description
        if kb is not None:
            data["processDefinition"]["kb"] = kb
        if agentic_activities is not None:
            data["processDefinition"]["agenticActivities"] = agentic_activities
        if artifact_signals is not None:
            data["processDefinition"]["artifactSignals"] = artifact_signals
        if user_signals is not None:
            data["processDefinition"]["userSignals"] = user_signals
        if start_event is not None:
            data["processDefinition"]["startEvent"] = start_event
        if end_event is not None:
            data["processDefinition"]["endEvent"] = end_event
        if sequence_flows is not None:
            data["processDefinition"]["sequenceFlows"] = sequence_flows
        if variables:
            data["processDefinition"]["variables"] = variables

        if kb is None and not upsert:
            current_process = self.get_process(project_id=project_id, process_id=process_id, process_name=name)
            if isinstance(current_process, dict) and "processDefinition" in current_process:
                kb = current_process["processDefinition"].get("kb")

        if agentic_activities is None and not upsert:
            current_process = self.get_process(project_id=project_id, process_id=process_id, process_name=name)
            if isinstance(current_process, dict) and "processDefinition" in current_process:
                agentic_activities = current_process["processDefinition"].get("agenticActivities")
        if agentic_activities is not None:
            data["processDefinition"]["agenticActivities"] = agentic_activities

        if process_id:
            logger.debug(f"Updating agentic process with ID {process_id} with data: {data}")
        else:
            logger.debug(f"Updating agentic process with name{name} with data: {data}")

        response = self.api_service.put(
            endpoint=endpoint,
            headers=headers,
            data=data
        )
        try:
            result = response.json()
        except JSONDecodeError:
            result = response.text

        return result

    def get_process(
            self,
            project_id: str,
            process_id: str = None,
            process_name: str = None,
            revision: str = "0",
            version: int = 0,
            allow_drafts: bool = True
    ):
        """
        Retrieves details of a specific process in the specified project, identified by either its ID or name.

        :param project_id: str - Unique identifier of the project.
        :param process_id: str, optional - Unique identifier of the process to retrieve. Defaults to None.
        :param process_name: str, optional - Name of the process to retrieve. Defaults to None.
        :param revision: str - Revision of the process to retrieve. Defaults to '0' (latest revision).
        :param version: int - Version of the process to retrieve. Defaults to 0 (latest version).
        :param allow_drafts: bool - Whether to include draft processes in the retrieval. Defaults to True.
        :return: dict or str - JSON response containing the process details if successful, otherwise the raw response text.
        :raises ValueError: If neither process_id nor process_name is provided.
        """
        if not (process_id or process_name):
            raise ValueError("Either process_id or process_name must be provided.")

        identifier = process_id if process_id else process_name
        endpoint = GET_PROCESS_V2.format(processId=identifier)

        headers = {
            "Authorization": self.api_service.token,
            "ProjectId": project_id
        }
        params = {
            "revision": revision,
            "version": version,
            "allowDrafts": allow_drafts
        }

        if process_id:
            logger.debug(f"Retrieving agentic process detail with ID {process_id}")
        else:
            logger.debug(f"Retrieving agentic process detail with name '{process_name}'")

        response = self.api_service.get(
            endpoint=endpoint,
            headers=headers,
            params=params
        )
        try:
            result = response.json()
        except JSONDecodeError:
            result = response.text

        return result

    def list_processes(
            self,
            project_id: str,
            id: str = None,
            name: str = None,
            status: str = None,
            start: str = "0",
            count: str = "100",
            allow_draft: bool = True
    ):
        """
        Retrieves a list of processes in the specified project, filtered by the provided criteria.

        :param project_id: str - Unique identifier of the project.
        :param id: str, optional - ID of the process to filter by. Defaults to None.
        :param name: str, optional - Name of the process to filter by. Defaults to None.
        :param status: str, optional - Status of the processes to filter by (e.g., 'active', 'inactive'). Defaults to None.
        :param start: str - Starting index for pagination. Defaults to '0'.
        :param count: str - Number of processes to retrieve. Defaults to '100'.
        :param allow_draft: bool - Whether to include draft processes in the list. Defaults to True.
        :return: dict or str - JSON response containing the list of processes if successful, otherwise the raw response text.
        """
        endpoint = LIST_PROCESSES_V2
        headers = {
            "Authorization": self.api_service.token,
            "ProjectId": project_id
        }
        params = {
            "start": start,
            "count": count,
            "allowDraft": allow_draft
        }
        if id:
            params["id"] = id
        if name:
            params["name"] = name
        if status:
            params["status"] = status

        logger.debug(f"Listing agentic processes for project with ID {project_id}")

        response = self.api_service.get(
            endpoint=endpoint,
            headers=headers,
            params=params
        )
        try:
            result = response.json()
        except JSONDecodeError:
            result = response.text

        return result

    def list_process_instances(
            self,
            project_id: str,
            process_id: str,
            is_active: bool = True,
            start: str = "0",
            count: str = "10"
    ):
        """
        Retrieves a list of process instances for a specific process in the specified project.

        :param project_id: str - Unique identifier of the project.
        :param process_id: str - Unique identifier of the process to list instances for.
        :param is_active: bool - Whether to list only active process instances. Defaults to True.
        :param start: str - Starting index for pagination. Defaults to '0'.
        :param count: str - Number of process instances to retrieve. Defaults to '10'.
        :return: dict or str - JSON response containing the list of process instances if successful, otherwise the raw response text.
        :raises ValueError: If process_id is not provided.
        """
        if not process_id:
            raise ValueError("Process ID must be provided.")

        endpoint = LIST_PROCESS_INSTANCES_V2.format(processId=process_id)
        headers = {
            "Authorization": self.api_service.token,
            "ProjectId": project_id
        }
        params = {
            "isActive": is_active,
            "start": start,
            "count": count
        }

        logger.debug(f"Listing instances for agentic process with ID {process_id}")

        response = self.api_service.get(
            endpoint=endpoint,
            headers=headers,
            params=params
        )
        try:
            result = response.json()
        except JSONDecodeError:
            result = response.text

        return result

    def delete_process(
            self,
            project_id: str,
            process_id: str = None,
            process_name: str = None
    ):
        """
        Deletes a specific process in the specified project, identified by either its ID or name.

        :param project_id: str - Unique identifier of the project.
        :param process_id: str, optional - Unique identifier of the process to delete. Defaults to None.
        :param process_name: str, optional - Name of the process to delete. Defaults to None.
        :return: dict or str - JSON response confirming the deletion if successful, otherwise the raw response text.
        :raises ValueError: If neither process_id nor process_name is provided.
        """
        if not (process_id or process_name):
            raise ValueError("Either process_id or process_name must be provided.")

        identifier = process_id if process_id else process_name
        endpoint = DELETE_PROCESS_V2.format(processId=identifier)

        headers = {
            "Authorization": self.api_service.token,
            "ProjectId": project_id
        }

        logger.debug(f"Deleting agentic process with ID {process_id}")

        response = self.api_service.delete(
            endpoint=endpoint,
            headers=headers
        )
        try:
            result = response.json()
        except JSONDecodeError:
            result = response.text

        return result

    def publish_process_revision(
            self,
            project_id: str,
            process_id: str = None,
            process_name: str = None,
            revision: str = None
    ):
        """
        Publishes a specific revision of a process in the specified project.

        :param project_id: str - Unique identifier of the project.
        :param process_id: str, optional - Unique identifier of the process to publish. Defaults to None.
        :param process_name: str, optional - Name of the process to publish. Defaults to None.
        :param revision: str - Revision of the process to publish.
        :return: dict or str - JSON response containing the result of the publish operation if successful, otherwise the raw response text.
        :raises ValueError: If neither process_id nor process_name is provided, or if revision is not specified.
        """
        if not (process_id or process_name):
            raise ValueError("Either process_id or process_name must be provided.")
        if not revision:
            raise ValueError("Revision must be provided.")

        identifier = process_id if process_id else process_name
        endpoint = PUBLISH_PROCESS_REVISION_V2.format(processId=identifier)

        headers = {
            "Authorization": self.api_service.token,
            "ProjectId": project_id
        }

        if process_id:
            logger.debug(f"Publishing revision {revision} for agentic process with ID {process_id}")
        else:
            logger.debug(f"Publishing revision {revision} for agentic process with name '{process_name}'")

        response = self.api_service.post(
            endpoint=endpoint,
            headers=headers,
            data={
                "revision": revision
            }
        )
        try:
            result = response.json()
        except JSONDecodeError:
            result = response.text

        return result

    def create_task(
            self,
            project_id: str,
            name: str,
            description: str = None,
            title_template: str = None,
            id: str = None,
            prompt_data: dict = None,
            artifact_types: List[dict] = None,
            automatic_publish: bool = False
    ):
        """
        Creates a new task in the specified project.

        :param project_id: str - Unique identifier of the project where the task will be created.
        :param name: str - Required name of the task, must be unique within the project and exclude ':' or '/'.
        :param description: str, optional - Description of what the task does, for user understanding (not used by agents).
        :param title_template: str, optional - Template for naming task instances (e.g., 'specs for {{issue}}'), with variables replaced during execution.
        :param id: str, optional - Custom identifier for the task; if provided, overrides system-assigned ID in insert mode.
        :param prompt_data: dict, optional - Prompt configuration (same as AgentData prompt), combined with agent prompt during execution.
        :param artifact_types: List[dict], optional - List of artifact types associated with the task, each with 'name', 'description', 'isRequired', 'usageType', and 'artifactVariableKey'.
        :param automatic_publish: bool - Whether to publish the task after creation. Defaults to False.
        :return: dict or str - JSON response with the created task details if successful, otherwise raw text.
        """
        endpoint = CREATE_TASK_V2
        if automatic_publish:
            endpoint = f"{endpoint}?automaticPublish=true"

        headers = {
            "Authorization": self.api_service.token,
            "ProjectId": project_id,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        data = {
            "taskDefinition": {
                "name": name
            }
        }
        if id:
            data["taskDefinition"]["id"] = id
        if description:
            data["taskDefinition"]["description"] = description
        if title_template:
            data["taskDefinition"]["titleTemplate"] = title_template
        if prompt_data:
            data["taskDefinition"]["promptData"] = prompt_data
        if artifact_types:
            data["taskDefinition"]["artifactTypes"] = artifact_types

        logger.debug(f"Creating task with data: {data}")

        response = self.api_service.post(endpoint=endpoint, headers=headers, data=data)
        try:
            return response.json()
        except JSONDecodeError:
            return response.text

    def get_task(
            self,
            project_id: str,
            task_id: str,
            task_name: str = None
    ):
        """
        Retrieves details of a specific task in the specified project.

        :param project_id: str - Unique identifier of the project.
        :param task_id: str, optional - Unique identifier of the task to retrieve.
        :param task_name: str, optional - Name of the task to retrieve.
        :return: dict or str - JSON response containing the task details if successful, otherwise raw text.
        :raises ValueError: If neither task_id nor task_name is provided.
        """
        if not (task_id or task_name):
            raise ValueError("Either task_id or task_name must be provided.")

        identifier = task_id if task_id else task_name
        endpoint = GET_TASK_V2.format(taskId=identifier)
        headers = {
            "Authorization": self.api_service.token,
            "ProjectId": project_id
        }

        if task_id:
            logger.debug(f"Retrieving task detail with ID {task_id}")
        else:
            logger.debug(f"Retrieving task detail with name {task_name}")

        response = self.api_service.get(endpoint=endpoint, headers=headers)
        try:
            return response.json()
        except JSONDecodeError:
            return response.text

    def list_tasks(
            self,
            project_id: str,
            id: str = None,
            start: str = "0",
            count: str = "100",
            allow_drafts: bool = True
    ):
        """
        Retrieves a list of tasks in the specified project.

        :param project_id: str - Unique identifier of the project.
        :param id: str, optional - ID of the task to filter by.
        :param start: str - Starting index for pagination. Defaults to '0'.
        :param count: str - Number of tasks to retrieve. Defaults to '100'.
        :param allow_drafts: bool - Whether to include draft tasks in the list. Defaults to True.
        :return: dict or str - JSON response containing the list of tasks if successful, otherwise raw text.
        """
        endpoint = LIST_TASKS_V2
        headers = {
            "Authorization": self.api_service.token,
            "ProjectId": project_id
        }
        params = {
            "start": start,
            "count": count,
            "allowDrafts": allow_drafts
        }
        if id:
            params["id"] = id

        logger.debug(f"Listing tasks for project with ID {project_id}")

        response = self.api_service.get(endpoint=endpoint, headers=headers, params=params)
        try:
            return response.json()
        except JSONDecodeError:
            return response.text

    def update_task(
            self,
            project_id: str,
            task_id: str,
            name: str = None,
            description: str = None,
            title_template: str = None,
            id: str = None,
            prompt_data: dict = None,
            artifact_types: List[dict] = None,
            automatic_publish: bool = False,
            upsert: bool = False
    ):
        """
        Updates an existing task in the specified project or upserts it if specified.

        :param project_id: str - Unique identifier of the project where the task resides.
        :param task_id: str - Unique identifier of the task to update.
        :param name: str, optional - Updated name of the task, must be unique within the project and exclude ':' or '/' if provided.
        :param description: str, optional - Updated description of what the task does, for user understanding (not used by agents).
        :param title_template: str, optional - Updated template for naming task instances (e.g., 'specs for {{issue}}'), with variables replaced during execution.
        :param id: str, optional - Custom identifier for the task; only used in upsert mode to set the ID if creating a new task.
        :param prompt_data: dict, optional - Updated prompt configuration (same as AgentData prompt), combined with agent prompt during execution.
        :param artifact_types: List[dict], optional - Updated list of artifact types associated with the task, each with 'name', 'description', 'isRequired', 'usageType', and 'artifactVariableKey'.
        :param automatic_publish: bool - Whether to publish the task after updating. Defaults to False.
        :param upsert: bool - Whether to insert the task if it does not exist. Defaults to False.
        :return: dict or str - JSON response with the updated task details if successful, otherwise raw text.
        :raises ValueError: If task_id is not provided.
        """
        if not task_id:
            raise ValueError("Task ID must be provided.")

        identifier = task_id
        endpoint = UPSERT_TASK_V2 if upsert else UPDATE_TASK_V2
        endpoint = endpoint.format(taskId=identifier)
        if automatic_publish:
            endpoint = f"{endpoint}?automaticPublish=true"

        headers = {
            "Authorization": self.api_service.token,
            "ProjectId": project_id,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        data = {
            "taskDefinition": {}
        }
        if id is not None and upsert:
            data["taskDefinition"]["id"] = id
        if name is not None:
            data["taskDefinition"]["name"] = name
        if description is not None:
            data["taskDefinition"]["description"] = description
        if title_template is not None:
            data["taskDefinition"]["titleTemplate"] = title_template
        if prompt_data is not None:
            data["taskDefinition"]["promptData"] = prompt_data
        if artifact_types is not None:
            data["taskDefinition"]["artifactTypes"] = artifact_types

        logger.debug(f"Updating task with ID {task_id} with data: {data}")

        response = self.api_service.put(endpoint=endpoint, headers=headers, data=data)
        try:
            return response.json()
        except JSONDecodeError:
            return response.text

    def delete_task(
            self,
            project_id: str,
            task_id: str,
            task_name: str = None
    ):
        """
        Deletes a specific task in the specified project.

        :param project_id: str - Unique identifier of the project.
        :param task_id: str, optional - Unique identifier of the task to delete.
        :param task_name: str, optional - Name of the task to delete.
        :return: dict or str - JSON response confirming deletion if successful, otherwise raw text.
        :raises ValueError: If neither task_id nor task_name is provided.
        """
        if not (task_id or task_name):
            raise ValueError("Either task_id or task_name must be provided.")

        identifier = task_id if task_id else task_name
        endpoint = DELETE_TASK_V2.format(taskId=identifier)
        headers = {
            "Authorization": self.api_service.token,
            "ProjectId": project_id
        }

        if task_id:
            logger.debug(f"Deleting task with ID {task_id}")
        else:
            logger.debug(f"Deleting task with name {task_name}")

        response = self.api_service.delete(endpoint=endpoint, headers=headers)
        try:
            return response.json()
        except JSONDecodeError:
            return response.text

    def publish_task_revision(
            self,
            project_id: str,
            task_id: str,
            task_name: str = None,
            revision: str = None
    ):
        """
        Publishes a specific revision of a task in the specified project.

        :param project_id: str - Unique identifier of the project.
        :param task_id: str, optional - Unique identifier of the task to publish.
        :param task_name: str, optional - Name of the task to publish.
        :param revision: str - Revision of the task to publish.
        :return: dict or str - JSON response containing the result of the publish operation if successful, otherwise raw text.
        :raises ValueError: If neither task_id nor task_name is provided, or if revision is not specified.
        """
        if not (task_id or task_name):
            raise ValueError("Either task_id or task_name must be provided.")
        if not revision:
            raise ValueError("Revision must be provided.")

        identifier = task_id if task_id else task_name
        endpoint = PUBLISH_TASK_REVISION_V2.format(taskId=identifier)
        headers = {
            "Authorization": self.api_service.token,
            "ProjectId": project_id,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        data = {
            "revision": revision
        }

        if task_id:
            logger.debug(f"Publishing revision {revision} for task with ID {task_id}")
        else:
            logger.debug(f"Publishing revision {revision} for task with name {task_name}")

        response = self.api_service.post(endpoint=endpoint, headers=headers, data=data)
        try:
            return response.json()
        except JSONDecodeError:
            return response.text

    def start_instance(
            self,
            project_id: str,
            process_name: str,
            subject: str = None,
            variables: list = None
    ):
        """
        Starts a new process instance in the specified project.

        :param project_id: str - Unique identifier of the project.
        :param process_name: str - Name of the process to start an instance for.
        :param subject: str, optional - Subject of the process instance.
        :param variables: list, optional - List of variables for the instance (e.g., [{"key": "location", "value": "Paris"}]).
        :return: dict or str - JSON response with the started instance details if successful, otherwise raw text.
        """
        endpoint = START_INSTANCE_V2
        headers = {
            "Authorization": self.api_service.token,
            "ProjectId": project_id,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        data = {
            "instanceDefinition": {
                "process": process_name
            }
        }
        if subject:
            data["instanceDefinition"]["subject"] = subject
        if variables:
            data["instanceDefinition"]["variables"] = variables

        logger.info(f"Starting instance for process with name '{process_name}'")

        response = self.api_service.post(endpoint=endpoint, headers=headers, data=data)
        try:
            return response.json()
        except JSONDecodeError:
            return response.text

    def abort_instance(
            self,
            project_id: str,
            instance_id: str
    ):
        """
        Aborts a specific process instance in the specified project.

        :param project_id: str - Unique identifier of the project.
        :param instance_id: str - Unique identifier of the instance to abort.
        :return: dict or str - JSON response confirming the abort operation if successful, otherwise raw text.
        :raises ValueError: If instance_id is not provided.
        """
        if not instance_id:
            raise ValueError("Instance ID must be provided.")

        endpoint = ABORT_INSTANCE_V2.format(instanceId=instance_id)
        headers = {
            "Authorization": self.api_service.token,
            "ProjectId": project_id,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        logger.info(f"Aborting instance with ID '{instance_id}'")

        response = self.api_service.post(endpoint=endpoint, headers=headers, data={})
        try:
            return response.json()
        except JSONDecodeError:
            return response.text

    def get_instance(
            self,
            project_id: str,
            instance_id: str
    ):
        """
        Retrieves details of a specific process instance in the specified project.

        :param project_id: str - Unique identifier of the project.
        :param instance_id: str - Unique identifier of the instance to retrieve.
        :return: dict or str - JSON response containing the instance details if successful, otherwise raw text.
        :raises ValueError: If instance_id is not provided.
        """
        if not instance_id:
            raise ValueError("Instance ID must be provided.")

        endpoint = GET_INSTANCE_V2.format(instanceId=instance_id)
        headers = {
            "Authorization": self.api_service.token,
            "ProjectId": project_id
        }

        logger.info(f"Retrieving instance detail with ID '{instance_id}'")

        response = self.api_service.get(endpoint=endpoint, headers=headers)
        try:
            return response.json()
        except JSONDecodeError:
            return response.text

    def get_instance_history(
            self,
            project_id: str,
            instance_id: str
    ):
        """
        Retrieves the history (trace) of a specific process instance in the specified project.

        :param project_id: str - Unique identifier of the project.
        :param instance_id: str - Unique identifier of the instance to retrieve history for.
        :return: dict or str - JSON response containing the instance history if successful, otherwise raw text.
        :raises ValueError: If instance_id is not provided.
        """
        if not instance_id:
            raise ValueError("Instance ID must be provided.")

        endpoint = GET_INSTANCE_HISTORY_V2.format(instanceId=instance_id)
        headers = {
            "Authorization": self.api_service.token,
            "ProjectId": project_id
        }

        logger.info(f"Retrieving instance history with ID '{instance_id}'")

        response = self.api_service.get(endpoint=endpoint, headers=headers)
        try:
            return response.json()
        except JSONDecodeError:
            return response.text

    def get_thread_information(
            self,
            project_id: str,
            thread_id: str
    ):
        """
        Retrieves information about a specific thread in the specified project.

        :param project_id: str - Unique identifier of the project.
        :param thread_id: str - Unique identifier of the thread to retrieve information for.
        :return: dict or str - JSON response containing the thread information if successful, otherwise raw text.
        :raises ValueError: If thread_id is not provided.
        """
        if not thread_id:
            raise ValueError("Thread ID must be provided.")

        endpoint = GET_THREAD_INFORMATION_V2.format(threadId=thread_id)
        headers = {
            "Authorization": self.api_service.token,
            "ProjectId": project_id
        }

        logger.debug(f"Retrieving information about thread with ID {thread_id}")

        response = self.api_service.get(endpoint=endpoint, headers=headers)
        try:
            return response.json()
        except JSONDecodeError:
            return response.text

    def send_user_signal(
            self,
            project_id: str,
            instance_id: str,
            signal_name: str
    ):
        """
        Sends a user signal to a specific process instance in the specified project.

        :param project_id: str - Unique identifier of the project.
        :param instance_id: str - Unique identifier of the instance to send the signal to.
        :param signal_name: str - Name of the user signal to send (e.g., 'approval').
        :return: dict or str - JSON response confirming the signal operation if successful, otherwise raw text.
        :raises ValueError: If instance_id or signal_name is not provided.
        """
        if not instance_id:
            raise ValueError("Instance ID must be provided.")
        if not signal_name:
            raise ValueError("Signal name must be provided.")

        endpoint = SEND_USER_SIGNAL_V2.format(instanceId=instance_id)
        headers = {
            "Authorization": self.api_service.token,
            "ProjectId": project_id,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        data = {
            "name": signal_name
        }

        logger.debug(f"Sending user signal to process instance with ID {instance_id} with data: {data}")

        response = self.api_service.post(endpoint=endpoint, headers=headers, data=data)
        try:
            return response.json()
        except JSONDecodeError:
            return response.text

    def create_kb(
            self,
            project_id: str,
            name: str,
            artifacts: List[str] = None,
            metadata: List[str] = None
    ):
        """
        Creates a new knowledge base (KB) in the specified project.

        :param project_id: str - Unique identifier of the project.
        :param name: str - Name of the knowledge base.
        :param artifacts: List[str], optional - List of artifact names associated with the KB.
        :param metadata: List[str], optional - List of metadata fields for the KB.
        :return: dict or str - JSON response with the created KB details if successful, otherwise raw text.
        """
        endpoint = CREATE_KB_V1
        headers = {
            "Authorization": self.api_service.token,
            "ProjectId": project_id,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        data = {
            "KBDefinition": {
                "name": name
            }
        }
        if artifacts:
            data["KBDefinition"]["artifacts"] = artifacts
        if metadata:
            data["KBDefinition"]["metadata"] = metadata

        logger.debug(f"Creating KB with data: {data}")

        response = self.api_service.post(
            endpoint=endpoint,
            headers=headers,
            data=data
        )
        try:
            return response.json()
        except JSONDecodeError:
            return response.text

    def get_kb(
            self,
            project_id: str,
            kb_id: str = None,
            kb_name: str = None
    ):
        """
        Retrieves details of a specific knowledge base (KB) in the specified project.

        :param project_id: str - Unique identifier of the project.
        :param kb_id: str, optional - Unique identifier of the KB to retrieve.
        :param kb_name: str, optional - Name of the KB to retrieve.
        :return: dict or str - JSON response containing the KB details if successful, otherwise raw text.
        :raises ValueError: If neither kb_id nor kb_name is provided.
        """
        if not (kb_id or kb_name):
            raise ValueError("Either kb_id or kb_name must be provided.")

        identifier = kb_id if kb_id else kb_name
        endpoint = GET_KB_V1.format(kbId=identifier)
        headers = {
            "Authorization": self.api_service.token,
            "ProjectId": project_id
        }

        if kb_id:
            logger.debug(f"Retrieving KB detail with ID {kb_id}")
        else:
            logger.debug(f"Retrieving KB detail with name {kb_name}")

        response = self.api_service.get(endpoint=endpoint, headers=headers)
        try:
            return response.json()
        except JSONDecodeError:
            return response.text

    def list_kbs(
            self,
            project_id: str,
            name: str = None,
            start: str = "0",
            count: str = "100"
    ):
        """
        Retrieves a list of knowledge bases (KBs) in the specified project, filtered by the provided criteria.

        :param project_id: str - Unique identifier of the project.
        :param name: str, optional - Name of the KB to filter by. Defaults to None.
        :param start: str - Starting index for pagination. Defaults to '0'.
        :param count: str - Number of KBs to retrieve. Defaults to '100'.
        :return: dict or str - JSON response containing the list of KBs if successful, otherwise raw text.
        """
        endpoint = LIST_KBS_V1
        headers = {
            "Authorization": self.api_service.token,
            "ProjectId": project_id
        }
        params = {
            "start": start,
            "count": count
        }
        if name:
            params["name"] = name

        logger.debug(f"Listing tasks in project with ID {project_id}")

        response = self.api_service.get(endpoint=endpoint, headers=headers, params=params)
        try:
            return response.json()
        except JSONDecodeError:
            return response.text

    def delete_kb(
            self,
            project_id: str,
            kb_id: str = None,
            kb_name: str = None
    ):
        """
        Deletes a specific knowledge base (KB) in the specified project.

        :param project_id: str - Unique identifier of the project.
        :param kb_id: str, optional - Unique identifier of the KB to delete.
        :param kb_name: str, optional - Name of the KB to delete.
        :return: dict or str - JSON response confirming deletion if successful, otherwise raw text.
        :raises ValueError: If neither kb_id nor kb_name is provided.
        """
        if not (kb_id or kb_name):
            raise ValueError("Either kb_id or kb_name must be provided.")

        identifier = kb_id if kb_id else kb_name
        endpoint = DELETE_KB_V1.format(kbId=identifier)
        headers = {
            "Authorization": self.api_service.token,
            "ProjectId": project_id
        }

        if kb_id:
            logger.debug(f"Deleting KB with ID {kb_id}")
        else:
            logger.debug(f"Deleting KB with name {kb_name}")

        response = self.api_service.delete(endpoint=endpoint, headers=headers)
        try:
            return response.json()
        except JSONDecodeError:
            return response.text

    def list_jobs(
            self,
            project_id: str,
            start: str = "0",
            count: str = "100",
            topic: str = None,
            token: str = None,
            name: str = None
    ):
        """
        Retrieves a list of jobs in the specified project, filtered by the provided criteria.

        :param project_id: str - Unique identifier of the project.
        :param start: str - Starting index for pagination. Defaults to '0'.
        :param count: str - Number of jobs to retrieve. Defaults to '100'.
        :param topic: str, optional - Topic of the jobs to filter by. Defaults to None.
        :param token: str, optional - Token of the jobs to filter by. Defaults to None.
        :param name: str, optional - Name of the jobs to filter by. Defaults to None.
        :return: dict or str - JSON response containing the list of jobs if successful, otherwise the raw response text.
        """
        endpoint = LIST_JOBS_V1
        headers = {
            "Authorization": self.api_service.token,
            "ProjectId": project_id
        }
        params = {
            "start": start,
            "count": count
        }
        if topic:
            params["topic"] = topic
        if token:
            params["token"] = token
        if name:
            params["name"] = name

        logger.debug(f"Listing jobs for project with ID {project_id}")

        response = self.api_service.get(
            endpoint=endpoint,
            headers=headers,
            params=params
        )
        try:
            result = response.json()
        except JSONDecodeError:
            result = response.text

        return result
