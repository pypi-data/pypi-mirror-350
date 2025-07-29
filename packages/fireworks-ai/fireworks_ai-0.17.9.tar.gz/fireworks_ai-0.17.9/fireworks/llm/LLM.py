from collections import defaultdict, deque
from datetime import timedelta
import inspect
import re
import os
import sys
import time

import grpc
from ._list_fireworks_models_response_cached import models
from fireworks.client.error import RateLimitError
from fireworks.client.api_client import FireworksClient
from fireworks.client.chat import Chat as FireworksChat
from fireworks.client.chat_completion import ChatCompletionV2 as FireworksChatCompletion
from asyncstdlib.functools import cache
from functools import cache as sync_cache
from google.protobuf.field_mask_pb2 import FieldMask as SyncFieldMask
from typing import (
    AsyncGenerator,
    Generator,
    Iterable,
    List,
    Literal,
    Optional,
    Union,
    overload,
)
from fireworks.client.error import BadGatewayError, ServiceUnavailableError
from fireworks.dataset import Dataset
from fireworks.supervised_fine_tuning_job import SupervisedFineTuningJob
from fireworks.gateway import Gateway
from google.protobuf.duration_pb2 import Duration
from fireworks.control_plane.generated.protos_grpcio.gateway.deployment_pb2 import (
    ListDeploymentsRequest as SyncListDeploymentsRequest,
    UpdateDeploymentRequest as SyncUpdateDeploymentRequest,
    Deployment as SyncDeployment,
    AutoscalingPolicy as SyncAutoscalingPolicy,
    AcceleratorType as SyncAcceleratorType,
    Region as SyncRegion,
    DirectRouteType as SyncDirectRouteType,
    AutoTune as SyncAutoTune,
)
from fireworks.control_plane.generated.protos.gateway import (
    AcceleratorType as AcceleratorTypeEnum,
    AutoTune,
    AutoscalingPolicy,
    CreateSupervisedFineTuningJobRequest,
    DeployedModelState,
    Deployment,
    DeploymentPrecision,
    DeploymentState,
    DirectRouteType,
    JobState,
    ListSupervisedFineTuningJobsRequest,
    Model,
    Region,
    SupervisedFineTuningJobWeightPrecision,
    WandbConfig,
)
from fireworks.supervised_fine_tuning_job.SupervisedFineTuningJob import SupervisedFineTuningJobWeightPrecisionLiteral
import asyncio
import logging
import atexit
from openai.types.chat.chat_completion import ChatCompletion as OpenAIChatCompletion
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from openai.types.chat.completion_create_params import ResponseFormat
from openai import NOT_GIVEN, NotGiven
from fireworks._util import is_valid_resource_name
import sysconfig
from fireworks._literals import (
    DeploymentStrategyLiteral,
    DeploymentTypeLiteral,
    RegionLiteral,
    AcceleratorTypeLiteral,
    ReasoningEffort,
)

# Configure logger with a consistent format for better debugging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.propagate = False  # Prevent duplicate logs

if os.environ.get("FIREWORKS_SDK_DEBUG"):
    logger.setLevel(logging.DEBUG)

DEFAULT_MAX_RETRIES = 5
DEFAULT_DELAY = 0.5


