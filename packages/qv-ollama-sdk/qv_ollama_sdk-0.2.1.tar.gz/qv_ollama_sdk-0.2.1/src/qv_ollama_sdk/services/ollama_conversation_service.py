"""Service for interacting with the Ollama API for conversation generation."""

import ollama
from typing import Dict, Any, Optional, Iterator

from ..domain.models import (
    Conversation, 
    Message, 
    ModelParameters, 
    GenerationResponse,
    MessageRole
)


class OllamaConversationService:
    """Service for generating responses in conversations using the Ollama API."""
    
    def __init__(self):
        """Initialize the Ollama conversation service.
        
        """

    
    def generate_response(
        self, 
        conversation: Conversation, 
        parameters: Optional[ModelParameters] = None
    ) -> GenerationResponse:
        """Generate a response for the given conversation.
        
        Args:
            conversation: The conversation to generate a response for
            parameters: Optional model parameters to use for generation
            
        Returns:
            A GenerationResponse containing the generated content
        """
        params = parameters.to_dict() if parameters else ModelParameters().to_dict()
        
        response = ollama.chat(
            model=conversation.model_name,
            messages=conversation.get_message_history(),
            options=params
        )
        
        # Extract the assistant's response
        content = response.get("message", {}).get("content", "")
        
        # Create and return the generation response
        return GenerationResponse(
            model_name=conversation.model_name,
            content=content,
            raw_response=response,
            finish_reason=response.get("done"),
            usage=response.get("prompt_eval_count", {})
        )
    
    def stream_response(
        self, 
        conversation: Conversation, 
        parameters: Optional[ModelParameters] = None
    ) -> Iterator[str]:
        """Generate a streaming response for the given conversation.
        
        Args:
            conversation: The conversation to generate a response for
            parameters: Optional model parameters to use for generation
            
        Yields:
            Chunks of the generated response as they become available
        """
        params = parameters.to_dict() if parameters else ModelParameters().to_dict()
        
        stream = ollama.chat(
            model=conversation.model_name,
            messages=conversation.get_message_history(),
            options=params,
            stream=True
        )
        
        for chunk in stream:
            if "message" in chunk and "content" in chunk["message"]:
                yield chunk["message"]["content"]
    