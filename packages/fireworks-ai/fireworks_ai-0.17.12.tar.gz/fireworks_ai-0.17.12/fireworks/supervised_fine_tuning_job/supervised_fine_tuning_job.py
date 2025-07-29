import asyncio
from datetime import datetime
import time
from typing import Literal, Optional, Union, TYPE_CHECKING
from fireworks.gateway import Gateway
from fireworks.dataset import Dataset
from fireworks.control_plane.generated.protos.gateway import (
    CreateSupervisedFineTuningJobRequest,
    JobState,
    Region,
    SupervisedFineTuningJob as SupervisedFineTuningJobProto,
    ListSupervisedFineTuningJobsRequest,
    SupervisedFineTuningJobWeightPrecision,
    WandbConfig,
    AcceleratorType as AcceleratorTypeEnum,
)
from google.protobuf.timestamp_pb2 import Timestamp as TimestampProto
from fireworks.control_plane.generated.protos_grpcio.gateway.supervised_fine_tuning_job_pb2 import (
    ListSupervisedFineTuningJobsRequest as SyncListSupervisedFineTuningJobsRequest,
    CreateSupervisedFineTuningJobRequest as SyncCreateSupervisedFineTuningJobRequest,
    SupervisedFineTuningJob as SyncSupervisedFineTuningJob,
)
from fireworks.control_plane.generated.protos_grpcio.gateway.status_pb2 import (
    JobState as SyncJobState,
)
from fireworks.control_plane.generated.protos_grpcio.gateway.wandb_pb2 import (
    WandbConfig as SyncWandbConfig,
)
from fireworks.control_plane.generated.protos_grpcio.gateway.deployment_pb2 import (
    AcceleratorType as SyncAcceleratorType,
    Region as SyncRegion,
)

from fireworks._logger import logger
from fireworks._literals import RegionLiteral, AcceleratorTypeLiteral

# Type checking imports to avoid circular imports
if TYPE_CHECKING:
    from fireworks.llm.llm import LLM


def wandb_config_proto_to_dataclass(wandb_config: SyncWandbConfig) -> WandbConfig:
    return WandbConfig(
        enabled=wandb_config.enabled,
        api_key=wandb_config.api_key,
        project=wandb_config.project,
        entity=wandb_config.entity,
        run_id=wandb_config.run_id,
    )


def timestamp_proto_to_datetime(timestamp: TimestampProto) -> datetime:
    dt = datetime.fromtimestamp(timestamp.seconds + timestamp.nanos / 1e9)
    return dt


def region_proto_to_literal(region: SyncRegion) -> RegionLiteral:
    if region == SyncRegion.REGION_UNSPECIFIED:
        return "REGION_UNSPECIFIED"
    elif region == SyncRegion.US_IOWA_1:
        return "US_IOWA_1"
    elif region == SyncRegion.US_VIRGINIA_1:
        return "US_VIRGINIA_1"
    elif region == SyncRegion.US_VIRGINIA_2:
        return "US_VIRGINIA_2"
    elif region == SyncRegion.US_ILLINOIS_1:
        return "US_ILLINOIS_1"
    elif region == SyncRegion.AP_TOKYO_1:
        return "AP_TOKYO_1"
    elif region == SyncRegion.EU_LONDON_1:
        return "EU_LONDON_1"
    elif region == SyncRegion.US_ARIZONA_1:
        return "US_ARIZONA_1"
    elif region == SyncRegion.US_TEXAS_1:
        return "US_TEXAS_1"
    elif region == SyncRegion.US_ILLINOIS_2:
        return "US_ILLINOIS_2"
    elif region == SyncRegion.EU_FRANKFURT_1:
        return "EU_FRANKFURT_1"
    elif region == SyncRegion.US_TEXAS_2:
        return "US_TEXAS_2"
    elif region == SyncRegion.EU_PARIS_1:
        return "EU_PARIS_1"
    elif region == SyncRegion.EU_HELSINKI_1:
        return "EU_HELSINKI_1"
    elif region == SyncRegion.US_NEVADA_1:
        return "US_NEVADA_1"
    elif region == SyncRegion.EU_ICELAND_1:
        return "EU_ICELAND_1"
    elif region == SyncRegion.EU_ICELAND_2:
        return "EU_ICELAND_2"
    elif region == SyncRegion.US_WASHINGTON_1:
        return "US_WASHINGTON_1"
    elif region == SyncRegion.US_WASHINGTON_2:
        return "US_WASHINGTON_2"
    raise ValueError(f"Unknown region: {region}")


SupervisedFineTuningJobWeightPrecisionLiteral = Literal["WEIGHT_PRECISION_UNSPECIFIED", "BFLOAT16", "INT8", "NF4"]


