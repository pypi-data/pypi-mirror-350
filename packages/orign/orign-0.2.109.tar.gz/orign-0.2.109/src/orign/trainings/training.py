from typing import Any, Dict, List, Optional

import requests
from nebu import V1ResourceMetaRequest, V1ResourceReference
from nebu.logging import logger

from orign.config import GlobalConfig
from orign.trainings.models import (
    V1LogRequest,
    V1Training,
    V1TrainingRequest,
    V1Trainings,
    V1TrainingStatus,
    V1TrainingUpdateRequest,
)


class Training:
    def __init__(
        self,
        name: str,
        namespace: Optional[str] = None,
        config_data: Optional[Dict[str, Any]] = None,
        adapter: Optional[V1ResourceReference] = None,
        labels: Optional[Dict[str, str]] = None,
        config: Optional[GlobalConfig] = None,
        unique_adapter_active: bool = False,
        api_key: Optional[str] = None,
    ):
        config = config or GlobalConfig.read()
        current_server = config.get_current_server_config()
        if not current_server:
            raise ValueError("No current server config found.")
        self.api_key = api_key or current_server.api_key
        self.orign_host = current_server.server
        self.trainings_url = f"{self.orign_host}/v1/trainings"

        name_parts = name.split("/")
        if len(name_parts) == 2:
            self.namespace = name_parts[0]
            self.name = name_parts[1]
        else:
            self.namespace = namespace
            self.name = name

        if not self.namespace:
            self.namespace = "-"

        training_id = f"{self.namespace}/{self.name}"
        get_url = f"{self.trainings_url}/{training_id}"

        try:
            response = requests.get(
                get_url, headers={"Authorization": f"Bearer {self.api_key}"}
            )
            logger.debug("Get training response status: {}", response.status_code)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            logger.debug(
                "Get training response JSON (after raise_for_status): {}",
                response.json(),
            )
            self.training = V1Training.model_validate(response.json())
            logger.info(f"Found existing training {self.training.metadata.name}")

        except requests.exceptions.HTTPError as e:
            if e.response is not None and e.response.status_code == 404:
                # Training not found, create it
                logger.info(
                    f"Creating training {self.name} in namespace {self.namespace}"
                )
                request = V1TrainingRequest(
                    metadata=V1ResourceMetaRequest(
                        name=self.name,
                        namespace=self.namespace,
                        labels=labels,
                    ),
                    config=config_data,
                    adapter=adapter,
                    unique_adapter_active=unique_adapter_active,
                )

                request_json = request.model_dump(exclude_none=True)
                logger.debug("Create training request JSON: {}", request_json)
                logger.debug("API Key used: {}", self.api_key)
                response = requests.post(
                    self.trainings_url,
                    json=request_json,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                )
                response.raise_for_status()
                self.training = V1Training.model_validate(response.json())
                logger.info(f"Created training {self.training.metadata.name}")
            else:
                # Re-raise other HTTP errors
                raise e
        except requests.exceptions.RequestException as e:
            # Handle connection errors, timeouts, etc.
            logger.error(f"Request failed: {e}")
            raise

    def update(
        self,
        status: Optional[V1TrainingStatus] = None,
        summary_metrics: Optional[Dict[str, Any]] = None,
    ):
        if (
            not self.training
            or not self.training.metadata.namespace
            or not self.training.metadata.name
        ):
            raise ValueError("Training information is missing")

        url = f"{self.trainings_url}/{self.training.metadata.namespace}/{self.training.metadata.name}"
        request = V1TrainingUpdateRequest(
            status=status,
            summary_metrics=summary_metrics,
        )

        response = requests.patch(
            url,
            json=request.model_dump(exclude_none=True),
            headers={"Authorization": f"Bearer {self.api_key}"},
        )
        response.raise_for_status()

        # Update local state with the response
        updated_training_data = response.json()
        self.training = V1Training.model_validate(updated_training_data)

        logger.info(f"Updated training {self.training.metadata.name}")
        return self.training

    def log(
        self,
        data: Dict[str, Any],
        step: Optional[int] = None,
        timestamp: Optional[int] = None,
    ):
        if (
            not self.training
            or not self.training.metadata.namespace
            or not self.training.metadata.name
        ):
            raise ValueError("Training information is missing")

        url = f"{self.trainings_url}/{self.training.metadata.namespace}/{self.training.metadata.name}/log"
        request = V1LogRequest(data=data, step=step, timestamp=timestamp)

        response = requests.post(
            url,
            json=request.model_dump(exclude_none=True),
            headers={"Authorization": f"Bearer {self.api_key}"},
        )
        response.raise_for_status()
        logger.info(f"Logged data for training {self.training.metadata.name}")
        # Log endpoint typically returns a 200 OK or similar, no body needed
        return

    @staticmethod
    def get(
        namespace: Optional[str] = None,
        name: Optional[str] = None,
        config: Optional[GlobalConfig] = None,
        labels: Optional[Dict[str, str]] = None,
        adapter_ref: Optional[V1ResourceReference] = None,
        api_key: Optional[str] = None,
    ) -> List[V1Training]:
        config = config or GlobalConfig.read()
        current_server = config.get_current_server_config()
        if not current_server:
            raise ValueError("No current server config found.")
        api_key = api_key or current_server.api_key
        trainings_url = f"{current_server.server}/v1/trainings"

        # Build query parameters for server-side filtering
        params = {}
        if labels:
            for key, value in labels.items():
                params[f"labels[{key}]"] = value
        if adapter_ref:
            params["adapter_ref"] = adapter_ref.to_string()

        response = requests.get(
            trainings_url,
            headers={"Authorization": f"Bearer {api_key}"},
            params=params,
        )
        response.raise_for_status()
        resp_json = response.json()
        trainings_response = V1Trainings.model_validate(resp_json)

        trainings = trainings_response.trainings

        # Client-side filtering for backward compatibility
        if namespace:
            trainings = [t for t in trainings if t.metadata.namespace == namespace]

        if name:
            trainings = [t for t in trainings if t.metadata.name == name]

        return trainings
