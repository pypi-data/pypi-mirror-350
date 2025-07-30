import time
from typing import Any, Dict, List, Optional, Union

import requests
from nebu import Processor, V1ResourceMetaRequest, V1ResourceReference
from nebu.logging import logger

from orign.config import GlobalConfig
from orign.humans.models import (
    V1ApprovalRequest,
    V1ApprovalResponse,
    V1FeedbackItem,
    V1FeedbackRequest,
    V1FeedbackResponse,
    V1Human,
    V1HumanMessage,
    V1HumanRequest,
    V1Humans,
    V1UpdateHumanRequest,
)


class Human:
    def __init__(
        self,
        name: str,
        medium: str,
        callback: Union[V1ResourceReference, Processor],
        namespace: Optional[str] = None,
        channel: Optional[str] = None,
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

        if isinstance(callback, Processor):
            callback_ref = callback.ref()
        else:
            callback_ref = callback

        namespace = namespace or "-"
        self.namespace = namespace
        self.name = name

        self.humans_url = f"{self.orign_host}/v1/humans"
        specific_human_url = f"{self.humans_url}/{self.namespace}/{self.name}"

        response = requests.get(
            specific_human_url, headers={"Authorization": f"Bearer {self.api_key}"}
        )

        if response.status_code == 404:
            self.human = None
        elif response.ok:
            self.human = V1Human.model_validate(response.json())
        else:
            response.raise_for_status()

        if not self.human:
            logger.info(f"Creating human {name} in namespace {namespace}")
            request = V1HumanRequest(
                metadata=V1ResourceMetaRequest(
                    name=name, namespace=namespace, labels=labels, owner=owner
                ),
                medium=medium,
                channel=channel,
                callback=callback_ref,
            )
            response = requests.post(
                self.humans_url,
                json=request.model_dump(exclude_unset=True),
                headers={"Authorization": f"Bearer {self.api_key}"},
            )
            response.raise_for_status()
            self.human = V1Human.model_validate(response.json())
            logger.info(f"Created human {self.human.metadata.name}")
        else:
            logger.info(
                f"Found human {self.human.metadata.name}, updating if necessary"
            )
            update_data = V1UpdateHumanRequest(
                medium=medium,
                channel=channel,
                callback=callback_ref,
            ).model_dump(exclude_unset=True)

            patch_url = f"{self.humans_url}/{self.human.metadata.namespace}/{self.human.metadata.name}"
            response = requests.patch(
                patch_url,
                json=update_data,
                headers={"Authorization": f"Bearer {self.api_key}"},
            )
            response.raise_for_status()
            # Update local human object with potentially updated data
            self.human = V1Human.model_validate(response.json())
            logger.info(
                f"Patched existing human {self.human.metadata.namespace}/{self.human.metadata.name}"
            )

    def feedback(
        self,
        content: str,
        messages: Optional[Dict[str, Any]] = None,
        images: Optional[List[str]] = None,
        videos: Optional[List[str]] = None,
        wait: bool = False,
    ) -> V1FeedbackItem:
        """
        Request feedback from a human.
        """
        if not self.human:
            raise ValueError("Human not found")

        url = f"{self.humans_url}/{self.human.metadata.namespace}/{self.human.metadata.name}/feedback"

        request = V1FeedbackRequest(
            kind="approval",
            request=V1ApprovalRequest(
                content=content,
                images=images,
                videos=videos,
                messages=messages,
            ),
        )

        response = requests.post(
            url,
            json=request.model_dump(),
            headers={"Authorization": f"Bearer {self.api_key}"},
        )
        response.raise_for_status()
        resp = V1FeedbackItem.model_validate(response.json())
        if wait:
            resp = self.get_feedback(resp.feedback_id)
            while resp.response is None:
                logger.info("Waiting for human feedback...")
                time.sleep(5)
                resp = self.get_feedback(resp.feedback_id)
        return resp

    def record_response(
        self,
        feedback_id: str,
        content: str,
        approved: bool = False,
        messages: Optional[Dict[str, Any]] = None,
        images: Optional[List[str]] = None,
        videos: Optional[List[str]] = None,
    ) -> dict:
        """
        Record a human's response to a feedback request.
        """
        if not self.human:
            raise ValueError("Human not found")

        url = f"{self.humans_url}/{self.human.metadata.namespace}/{self.human.metadata.name}/feedback/{feedback_id}"

        data = V1FeedbackResponse(
            kind="approval",
            response=V1ApprovalResponse(
                content=content,
                images=images,
                videos=videos,
                approved=approved,
                messages=messages,
            ),
        )

        response = requests.post(
            url,
            json=data.model_dump(),
            headers={"Authorization": f"Bearer {self.api_key}"},
        )
        response.raise_for_status()
        return response.json()

    def delete(self) -> dict:
        """
        Delete this human.
        """
        if not self.human:
            raise ValueError("Human not found")

        url = f"{self.humans_url}/{self.human.metadata.namespace}/{self.human.metadata.name}"

        response = requests.delete(
            url,
            headers={"Authorization": f"Bearer {self.api_key}"},
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
    ) -> List[V1Human]:
        """
        Get a list of humans, optionally filtered by namespace and/or name.
        """
        config = config or GlobalConfig.read()
        current_server = config.get_current_server_config()
        if not current_server:
            raise ValueError("No current server config found.")
        api_key = api_key or current_server.api_key
        humans_url = f"{current_server.server}/v1/humans"

        response = requests.get(
            humans_url, headers={"Authorization": f"Bearer {api_key}"}
        )
        response.raise_for_status()

        humans_response = V1Humans.model_validate(response.json())
        humans = humans_response.humans

        if name:
            humans = [h for h in humans if h.metadata.name == name]

        if namespace:
            humans = [h for h in humans if h.metadata.namespace == namespace]

        return humans

    def get_feedback(
        self,
        feedback_id: str,
        config: Optional[GlobalConfig] = None,
        api_key: Optional[str] = None,
    ) -> V1FeedbackItem:
        """
        Get a list of humans, optionally filtered by namespace and/or name.
        """
        config = config or GlobalConfig.read()
        current_server = config.get_current_server_config()
        if not current_server:
            raise ValueError("No current server config found.")
        api_key = api_key or current_server.api_key
        if not self.human or not self.human.metadata:
            raise ValueError("Human not found")

        feedback_url = f"{self.humans_url}/{self.human.metadata.namespace}/{self.human.metadata.name}/feedback/{feedback_id}"

        response = requests.get(
            feedback_url, headers={"Authorization": f"Bearer {api_key}"}
        )
        response.raise_for_status()
        feedback_response = V1FeedbackItem.model_validate(response.json())

        return feedback_response

    def send_message(
        self,
        message: str,
        config: Optional[GlobalConfig] = None,
        api_key: Optional[str] = None,
    ) -> V1HumanMessage:
        """
        Send a message to the human.
        """
        config = config or GlobalConfig.read()
        current_server = config.get_current_server_config()
        if not current_server:
            raise ValueError("No current server config found.")
        api_key = api_key or current_server.api_key
        if not self.human or not self.human.metadata:
            raise ValueError("Human not found")

        url = f"{self.humans_url}/{self.human.metadata.namespace}/{self.human.metadata.name}/messages"

        response = requests.post(
            url,
            json={"message": message},
            headers={"Authorization": f"Bearer {api_key}"},
        )
        response.raise_for_status()
        msg = V1HumanMessage.model_validate(response.json())
        return msg
