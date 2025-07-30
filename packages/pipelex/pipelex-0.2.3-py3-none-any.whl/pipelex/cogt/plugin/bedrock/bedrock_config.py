from enum import StrEnum

from pydantic import Field

from pipelex.tools.config.models import ConfigModel


class BedrockClientMethod(StrEnum):
    BOTO3 = "boto3"
    AIBOTO3 = "aioboto3"


class BedrockConfig(ConfigModel):
    aws_region: str
    client_method: BedrockClientMethod = Field(strict=False)
