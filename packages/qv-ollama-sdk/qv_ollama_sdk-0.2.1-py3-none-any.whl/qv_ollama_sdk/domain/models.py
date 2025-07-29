from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4


class MessageRole(str, Enum):
    """Enumeration of possible message roles in a conversation."""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


@dataclass
class Message:
    """Represents a single message in a conversation."""
    role: MessageRole
    content: str
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to a dictionary format for the Ollama API."""
        return {
            "role": self.role.value,
            "content": self.content
        }
    
    def to_db_dict(self) -> Dict[str, Any]:
        """Convert message to a dictionary format for database storage."""
        return {
            "id": str(self.id),
            "role": self.role.value,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata
        }
    
    @classmethod
    def from_db_dict(cls, data: Dict[str, Any]) -> 'Message':
        """Create a Message instance from database dictionary format."""
        return cls(
            id=UUID(data["id"]),
            role=MessageRole(data["role"]),
            content=data["content"],
            created_at=datetime.fromisoformat(data["created_at"]),
            metadata=data.get("metadata", {})
        )


@dataclass
class Conversation:
    """Represents a complete conversation consisting of multiple messages."""
    model_name: str = "llama3"
    id: UUID = field(default_factory=uuid4)
    title: Optional[str] = None
    messages: List[Message] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_system_message(self, content: str) -> Message:
        """Add a system message to the conversation."""
        message = Message(role=MessageRole.SYSTEM, content=content)
        self.messages.append(message)
        self.updated_at = datetime.now()
        return message
    
    def add_user_message(self, content: str) -> Message:
        """Add a user message to the conversation."""
        message = Message(role=MessageRole.USER, content=content)
        self.messages.append(message)
        self.updated_at = datetime.now()
        return message
    
    def add_assistant_message(self, content: str) -> Message:
        """Add an assistant message to the conversation."""
        message = Message(role=MessageRole.ASSISTANT, content=content)
        self.messages.append(message)
        self.updated_at = datetime.now()
        return message
    
    def get_message_history(self) -> List[Dict[str, str]]:
        """Get the message history in a format suitable for the Ollama API."""
        return [message.to_dict() for message in self.messages]
    
    def clear(self) -> None:
        """Clear all messages from the conversation."""
        self.messages.clear()
        self.updated_at = datetime.now()
    
    def to_db_dict(self) -> Dict[str, Any]:
        """Convert conversation to a dictionary format for database storage.
        
        Note: Messages are stored separately and not included in this output.
        """
        return {
            "id": str(self.id),
            "model_name": self.model_name,
            "title": self.title,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "metadata": self.metadata
        }
    
    @classmethod
    def from_db_dict(cls, data: Dict[str, Any]) -> 'Conversation':
        """Create a Conversation instance from database dictionary format.
        
        Note: Messages must be loaded separately and added to the conversation.
        """
        return cls(
            id=UUID(data["id"]),
            model_name=data["model_name"],
            title=data.get("title"),
            messages=[],  # Messages are loaded separately
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            metadata=data.get("metadata", {})
        )


class ModelParameters:
    """Parameters for controlling model generation behavior.
    
    Only parameters that are explicitly set will be sent to the API.
    The Ollama API will use its own defaults for any parameters not specified.
    
    Common parameters:
        temperature: Controls randomness. Higher values make output more random.
        max_tokens: Maximum number of tokens to generate.
        top_p: Nucleus sampling parameter.
        top_k: Limits token selection to top k options.
        stop: Sequences where the model should stop generating.
        frequency_penalty: Penalize frequent tokens.
        presence_penalty: Penalize tokens already used.
        repeat_penalty: How strongly to penalize repetitions.
        num_ctx: Context window size.
        
    Any model-specific parameters can be provided through the constructor.
    """

    def __init__(self, **kwargs):
        """Initialize model parameters.
        
        Args:
            **kwargs: Parameter values to set. Only parameters explicitly
                     set here will be sent to the API.
        
        Common parameters include:
            temperature: Controls randomness (0.0-2.0)
            max_tokens: Maximum number of tokens to generate
            top_p: Nucleus sampling parameter (0.0-1.0) 
            top_k: Limits token selection to top k options
            stop: Sequences where the model should stop generating
            frequency_penalty: Penalize frequent tokens (0.0-2.0)
            presence_penalty: Penalize tokens already used (0.0-2.0)
            repeat_penalty: How strongly to penalize repetitions
            num_ctx: Context window size
        """
        # Store parameters that were explicitly set
        self._parameters = {}
        
        # Common parameters
        self._common_params = [
            'temperature', 'max_tokens', 'top_p', 'top_k', 'stop',
            'frequency_penalty', 'presence_penalty', 'repeat_penalty', 'num_ctx'
        ]
        
        # Set provided parameters
        for key, value in kwargs.items():
            self._parameters[key] = value
        
    def __getattr__(self, name):
        """Get a parameter value."""
        if name in self._parameters:
            return self._parameters[name]
        raise AttributeError(f"'ModelParameters' object has no attribute '{name}'")
    
    def __setattr__(self, name, value):
        """Set a parameter value."""
        if name.startswith('_'):
            # Private attributes
            super().__setattr__(name, value)
        else:
            # Parameters
            self._parameters[name] = value
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert parameters to a dictionary for API requests.
        
        Returns:
            Dictionary of explicitly set parameters
        """
        params = {}
        
        # Map special parameter names to their API equivalents
        api_param_mapping = {
            'max_tokens': 'num_predict'
        }
        
        for key, value in self._parameters.items():
            # Use API-specific name if it exists
            api_key = api_param_mapping.get(key, key)
            params[api_key] = value
            
        return params


@dataclass
class GenerationResponse:
    """Represents a response from the model generation."""
    model_name: str
    content: str
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    raw_response: Optional[Dict[str, Any]] = None
    finish_reason: Optional[str] = None
    usage: Optional[Dict[str, int]] = None 