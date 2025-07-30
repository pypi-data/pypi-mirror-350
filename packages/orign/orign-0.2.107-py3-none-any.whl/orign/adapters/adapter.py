from typing import Dict, List, Optional

import requests
from nebu import V1ResourceMetaRequest
from nebu.logging import logger

from orign.config import GlobalConfig

from .models import (
    V1Adapter,
    V1AdapterRequest,
    V1Adapters,
    V1AdapterUpdateRequest,
    V1LoraParams,
)


class Adapter:
    """
    Client for interacting with Orign Adapters API.

    This class allows retrieving, creating, updating, and deleting adapters.
    On initialization, it checks if an adapter with the given name and namespace
    exists. If not, it creates one. If it exists, it may update certain fields
    if provided during initialization.
    """

    def __init__(
        self,
        name: str,
        base_model: str,
        model_uri: str,
        checkpoint_uri: str,
        namespace: Optional[str] = None,
        lora: Optional[V1LoraParams] = None,
        learning_rate: Optional[float] = None,
        labels: Optional[Dict[str, str]] = None,
        epochs_trained: Optional[int] = None,
        examples_trained: Optional[int] = None,
        last_trained: Optional[int] = None,
        owner: Optional[str] = None,
        config: Optional[GlobalConfig] = None,
        api_key: Optional[str] = None,
    ):
        """
        Initializes the Adapter client.

        Args:
            name: The name of the adapter.
            base_model: The base model identifier used for this adapter.
            model_uri: The URI pointing to the adapter data/location.
            checkpoint_uri: The URI pointing to the adapter checkpoint data/location.
            namespace: The namespace for the adapter. If None, resolved from user profile.
            lora: Optional LoRA configuration parameters.
            learning_rate: Optional learning rate for the adapter.
            labels: Optional dictionary of labels for the adapter.
            epochs_trained: Optional count of epochs trained.
            examples_trained: Optional count of examples trained.
            last_trained: Optional timestamp of the last training epoch.
            owner: Optional owner of the adapter.
            config: Optional GlobalConfig instance. Reads default if None.
            api_key: Optional API key.
        """
        self.config = config or GlobalConfig.read()
        current_server = self.config.get_current_server_config()
        if not current_server:
            raise ValueError("No current server config found.")
        self.api_key = api_key or current_server.api_key
        self.orign_host = current_server.server
        self.adapters_url = f"{self.orign_host}/v1/adapters"

        if not self.api_key:
            raise ValueError(
                "No API key provided. Please set ORIGN_API_KEY environment variable or pass config."
            )

        name_parts = name.split("/")
        if len(name_parts) == 2:
            self.namespace = name_parts[0]
            self.name = name_parts[1]
        else:
            self.namespace = namespace
            self.name = name

        if not self.namespace:
            self.namespace = "-"

        self.adapter: Optional[V1Adapter] = None  # Initialize adapter state

        # Try to fetch the existing adapter
        self.adapter = self._get_adapter_by_name(self.namespace, self.name)

        if not self.adapter:
            logger.info(f"Creating adapter {self.name} in namespace {self.namespace}")
            request = V1AdapterRequest(
                metadata=V1ResourceMetaRequest(
                    name=self.name,
                    namespace=self.namespace,
                    labels=labels,
                    owner=owner,
                ),
                model_uri=model_uri,
                checkpoint_uri=checkpoint_uri,
                base_model=base_model,
                lora=lora,
                learning_rate=learning_rate,
                epochs_trained=epochs_trained,
                examples_trained=examples_trained,
                last_trained=last_trained,
            )
            logger.debug("Adapter request: {}", request.model_dump(exclude_none=True))
            logger.debug("Auth headers: {}", self._auth_headers())
            logger.debug("Adapters url: {}", self.adapters_url)

            response = requests.post(
                self.adapters_url,
                json=request.model_dump(exclude_none=True),
                headers=self._auth_headers(),
            )
            response.raise_for_status()

            self.adapter = V1Adapter.model_validate(response.json())
            logger.info(f"Created adapter {self.adapter.metadata.name}")

        else:
            logger.info(f"Found existing adapter {self.adapter.metadata.name}")

            update_payload = V1AdapterUpdateRequest(
                model_uri=model_uri,
                checkpoint_uri=checkpoint_uri,
                lora=lora,
                learning_rate=learning_rate,
                epochs_trained=epochs_trained,
                examples_trained=examples_trained,
                last_trained=last_trained,
                # labels=labels,
            ).model_dump(exclude_unset=True)

            if update_payload:
                logger.info(
                    f"Updating adapter {self.adapter.metadata.name} with provided init args"
                )
                self._update_adapter_instance(update_payload)

    def _auth_headers(self, api_key: Optional[str] = None) -> Dict[str, str]:
        """Returns authorization headers."""
        return {"Authorization": f"Bearer {api_key or self.api_key}"}

    def _get_adapter_by_name(self, namespace: str, name: str) -> Optional[V1Adapter]:
        """Helper to fetch a specific adapter by namespace and name."""
        url = f"{self.adapters_url}/{namespace}/{name}"
        try:
            response = requests.get(url, headers=self._auth_headers())
            response.raise_for_status()
            return V1Adapter.model_validate(response.json())
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return None  # Not found is expected
            else:
                logger.error(f"Error fetching adapter {namespace}/{name}: {e}")
                raise e

    def _update_adapter_instance(self, update_data: Dict):
        """Helper method to call the PATCH endpoint and update local state."""
        if not self.adapter:
            raise ValueError("Adapter object is not initialized or was deleted.")

        url = f"{self.adapters_url}/{self.adapter.metadata.namespace}/{self.adapter.metadata.name}"
        try:
            response = requests.patch(
                url,
                json=update_data,
                headers=self._auth_headers(),
            )
            response.raise_for_status()
            # Update local state with the response from the server
            self.adapter = V1Adapter.model_validate(response.json())
            logger.info(f"Successfully updated adapter {self.adapter.metadata.name}")
        except requests.exceptions.HTTPError as e:
            logger.error(
                f"Error updating adapter {self.adapter.metadata.namespace}/{self.adapter.metadata.name}: {e}"
            )
            raise e

    def update(
        self,
        model_uri: Optional[str] = None,
        checkpoint_uri: Optional[str] = None,
        epochs_trained: Optional[int] = None,
        examples_trained: Optional[int] = None,
        last_trained: Optional[int] = None,
        labels: Optional[Dict[str, str]] = None,
        learning_rate: Optional[float] = None,
        lora: Optional[V1LoraParams] = None,
    ):
        """
        Updates the adapter fields via a PATCH request.

        Only fields provided (not None) will be included in the update request.

        Args:
            model_uri: New URI for the adapter data.
            checkpoint_uri: New URI for the adapter checkpoint data.
            epochs_trained: Updated count of epochs trained.
            examples_trained: Updated count of examples trained.
            last_trained: Timestamp of the last training epoch.
            labels: New set of labels (Note: Check if API supports label updates via PATCH).
            learning_rate: New learning rate.
            lora: New LoRA configuration.
        """
        if not self.adapter:
            raise ValueError("Adapter not initialized or was deleted.")

        request = V1AdapterUpdateRequest(
            model_uri=model_uri,
            checkpoint_uri=checkpoint_uri,
            epochs_trained=epochs_trained,
            examples_trained=examples_trained,
            last_trained=last_trained,
            labels=labels,
            learning_rate=learning_rate,
            lora=lora,
        )
        # Only include fields that were explicitly passed to the method
        update_data = request.model_dump(exclude_unset=True)

        if not update_data:
            logger.info("No fields provided for update.")
            return

        logger.info(
            f"Requesting update for adapter {self.adapter.metadata.name} with data: {update_data}"
        )
        self._update_adapter_instance(update_data)

    def delete(self):
        """Deletes the adapter from the server."""
        if not self.adapter:
            logger.info("Adapter already deleted or not initialized.")
            return

        url = f"{self.adapters_url}/{self.adapter.metadata.namespace}/{self.adapter.metadata.name}"
        try:
            response = requests.delete(url, headers=self._auth_headers())
            response.raise_for_status()
            logger.info(
                f"Successfully deleted adapter {self.adapter.metadata.namespace}/{self.adapter.metadata.name}"
            )
            self.adapter = None  # Clear local state
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                logger.info(
                    f"Adapter {self.adapter.metadata.namespace}/{self.adapter.metadata.name} already deleted."  # type: ignore
                )
                self.adapter = None  # Align local state
            else:
                logger.error(
                    f"Error deleting adapter {self.adapter.metadata.namespace}/{self.adapter.metadata.name}: {e}"  # type: ignore
                )
                raise e

    @classmethod
    def get(
        cls,
        namespace: Optional[str] = None,
        name: Optional[str] = None,
        config: Optional[GlobalConfig] = None,
        api_key: Optional[str] = None,
    ) -> List[V1Adapter]:
        """
        Gets one specific adapter or lists adapters.

        Args:
            namespace: The namespace to filter by. Required if 'name' is provided.
            name: The name of the specific adapter to get.
            config: Optional GlobalConfig instance.

        Returns:
            A list containing the requested adapter(s). Returns an empty list if
            not found or if no adapters match the criteria.
        """
        config = config or GlobalConfig.read()
        current_server = config.get_current_server_config()
        if not current_server:
            raise ValueError("No current server config found.")
        api_key = api_key or current_server.api_key
        orign_host = current_server.server
        adapters_url = f"{orign_host}/v1/adapters"

        if not api_key:
            raise ValueError("No API key provided.")

        headers = {"Authorization": f"Bearer {api_key}"}

        try:
            if name:
                if not namespace:
                    raise ValueError(
                        "Namespace must be provided when specifying an adapter name."
                    )
                # Get a specific adapter
                url = f"{adapters_url}/{namespace}/{name}"
                response = requests.get(url, headers=headers)
                response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
                return [V1Adapter.model_validate(response.json())]
            else:
                # List adapters (optionally filtered by namespace server-side if API supports it,
                # otherwise filter client-side)
                # Assuming no server-side namespace filter for listing based on route provided
                response = requests.get(adapters_url, headers=headers)
                response.raise_for_status()
                adapters_response = V1Adapters.model_validate(response.json())
                all_adapters = adapters_response.adapters
                if namespace:
                    # Filter client-side if a namespace is specified
                    return [
                        a for a in all_adapters if a.metadata.namespace == namespace
                    ]
                else:
                    return all_adapters
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404 and name:
                logger.info(f"Adapter {namespace}/{name} not found.")
                return []  # Return empty list if specific adapter not found
            else:
                logger.error(f"Error getting adapters: {e}")
                raise e  # Re-raise other HTTP errors
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            raise e

    # --- Property accessors for convenience ---
    @property
    def metadata(self):
        if not self.adapter:
            raise ValueError("Adapter not initialized or was deleted.")
        return self.adapter.metadata

    @property
    def model_uri(self):
        if not self.adapter:
            raise ValueError("Adapter not initialized or was deleted.")
        return self.adapter.model_uri

    @property
    def base_model(self):
        if not self.adapter:
            raise ValueError("Adapter not initialized or was deleted.")
        return self.adapter.base_model

    @property
    def epochs_trained(self):
        if not self.adapter:
            raise ValueError("Adapter not initialized or was deleted.")
        return self.adapter.epochs_trained

    @property
    def examples_trained(self):
        if not self.adapter:
            raise ValueError("Adapter not initialized or was deleted.")
        return self.adapter.examples_trained

    @property
    def last_trained(self):
        if not self.adapter:
            raise ValueError("Adapter not initialized or was deleted.")
        return self.adapter.last_trained

    @property
    def lora_params(self) -> Optional[V1LoraParams]:
        if not self.adapter:
            raise ValueError("Adapter not initialized or was deleted.")
        return self.adapter.lora

    @property
    def current_learning_rate(self) -> Optional[float]:
        if not self.adapter:
            raise ValueError("Adapter not initialized or was deleted.")
        return self.adapter.learning_rate

    def __repr__(self) -> str:
        if self.adapter:
            # Direct access is safe here because of the `if self.adapter:` check
            return f"<Adapter(name='{self.adapter.metadata.name}', namespace='{self.adapter.metadata.namespace}', model_uri='{self.adapter.model_uri}', checkpoint_uri='{self.adapter.checkpoint_uri}')>"
        else:
            # Use instance attributes when adapter is None (e.g., after deletion)
            return f"<Adapter(name='{self.name}', namespace='{self.namespace}', state='deleted or not initialized')>"
