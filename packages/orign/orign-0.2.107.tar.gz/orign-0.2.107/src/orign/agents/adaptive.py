from typing import Any, Dict, List, Optional

from chatmux import ChatRequest, ChatResponse
from mcp_use import MCPClient
from namesgenerator import get_random_name
from nebu import Message, Processor, processor
from nebu.logging import logger

from orign.actors.models import Action
from orign.humans.human import Human
from orign.humans.models import V1Feedback as Feedback
from orign.llms.llm import OnlineLLM
from orign.zoo.llms.qwen_vl import QwenVL2_5


class AdaptiveAgent:
    """An agent that can learn to adapt to its environment."""

    def __init__(
        self,
        mcp_config: Dict[str, Any],
        server_name: str,
        observation: Action,
        max_steps: int = 30,
        name: Optional[str] = None,
        llm: Optional[OnlineLLM[ChatRequest, ChatResponse, ChatRequest]] = None,
        platform: str = "runpod",
        model: str = "unsloth/Qwen2.5-VL-32B-Instruct",
        accelerators: List[str] = ["1:A100_SXM"],
        human_medium: str = "ui",
        interactive: bool = True,
        initial_action: Optional[Action] = None,
        namespace: Optional[str] = None,
    ):
        if not name:
            name = get_random_name("-")
            if not name:
                raise ValueError("Name cannot be None")
        if not llm:
            llm = QwenVL2_5(
                name=name, platform=platform, model=model, accelerators=accelerators
            )

        self.llm = llm
        self.max_steps = max_steps
        self.client = MCPClient(mcp_config)
        self.session = None
        self.interactive = interactive
        self.human_medium = human_medium
        self.namespace = namespace
        self.server_name = server_name
        feedback_proc = new_feedback_processor(
            llm=llm, platform=platform, namespace=namespace
        )
        self.human = Human(
            name=name,
            namespace=namespace,
            medium=self.human_medium,
            callback=feedback_proc,
        )
        self.result = None
        self.initial_action = initial_action
        self.observation = observation

    async def async_init(self):
        """Initialize asynchronous components."""
        if not self.session:
            self.session = await self.client.create_session(self.server_name)

    async def ctx(self, task: str):
        await self.async_init()  # Ensure session is initialized
        assert self.session is not None  # Assure type checker session is initialized
        return f"""You are operating a web browser helping accomplish tasks.
Please help complete the task '{task}' with the tools: {await self.session.discover_tools()}
Given the current screenshot of the browser, please select your next action.
Please output the action in a JSON format, following the example:
{{
    "action": "browser_navigate",
    "parameters": {{
        "url": "https://flights.google.com"
    }}
}}
If you are done, simple return the `end` action.
"""

    async def solve(
        self,
        task: str,
        max_steps: int = 30,
    ):
        await self.async_init()  # Ensure session is initialized
        assert self.session is not None  # Assure type checker session is initialized
        if self.initial_action:
            await self.session.call_tool(
                self.initial_action.name, self.initial_action.parameters
            )

        max_steps = max_steps or self.max_steps
        # Initialize messages list outside the loop if it needs to persist across steps for context
        all_messages_history = []

        for i in range(max_steps):
            logger.info(f"Taking step: {i}")

            # Take screenshot
            output = await self.session.call_tool(
                self.observation.name, self.observation.parameters
            )
            # Check if output.content is not empty and access the first element
            if not output.content:
                logger.error("No content received from observation tool.")
                continue  # or handle error appropriately

            image_b64 = output.content[0].data
            mime_type = getattr(output.content[0], "mimeType", "image/jpeg")

            # Construct data URI
            data_uri = f"data:{mime_type};base64,{image_b64}"

            # Build messages for vision model for this step
            # Incorporate history if needed, or just the current state
            current_step_messages = {
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": await self.ctx(task),
                            },  # Await ctx call
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": data_uri,
                                },
                            },
                        ],
                    }
                ]
            }
            # Option: Add history messages here if context across steps is needed by the LLM
            # current_step_messages["messages"] = all_messages_history + current_step_messages["messages"]

            # Generate an action
            resp = self.llm.generate(current_step_messages)  # Await LLM call
            if not resp.choices or not resp.choices[0].message.content:
                logger.warning("No content generated by LLM, skipping step.")
                continue

            content = resp.choices[0].message.content
            logger.debug(f"LLM generated content: {content}")

            try:
                action = Action.model_validate_json(content)
            except Exception as e:
                logger.error(f"Error validating action JSON: {e}")
                continue

            if action.name == "end":
                logger.info("Task marked as done by LLM.")
                break

            # Take mcp action
            logger.info(
                f"Executing action: {action.name} with parameters: {action.parameters}"
            )
            try:
                await self.session.call_tool(
                    action.name, action.parameters
                )  # Await tool call
            except Exception as e:
                logger.error(f"Error executing action '{action.name}': {e}")
                continue
            logger.info("Action executed successfully.")

            # Prepare messages for feedback, including the LLM's response
            feedback_messages = current_step_messages["messages"] + [
                {"role": "assistant", "content": content}
            ]
            # Update history
            all_messages_history.extend(feedback_messages)

            # Ask a human for feedback, waiting to continue loop until approved
            self.human.feedback(  # Await human feedback
                "Was this action correct?",
                messages={"messages": feedback_messages},
                wait=self.interactive,
            )

        # Now lets use all the feedback we collected to fine-tune the LLM!
        if self.interactive:
            logger.info("Starting LLM training with collected feedback.")
            self.llm.train()  # Await training


def new_feedback_processor(
    llm: OnlineLLM,
    image: str = "python:3.11-slim",
    platform: str = "runpod",
    namespace: Optional[str] = None,
) -> Processor:
    @processor(image=image, platform=platform, namespace=namespace)
    def on_feedback(message: Message[Feedback]) -> None:
        # Parse the feedback from the message
        feedback = message.content
        if not feedback:
            logger.info("No feedback content found, skipping learning step.")
            return

        response = feedback.response
        if not response:
            logger.info(
                "No response from the user in feedback, skipping learning step."
            )
            return

        if response.approved and feedback.request.messages:
            # Send to the LLM to learn
            logger.info("Sending approved feedback to LLM for learning.")
            logger.debug("Feedback data: {}", feedback.request.messages)
            llm.learn(feedback.request.messages)

    return on_feedback
