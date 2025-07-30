"""Scout SDK - Python client library for Scout."""

from .api import ScoutAPI
from .shared.assistants_types import AssistantFile
from .shared.conversations_types import SignedUploadUrlResponse
from .shared.defines import VariableNames
from .api.types.assistants import AssistantResponse
from .api.constants import SCOUT_CUSTOM_FUNCTION_CONTENT_TYPE
from .api.project_helpers import scout
from .shared.document_chunker_types import (
    ChunkMetadata,
    Chunk,
    DocumentChunks,
    AbstractDocumentChunker,
)
from .shared.audio_types import AudioTranscriptionResponse
from .shared.protected_types import SignedUrlResponse

# Exposing CLI components
from .cli import ScoutCLI

__all__ = [
    # API components
    "ScoutAPI",
    "AssistantResponse",
    "SCOUT_CUSTOM_FUNCTION_CONTENT_TYPE",
    # CLI components
    "ScoutCLI",
    # shared components
    "AssistantFile",
    "SignedUploadUrlResponse",
    "VariableNames",
    "scout",
    # Types
    "ChunkMetadata",
    "Chunk",
    "DocumentChunks",
    "AbstractDocumentChunker",
    "AudioTranscriptionResponse",
    "SignedUrlResponse",
]
