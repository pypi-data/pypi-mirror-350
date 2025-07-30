# orign-py

A Python client for [Orign](https://github.com/agentsea/orign)

## Installation

```bash
pip install orign
```

Install the Orign CLI

```sh
curl -fsSL -H "Cache-Control: no-cache" https://storage.googleapis.com/orign/releases/install.sh | bash
```

To run the server locally

```sh
orign server --docker
```

## Quick Start

Let's create a stream processor that can be used to train an LLM.   
   
In this example we will create a processor that trains an LLM using TRL with 1 A100 gpu on Runpod. This function will autoscale as needed.
```python
from pydantic import BaseModel
from trl import SFTTrainer
from datasets import load_dataset
from orign import processor, Message, Bucket

class TrainingRequest(BaseModel):
    model: str
    dataset: str

@processor(
    image="pytorch/pytorch:2.6.0-cuda12.6-cudnn9-devel",
    setup_script="pip install trl",
    accelerators=["1:A100_SXM"],
    platform="runpod",
)
def train(message: Message[TrainingRequest]):
    request = message.content
    user = message.user_id

    dataset = load_dataset(request.dataset, split="train")

    trainer = SFTTrainer(
        model=,
        train_dataset=dataset,
    )
    trainer.train()

    bucket = Bucket()
    bucket.copy(
        "./output",
        "s3://mybucket/training",
    )

if __name__ == "__main__":
    req = TrainingRequest(model="Qwen/Qwen2.5-0.5B", dataset="trl-lib/Capybara")

    train(req)
```

Now let's create a processor that can run inference on our trained LLM.   
   
In this example, we create a processor that runs on GCE with 1 H100 and generates using OpenAI chat schema from our trained model.
```python
from chatx.openai import ChatCompletionRequest, ChatCompletionResponse
from orign import processor, Message, Bucket

@processor(
    image="pytorch/pytorch:2.6.0-cuda12.6-cudnn9-devel",
    setup_script="pip install transformers",
    accelerators=["1:H100_SXM"],
    platform="gce",
)
def infer(message: Message[ChatCompletionRequest]) -> ChatCompletionResponse:
    request = message.content

    return ChatCompletionResponse()

if __name__ == "__main__":
    req = ChatCompletionRequest()

    infer(req)
```

Now, lets create a replay buffer that will store our live agent experiences and allow use to sample datasets from.   
```python
from orign import ReplayBuffer

buffer = ReplayBuffer(name="mybuffer")

messages = [
    {"role": "user", "content": "Hello, how are you?"}, 
    {"role": "assistant", "content": "I'm good, thank you!"}
]

buffer.send(messages)

# Randomly sample 100 datapoints from the buffer
samples = buffer.sample(n=100, strategy="Random")
train(samples)
```

Next, let's create a human that can provide feedback to the model.   
   
In this example, we create an Slack channel where the user can provide feedback to the model. Once the user does this the `on_feedback` processor will run on ec2.
```python
from orign import Human, FeedbackResponse

# This function will be called when the human provides feedback
@processor(image="python:latest", platform="ec2")s
def on_feedback(message: Message[FeedbackResponse]):
    from orign import ReplayBuffer

    data = message.content

    buffer = ReplayBuffer.load("mybuffer")
    buffer.send(data)

# The Orign app must be installed in your slack workspace
human = Human(
    name="my-slack-human",
    medium="slack",
    channel="#my-channel",
    callback=on_feedback,
)

# This will send a message to the human asking for feedback
needs_review = [
    {"role": "user", "content": "Hello, how are you?"}, 
    {"role": "assistant", "content": "I'm good, thank you!"}
]
human.request_feedback(content="Is this a good response?", messages=needs_review)

# We can also post update messages to the human
human.post_message(content="I'm training the model on your feedback...")
```

Finally putting it all together, let't train a model to learn to accomplish tasks interactively using MCP.   
```python
from mcp_use import MCPClient

task = "Search for the latest cat videos"

config = {
    "mcpServers": {
        "playwright": {
            "command": "npx",
            "args": ["@playwright/mcp@latest"],
            "env": {"DISPLAY": ":1"},
        }
    }
}
client = MCPClient.from_dict(config)
max_steps = 20

for i in range(max_steps):
    prompt = "Please try to accomplish the task: " + task + "with these tools: "  + client.tools()
    messages = [{"role": "user", "content": prompt}]

    mcp_state = # ... get MCP state

    resp = llm.chat(messages)
    print(resp)

    mcp_action = # ... take MCP action

    messages.append(resp['choices'][0]['message'])
    human.request_feedback(content="Was this a good action?", messages=messages)
```

Or optionally use our high level objects.

```python
from orign import actor, validator, solve

@actor
def act(task: str, mcp_servers: List[Any], history: List[Step]) -> Step:
    prompt = "Please try to accomplish the task: " + task + "with these tools: "  # ... MCP tools
    messages = [{"role": "user", "content": prompt}]

    mcp_state = # ... get MCP state

    resp = llm.chat(messages)
    print(resp)

    mcp_action = # ... take MCP action

    messages.append(resp['choices'][0]['message'])
    human.request_feedback(content="Was this a good action?", messages=messages)

    return Step(
        state=EnvState(
            text=mcp_state,
        ),
        action=mcp_action,
    )

@validator
def score(step: Step) -> float:

    prompt = f"""Given the step {step.model_dump()}, return a value between 1-10 on how good 
    it was with respect to the task {step.task} 
    """
    messages = [{"role": "user", "content": prompt}]
    resp = reward_llm.chat()

    human.request_feedback(content="Was this a good action?", messages=messages)

    return resp['choices'][0]['message']

solve(
    task="Find the latest news on Cats",
    actor=act,
    validator=score,
    mcp_servers=[],
)
```

Now as you solve tasks with the actor, every action will be sent for a human to review. Once they do the `on_feedback` function will be called sending the feedback to the replay buffer which will train the model online.

// TODO: agents via processors

## Examples

See the [examples](examples) directory for more usage examples.
