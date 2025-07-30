# TODO
import os
from typing import Any, Dict, List, Optional

import requests
from nebu.config import GlobalConfig
from nebu.containers.models import (
    V1Container,
    V1ContainerRequest,
    V1Containers,
    V1ContainerStatus,
    V1EnvVar,
    V1Meter,
    V1ResourceMetaRequest,
    V1UpdateContainer,
    V1VolumeDriver,
    V1VolumePath,
)
from openai import OpenAI
from openai.types.chat import ChatCompletion

from orign.auth import get_user_profile
from orign.config import Config


class VLLMRequest(V1ContainerRequest):  # type: ignore
    """
    A wrapper class for creating VLLM inference services.
    """

    def __init__(
        self,
        name: str,
        model: str,
        platform: str,
        bucket: str,
        accelerators: List[str],
        namespace: Optional[str] = None,
        gpu_memory_utilization: float = 0.8,
        max_num_seqs: int = 1,
        dtype: str = "bfloat16",
        max_seq_length: int = 2048,
        enable_lora: bool = False,
        price_per_token: Optional[float] = None,
        bucket_base_key: str = "vllm",
        labels: Optional[Dict[str, str]] = None,
    ):
        """
        Initialize a VLLM container request for inference services.
        Inherits from V1ContainerRequest.

        Args:
            name: Name for the inference service
            model: HuggingFace model ID to use
            platform: The compute platform to use
            bucket: S3 bucket for model storage
            accelerators: List of accelerators to use (e.g., ["A100"])
            namespace: Kubernetes namespace
            gpu_memory_utilization: GPU memory utilization percentage (0.0-1.0)
            max_num_seqs: Maximum number of sequences
            dtype: Data type for inference
            max_seq_length: Maximum sequence length for inference
            enable_lora: Whether to enable LoRA adapters
            price_per_token: Optional cost per generated token
            bucket_base_key: Base key for S3 bucket path
            labels: Optional labels to add to resources
        """
        inference_command = f"""
env && python3 -m vllm.entrypoints.openai.api_server \
    --model $MODEL \
    --port 8000 \
    --host 0.0.0.0 \
    --gpu-memory-utilization {gpu_memory_utilization} \
    --max-model-len {max_seq_length} \
    --max-num-seqs {max_num_seqs} \
    --dtype {dtype}
"""
        # optionally add lora
        if enable_lora:
            inference_command += " --enable-lora"

        inference_env = [
            V1EnvVar(key="MODEL", value=model),
        ]

        if os.getenv("HF_TOKEN"):
            inference_env.append(V1EnvVar(key="HF_TOKEN", value=os.getenv("HF_TOKEN")))
        if enable_lora:
            inference_env.append(
                V1EnvVar(key="VLLM_ALLOW_RUNTIME_LORA_UPDATING", value="True")
            )

        inference_volumes = [
            V1VolumePath(
                source=f"s3://{bucket}/{bucket_base_key}",
                dest="/adapters",
                driver=V1VolumeDriver.RCLONE_SYNC,
                continuous=True,
            )
        ]

        inference_meters = None
        if price_per_token:
            inference_meters = [
                V1Meter(
                    cost=price_per_token,
                    unit="token",
                    metric="response_value",
                    json_path="$.usage.completion_tokens",
                    currency="USD",
                )
            ]

        # Initialize the parent V1ContainerRequest
        super().__init__(
            image="vllm/vllm-openai:latest",
            platform=platform,
            metadata=V1ResourceMetaRequest(
                name=name,
                namespace=namespace,
                labels=labels,
            ),
            command=inference_command,
            accelerators=accelerators,
            env=inference_env,
            volumes=inference_volumes,
            meters=inference_meters,
            restart="Always",
            proxy_port=8000,
        )


