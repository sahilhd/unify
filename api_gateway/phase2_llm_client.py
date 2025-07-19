"""
Custom UniLLM client for Phase 2 that uses environment variables for different providers.
"""

import os
import sys
from typing import Any, Dict, Generator, List, Optional, Union

# Add the src directory to the path
sys.path.append('../src')

from unillm.adapters import (
    AnthropicAdapter,
    BaseAdapter,
    CohereAdapter,
    GeminiAdapter,
    MistralAdapter,
    OpenAIAdapter,
)
from unillm.exceptions import ModelNotFoundError, UniLLMError
from unillm.models import ChatMessage, ChatRequest, ChatResponse
from unillm.registry import model_registry


class Phase2LLMClient:
    """Custom UniLLM client for Phase 2 that uses environment variables."""
    
    def __init__(self):
        self.timeout = 30
        self._adapters: Dict[str, BaseAdapter] = {}
        
        # Load API keys from environment variables
        self.api_keys = {
            "openai": os.getenv("OPENAI_API_KEY"),
            "anthropic": os.getenv("ANTHROPIC_API_KEY"),
            "gemini": os.getenv("GEMINI_API_KEY"),  # Fixed: was GOOGLE_API_KEY
            "mistral": os.getenv("MISTRAL_API_KEY"),
            "cohere": os.getenv("COHERE_API_KEY"),
        }
        
        # Debug: Print API keys (masked for security)
        print(f"[Phase2LLMClient DEBUG] API keys loaded:")
        for provider, key in self.api_keys.items():
            if key:
                masked_key = key[:10] + "..." + key[-10:] if len(key) > 20 else "***"
                print(f"  {provider}: {masked_key}")
            else:
                print(f"  {provider}: None")
    
    def _get_adapter(self, provider: str) -> BaseAdapter:
        """Get or create an adapter for the given provider."""
        if provider not in self._adapters:
            api_key = self.api_keys.get(provider)
            if not api_key:
                raise UniLLMError(
                    f"API key not found for provider '{provider}'. "
                    f"Please set {provider.upper()}_API_KEY environment variable."
                )
            
            # Create the appropriate adapter
            if provider == "openai":
                adapter = OpenAIAdapter(api_key)
            elif provider == "anthropic":
                adapter = AnthropicAdapter(api_key)
            elif provider == "gemini":
                adapter = GeminiAdapter(api_key)
            elif provider == "mistral":
                adapter = MistralAdapter(api_key)
            elif provider == "cohere":
                adapter = CohereAdapter(api_key)
            else:
                raise UniLLMError(f"Unsupported provider: {provider}")
            
            self._adapters[provider] = adapter
        
        return self._adapters[provider]
    
    def chat(
        self,
        model: str,
        messages: List[Union[Dict[str, str], ChatMessage]],
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        n: Optional[int] = None,
        stream: bool = False,
        max_tokens: Optional[int] = None,
        presence_penalty: Optional[float] = None,
        frequency_penalty: Optional[float] = None,
        logit_bias: Optional[Dict[str, float]] = None,
        user: Optional[str] = None,
    ) -> Union[ChatResponse, Generator[ChatResponse, None, None]]:
        """
        Send a chat completion request.
        
        Args:
            model: The model to use (e.g., "gpt-4", "claude-3-sonnet")
            messages: List of message dictionaries or ChatMessage objects
            temperature: Sampling temperature (0-2)
            top_p: Nucleus sampling parameter (0-1)
            n: Number of completions to generate
            stream: Whether to stream the response
            max_tokens: Maximum number of tokens to generate
            presence_penalty: Presence penalty (-2 to 2)
            frequency_penalty: Frequency penalty (-2 to 2)
            logit_bias: Logit bias for specific tokens
            user: User identifier for tracking
            
        Returns:
            ChatResponse or generator of ChatResponse for streaming
        """
        # Normalize the model name using aliases
        normalized_model = model_registry.resolve_alias(model)
        
        # Convert messages to ChatMessage objects if needed
        chat_messages = []
        for msg in messages:
            if isinstance(msg, dict):
                chat_messages.append(ChatMessage(**msg))
            elif isinstance(msg, ChatMessage):
                chat_messages.append(msg)
            else:
                raise ValueError(f"Invalid message format: {type(msg)}")
        
        # Get provider for the normalized model
        provider = model_registry.get_provider(normalized_model)
        if not provider:
            raise ModelNotFoundError(
                f"Model '{model}' not found. Available models: {model_registry.list_models()}"
            )
        
        # Create request with normalized model name
        request = ChatRequest(
            model=normalized_model,
            messages=chat_messages,
            temperature=temperature,
            top_p=top_p,
            n=n,
            stream=stream,
            max_tokens=max_tokens,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            logit_bias=logit_bias,
            user=user,
        )
        
        # Get adapter and send request
        adapter = self._get_adapter(provider)
        
        if stream:
            return adapter.chat_stream(request)
        else:
            return adapter.chat(request)
    
    def list_models(self) -> List[str]:
        """List all available models."""
        return model_registry.list_models()
    
    def list_providers(self) -> List[str]:
        """List all available providers."""
        return model_registry.list_providers()
    
    def get_model_info(self, model: str) -> Optional[Dict[str, str]]:
        """Get information about a specific model."""
        normalized_model = model_registry.resolve_alias(model)
        return model_registry.get_model_info(normalized_model)
    
    def is_model_supported(self, model: str) -> bool:
        """Check if a model is supported."""
        normalized_model = model_registry.resolve_alias(model)
        return model_registry.is_model_supported(normalized_model)
    
    def get_available_providers(self) -> List[str]:
        """Get list of providers that have API keys configured."""
        return [provider for provider, api_key in self.api_keys.items() if api_key] 