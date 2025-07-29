"""QV Ollama SDK - A Domain-Driven Design SDK for the Ollama API."""

__version__ = "0.1.0"

from .domain.models import (
    MessageRole,
    Message,
    Conversation,
    ModelParameters,
    GenerationResponse
)

from .services.ollama_conversation_service import OllamaConversationService
from .client import OllamaChatClient

__all__ = [
    # Domain models
    "MessageRole",
    "Message",
    "Conversation",
    "ModelParameters",
    "GenerationResponse",
    
    # Services
    "OllamaConversationService",
    
    # Client
    "OllamaChatClient",
] 