class VLLM:
    def __init__(
        self,
        name: str,
        model: str,
        platform: str,
        bucket: str,
        accelerators: List[str],
        namespace: Optional[str] = None,
        gpu_memory_utilization: float = 0.8,
        max_num_seqs: int = 1,
        dtype: str = "bfloat16",
        max_seq_length: int = 2048,
        enable_lora: bool = False,
        price_per_token: Optional[float] = None,
        bucket_base_key: str = "vllm",
        labels: Optional[Dict[str, str]] = None,
        config: Optional[GlobalConfig] = None,
        no_delete: bool = False,
    ):
        """
        Initialize a VLLM container request for inference services.
        Inherits from V1ContainerRequest.

        Args:
            name: Name for the inference service
            model: HuggingFace model ID to use
            platform: The compute platform to use
            bucket: S3 bucket for model storage
            accelerators: List of accelerators to use (e.g., ["A100"])
            namespace: Kubernetes namespace
            gpu_memory_utilization: GPU memory utilization percentage (0.0-1.0)
            max_num_seqs: Maximum number of sequences
            dtype: Data type for inference
            max_seq_length: Maximum sequence length for inference
            enable_lora: Whether to enable LoRA adapters
            price_per_token: Optional cost per generated token
            bucket_base_key: Base key for S3 bucket path
            labels: Optional labels to add to resources
            config: Optional global config
            no_delete: Whether to prevent deletion of the resource
        """
        if not labels:
            labels = {}
        labels["model"] = model

        self.config = config or GlobalConfig.read()
        current_server_config = self.config.get_current_server_config()
        if not current_server_config:
            raise ValueError("No server config found")
        self.api_key = current_server_config.api_key
        self.nebu_host = current_server_config.server
        self.name = name
        self.namespace = namespace
        self.labels = labels
        self.model = model
        # Construct the URL for LLMs
        self.containers_url = f"{self.nebu_host}/v1/containers"

        if not namespace:
            if not self.api_key:
                raise ValueError("No API key provided")

            user_profile = get_user_profile(self.api_key)
            namespace = user_profile.handle

            if not namespace:
                namespace = user_profile.email.replace("@", "-").replace(".", "-")

            print(f"Using namespace: {namespace}")

        self.request = VLLMRequest(
            name=name,
            model=model,
            platform=platform,
            bucket=bucket,
            accelerators=accelerators,
            namespace=namespace,
            gpu_memory_utilization=gpu_memory_utilization,
            max_num_seqs=max_num_seqs,
            dtype=dtype,
            max_seq_length=max_seq_length,
            enable_lora=enable_lora,
            price_per_token=price_per_token,
            bucket_base_key=bucket_base_key,
            labels=labels,
        )

        # Fetch existing LLMs
        response = requests.get(
            self.containers_url, headers={"Authorization": f"Bearer {self.api_key}"}
        )
        response.raise_for_status()

        existing_containers = V1Containers.model_validate(response.json())
        self.container: Optional[V1Container] = next(
            (
                container_val
                for container_val in existing_containers.containers
                if container_val.metadata.name == name
                and container_val.metadata.namespace == namespace
            ),
            None,
        )

        # If not found, create
        if not self.container:
            print("Request:")
            print(self.request.model_dump_json())
            create_response = requests.post(
                self.containers_url,
                json=self.request.model_dump(),
                headers={"Authorization": f"Bearer {self.api_key}"},
            )
            create_response.raise_for_status()
            self.container = V1Container.model_validate(create_response.json())
            print(f"Created container {self.container.metadata.name}")  # type: ignore
        else:
            # Else, update
            print(
                f"Found container {self.container.metadata.name}, updating if necessary"
            )
            update_request = V1UpdateContainer(
                image=self.request.image,
                env=self.request.env,
                command=self.request.command,
                volumes=self.request.volumes,
                accelerators=self.request.accelerators,
                platform=self.request.platform,
                meters=self.request.meters,
                restart=self.request.restart,
                queue=self.request.queue,
                timeout=self.request.timeout,
                resources=self.request.resources,
                no_delete=no_delete,
            )
            print("Update request:")
            print(update_request.model_dump_json())
            patch_response = requests.patch(
                f"{self.containers_url}/{self.container.metadata.namespace}/{self.container.metadata.name}",
                json=update_request.model_dump(),
                headers={"Authorization": f"Bearer {self.api_key}"},
            )
            patch_response.raise_for_status()
            print(f"Updated container {self.container.metadata.name}")
            self.container = V1Container.model_validate(patch_response.json())

    def chat(self, messages: List[Dict[str, Any]]) -> ChatCompletion:
        """
        Chat with the LLM using the new OpenAI Python client.
        """
        if not self.container or not self.container.metadata.name:
            raise ValueError("Container not found")

        Config.refresh()
        # Pass the NEBU proxy URL if you want custom routing:
        client = OpenAI(api_key=self.api_key, base_url=f"{Config.NEBU_PROXY_URL}/v1")

        resource = f"{self.container.metadata.name}.{self.container.metadata.namespace}.Container"
        # Create a chat completion
        completion = client.chat.completions.create(
            model=self.model,
            messages=messages,  # type: ignore
            extra_headers={"X-Resource": resource},
        )

        # Convert the result to the older ChatCompletion style if desired:
        return ChatCompletion.model_validate(completion.to_dict())

    @classmethod
    def load(
        cls,
        name: str,
        namespace: Optional[str] = None,
        config: Optional[GlobalConfig] = None,
    ):
        """
        Get an LLM from the remote server.
        """
        servers = cls.get(namespace=namespace, name=name, config=config)
        if not servers:
            raise ValueError("LLM not found")
        server = servers[0]

        if not server.metadata.labels:
            raise ValueError("No labels found on container")

        model = server.metadata.labels.get("model")
        if not model:
            raise ValueError("Required 'model' label not found on container")

        out = cls.__new__(cls)
        out.container = server
        out.config = config or GlobalConfig.read()
        current_server_config = out.config.get_current_server_config()
        if not current_server_config:
            raise ValueError("No server config found")
        out.api_key = current_server_config.api_key
        out.nebu_host = current_server_config.server
        out.containers_url = f"{out.nebu_host}/v1/containers"
        out.name = name
        out.namespace = namespace
        out.model = model
        return out

    @classmethod
    def get(
        cls,
        name: Optional[str] = None,
        namespace: Optional[str] = None,
        config: Optional[GlobalConfig] = None,
    ) -> List[V1Container]:
        """
        Get a list of LLMs that match the optional name and/or namespace filters.
        """
        config = config or GlobalConfig.read()
        current_server_config = config.get_current_server_config()  # type: ignore
        if not current_server_config:
            raise ValueError("No server config found")
        containers_url = f"{current_server_config.server}/v1/containers"

        response = requests.get(
            containers_url,
            headers={"Authorization": f"Bearer {current_server_config.api_key}"},
        )
        response.raise_for_status()

        llms_response = V1Containers.model_validate(response.json())
        filtered_llms = llms_response.containers

        if name:
            filtered_llms = [llm for llm in filtered_llms if llm.metadata.name == name]
        if namespace:
            filtered_llms = [
                llm for llm in filtered_llms if llm.metadata.namespace == namespace
            ]

        return filtered_llms

    def ref(self) -> str:
        """
        Get the resource ref for the container.
        """
        return f"{self.name}.{self.namespace}.Container"

    def delete(self):
        """
        Delete the container.
        """
        if not self.container or not self.container.metadata.name:
            raise ValueError("Container not found")

        url = f"{self.containers_url}/{self.container.metadata.namespace}/{self.container.metadata.name}"
        response = requests.delete(
            url, headers={"Authorization": f"Bearer {self.api_key}"}
        )
        response.raise_for_status()
        return

    def status(self) -> Optional[V1ContainerStatus]:
        """
        Get the status of the container.
        """
        if not self.container or not self.container.metadata.name:
            raise ValueError("Container not found")
        containers = self.get(
            namespace=self.container.metadata.namespace,
            name=self.container.metadata.name,
        )
        if not containers:
            raise ValueError("Container not found")
        container = containers[0]
        return container.status
