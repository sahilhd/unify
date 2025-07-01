"""
UniLLM API Gateway Client

A simple Python client for the UniLLM API Gateway that provides
a unified interface to multiple LLM providers.
"""

import requests
import json
from typing import Dict, List, Optional, Any
from datetime import datetime

class UniLLMClient:
    """Client for the UniLLM API Gateway."""
    
    def __init__(self, api_key: str = "your-api-key", base_url: str = "http://localhost:8000"):
        """
        Initialize the UniLLM client.
        
        Args:
            api_key: Your UniLLM API key (can be any string for now)
            base_url: The base URL of the API gateway
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })
    
    def chat(self, 
             model: str, 
             messages: List[Dict[str, str]], 
             temperature: Optional[float] = 1.0,
             top_p: Optional[float] = 1.0,
             max_tokens: Optional[int] = None,
             stream: bool = False,
             **kwargs) -> Dict[str, Any]:
        """
        Send a chat completion request.
        
        Args:
            model: The model to use (e.g., 'gpt-4', 'claude-3-sonnet', 'gemini-pro')
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Sampling temperature (0.0 to 2.0)
            top_p: Nucleus sampling parameter (0.0 to 1.0)
            max_tokens: Maximum number of tokens to generate
            stream: Whether to stream the response
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            Dictionary containing the response data
        """
        url = f"{self.base_url}/chat/completions"
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
            "stream": stream,
            **kwargs
        }
        
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        
        # Remove None values
        payload = {k: v for k, v in payload.items() if v is not None}
        
        response = self.session.post(url, json=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API request failed: {response.status_code} - {response.text}")
    
    def list_models(self) -> Dict[str, Any]:
        """Get a list of all available models."""
        url = f"{self.base_url}/models"
        response = self.session.get(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get models: {response.status_code} - {response.text}")
    
    def health_check(self) -> Dict[str, Any]:
        """Check if the API gateway is healthy."""
        url = f"{self.base_url}/health"
        response = self.session.get(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Health check failed: {response.status_code} - {response.text}")
    
    def get_provider_for_model(self, model: str) -> Optional[str]:
        """Get the provider for a specific model."""
        try:
            models_data = self.list_models()
            return models_data.get("model_provider_map", {}).get(model)
        except:
            return None

class ChatSession:
    """A chat session that can switch between providers."""
    
    def __init__(self, client: UniLLMClient):
        """
        Initialize a chat session.
        
        Args:
            client: The UniLLM client to use
        """
        self.client = client
        self.messages = []
        self.current_model = None
    
    def add_message(self, role: str, content: str):
        """Add a message to the conversation."""
        self.messages.append({"role": role, "content": content})
    
    def chat(self, 
             content: str, 
             model: str, 
             system_message: Optional[str] = None,
             **kwargs) -> Dict[str, Any]:
        """
        Send a message and get a response.
        
        Args:
            content: The user's message
            model: The model to use for this response
            system_message: Optional system message to prepend
            **kwargs: Additional parameters for the chat request
            
        Returns:
            The response from the model
        """
        # Add user message
        self.add_message("user", content)
        
        # Prepare messages for the request
        request_messages = []
        
        if system_message:
            request_messages.append({"role": "system", "content": system_message})
        
        request_messages.extend(self.messages)
        
        # Make the request
        response = self.client.chat(model=model, messages=request_messages, **kwargs)
        
        # Add assistant response to conversation
        self.add_message("assistant", response["content"])
        self.current_model = model
        
        return response
    
    def switch_provider(self, new_model: str, **kwargs) -> Dict[str, Any]:
        """
        Switch to a different provider for the next response.
        
        Args:
            new_model: The new model to use
            **kwargs: Additional parameters for the chat request
            
        Returns:
            The response from the new model
        """
        if not self.messages:
            raise ValueError("No conversation history to continue")
        
        # Use the last user message
        last_user_message = None
        for msg in reversed(self.messages):
            if msg["role"] == "user":
                last_user_message = msg["content"]
                break
        
        if not last_user_message:
            raise ValueError("No user message found in conversation")
        
        return self.chat(last_user_message, new_model, **kwargs)
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get a summary of the conversation."""
        return {
            "message_count": len(self.messages),
            "current_model": self.current_model,
            "messages": self.messages
        }

# Convenience functions
def create_client(api_key: str = "your-api-key", base_url: str = "http://localhost:8000") -> UniLLMClient:
    """Create a new UniLLM client."""
    return UniLLMClient(api_key, base_url)

def create_session(client: UniLLMClient) -> ChatSession:
    """Create a new chat session."""
    return ChatSession(client)

# Example usage
if __name__ == "__main__":
    # Create a client
    client = create_client()
    
    # Check if the API is running
    try:
        health = client.health_check()
        print(f"✅ API Gateway is running: {health}")
    except Exception as e:
        print(f"❌ API Gateway is not running: {e}")
        exit(1)
    
    # List available models
    try:
        models = client.list_models()
        print(f"📋 Available models: {len(models['models'])}")
        print(f"🔧 Providers: {models['providers']}")
    except Exception as e:
        print(f"❌ Failed to get models: {e}")
    
    # Create a chat session
    session = create_session(client)
    
    # Start a conversation
    print("\n🗣️ Starting conversation...")
    
    try:
        # First response from OpenAI
        response1 = session.chat(
            "What is the capital of France?",
            model="gpt-4",
            max_tokens=100
        )
        print(f"🤖 OpenAI: {response1['content'][:100]}...")
        
        # Switch to Anthropic
        response2 = session.switch_provider(
            "claude-3-sonnet",
            max_tokens=100
        )
        print(f"🤖 Anthropic: {response2['content'][:100]}...")
        
        # Continue with Gemini
        response3 = session.chat(
            "What about the best time to visit?",
            model="gemini-pro",
            max_tokens=100
        )
        print(f"🤖 Gemini: {response3['content'][:100]}...")
        
        # Show conversation summary
        summary = session.get_conversation_summary()
        print(f"\n📊 Conversation summary: {summary['message_count']} messages")
        
    except Exception as e:
        print(f"❌ Error during conversation: {e}")
        print("💡 Make sure you have valid API keys configured in your .env file") 