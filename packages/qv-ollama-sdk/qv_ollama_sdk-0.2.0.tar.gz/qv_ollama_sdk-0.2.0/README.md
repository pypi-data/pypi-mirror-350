# QV Ollama SDK

A simple SDK for interacting with the Ollama API.

## Features

- Simple conversation management
- Support for synchronous API calls
- Streaming response support
- Explicit parameter handling (no unnecessary defaults)
- User-friendly client interface

## Installation

```bash
pip install qv-ollama-sdk
```

## Quick Start

```python
from qv_ollama_sdk import OllamaChatClient

# Create a client with a system message
client = OllamaChatClient(
    model_name="gemma2:2b",
    system_message="You are a helpful assistant."
)

# Simple chat - uses Ollama's default parameters
response = client.chat("What is the capital of France?")
print(response)

# Continue the conversation
response = client.chat("And what is its population?")
print(response)

# Set specific parameters only when you need them
client.temperature = 1.0  # Using property setter
client.max_tokens = 500   # Using property setter
client.set_parameters(num_ctx=2048)  # For multiple parameters

# Get conversation history
history = client.get_history()
```

## Streaming Responses

```python
from qv_ollama_sdk import OllamaChatClient

client = OllamaChatClient(model_name="gemma2:2b")

# Stream the response
for chunk in client.stream_chat("Explain quantum computing."):
    print(chunk, end="", flush=True)
```


## Advanced Usage

For more control, you can use the lower-level API:

```python
from qv_ollama_sdk import Conversation, OllamaConversationService, ModelParameters

# Create a conversation
conversation = Conversation(model_name="gemma2:2b")
conversation.add_system_message("You are a helpful assistant.")
conversation.add_user_message("What is the capital of France?")

# Generate a response with specific parameters
service = OllamaConversationService()
parameters = ModelParameters(temperature=0.7, num_ctx=2048)
response = service.generate_response(conversation, parameters)

print(response.content)
```