class ChatCompletion:
    def __init__(self, llm: "LLM"):
        self._client = FireworksChatCompletion(llm._client)
        self._llm = llm

    def _create_setup(self):
        """
        Setup for .create() and .acreate()
        """
        self._llm._ensure_deployment_ready()
        model_id = self._llm.model_id()
        return model_id

    @overload
    def create(
        self,
        messages: Iterable[ChatCompletionMessageParam],
        stream: Literal[False] = False,
        response_format: Optional[ResponseFormat] = None,
        reasoning_effort: Optional[ReasoningEffort] = None,
        max_tokens: Optional[int] = None,
        extra_headers=None,
        **kwargs,
    ) -> OpenAIChatCompletion:
        pass

    @overload
    def create(
        self,
        messages: Iterable[ChatCompletionMessageParam],
        stream: Literal[True] = True,
        response_format: Optional[ResponseFormat] = None,
        reasoning_effort: Optional[ReasoningEffort] = None,
        max_tokens: Optional[int] = None,
        extra_headers=None,
        **kwargs,
    ) -> Generator[ChatCompletionChunk, None, None]:
        pass

    def create(
        self,
        messages: Iterable[ChatCompletionMessageParam],
        stream: bool = False,
        response_format: Optional[ResponseFormat] = None,
        reasoning_effort: Optional[ReasoningEffort] = None,
        max_tokens: Optional[int] = None,
        extra_headers=None,
        **kwargs,
    ) -> Union[OpenAIChatCompletion, Generator[ChatCompletionChunk, None, None]]:
        model_id = self._create_setup()
        retries = 0
        delay = DEFAULT_DELAY
        while retries < self._llm.max_retries:
            try:
                if self._llm.enable_metrics:
                    start_time = time.time()
                result = self._client.create(
                    model=model_id,
                    prompt_or_messages=messages,
                    stream=stream,
                    extra_headers=extra_headers,
                    response_format=response_format,
                    reasoning_effort=reasoning_effort,
                    max_tokens=max_tokens,
                    **kwargs,
                )
                if self._llm.enable_metrics:
                    end_time = time.time()
                    self._llm._metrics.add_metric("time_to_last_token", end_time - start_time)
                return result
            except (BadGatewayError, ServiceUnavailableError, RateLimitError) as e:
                logger.debug(f"{type(e).__name__}: {e}. model_id: {model_id}")
                time.sleep(delay)
                retries += 1
                delay *= 2
        raise Exception(f"Failed to create chat completion after {self._llm.max_retries} retries")

    @overload
    async def acreate(
        self,
        messages: Iterable[ChatCompletionMessageParam],
        stream: Literal[False] = False,
        response_format: Optional[ResponseFormat] = None,
        reasoning_effort: Optional[ReasoningEffort] = None,
        max_tokens: Optional[int] = None,
        extra_headers=None,
        **kwargs,
    ) -> OpenAIChatCompletion: ...

    @overload
    async def acreate(
        self,
        messages: Iterable[ChatCompletionMessageParam],
        stream: Literal[True] = True,
        response_format: Optional[ResponseFormat] = None,
        reasoning_effort: Optional[ReasoningEffort] = None,
        max_tokens: Optional[int] = None,
        extra_headers=None,
        **kwargs,
    ) -> AsyncGenerator[ChatCompletionChunk, None]:
        pass

    async def acreate(
        self,
        messages: Iterable[ChatCompletionMessageParam],
        stream: bool = False,
        response_format: Optional[ResponseFormat] = None,
        reasoning_effort: Optional[ReasoningEffort] = None,
        max_tokens: Optional[int] = None,
        extra_headers=None,
        **kwargs,
    ) -> Union[OpenAIChatCompletion, AsyncGenerator[ChatCompletionChunk, None]]:
        model_id = self._create_setup()
        retries = 0
        delay = DEFAULT_DELAY
        while retries < self._llm.max_retries:
            try:
                resp_or_generator = self._client.acreate(  # type: ignore
                    model=model_id,
                    prompt_or_messages=messages,
                    stream=stream,
                    extra_headers=extra_headers,
                    response_format=response_format,
                    reasoning_effort=reasoning_effort,
                    max_tokens=max_tokens,
                    **kwargs,
                )
                if stream:
                    return resp_or_generator  # type: ignore
                else:
                    if self._llm.enable_metrics:
                        start_time = time.time()
                    resp = await resp_or_generator  # type: ignore
                    if self._llm.enable_metrics:
                        end_time = time.time()
                        self._llm._metrics.add_metric("time_to_last_token", end_time - start_time)
                    return resp
            except (BadGatewayError, ServiceUnavailableError, RateLimitError) as e:
                logger.debug(f"{type(e).__name__}: {e}. model_id: {model_id}")
                await asyncio.sleep(delay)
                retries += 1
                delay *= 2
        raise Exception(f"Failed to create chat completion after {self._llm.max_retries} retries")


class Chat:
    def __init__(self, llm: "LLM", model):
        self.completions = ChatCompletion(llm)