def accelerator_type_proto_to_literal(
    accelerator_type: SyncAcceleratorType,
) -> AcceleratorTypeLiteral:
    if accelerator_type == SyncAcceleratorType.ACCELERATOR_TYPE_UNSPECIFIED:
        return "ACCELERATOR_TYPE_UNSPECIFIED"
    elif accelerator_type == SyncAcceleratorType.NVIDIA_A100_80GB:
        return "NVIDIA_A100_80GB"
    elif accelerator_type == SyncAcceleratorType.NVIDIA_H100_80GB:
        return "NVIDIA_H100_80GB"
    elif accelerator_type == SyncAcceleratorType.AMD_MI300X_192GB:
        return "AMD_MI300X_192GB"
    elif accelerator_type == SyncAcceleratorType.NVIDIA_A10G_24GB:
        return "NVIDIA_A10G_24GB"
    elif accelerator_type == SyncAcceleratorType.NVIDIA_A100_40GB:
        return "NVIDIA_A100_40GB"
    elif accelerator_type == SyncAcceleratorType.NVIDIA_L4_24GB:
        return "NVIDIA_L4_24GB"
    elif accelerator_type == SyncAcceleratorType.NVIDIA_H200_141GB:
        return "NVIDIA_H200_141GB"
    elif accelerator_type == SyncAcceleratorType.NVIDIA_B200_180GB:
        return "NVIDIA_B200_180GB"
    raise ValueError(f"Unknown accelerator type: {accelerator_type}")


def precision_proto_to_literal(
    precision: SyncSupervisedFineTuningJob.WeightPrecision,
) -> SupervisedFineTuningJobWeightPrecisionLiteral:
    if precision == SyncSupervisedFineTuningJob.WeightPrecision.WEIGHT_PRECISION_UNSPECIFIED:
        return "WEIGHT_PRECISION_UNSPECIFIED"
    elif precision == SyncSupervisedFineTuningJob.WeightPrecision.BFLOAT16:
        return "BFLOAT16"
    elif precision == SyncSupervisedFineTuningJob.WeightPrecision.INT8:
        return "INT8"
    elif precision == SupervisedFineTuningJobWeightPrecision.NF4:
        return "NF4"
    raise ValueError(f"Unknown precision: {precision}")


JobStateLiteral = Literal[
    "UNSPECIFIED",
    "CREATING",
    "RUNNING",
    "COMPLETED",
    "FAILED",
    "CANCELLED",
    "DELETING",
    "WRITING_RESULTS",
    "VALIDATING",
    "ROLLOUT",
    "EVALUATION",
    "FAILED_CLEANING_UP",
    "DELETING_CLEANING_UP",
    "POLICY_UPDATE",
]


def job_state_proto_to_literal(state: SyncJobState) -> JobStateLiteral:
    if state == SyncJobState.JOB_STATE_UNSPECIFIED:
        return "UNSPECIFIED"
    elif state == SyncJobState.JOB_STATE_CREATING:
        return "CREATING"
    elif state == SyncJobState.JOB_STATE_RUNNING:
        return "RUNNING"
    elif state == SyncJobState.JOB_STATE_COMPLETED:
        return "COMPLETED"
    elif state == SyncJobState.JOB_STATE_FAILED:
        return "FAILED"
    elif state == SyncJobState.JOB_STATE_CANCELLED:
        return "CANCELLED"
    elif state == SyncJobState.JOB_STATE_DELETING:
        return "DELETING"
    elif state == SyncJobState.JOB_STATE_WRITING_RESULTS:
        return "WRITING_RESULTS"
    elif state == SyncJobState.JOB_STATE_VALIDATING:
        return "VALIDATING"
    elif state == SyncJobState.JOB_STATE_ROLLOUT:
        return "ROLLOUT"
    elif state == SyncJobState.JOB_STATE_EVALUATION:
        return "EVALUATION"
    elif state == SyncJobState.JOB_STATE_FAILED_CLEANING_UP:
        return "FAILED_CLEANING_UP"
    elif state == SyncJobState.JOB_STATE_DELETING_CLEANING_UP:
        return "DELETING_CLEANING_UP"
    elif state == SyncJobState.JOB_STATE_POLICY_UPDATE:
        return "POLICY_UPDATE"
    raise ValueError(f"Unknown job state: {state}")


