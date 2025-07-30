"""API module for the Scout SDK."""

from .api import ScoutAPI, Response, AssistantData, AssistantDataList
from .types.assistants import AssistantResponse
from .types.chat import (
    ChatCompletionMessage,
    ChatCompletionMessageTextContent,
    ChatCompletionMessageImageContent,
    ChatCompletionMessagePDFContent,
)
from .types.images import (
    ImageRequest,
    ImageResponse,
    ImageQuality,
    ImageAspectRatio,
    ImageBackground,
)
from .constants import SCOUT_CUSTOM_FUNCTION_CONTENT_TYPE
from .utils import upload_file_to_signed_url


__all__ = [
    "ScoutAPI",
    "AssistantResponse",
    "SCOUT_CUSTOM_FUNCTION_CONTENT_TYPE",
    "Response",
    "upload_file_to_signed_url",
    "AssistantData",
    "AssistantDataList",
    # chat
    "ChatCompletionMessage",
    "ChatCompletionMessageTextContent",
    "ChatCompletionMessageImageContent",
    "ChatCompletionMessagePDFContent",
    # images
    "ImageRequest",
    "ImageResponse",
    "ImageQuality",
    "ImageAspectRatio",
    "ImageBackground",
]
