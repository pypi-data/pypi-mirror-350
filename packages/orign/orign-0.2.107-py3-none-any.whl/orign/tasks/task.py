from typing import Any, Dict, List, Optional

import requests
from nebu import V1ResourceMetaRequest
from nebu.logging import logger

from orign.config import GlobalConfig
from orign.tasks.models import (
    V1Action,
    V1Attempt,
    V1EnvState,
    V1Review,
    V1ReviewRequest,
    V1Reviews,
    V1Step,
    V1StepRequest,
    V1Task,
    V1TaskRequest,
    V1Tasks,
)


class Task:
    def __init__(
        self,
        name: str,
        description: str,
        max_steps: int,
        namespace: Optional[str] = None,
        labels: Optional[Dict[str, str]] = None,
        config: Optional[GlobalConfig] = None,
        api_key: Optional[str] = None,
    ):
        config = config or GlobalConfig.read()
        current_server = config.get_current_server_config()
        if not current_server:
            raise ValueError("No current server config found.")
        self.api_key = api_key or current_server.api_key
        self.orign_host = current_server.server
        self.tasks_url = f"{self.orign_host}/v1/tasks"
        self.reviews_url = f"{self.orign_host}/v1/reviews"

        if not self.api_key:
            raise ValueError("No API key provided")

        if not namespace:
            namespace = "-"

        name_parts = name.split("/")
        if len(name_parts) == 2:
            self.namespace = name_parts[0]
            self.name = name_parts[1]
        else:
            self.namespace = namespace
            self.name = name

        # Check if task exists
        try:
            existing_tasks = self.get(
                namespace=self.namespace, name=self.name, config=config
            )
            if existing_tasks:
                self.task = existing_tasks[0]
                logger.info(f"Found existing task: {self.task.metadata.id}")
            else:
                self.task = None
        except Exception as e:  # Could be 404 or other issues during fetch
            logger.error(f"Error checking for existing task: {e}")
            self.task = None

        if not self.task:
            logger.info(f"Creating task {self.name} in namespace {self.namespace}")
            request = V1TaskRequest(
                metadata=V1ResourceMetaRequest(
                    name=self.name,
                    namespace=self.namespace,
                    labels=labels,
                ),
                description=description,
                max_steps=max_steps,
            )
            response = requests.post(
                self.tasks_url,
                json=request.model_dump(),
                headers={"Authorization": f"Bearer {self.api_key}"},
            )
            response.raise_for_status()
            self.task = V1Task.model_validate(response.json())
            logger.info(f"Created task {self.task.metadata.id}")
        # No update logic needed as per API spec

        if not self.task or not self.task.metadata or not self.task.metadata.id:
            raise ValueError("Failed to get or create task ID")

        self.task_id = self.task.metadata.id

    def _get_auth_headers(self) -> Dict[str, str]:
        if not self.api_key:
            raise ValueError("API key not configured.")
        return {"Authorization": f"Bearer {self.api_key}"}

    def get_details(self) -> V1Task:
        """Refreshes and returns the details of the current task."""
        url = f"{self.tasks_url}/{self.task_id}"
        response = requests.get(url, headers=self._get_auth_headers())
        response.raise_for_status()
        self.task = V1Task.model_validate(response.json())
        return self.task

    def list_attempts(self) -> List[V1Attempt]:
        """Lists all attempts for this task."""
        url = f"{self.tasks_url}/{self.task_id}/attempts"
        response = requests.get(url, headers=self._get_auth_headers())
        response.raise_for_status()
        # Assuming the API returns a list of attempts directly
        return [V1Attempt.model_validate(attempt) for attempt in response.json()]

    def get_attempt(self, attempt_id: str) -> V1Attempt:
        """Gets a specific attempt by its ID."""
        url = f"{self.tasks_url}/{self.task_id}/attempts/{attempt_id}"
        response = requests.get(url, headers=self._get_auth_headers())
        response.raise_for_status()
        return V1Attempt.model_validate(response.json())

    def create_step(
        self,
        attempt_id: str,
        state: V1EnvState,
        action: V1Action,
        model_id: Optional[str] = None,
        chat_event: Optional[Any] = None,  # TODO: Use V1ChatEvent model when available
        reason: Optional[str] = None,
    ) -> V1Step:
        """Creates a new step within a specific attempt."""
        url = f"{self.tasks_url}/{self.task_id}/attempts/{attempt_id}/steps"
        step_request = V1StepRequest(
            state=state,
            action=action,
            model_id=model_id,
            chat_event=chat_event,  # TODO: Pass validated V1ChatEvent
            reason=reason,
        )
        response = requests.post(
            url,
            json=step_request.model_dump(),
            headers=self._get_auth_headers(),
        )
        response.raise_for_status()
        return V1Step.model_validate(response.json())

    def list_steps(self, attempt_id: str) -> List[V1Step]:
        """Lists all steps for a specific attempt."""
        url = f"{self.tasks_url}/{self.task_id}/attempts/{attempt_id}/steps"
        response = requests.get(url, headers=self._get_auth_headers())
        response.raise_for_status()
        # Assuming the API returns a list of steps directly
        return [V1Step.model_validate(step) for step in response.json()]

    def get_step(self, attempt_id: str, step_id: str) -> V1Step:
        """Gets a specific step by its ID."""
        url = f"{self.tasks_url}/{self.task_id}/attempts/{attempt_id}/steps/{step_id}"
        response = requests.get(url, headers=self._get_auth_headers())
        response.raise_for_status()
        return V1Step.model_validate(response.json())

    def create_review(self, review_request: V1ReviewRequest) -> V1Review:
        """Creates a new review."""
        response = requests.post(
            self.reviews_url,
            json=review_request.model_dump(),
            headers=self._get_auth_headers(),
        )
        response.raise_for_status()
        return V1Review.model_validate(response.json())

    def list_reviews(self, params: Optional[Dict[str, Any]] = None) -> V1Reviews:
        """Lists reviews, optionally filtered by query parameters."""
        response = requests.get(
            self.reviews_url, headers=self._get_auth_headers(), params=params or {}
        )
        response.raise_for_status()
        return V1Reviews.model_validate(response.json())

    def get_review(self, review_id: str) -> V1Review:
        """Gets a specific review by its ID."""
        url = f"{self.reviews_url}/{review_id}"
        response = requests.get(url, headers=self._get_auth_headers())
        response.raise_for_status()
        return V1Review.model_validate(response.json())

    @classmethod
    def get(
        cls,
        namespace: Optional[str] = None,
        name: Optional[str] = None,
        config: Optional[GlobalConfig] = None,
        api_key: Optional[str] = None,
    ) -> List[V1Task]:
        config = config or GlobalConfig.read()
        current_server = config.get_current_server_config()
        if not current_server:
            raise ValueError("No current server config found.")
        api_key = api_key or current_server.api_key
        orign_host = current_server.server
        tasks_url = f"{orign_host}/v1/tasks"

        if not api_key:
            raise ValueError("No API key provided")

        headers = {"Authorization": f"Bearer {api_key}"}
        params: Dict[str, str] = {}
        # The API spec doesn't explicitly mention query params for list_tasks
        # but we add them here assuming they might exist for filtering.
        # If not, the filtering happens below.
        if namespace:
            params["namespace"] = namespace
        if name:
            params["name"] = name  # This might not be supported by the API

        response = requests.get(tasks_url, headers=headers, params=params)
        response.raise_for_status()
        tasks_response = V1Tasks.model_validate(response.json())
        tasks = tasks_response.tasks

        # Manual filtering if API doesn't support query params
        if name:
            tasks = [t for t in tasks if t.metadata.name == name]
        if namespace:
            tasks = [t for t in tasks if t.metadata.namespace == namespace]

        return tasks