class Metrics:
    """
    A class for tracking and analyzing performance metrics for LLM operations.

    This class maintains a rolling window of metrics such as response times,
    token generation speeds, and other performance indicators. It provides
    statistical methods to analyze these metrics (mean, median, min, max).

    Each metric is stored as a list of values with a maximum size to prevent
    unbounded memory growth. When the maximum size is reached, the oldest
    values are removed in a FIFO manner.
    """

    def __init__(self, max_metrics: int = 1000):
        """
        Initialize the metrics tracker.

        Args:
            max_metrics: Maximum number of values to store for each metric.
                         Defaults to 1000. When exceeded, oldest values are removed.
        """
        self._metrics = defaultdict(deque)
        self._max_metrics = max_metrics

    def add_metric(self, metric_name: str, metric_value: float):
        """
        Add a new metric value to the specified metric.

        Args:
            metric_name: Name of the metric to track
            metric_value: Value to add to the metric
        """
        self._metrics[metric_name].append(metric_value)
        if len(self._metrics[metric_name]) > self._max_metrics:
            self._metrics[metric_name].popleft()

    def get_metric(self, metric_name: str):
        """
        Get all recorded values for a specific metric.

        Args:
            metric_name: Name of the metric to retrieve

        Returns:
            List of metric values or None if the metric doesn't exist
        """
        if metric_name not in self._metrics:
            return None
        return self._metrics[metric_name]

    def get_metric_mean(self, metric_name: str) -> Optional[float]:
        """
        Calculate the arithmetic mean of a metric's values.

        Args:
            metric_name: Name of the metric

        Returns:
            Mean value or None if the metric doesn't exist
        """
        if metric_name not in self._metrics:
            return None
        return sum(self._metrics[metric_name]) / len(self._metrics[metric_name])

    def get_metric_median(self, metric_name: str):
        """
        Calculate the median value of a metric.

        Args:
            metric_name: Name of the metric

        Returns:
            Median value or None if the metric doesn't exist
        """
        if metric_name not in self._metrics:
            return None
        return sorted(self._metrics[metric_name])[len(self._metrics[metric_name]) // 2]

    def get_metric_min(self, metric_name: str):
        """
        Get the minimum value recorded for a metric.

        Args:
            metric_name: Name of the metric

        Returns:
            Minimum value or None if the metric doesn't exist
        """
        if metric_name not in self._metrics:
            return None
        return min(self._metrics[metric_name])

    def get_metric_max(self, metric_name: str):
        """
        Get the maximum value recorded for a metric.

        Args:
            metric_name: Name of the metric

        Returns:
            Maximum value or None if the metric doesn't exist
        """
        if metric_name not in self._metrics:
            return None
        return max(self._metrics[metric_name])


class LLM:
    def __init__(
        self,
        model: str,
        deployment_type: DeploymentTypeLiteral,
        name: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: str = "https://api.fireworks.ai/inference/v1",
        accelerator_type: Union[AcceleratorTypeLiteral, NotGiven] = NOT_GIVEN,
        scale_up_window: timedelta = timedelta(seconds=1),
        scale_down_window: timedelta = timedelta(minutes=1),
        scale_to_zero_window: timedelta = timedelta(minutes=5),
        enable_metrics: bool = False,
        max_retries: int = DEFAULT_MAX_RETRIES,
        region: Optional[RegionLiteral] = None,
        description: Optional[str] = None,
        annotations: Optional[dict[str, str]] = None,
        min_replica_count: Optional[int] = None,
        max_replica_count: Optional[int] = None,
        replica_count: Optional[int] = None,
        accelerator_count: Optional[int] = None,
        precision: Optional[
            Literal[
                "FP16",
                "FP8",
                "FP8_MM",
                "FP8_AR",
                "FP8_MM_KV_ATTN",
                "FP8_KV",
                "FP8_MM_V2",
                "FP8_V2",
                "FP8_MM_KV_ATTN_V2",
                "NF4",
            ]
        ] = None,
        world_size: Optional[int] = None,
        generator_count: Optional[int] = None,
        disaggregated_prefill_count: Optional[int] = None,
        disaggregated_prefill_world_size: Optional[int] = None,
        max_batch_size: Optional[int] = None,
        cluster: Optional[str] = None,
        enable_addons: Optional[bool] = None,
        live_merge: Optional[bool] = None,
        draft_token_count: Optional[int] = None,
        draft_model: Optional[str] = None,
        ngram_speculation_length: Optional[int] = None,
        max_peft_batch_size: Optional[int] = None,
        kv_cache_memory_pct: Optional[int] = None,
        enable_session_affinity: Optional[bool] = None,
        direct_route_api_keys: Optional[list[str]] = None,
        num_peft_device_cached: Optional[int] = None,
        direct_route_type: Optional[Literal["INTERNET", "GCP_PRIVATE_SERVICE_CONNECT", "AWS_PRIVATELINK"]] = None,
        direct_route_handle: Optional[str] = None,
        long_prompt_optimized: Optional[bool] = None,
    ):
        """
        Initialize the LLM.

        Args:
            model: The model to use.
            deployment_type: The deployment type to use. Must be one of
                "serverless", "on-demand", or "auto". For experimentation on
                quality, we recommend using "auto" to default to the most
                cost-effective option. If you plan to run large evaluation jobs or
                have workloads that would benefit from dedicated resources, we
                recommend using "on-demand". Otherwise, you can enforce that you
                only use "serverless" by setting this parameter to "serverless".
            api_key: The API key to use.
            base_url: The base URL to use.
            accelerator_type: The accelerator type to use.
            scale_up_window: The scale up window to use.
            scale_down_window: The scale down window to use.
            scale_to_zero_window: The scale to zero window to use.
            enable_metrics: Whether to enable metrics. Only records time to last token for non-streaming requests.
                TODO: add support for streaming requests.
                TODO: add support for more metrics (TTFT, Tokens/second)
            max_retries: The maximum number of retries to use.
        """
        if not model:
            raise ValueError("model is required")
        if deployment_type is None:
            raise ValueError('deployment_type is required - must be one of "serverless", "on-demand", or "auto"')
        self._client = FireworksClient(api_key=api_key, base_url=base_url)
        if name is not None and name == "":
            raise ValueError("name must be non-empty")
        if name and not is_valid_resource_name(name):
            raise ValueError("LLM name must only contain lowercase a-z, 0-9, and hyphen (-)")
        self._name = name
        self._model = model
        self.chat = Chat(self, self.model)
        self.deployment_type: DeploymentTypeLiteral = deployment_type
        self.max_retries = max_retries
        self.enable_metrics = enable_metrics
        self._gateway = Gateway(api_key=api_key)
        self._metrics = Metrics()

        # This needs to be run in __init__ to ensure we capture deployment name
        # inside of this thread
        self._get_deployment_name()

        if isinstance(accelerator_type, str):
            self._accelerator_type = AcceleratorTypeEnum.from_string(accelerator_type)
            self._validate_model_for_gpu(self.model, self._accelerator_type)
            self._accelerator_type_sync: Union[NotGiven, SyncAcceleratorType] = getattr(
                SyncAcceleratorType, accelerator_type
            )
        else:
            self._accelerator_type = accelerator_type
            self._accelerator_type_sync = accelerator_type

        # aggressive defaults for experimentation to save on cost
        self._autoscaling_policy: AutoscalingPolicy = AutoscalingPolicy(
            scale_up_window=scale_up_window,
            scale_down_window=scale_down_window,
            scale_to_zero_window=scale_to_zero_window,
        )
        self._autoscaling_policy_sync = SyncAutoscalingPolicy(
            scale_up_window=Duration(seconds=int(scale_up_window.total_seconds())),
            scale_down_window=Duration(seconds=int(scale_down_window.total_seconds())),
            scale_to_zero_window=Duration(seconds=int(scale_to_zero_window.total_seconds())),
        )
        self._region = region
        self._description = description
        self._annotations = annotations
        self._min_replica_count = min_replica_count
        self._max_replica_count = max_replica_count
        self._replica_count = replica_count
        self._accelerator_count = accelerator_count
        self._precision = precision
        self._world_size = world_size
        self._generator_count = generator_count
        self._disaggregated_prefill_count = disaggregated_prefill_count
        self._disaggregated_prefill_world_size = disaggregated_prefill_world_size
        self._max_batch_size = max_batch_size
        self._cluster = cluster
        self._enable_addons = enable_addons
        self._live_merge = live_merge
        self._draft_token_count = draft_token_count
        self._draft_model = draft_model
        self._ngram_speculation_length = ngram_speculation_length
        self._max_peft_batch_size = max_peft_batch_size
        self._kv_cache_memory_pct = kv_cache_memory_pct
        self._enable_session_affinity = enable_session_affinity
        self._direct_route_api_keys = direct_route_api_keys
        self._num_peft_device_cached = num_peft_device_cached
        self._direct_route_type = direct_route_type
        self._direct_route_handle = direct_route_handle
        self._auto_tune = AutoTune()
        self._auto_tune_sync = SyncAutoTune()
        if long_prompt_optimized is not None:
            self._auto_tune.long_prompt_optimized = long_prompt_optimized
            self._auto_tune_sync.long_prompt = long_prompt_optimized

        if not self.is_available_on_serverless() and self.deployment_type == "serverless":
            raise ValueError(
                f"Model {self.model} is not available on serverless, but deployment_type is serverless, please use deployment_type='auto' or 'on-demand'"
            )

    @property
    def model(self):
        if not self._model.startswith("accounts/fireworks/models/") and "/" not in self._model:
            return f"accounts/fireworks/models/{self._model}"
        return self._model

    @staticmethod
    def _validate_model_for_gpu(model: str, accelerator_type: AcceleratorTypeEnum):
        """
        Models are not always supported on all GPU types. This function checks if the model is supported on a GPU.
        """
        if "qwen3-1p7b" in model:
            supported_accelerators = [
                AcceleratorTypeEnum.NVIDIA_H100_80GB,
                AcceleratorTypeEnum.NVIDIA_H200_141GB,
            ]
            if accelerator_type not in supported_accelerators:
                raise ValueError(
                    f"Qwen3-1p7b is not supported on {accelerator_type}. "
                    f"Please pass one of the following accelerators: {list(map(str, supported_accelerators))} "
                    f"to the LLM constructor using the accelerator_type parameter.\n\n"
                    f"Example:\n"
                    f"    from fireworks import LLM\n"
                    f"    llm = LLM(\n"
                    f'        model="qwen3-1p7b",\n'
                    f'        accelerator_type="NVIDIA_H100_80GB"\n'
                    f"    )"
                )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._gateway.__aexit__(exc_type, exc_val, exc_tb)

    @property
    def deployment_display_name(self) -> str:
        return self._get_deployment_name()

    @sync_cache
    def _get_deployment_name(self):
        """
        If a name was specified, deployment name will be the specified name.
        Otherwise, the deployment name will be generated from the filename of the caller where this LLM was instantiated.

        In Jupyter notebooks, we'll use the actual notebook filename rather than the temporary execution file.
        """
        if self._name is not None:
            return self._name

        # Check if running in a Jupyter notebook environment
        try:
            # Check for Jupyter environment via environment variable
            notebook_path = os.environ.get("JPY_SESSION_NAME")

            if notebook_path:
                logger.debug(f"Found notebook path from environment: {notebook_path}")
                notebook_filename = os.path.basename(notebook_path)
                logger.debug(f"Extracted notebook filename: {notebook_filename}")
                return notebook_filename
        except Exception as e:
            logger.debug(f"Error getting notebook name from environment: {str(e)}")
            pass

        # Get fireworks package path and Python stdlib path
        import fireworks

        package_path = os.path.dirname(fireworks.__file__)
        stdlib_path = sysconfig.get_path("stdlib")

        stack = inspect.stack()
        for frame_info in stack:
            filename = frame_info.filename
            # Skip frames from our package, Python stdlib, other libraries, and internal Python
            if (
                not filename.startswith(package_path)
                and not filename.startswith(stdlib_path)
                and not "/site-packages/" in filename
                and not filename.startswith("<")
            ):
                logger.debug(f"Found caller outside of library code to generate name: {filename}")
                return os.path.basename(filename)
        raise ValueError("No caller found outside of library code")

    def apply(self):
        """
        Like Terraform apply, this will ensure the deployment is ready and return the deployment.
        """
        self._ensure_deployment_ready()
        return self

    def get_time_to_last_token_mean(self) -> Optional[float]:
        """
        Returns the mean time to last token for non-streaming requests. If no metrics are available, returns None.
        """
        if not self.enable_metrics:
            raise ValueError("Metrics are not enabled for this LLM")
        return self._metrics.get_metric_mean("time_to_last_token")

    def is_available_on_serverless(self):
        """
        Checks if the model is available on serverless.
        """
        return self._is_available_on_serverless()

    def deployment_strategy(self) -> DeploymentStrategyLiteral:
        return self._deployment_strategy()

    def delete(self, ignore_checks: bool = False):
        deployment = self.get_deployment()
        if deployment is None:
            logger.debug("No deployment found to delete")
            return
        logger.debug(f"Deleting deployment {deployment.name}")
        self._gateway.delete_deployment_sync(deployment.name, ignore_checks)
        # spin until deployment is deleted
        start_time = time.time()
        while deployment is not None:
            current_time = time.time()
            if current_time - start_time >= 10:
                logger.debug(f"Waiting for deployment {deployment.name} to be deleted...")
                start_time = current_time
            deployment = self.get_deployment()
            time.sleep(1)

    @sync_cache
    def _deployment_strategy(self) -> DeploymentStrategyLiteral:
        """
        Determines whether to use serverless or dedicated deployment based on model availability
        and configured deployment type.

        Returns:
            bool: True if a dedicated deployment is needed, False if serverless can be used.
        """
        if self.is_available_on_serverless():
            if self.deployment_type == "serverless" or self.deployment_type == "auto":
                logger.debug(f"Model {self.model} is available on serverless, using serverless deployment")
                return "serverless"
            else:
                logger.debug(
                    f"Model {self.model} is available on serverless, but deployment_type is on-demand, continuing to ensure deployment is ready"
                )
                return "on-demand"
        else:
            logger.debug(
                f"Model {self.model} is not available on serverless, continuing to check for existing deployment"
            )
            return "on-demand"

    @sync_cache
    def _is_available_on_serverless(self):
        logger.debug(f"Checking if {self.model} is available on serverless")
        models = self._list_fireworks_models()

        # find model in models
        model = next((m for m in models if m.name == self.model), None)
        if model is None:
            return False
        logger.debug(f"Found model {self.model} on under fireworks account")
        is_serverless = self._is_model_on_serverless_account(model)
        logger.debug(f"Model {self.model} is {'serverless' if is_serverless else 'not serverless'}")
        return is_serverless

    def _list_fireworks_models(self) -> List[Model]:
        """
        Find all models on the fireworks account
        """
        # models = await self._gateway.list_models(parent="accounts/fireworks", include_deployed_model_refs=True)
        return models

    @staticmethod
    def _is_model_on_serverless_account(model: Model) -> bool:
        """
        Check if the model is deployed on a serverless-enabled account.

        Args:
            model: The model object to check

        Returns:
            bool: True if the model is deployed on a supported serverless account, False otherwise
        """
        if model.deployed_model_refs:
            for ref in model.deployed_model_refs:
                if (
                    hasattr(ref, "state")
                    and (ref.state == DeployedModelState.DEPLOYED or ref.state == "DEPLOYED")
                    and hasattr(ref, "deployment")
                    and ref.deployment
                ):
                    # Check if deployment is on a supported account
                    if (
                        ref.deployment.startswith("accounts/fireworks/")
                        or ref.deployment.startswith("accounts/yi-01-ai/")
                        or ref.deployment.startswith("accounts/sentientfoundation/")
                    ):
                        return True
        return False

    def _query_existing_deployment(self) -> Optional[SyncDeployment]:
        """
        Queries all deployments for the same model and accelerator type (if given) and returns the first one.
        """
        deployments = self._gateway.list_deployments_sync(
            filter=f'display_name="{self.deployment_display_name}" AND base_model="{self.model}"'
        )
        deployment = next(iter(deployments), None)
        return deployment

    def _ensure_deployment_ready(self) -> None:
        """
        If a deployment is inferred for this LLM, ensure it's deployed and
        ready. A deployment is required if the model is not available on
        serverless or this LLM has deployment_type="on-demand".

        This method uses a lock to prevent concurrent calls from multiple coroutines.
        """
        deployment_strategy = self.deployment_strategy()
        if deployment_strategy == "serverless":
            return

        deployment = self._query_existing_deployment()

        if deployment is None:
            logger.debug(f"No existing deployment found, creating deployment for {self.model}")
            deployment_proto = SyncDeployment(
                display_name=self.deployment_display_name,
                base_model=self.model,
                autoscaling_policy=self._autoscaling_policy_sync,
            )
            if not isinstance(self._accelerator_type_sync, NotGiven):
                deployment_proto.accelerator_type = self._accelerator_type_sync
            if self._accelerator_count is not None:
                deployment_proto.accelerator_count = self._accelerator_count
            if self._precision is not None:
                deployment_proto.precision = getattr(SyncDeployment.Precision, self._precision)
            if self._world_size is not None:
                deployment_proto.world_size = self._world_size
            if self._generator_count is not None:
                deployment_proto.generator_count = self._generator_count
            if self._region is not None:
                deployment_proto.region = getattr(SyncRegion, self._region)
            if self._description is not None:
                deployment_proto.description = self._description
            if self._annotations is not None:
                deployment_proto.annotations.update(self._annotations)
            if self._min_replica_count is not None:
                deployment_proto.min_replica_count = self._min_replica_count
            if self._max_replica_count is not None:
                deployment_proto.max_replica_count = self._max_replica_count
            if self._replica_count is not None:
                deployment_proto.replica_count = self._replica_count
            if self._disaggregated_prefill_count is not None:
                deployment_proto.disaggregated_prefill_count = self._disaggregated_prefill_count
            if self._disaggregated_prefill_world_size is not None:
                deployment_proto.disaggregated_prefill_world_size = self._disaggregated_prefill_world_size
            if self._max_batch_size is not None:
                deployment_proto.max_batch_size = self._max_batch_size
            if self._cluster is not None:
                deployment_proto.cluster = self._cluster
            if self._enable_addons is not None:
                deployment_proto.enable_addons = self._enable_addons
            if self._live_merge is not None:
                deployment_proto.live_merge = self._live_merge
            if self._draft_token_count is not None:
                deployment_proto.draft_token_count = self._draft_token_count
            if self._draft_model is not None:
                deployment_proto.draft_model = self._draft_model
            if self._ngram_speculation_length is not None:
                deployment_proto.ngram_speculation_length = self._ngram_speculation_length
            if self._max_peft_batch_size is not None:
                deployment_proto.max_peft_batch_size = self._max_peft_batch_size
            if self._kv_cache_memory_pct is not None:
                deployment_proto.kv_cache_memory_pct = self._kv_cache_memory_pct
            if self._enable_session_affinity is not None:
                deployment_proto.enable_session_affinity = self._enable_session_affinity
            if self._direct_route_api_keys is not None:
                deployment_proto.direct_route_api_keys.extend(self._direct_route_api_keys)
            if self._num_peft_device_cached is not None:
                deployment_proto.num_peft_device_cached = self._num_peft_device_cached
            if self._direct_route_type is not None:
                deployment_proto.direct_route_type = getattr(SyncDirectRouteType, self._direct_route_type)
            if self._direct_route_handle is not None:
                deployment_proto.direct_route_handle = self._direct_route_handle
            if self._auto_tune_sync.long_prompt:
                deployment_proto.auto_tune.long_prompt = self._auto_tune_sync.long_prompt
            created_deployment = self._gateway.create_deployment_sync(deployment_proto)
            logger.debug(f"Deployment {created_deployment.name} created, waiting for it to be ready")

            # poll deployment status until it's ready
            start_time = time.time()
            last_log_time = 0
            while created_deployment.state != DeploymentState.READY:
                current_time = time.time()
                # wait for 9 seconds
                time.sleep(9)
                created_deployment = self._gateway.get_deployment_sync(created_deployment.name)
                if current_time - last_log_time >= 10:
                    elapsed_so_far = current_time - start_time
                    logger.debug(
                        f"Waiting for deployment {created_deployment.name} to be ready, current state: {created_deployment.state}, elapsed time: {elapsed_so_far:.2f}s"
                    )
                    last_log_time = current_time

            total_time = time.time() - start_time
            logger.debug(
                f"Deployment {created_deployment.name} state is READY, checking replicas now (Became READY in {total_time:.2f} seconds)"
            )
        else:
            logger.debug(f"Deployment {deployment.name} already exists, checking if it needs to be scaled up")

            field_mask = SyncFieldMask()

            # if autoscaling policy is not equal, update it
            if not self._is_autoscaling_policy_equal(deployment):
                logger.debug(
                    f"Updating autoscaling policy for {deployment.name} to "
                    f"{self._autoscaling_policy.scale_up_window.total_seconds()}s up, "
                    f"{self._autoscaling_policy.scale_down_window.total_seconds()}s down, "
                    f"{self._autoscaling_policy.scale_to_zero_window.total_seconds()}s to zero"
                )
                deployment.autoscaling_policy.scale_up_window = self._autoscaling_policy.scale_up_window  # type: ignore
                deployment.autoscaling_policy.scale_down_window = self._autoscaling_policy.scale_down_window  # type: ignore
                deployment.autoscaling_policy.scale_to_zero_window = self._autoscaling_policy.scale_to_zero_window  # type: ignore
                field_mask.paths.append("autoscaling_policy")

            if self._min_replica_count is not None and deployment.min_replica_count != self._min_replica_count:
                logger.debug(f"Updating min_replica_count for {deployment.name} to {self._min_replica_count}")
                deployment.min_replica_count = self._min_replica_count
                field_mask.paths.append("min_replica_count")

            if deployment.accelerator_type != self._accelerator_type and self._accelerator_type is not NOT_GIVEN:
                raise ValueError(
                    f'Deployment with name "{deployment.name}" has accelerator type {deployment.accelerator_type}, ',
                    f"but the LLM has accelerator type {self._accelerator_type}. You must specify a different name ",
                    f"for this LLM to use a different accelerator type since it is not possible to change the accelerator ",
                    f"type of an existing deployment.",
                )

            if len(field_mask.paths) > 0:
                logger.debug(f"Updating deployment {deployment.name} with {field_mask}")
                start_time = time.time()
                self._gateway.update_deployment_sync(deployment, field_mask)

                # poll until deployment is ready
                while deployment.state != DeploymentState.READY:
                    time.sleep(1)
                    deployment = self._gateway.get_deployment_sync(deployment.name)

                elapsed_time = time.time() - start_time
                logger.debug(f"Deployment update completed in {elapsed_time:.2f} seconds")

            if deployment.replica_count == 0:
                logger.debug(f"Deployment {deployment.name} is not ready, scaling to 1 replica")
                start_time = time.time()
                self._gateway.scale_deployment_sync(deployment.name, 1)

                # Poll until deployment has at least one replica
                last_log_time = 0
                while deployment.replica_count == 0:
                    current_time = time.time()
                    time.sleep(1)
                    deployment = self._gateway.get_deployment_sync(deployment.name)
                    if current_time - last_log_time >= 10:
                        elapsed_so_far = current_time - start_time
                        logger.debug(
                            f"Waiting for deployment {deployment.name} to scale up, current replicas: {deployment.replica_count}, elapsed time: {elapsed_so_far:.2f}s"
                        )
                        last_log_time = current_time

                total_scale_time = time.time() - start_time
                logger.debug(f"Deployment {deployment.name} scaled up in {total_scale_time:.2f} seconds")
            logger.debug(f"Deployment {deployment.name} is ready, using deployment")

    def scale_to_zero(self) -> Optional[SyncDeployment]:
        """
        Sends a request to scale the deployment to 0 replicas but does not wait for it to complete.
        """
        deployment = self.get_deployment()
        if deployment is None:
            return None
        self._gateway.scale_deployment_sync(deployment.name, 0)
        return deployment

    def scale_to_1_replica(self):
        """
        Scales the deployment to at least 1 replica.
        """
        deployment = self.get_deployment()
        if deployment is None:
            return
        self._gateway.scale_deployment_sync(deployment.name, 1)

    def _is_autoscaling_policy_equal(self, deployment: Union[Deployment, SyncDeployment]) -> bool:
        if isinstance(deployment, SyncDeployment):
            return (
                deployment.autoscaling_policy.scale_up_window == self._autoscaling_policy_sync.scale_up_window
                and deployment.autoscaling_policy.scale_down_window == self._autoscaling_policy_sync.scale_down_window
                and deployment.autoscaling_policy.scale_to_zero_window
                == self._autoscaling_policy_sync.scale_to_zero_window
            )
        return (
            deployment.autoscaling_policy.scale_up_window == self._autoscaling_policy.scale_up_window
            and deployment.autoscaling_policy.scale_down_window == self._autoscaling_policy.scale_down_window
            and deployment.autoscaling_policy.scale_to_zero_window == self._autoscaling_policy.scale_to_zero_window
        )

    def get_deployment(self) -> Optional[SyncDeployment]:
        return self._query_existing_deployment()

    def model_id(self):
        """
        Returns the model ID, which is the model name plus the deployment name
        if it exists. This is used for the "model" arg when calling the model.
        """
        if self.is_available_on_serverless():
            return self.model
        deployment = self.get_deployment()
        if deployment is None:
            if self.deployment_strategy() == "on-demand":
                raise ValueError(
                    f"Model {self.model} is not available on serverless and no deployment exists. Make sure to call apply() before calling model_id() or call the model to trigger a deployment."
                )
            else:
                return self.model
        return f"{self.model}#{deployment.name}"

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"LLM(model={self.model})"

    def fine_tune(
        self,
        name: str,
        dataset_or_id: Union[Dataset, str],
        epochs: Optional[int] = None,
        learning_rate: Optional[float] = None,
        lora_rank: Optional[int] = None,
        jinja_template: Optional[str] = None,
        early_stop: Optional[bool] = None,
        max_context_length: Optional[int] = None,
        base_model_weight_precision: Optional[SupervisedFineTuningJobWeightPrecisionLiteral] = None,
        wandb_config: Optional[WandbConfig] = None,
        evaluation_dataset: Optional[str] = None,
        accelerator_type: Optional[AcceleratorTypeLiteral] = None,
        accelerator_count: Optional[int] = None,
        is_turbo: Optional[bool] = None,
        eval_auto_carveout: Optional[bool] = None,
        region: Optional[RegionLiteral] = None,
        nodes: Optional[int] = None,
        batch_size: Optional[int] = None,
        output_model: Optional[str] = None,
    ):
        """
        Creates a fine-tuning job for this dataset. If the fine-tuning job already exists, it will block until the job is ready.

        Args:
            dataset_or_id: The dataset instance to fine-tune on or the dataset id to fine-tune on.
            output_model_name: The name of the output model.
            epochs: The number of epochs to fine-tune for.
            learning_rate: The learning rate to use for fine-tuning.
        """
        if name is None:
            raise ValueError("name is required")
        if not is_valid_resource_name(name):
            raise ValueError("job name must only contain lowercase a-z, 0-9, and hyphen (-)")
        job = SupervisedFineTuningJob(
            name=name,
            dataset_or_id=dataset_or_id,
            llm=self,
            epochs=epochs,
            learning_rate=learning_rate,
            lora_rank=lora_rank,
            jinja_template=jinja_template,
            output_model=output_model,
            early_stop=early_stop,
            max_context_length=max_context_length,
            base_model_weight_precision=base_model_weight_precision,
            wandb_config=wandb_config,
            evaluation_dataset=evaluation_dataset,
            accelerator_type=accelerator_type,
            accelerator_count=accelerator_count,
            is_turbo=is_turbo,
            eval_auto_carveout=eval_auto_carveout,
            region=region,
            nodes=nodes,
            batch_size=batch_size,
        )
        job = job.sync()
        if job.id is not None:
            logger.info(f'Synced fine-tuning job "{name}". See https://fireworks.ai/dashboard/fine-tuning/{job.id}.')
        else:
            logger.info(f'Synced fine-tuning job "{name}".')
        # poll until job is COMPLETED
        while job.state != JobState.COMPLETED:
            if job.state == JobState.FAILED:
                raise ValueError(f'Fine-tuning job "{name}" failed')
            if job.create_time is not None:
                curr_time = time.time()
                create_time = job.create_time.timestamp()
                delta_seconds = int(curr_time - create_time)
                minutes = delta_seconds // 60
                seconds = delta_seconds % 60
                time_str = f"{seconds}s" if minutes == 0 else f"{minutes}m{seconds}s"
                logger.info(f'Fine-tuning job "{name}" is in state {job.state}. Job was created {time_str} ago.')
            time.sleep(5)
            job = job.get()
            if job is None:
                raise ValueError(f'Fine-tuning job "{name}" not found')
        logger.info(f'Fine-tuning job "{name}" completed')
        if job.output_model is None:
            raise ValueError(f'Fine-tuning job "{name}" did not create an output model')
        return LLM(model=job.output_model, deployment_type=self.deployment_type)
