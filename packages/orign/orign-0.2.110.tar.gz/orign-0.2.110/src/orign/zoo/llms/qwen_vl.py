from typing import Dict, List, Optional

from chatmux import ChatRequest, ChatResponse
from nebu.config import GlobalConfig as NebuGlobalConfig

from orign.buffers.models import V1Trainer
from orign.config import GlobalConfig
from orign.llms.llm import OnlineLLM
from orign.zoo.processors.qwen_server import QwenVLServer
from orign.zoo.processors.unsloth_trainer import UnslothSFT

supported_models = [
    "unsloth/Qwen2.5-VL-3B-Instruct",
    "unsloth/Qwen2.5-VL-3B-Instruct-bnb-4bit",
    "unsloth/Qwen2.5-VL-3B-Instruct-unsloth-bnb-4bit",
    "unsloth/Qwen2.5-VL-7B-Instruct",
    "unsloth/Qwen2.5-VL-7B-Instruct-bnb-4bit",
    "unsloth/Qwen2.5-VL-7B-Instruct-unsloth-bnb-4bit",
    "unsloth/Qwen2.5-VL-14B-Instruct",
    "unsloth/Qwen2.5-VL-32B-Instruct",
    "unsloth/Qwen2.5-VL-32B-Instruct-bnb-4bit",
    "unsloth/Qwen2.5-VL-32B-Instruct-unsloth-bnb-4bit",
    "unsloth/Qwen2.5-VL-72B-Instruct",
    "unsloth/Qwen2.5-VL-72B-Instruct-bnb-4bit",
    "unsloth/Qwen2.5-VL-72B-Instruct-unsloth-bnb-4bit",
]


class QwenVL2_5(OnlineLLM[ChatRequest, ChatResponse, ChatRequest]):
    def __init__(
        self,
        name: str,
        namespace: Optional[str] = None,
        model: str = "unsloth/Qwen2.5-VL-32B-Instruct",
        platform: str = "runpod",
        accelerators: List[str] = ["1:A100_SXM"],
        train_every: Optional[int] = None,
        sample_n: Optional[int] = None,
        sample_strategy: Optional[str] = None,
        num_epochs: Optional[int] = None,
        labels: Optional[Dict[str, str]] = None,
        config: Optional[GlobalConfig] = None,
        nebu_config: Optional[NebuGlobalConfig] = None,
        adapter: Optional[str] = None,
        no_delete: bool = False,
        hot_reload: bool = True,
        debug: bool = False,
    ):
        if model not in supported_models:
            raise ValueError(
                f"Model {model} is not supported, supported models are: {supported_models}"
            )

        server = QwenVLServer(
            platform=platform,
            accelerators=accelerators,
            model=model,
            namespace=namespace,
            config=nebu_config,
            hot_reload=hot_reload,
            debug=debug,
        )
        train_proc = UnslothSFT(
            platform=platform,
            accelerators=accelerators,
            namespace=namespace,
            config=nebu_config,
            hot_reload=hot_reload,
            debug=debug,
        )
        trainer = V1Trainer(
            model=model,
            processor=train_proc.ref(),
            adapter=adapter,
        )

        super().__init__(
            name=name,
            model=model,
            server=server.ref(),
            trainer=trainer,
            train_every=train_every,
            sample_n=sample_n,
            sample_strategy=sample_strategy,
            num_epochs=num_epochs,
            namespace=namespace,
            labels=labels,
            adapter=adapter,
            config=config,
            no_delete=no_delete,
        )
