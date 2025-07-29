"""High-level client for the QV Ollama SDK."""

from typing import Optional, Dict, Any, List, Iterator

from .domain.models import (
    Conversation,
    ModelParameters,
    MessageRole,
    GenerationResponse
)
from .services.ollama_conversation_service import OllamaConversationService


class OllamaChatClient:
    """A simplified client for chat interactions with Ollama models."""
    
    def __init__(
        self,
        model_name: str = "gemma2:2b",
        system_message: Optional[str] = None,

        parameters: Optional[ModelParameters] = None
    ):
        """Initialize the Ollama chat client.
        
        Args:
            model_name: The name of the model to use
            system_message: Optional system message to set the context
            host: The host URL for the Ollama API (currently not used)
            parameters: Optional model parameters to use for generation
        """
        self.conversation = Conversation(model_name=model_name)
        self.service = OllamaConversationService()
        self.parameters = parameters or ModelParameters()
        
        # Add system message if provided
        if system_message:
            self.conversation.add_system_message(system_message)
    
    def chat(self, message: str) -> str:
        """Send a message and get a response.
        
        Args:
            message: The user message to send
            
        Returns:
            The model's response text
        """
        # Add the user message
        self.conversation.add_user_message(message)
        
        # Generate a response
        response = self.service.generate_response(self.conversation, self.parameters)
        
        # Add the assistant's response to the conversation
        self.conversation.add_assistant_message(response.content)
        
        return response.content
    
    def stream_chat(self, message: str) -> Iterator[str]:
        """Send a message and stream the response.
        
        Args:
            message: The user message to send
            
        Yields:
            Chunks of the model's response as they become available
        """
        # Add the user message
        self.conversation.add_user_message(message)
        
        # Collect the full response
        full_response = ""
        
        # Stream the response
        for chunk in self.service.stream_response(self.conversation, self.parameters):
            full_response += chunk
            yield chunk
        
        # Add the assistant's response to the conversation
        self.conversation.add_assistant_message(full_response)
    
    def get_history(self) -> List[Dict[str, str]]:
        """Get the conversation history.
        
        Returns:
            The conversation history as a list of message dictionaries
        """
        return self.conversation.get_message_history()
    
    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.conversation.clear()
    
    def set_system_message(self, message: str) -> None:
        """Set or update the system message.
        
        Args:
            message: The system message to set
        """
        # Clear existing system messages
        self.conversation.messages = [
            msg for msg in self.conversation.messages 
            if msg.role != MessageRole.SYSTEM
        ]
        
        # Add the new system message
        self.conversation.add_system_message(message)
    
    def set_parameters(self, **kwargs) -> None:
        """Update model parameters.
        
        Args:
            **kwargs: Parameter values to update
        """
        # Set each parameter individually
        for key, value in kwargs.items():
            setattr(self.parameters, key, value)
    
    # Convenience properties for common parameters
    
    @property
    def temperature(self) -> float:
        """Get the current temperature parameter if set."""
        try:
            return self.parameters.temperature
        except AttributeError:
            return None
        
    @temperature.setter
    def temperature(self, value: float) -> None:
        """Set the temperature parameter."""
        self.set_parameters(temperature=value)
    
    @property
    def max_tokens(self) -> int:
        """Get the current max_tokens parameter if set."""
        try:
            return self.parameters.max_tokens
        except AttributeError:
            return None
        
    @max_tokens.setter
    def max_tokens(self, value: int) -> None:
        """Set the max_tokens parameter."""
        self.set_parameters(max_tokens=value)
    
    @property
    def top_p(self) -> float:
        """Get the current top_p parameter if set."""
        try:
            return self.parameters.top_p
        except AttributeError:
            return None
        
    @top_p.setter
    def top_p(self, value: float) -> None:
        """Set the top_p parameter."""
        self.set_parameters(top_p=value)
    
    @property
    def num_ctx(self) -> int:
        """Get the current context window size if set."""
        try:
            return self.parameters.num_ctx
        except AttributeError:
            return None
        
    @num_ctx.setter
    def num_ctx(self, value: int) -> None:
        """Set the context window size."""
        self.set_parameters(num_ctx=value) 