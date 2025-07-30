import os
from typing import Dict, List, Optional

from nebu.containers.models import (
    V1ContainerRequest,
    V1EnvVar,
    V1Meter,
    V1ResourceMetaRequest,
    V1VolumeDriver,
    V1VolumePath,
)


class TRLRequest(V1ContainerRequest):
    """
    A wrapper class for creating TRL training jobs.
    """

    def __init__(
        self,
        name: str,
        model: str,
        platform: str,
        bucket: str,
        accelerators: List[str],
        namespace: Optional[str] = None,
        train_type: str = "sft",
        num_train_epochs: int = 1,
        save_steps: int = 1,
        save_total_limit: int = 3,
        save_strategy: str = "steps",
        dtype: str = "bfloat16",
        per_device_train_batch_size: int = 1,
        per_device_eval_batch_size: int = 1,
        output_dir: str = "/output",
        use_peft: bool = True,
        price_per_training_second: Optional[float] = None,
        max_seq_length: int = 2048,
        timeout: str = "2h",
        bucket_base_key: str = "trl",
        labels: Optional[Dict[str, str]] = None,
    ):
        """
        Initialize a TRL container request for transformer reinforcement learning.
        Inherits from V1ContainerRequest.

        Args:
            name: Name for the training job
            model: HuggingFace model ID to use
            platform: The compute platform to use
            bucket: S3 bucket for model storage
            accelerators: List of accelerators to use (e.g., ["A100"])
            namespace: Kubernetes namespace
            train_type: Type of training (e.g., "sft", "rl", "dpo")
            num_train_epochs: Number of training epochs
            save_steps: How often to save the model
            save_total_limit: Maximum number of checkpoints to keep
            save_strategy: When to save checkpoints
            dtype: Data type for training
            per_device_train_batch_size: Training batch size per device
            per_device_eval_batch_size: Evaluation batch size per device
            output_dir: Directory to save model outputs
            use_peft: Whether to use Parameter-Efficient Fine-Tuning
            price_per_training_second: Optional cost per training second
            max_seq_length: Maximum sequence length for training
            timeout: Timeout duration for the job
            bucket_base_key: Base key for S3 bucket path
            labels: Optional labels to add to resources
        """
        train_command = f"""
DATASET_PATH="{output_dir}/dataset.json"
echo "Downloading dataset to $DATASET_PATH"
wget "$DATASET_URI" -O "$DATASET_PATH"
source activate trl && trl {train_type} \
    --model_name_or_path $MODEL \
    --dataset_name $DATASET_PATH \
    --dataset_train_split "train" \
    --dataset_test_split "test" \
    --output_dir {output_dir} \
    --torch_dtype {dtype} \
    --max_seq_length {max_seq_length} \
    --per_device_train_batch_size {per_device_train_batch_size} \
    --per_device_eval_batch_size {per_device_eval_batch_size} \
    --use_peft {use_peft} \
    --save_strategy {save_strategy} \
    --save_steps {save_steps} \
    --save_total_limit {save_total_limit} \
    --num_train_epochs {num_train_epochs}
LATEST="$(ls -1d {output_dir}/checkpoint-* | sort -V | tail -n 1)"
rclone sync "$LATEST" "s3://{bucket}/{bucket_base_key}/{namespace}/{name}/latest"
        """

        train_meters = None
        if price_per_training_second:
            train_meters = [
                V1Meter(
                    cost=price_per_training_second,
                    unit="second",
                    metric="runtime",
                    currency="USD",
                )
            ]

        train_queue_name = f"trl-{name}"

        train_env = [
            V1EnvVar(key="MODEL", value=model),
        ]

        if os.getenv("HF_TOKEN"):
            train_env.append(V1EnvVar(key="HF_TOKEN", value=os.getenv("HF_TOKEN")))

        train_volumes = [
            V1VolumePath(
                source=f"{output_dir}",
                dest=f"s3://{bucket}/{bucket_base_key}/{namespace}/{name}/jobs/$NEBU_CONTAINER_ID",
                driver=V1VolumeDriver.RCLONE_SYNC,
                continuous=True,
            )
        ]

        # Initialize the parent V1ContainerRequest
        super().__init__(
            image="huggingface/trl-latest-gpu:latest",
            platform=platform,
            metadata=V1ResourceMetaRequest(
                name=name,
                namespace=namespace,
                labels=labels,
            ),
            command=train_command,
            accelerators=accelerators,
            env=train_env,
            volumes=train_volumes,
            meters=train_meters,
            restart="Never",
            queue=train_queue_name,
            timeout=timeout,
        )
