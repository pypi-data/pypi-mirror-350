from typing import Dict, List, Optional

import requests
from nebu import V1ResourceMetaRequest, V1ResourceReference
from nebu.logging import logger

from orign.buffers.models import (
    V1ReplayBuffer,
    V1ReplayBufferData,
    V1ReplayBufferRequest,
    V1ReplayBuffersResponse,
    V1SampleBufferQuery,
    V1SampleResponse,
    V1Trainer,
    V1UpdateReplayBufferRequest,
)
from orign.config import GlobalConfig


class ReplayBuffer:
    def __init__(
        self,
        name: str,
        namespace: Optional[str] = None,
        trainer: Optional[V1Trainer] = None,
        train_every: Optional[int] = None,
        sample_n: Optional[int] = None,
        sample_strategy: Optional[str] = None,
        labels: Optional[Dict[str, str]] = None,
        owner: Optional[str] = None,
        config: Optional[GlobalConfig] = None,
        api_key: Optional[str] = None,
    ):
        config = config or GlobalConfig.read()
        current_server = config.get_current_server_config()
        if not current_server:
            raise ValueError("No current server config found.")
        self.api_key = api_key or current_server.api_key
        self.orign_host = current_server.server

        # Construct the WebSocket URL with query parameters
        self.buffers_url = f"{self.orign_host}/v1/buffers"

        name_parts = name.split("/")
        if len(name_parts) == 2:
            self.namespace = name_parts[0]
            self.name = name_parts[1]
        else:
            self.namespace = namespace
            self.name = name

        if not self.namespace:
            self.namespace = "-"

        specific_buffer_url = f"{self.buffers_url}/{self.namespace}/{self.name}"
        response = requests.get(
            specific_buffer_url, headers={"Authorization": f"Bearer {self.api_key}"}
        )

        if response.status_code == 404:
            self.buffer = None
        elif response.ok:
            self.buffer = V1ReplayBuffer.model_validate(response.json())
        else:
            response.raise_for_status()

        if not self.buffer:
            logger.info(f"Creating buffer {self.name} in namespace {self.namespace}")
            request = V1ReplayBufferRequest(
                metadata=V1ResourceMetaRequest(
                    name=self.name,
                    namespace=self.namespace,
                    labels=labels,
                    owner=owner,
                ),
                train_every=train_every,
                sample_n=sample_n,
                sample_strategy=sample_strategy,
                trainer=trainer,
            )

            response = requests.post(
                self.buffers_url,
                json=request.model_dump(),
                headers={"Authorization": f"Bearer {self.api_key}"},
            )
            response.raise_for_status()

            self.buffer = V1ReplayBuffer.model_validate(response.json())
            logger.info(f"Created buffer {self.buffer.metadata.name}")

        else:
            logger.info(
                f"Found buffer {self.buffer.metadata.name}, updating if necessary"
            )
            request = V1UpdateReplayBufferRequest(
                train_every=train_every,
                sample_n=sample_n,
                sample_strategy=sample_strategy,
                trainer=trainer,
            )

            response = requests.patch(
                f"{self.buffers_url}/{self.buffer.metadata.namespace}/{self.buffer.metadata.name}",
                json=request.model_dump(),
                headers={"Authorization": f"Bearer {self.api_key}"},
            )

            response.raise_for_status()
            resp_parsed = response.json()
            logger.debug("Update response JSON: {}", resp_parsed)

            if "buffer" in resp_parsed:
                self.buffer = V1ReplayBuffer.model_validate(resp_parsed["buffer"])
            else:
                self.buffer = V1ReplayBuffer.model_validate(resp_parsed)
            logger.info(f"Updated buffer {self.buffer.metadata.name}")

    def send(self, data: List[dict], train: Optional[bool] = None):
        if not self.buffer or not self.buffer.metadata.name:
            raise ValueError("Buffer not found")

        url = f"{self.buffers_url}/{self.buffer.metadata.namespace}/{self.buffer.metadata.name}/examples"

        request = V1ReplayBufferData(examples=data, train=train)  # type: ignore

        response = requests.post(
            url,
            json=request.model_dump(),
            headers={"Authorization": f"Bearer {self.api_key}"},
        )
        response.raise_for_status()
        return response.json()

    def sample(
        self,
        n: int = 10,
        strategy: str = "Random",
        link: bool = False,
    ) -> V1SampleResponse:
        """
        Samples data from the replay buffer using a POST request.

        Args:
            sample_n: The number of samples to retrieve.
            sample_strategy: The sampling strategy to use (e.g., "Random").

        Returns:
            A V1SampleResponse object containing information about the sampled dataset.
        """
        if not self.buffer or not self.buffer.metadata.name:
            raise ValueError("Buffer not found")

        url = f"{self.buffers_url}/{self.buffer.metadata.namespace}/{self.buffer.metadata.name}/sample"
        query = V1SampleBufferQuery(n=n, strategy=strategy, link=link)

        response = requests.post(
            url,
            json=query.model_dump(),
            headers={"Authorization": f"Bearer {self.api_key}"},
        )
        response.raise_for_status()
        return V1SampleResponse.model_validate(response.json())

    def train(self):
        if not self.buffer or not self.buffer.metadata.name:
            raise ValueError("Buffer not found")

        url = f"{self.buffers_url}/{self.buffer.metadata.namespace}/{self.buffer.metadata.name}/train"
        response = requests.post(
            url, headers={"Authorization": f"Bearer {self.api_key}"}
        )
        response.raise_for_status()
        return response.json()

    @classmethod
    def get(
        cls,
        namespace: Optional[str] = None,
        name: Optional[str] = None,
        config: Optional[GlobalConfig] = None,
        api_key: Optional[str] = None,
    ) -> List[V1ReplayBuffer]:
        config = config or GlobalConfig.read()
        current_server = config.get_current_server_config()
        if not current_server:
            raise ValueError("No current server config found.")
        api_key = api_key or current_server.api_key
        # Construct the WebSocket URL with query parameters
        buffers_url = f"{current_server.server}/v1/buffers"

        response = requests.get(
            buffers_url, headers={"Authorization": f"Bearer {api_key}"}
        )
        response.raise_for_status()
        buffer_response = V1ReplayBuffersResponse.model_validate(response.json())
        buffers = buffer_response.buffers
        if name:
            buffers = [b for b in buffers if b.metadata.name == name]

        if namespace:
            buffers = [b for b in buffers if b.metadata.namespace == namespace]

        return buffers

    def ref(self) -> V1ResourceReference:
        if not self.buffer:
            raise ValueError("Buffer not found")
        return V1ResourceReference(
            name=self.buffer.metadata.name,
            namespace=self.buffer.metadata.namespace,
            kind="ReplayBuffer",
        )