class SupervisedFineTuningJob:
    """
    Wrapper around proto for a supervised fine-tuning job in Fireworks. Can be
    constructed from a name, LLM, and dataset. Can be used to sync the job state
    to Fireworks and query the current state.
    """

    def __init__(
        self,
        name: str,
        llm: "LLM",
        dataset_or_id: Union[Dataset, str],
        id: Optional[str] = None,
        api_key: Optional[str] = None,
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
        state: Optional[JobStateLiteral] = None,
        create_time: Optional[datetime] = None,
        update_time: Optional[datetime] = None,
        created_by: Optional[str] = None,
        output_model: Optional[str] = None,
    ):
        self.id = id
        self.name = name
        self.llm = llm
        self.epochs = epochs
        self.learning_rate = learning_rate
        self.lora_rank = lora_rank
        self.jinja_template = jinja_template
        self.early_stop = early_stop
        self.max_context_length = max_context_length
        self.base_model_weight_precision = None
        if base_model_weight_precision is not None:
            self.base_model_weight_precision = getattr(
                SupervisedFineTuningJobWeightPrecision,
                base_model_weight_precision,
            )
        self.wandb_config = wandb_config
        self.evaluation_dataset = evaluation_dataset
        self.accelerator_type = None
        if accelerator_type is not None:
            self.accelerator_type = getattr(SyncAcceleratorType, accelerator_type)
        self.accelerator_count = accelerator_count
        self.is_turbo = is_turbo
        self.eval_auto_carveout = eval_auto_carveout
        self.region = None
        if region is not None:
            self.region = getattr(SyncRegion, region)
        self.nodes = nodes
        self.batch_size = batch_size
        self.state = None
        if state is not None:
            self.state = JobState.from_string(state)
        self.create_time = create_time
        self.update_time = update_time
        self.created_by = created_by
        self.output_model = output_model
        self._api_key = api_key
        self._gateway = Gateway(api_key=api_key)
        account = self._gateway.account_id()
        self.dataset_or_id = (
            dataset_or_id if isinstance(dataset_or_id, Dataset) else Dataset.construct_id(account, dataset_or_id)
        )

    @classmethod
    async def delete_by_name(cls, name: str, api_key: Optional[str] = None):
        gateway = Gateway(api_key=api_key)
        await gateway.delete_supervised_fine_tuning_job(name)
        job = await gateway.get_supervised_fine_tuning_job(name)
        while job is not None:
            await asyncio.sleep(1)

    async def delete(self):
        await self.delete_by_name(self.name, self._api_key)

    def sync(self) -> "SupervisedFineTuningJob":
        """
        Creates the job if it doesn't exist, otherwise returns the existing job.
        """
        if isinstance(self.dataset_or_id, Dataset):
            self.dataset_or_id.sync()
        existing_job = self.get()
        if existing_job is not None:
            return existing_job
        request = self._create_request()
        self._gateway.create_supervised_fine_tuning_job_sync(request)
        new_job = self.get()
        if new_job is None:
            raise ValueError(f"Failed to create supervised fine-tuning job {self.name}")
        return new_job

    def _create_request(self) -> SyncCreateSupervisedFineTuningJobRequest:
        dataset_id = self.dataset_or_id.id() if isinstance(self.dataset_or_id, Dataset) else self.dataset_or_id
        job_proto = SyncSupervisedFineTuningJob(
            display_name=self.name,
            base_model=self.llm.model,
            dataset=dataset_id,
        )
        if self.epochs is not None:
            job_proto.epochs = self.epochs
        if self.learning_rate is not None:
            job_proto.learning_rate = self.learning_rate
        if self.lora_rank is not None:
            job_proto.lora_rank = self.lora_rank
        if self.jinja_template is not None:
            job_proto.jinja_template = self.jinja_template
        if self.early_stop is not None:
            job_proto.early_stop = self.early_stop
        if self.max_context_length is not None:
            job_proto.max_context_length = self.max_context_length
        if self.base_model_weight_precision is not None:
            job_proto.base_model_weight_precision = self.base_model_weight_precision
        if self.wandb_config is not None:
            job_proto.wandb_config = SyncWandbConfig(
                enabled=self.wandb_config.enabled,
                api_key=self.wandb_config.api_key,
                project=self.wandb_config.project,
                entity=self.wandb_config.entity,
                run_id=self.wandb_config.run_id,
            )
        if self.evaluation_dataset is not None:
            job_proto.evaluation_dataset = self.evaluation_dataset
        if self.accelerator_type is not None:
            job_proto.accelerator_type = self.accelerator_type
        if self.accelerator_count is not None:
            job_proto.accelerator_count = self.accelerator_count
        if self.is_turbo is not None:
            job_proto.is_turbo = self.is_turbo
        if self.eval_auto_carveout is not None:
            job_proto.eval_auto_carveout = self.eval_auto_carveout
        if self.region is not None:
            job_proto.region = self.region
        if self.nodes is not None:
            job_proto.nodes = self.nodes
        if self.batch_size is not None:
            job_proto.batch_size = self.batch_size
        if self.output_model is not None:
            job_proto.output_model = self.output_model
        request = SyncCreateSupervisedFineTuningJobRequest(
            supervised_fine_tuning_job=job_proto,
        )
        return request

    def output_llm(self) -> "LLM":
        # Import here to avoid circular import
        from fireworks.llm.llm import LLM

        logger.info(f'Fine-tuning job "{self.name}" completed')
        if self.output_model is None:
            raise ValueError(f'Fine-tuning job "{self.name}" did not create an output model')
        return LLM(model=self.output_model, deployment_type=self.llm.deployment_type)

    def wait_for_completion(self) -> "SupervisedFineTuningJob":
        """
        Synchronously poll for job completion.
        """
        while self.state != JobState.COMPLETED:
            if self.state == JobState.FAILED:
                raise ValueError(f'Fine-tuning job "{self.name}" failed')
            if self.create_time is not None:
                curr_time = time.time()
                create_time = self.create_time.timestamp()
                delta_seconds = int(curr_time - create_time)
                minutes = delta_seconds // 60
                seconds = delta_seconds % 60
                time_str = f"{seconds}s" if minutes == 0 else f"{minutes}m{seconds}s"
                logger.info(f'Fine-tuning job "{self.name}" is in state {self.state}. Job was created {time_str} ago.')
            time.sleep(5)
            updated_job = self.get()
            if updated_job is None:
                raise ValueError(f'Fine-tuning job "{self.name}" not found')
            self = updated_job
        return self

    async def await_for_completion(self) -> "SupervisedFineTuningJob":
        """
        Asynchronously poll for job completion.
        """
        while self.state != JobState.COMPLETED:
            if self.state == JobState.FAILED:
                raise ValueError(f'Fine-tuning job "{self.name}" failed')
            if self.create_time is not None:
                curr_time = time.time()
                create_time = self.create_time.timestamp()
                delta_seconds = int(curr_time - create_time)
                minutes = delta_seconds // 60
                seconds = delta_seconds % 60
                time_str = f"{seconds}s" if minutes == 0 else f"{minutes}m{seconds}s"
                logger.info(f'Fine-tuning job "{self.name}" is in state {self.state}. Job was created {time_str} ago.')
            await asyncio.sleep(5)
            updated_job = self.get()
            if updated_job is None:
                raise ValueError(f'Fine-tuning job "{self.name}" not found')
            self = updated_job
        return self

    def get(self) -> Optional["SupervisedFineTuningJob"]:
        """
        TODO: we should not be using display_name to find the job, but instead
        the name. But due to a bug when reusing the same Job ID, we need to use
        display_name as our identifier.
        """
        request = SyncListSupervisedFineTuningJobsRequest()
        page_token = None
        while True:
            if page_token is not None:
                request.page_token = page_token
            list_response = self._gateway.list_supervised_fine_tuning_jobs_sync(request)
            for job_proto in list_response.supervised_fine_tuning_jobs:
                if job_proto.display_name == self.name and job_proto.base_model == self.llm.model:
                    id = job_proto.name.split("/")[-1]
                    return SupervisedFineTuningJob(
                        name=job_proto.display_name,
                        llm=self.llm,
                        id=id,
                        dataset_or_id=self.dataset_or_id,
                        api_key=self._api_key,
                        state=job_state_proto_to_literal(job_proto.state),
                        epochs=job_proto.epochs,
                        learning_rate=job_proto.learning_rate,
                        lora_rank=job_proto.lora_rank,
                        jinja_template=job_proto.jinja_template,
                        early_stop=job_proto.early_stop,
                        max_context_length=job_proto.max_context_length,
                        base_model_weight_precision=precision_proto_to_literal(job_proto.base_model_weight_precision),
                        wandb_config=wandb_config_proto_to_dataclass(job_proto.wandb_config),
                        evaluation_dataset=job_proto.evaluation_dataset,
                        accelerator_type=accelerator_type_proto_to_literal(job_proto.accelerator_type),
                        accelerator_count=job_proto.accelerator_count,
                        is_turbo=job_proto.is_turbo,
                        eval_auto_carveout=job_proto.eval_auto_carveout,
                        region=region_proto_to_literal(job_proto.region),
                        nodes=job_proto.nodes,
                        batch_size=job_proto.batch_size,
                        create_time=timestamp_proto_to_datetime(job_proto.create_time),
                        update_time=timestamp_proto_to_datetime(job_proto.update_time),
                        created_by=job_proto.created_by,
                        output_model=job_proto.output_model,
                    )
            if not list_response.next_page_token:
                return None
            page_token = list_response.next_page_token
