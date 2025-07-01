"""
UniLLM Python Client Library
A drop-in replacement for OpenAI's Python library that works with UniLLM API gateway.
"""

import requests
import json
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass
import time


@dataclass
class ChatMessage:
    """Represents a chat message."""
    role: str
    content: str


@dataclass
class ChatChoice:
    """Represents a chat completion choice."""
    index: int
    message: ChatMessage
    finish_reason: str


@dataclass
class Usage:
    """Represents token usage information."""
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


@dataclass
class ChatCompletion:
    """Represents a chat completion response."""
    id: str
    object: str
    created: int
    model: str
    choices: List[ChatChoice]
    usage: Usage
    provider: str
    cost: float
    remaining_credits: float


class UniLLMClient:
    """UniLLM client that mimics OpenAI's interface."""
    
    def __init__(self, api_key: str, base_url: str = "http://localhost:8000"):
        """
        Initialize the UniLLM client.
        
        Args:
            api_key: Your UniLLM API key (starts with 'unillm_')
            base_url: Base URL of your UniLLM API gateway
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })
    
    def ChatCompletion(self):
        """Return a ChatCompletion object for making requests."""
        return ChatCompletionAPI(self)
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics for the current user."""
        response = self.session.get(f"{self.base_url}/billing/usage")
        response.raise_for_status()
        return response.json()
    
    def purchase_credits(self, amount: float) -> Dict[str, Any]:
        """Purchase credits for the account."""
        data = {"credits": amount}
        response = self.session.post(f"{self.base_url}/billing/purchase-credits", json=data)
        response.raise_for_status()
        return response.json()


class ChatCompletionAPI:
    """Chat completion API interface."""
    
    def __init__(self, client: UniLLMClient):
        self.client = client
    
    def create(
        self,
        model: str,
        messages: List[Dict[str, str]],
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        frequency_penalty: Optional[float] = None,
        presence_penalty: Optional[float] = None,
        stop: Optional[Union[str, List[str]]] = None,
        stream: bool = False,
        **kwargs
    ) -> ChatCompletion:
        """
        Create a chat completion.
        
        Args:
            model: Model name (e.g., 'gpt-4o', 'claude-3-sonnet', 'gemini-pro')
            messages: List of message dictionaries with 'role' and 'content'
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0-2)
            top_p: Nucleus sampling parameter
            frequency_penalty: Frequency penalty (-2 to 2)
            presence_penalty: Presence penalty (-2 to 2)
            stop: Stop sequences
            stream: Whether to stream the response
            **kwargs: Additional parameters
        
        Returns:
            ChatCompletion object
        """
        # Prepare the request payload
        payload = {
            "model": model,
            "messages": messages,
            "stream": stream
        }
        
        # Add optional parameters
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        if temperature is not None:
            payload["temperature"] = temperature
        if top_p is not None:
            payload["top_p"] = top_p
        if frequency_penalty is not None:
            payload["frequency_penalty"] = frequency_penalty
        if presence_penalty is not None:
            payload["presence_penalty"] = presence_penalty
        if stop is not None:
            payload["stop"] = stop
        
        # Add any additional kwargs
        payload.update(kwargs)
        
        # Make the request
        response = self.client.session.post(
            f"{self.client.base_url}/chat/completions",
            json=payload
        )
        response.raise_for_status()
        
        # Parse the response
        data = response.json()
        
        # UniLLM returns a simplified format, not OpenAI's format
        # Convert it to OpenAI-compatible format for the client library
        
        # Create a mock OpenAI-style response
        choices = []
        message = ChatMessage(
            role="assistant",
            content=data.get('response', '')
        )
        choice = ChatChoice(
            index=0,
            message=message,
            finish_reason="stop"
        )
        choices.append(choice)
        
        usage = Usage(
            prompt_tokens=data.get('tokens', 0) // 2,  # Rough estimate
            completion_tokens=data.get('tokens', 0) // 2,  # Rough estimate
            total_tokens=data.get('tokens', 0)
        )
        
        return ChatCompletion(
            id=f"unillm_{int(time.time())}",
            object="chat.completion",
            created=int(time.time()),
            model=model,
            choices=choices,
            usage=usage,
            provider=data.get('provider', 'unknown'),
            cost=data.get('cost', 0.0),
            remaining_credits=data.get('remaining_credits', 0.0)
        )


# Convenience function for quick usage
def create_chat_completion(
    api_key: str,
    model: str,
    messages: List[Dict[str, str]],
    base_url: str = "http://localhost:8000",
    **kwargs
) -> ChatCompletion:
    """
    Quick function to create a chat completion.
    
    Args:
        api_key: Your UniLLM API key
        model: Model name
        messages: List of message dictionaries
        base_url: Base URL of UniLLM API
        **kwargs: Additional parameters for ChatCompletion.create()
    
    Returns:
        ChatCompletion object
    """
    client = UniLLMClient(api_key, base_url)
    return client.ChatCompletion().create(model, messages, **kwargs)


# Example usage and compatibility layer
if __name__ == "__main__":
    # Example 1: Using the client like OpenAI
    client = UniLLMClient("your_unillm_api_key_here")
    
    response = client.ChatCompletion().create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": "What's the difference between machine learning and deep learning?"}
        ],
        max_tokens=150,
        temperature=0.7
    )
    
    print(f"Response: {response.choices[0].message.content}")
    print(f"Provider: {response.provider}")
    print(f"Cost: ${response.cost:.6f}")
    print(f"Remaining credits: {response.remaining_credits}")
    
    # Example 2: Switch to Anthropic
    response2 = client.ChatCompletion().create(
        model="claude-3-sonnet",
        messages=[
            {"role": "user", "content": "Explain quantum computing in simple terms"}
        ],
        max_tokens=100
    )
    
    print(f"\nAnthropic Response: {response2.choices[0].message.content}")
    print(f"Provider: {response2.provider}")
    
    # Example 3: Get usage stats
    usage = client.get_usage_stats()
    print(f"\nUsage Stats: {usage}") 