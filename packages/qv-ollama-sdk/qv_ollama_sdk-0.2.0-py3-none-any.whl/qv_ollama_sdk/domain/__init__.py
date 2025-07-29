"""Domain layer for the Ollama SDK."""

from .models import (
    MessageRole,
    Message,
    Conversation,
    ModelParameters,
    GenerationResponse
)

__all__ = [
    # Models
    "MessageRole",
    "Message",
    "Conversation",
    "ModelParameters",
    "GenerationResponse",
] 