from typing import Literal


AcceleratorTypeLiteral = Literal[
    "ACCELERATOR_TYPE_UNSPECIFIED",
    "NVIDIA_A100_80GB",
    "NVIDIA_H100_80GB",
    "AMD_MI300X_192GB",
    "NVIDIA_A10G_24GB",
    "NVIDIA_A100_40GB",
    "NVIDIA_L4_24GB",
    "NVIDIA_H200_141GB",
    "NVIDIA_B200_180GB",
]


RegionLiteral = Literal[
    "REGION_UNSPECIFIED",
    "US_IOWA_1",
    "US_VIRGINIA_1",
    "US_VIRGINIA_2",
    "US_ILLINOIS_1",
    "AP_TOKYO_1",
    "EU_LONDON_1",
    "US_ARIZONA_1",
    "US_TEXAS_1",
    "US_ILLINOIS_2",
    "EU_FRANKFURT_1",
    "US_TEXAS_2",
    "EU_PARIS_1",
    "EU_HELSINKI_1",
    "US_NEVADA_1",
    "EU_ICELAND_1",
    "EU_ICELAND_2",
    "US_WASHINGTON_1",
    "US_WASHINGTON_2",
]


ReasoningEffort = Literal["low", "medium", "high"]

DeploymentTypeLiteral = Literal["serverless", "on-demand", "auto"]


DeploymentStrategyLiteral = Literal["serverless", "on-demand", "serverless-lora", "on-demand-lora"]
