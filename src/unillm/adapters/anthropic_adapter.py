"""
Anthropic adapter for UniLLM library.
"""

import json
import requests
import time
from datetime import datetime
from typing import Any, Dict, Generator, List, Optional

from .base import BaseAdapter
from ..exceptions import (
    AuthenticationError,
    InvalidRequestError,
    ModelNotFoundError,
    NetworkError,
    QuotaExceededError,
    RateLimitError,
    ServerError,
    TimeoutError,
    handle_http_error,
)
from ..models import ChatMessage, ChatRequest, ChatResponse, TokenUsage

print("[AnthropicAdapter DEBUG] File src/unillm/adapters/anthropic_adapter.py loaded")

class AnthropicAdapter(BaseAdapter):
    """Adapter for Anthropic API."""
    
    def __init__(self, api_key: str, base_url: Optional[str] = None):
        super().__init__(api_key, base_url)
        self.base_url = base_url or "https://api.anthropic.com/v1"
        # DEBUG: Print when adapter is created
        print(f"[AnthropicAdapter DEBUG] Adapter created with API key: {repr(api_key)}")
    
    def _make_request_with_retry(self, url: str, headers: Dict[str, str], payload: Dict[str, Any], max_retries: int = 3) -> requests.Response:
        """Make a request with exponential backoff retry logic for server overloads."""
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=self.timeout,
                )
                
                # If successful, return immediately
                if response.status_code == 200:
                    return response
                
                # Check if it's a server overload error
                if response.status_code >= 500:
                    error_data = response.json() if response.text else {}
                    error_message = error_data.get("error", {}).get("message", "").lower()
                    
                    # Check for overload-related errors
                    if any(keyword in error_message for keyword in ["overloaded", "server error", "internal error", "service unavailable"]):
                        if attempt < max_retries - 1:  # Don't sleep on last attempt
                            wait_time = (2 ** attempt) + (0.1 * attempt)  # Exponential backoff: 1s, 2.1s, 4.2s
                            print(f"[AnthropicAdapter] Server overloaded, retrying in {wait_time:.1f}s (attempt {attempt + 1}/{max_retries})")
                            time.sleep(wait_time)
                            continue
                
                # For other errors, don't retry
                return response
                
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) + (0.1 * attempt)
                    print(f"[AnthropicAdapter] Timeout, retrying in {wait_time:.1f}s (attempt {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                    continue
                else:
                    raise TimeoutError("Request timed out", provider="anthropic")
        
        # If we get here, all retries failed
        return response
    
    def chat(self, request: ChatRequest) -> ChatResponse:
        """Send a chat completion request to Anthropic."""
        self._validate_request(request)
        
        url = f"{self.base_url}/messages"
        headers = self._get_headers()
        headers["anthropic-version"] = "2023-06-01"
        
        # DEBUG: Print the API key being used
        print(f"[AnthropicAdapter DEBUG] API key repr: {repr(self.api_key)}")
        
        payload = {
            "model": request.model,
            "messages": self._convert_messages(request.messages),
            "temperature": request.temperature,
            "top_p": request.top_p,
            "max_tokens": request.max_tokens or 4096,
            "system": self._extract_system_message(request.messages),
        }
        
        # Remove None values
        payload = {k: v for k, v in payload.items() if v is not None}
        
        try:
            response = self._make_request_with_retry(url, headers, payload)
            
            if response.status_code != 200:
                # Log error details
                print(f"[AnthropicAdapter] Error: Status {response.status_code}, Response: {response.text}")
                raise handle_http_error(
                    response.status_code,
                    response.json(),
                    provider="anthropic",
                )
            
            response_data = response.json()
            return self._convert_response(response_data, request.model)
            
        except requests.exceptions.Timeout as e:
            print(f"[AnthropicAdapter] Timeout: {e}")
            raise TimeoutError("Request timed out", provider="anthropic")
        except requests.exceptions.RequestException as e:
            print(f"[AnthropicAdapter] Network error: {e}")
            raise NetworkError(f"Network error: {str(e)}", provider="anthropic")
        except Exception as e:
            print(f"[AnthropicAdapter] Unexpected error: {e}")
            raise
    
    def chat_stream(
        self,
        request: ChatRequest,
    ) -> Generator[ChatResponse, None, None]:
        """Send a streaming chat completion request to Anthropic."""
        self._validate_request(request)
        
        url = f"{self.base_url}/messages"
        headers = self._get_headers()
        headers["anthropic-version"] = "2023-06-01"
        
        payload = {
            "model": request.model,
            "messages": self._convert_messages(request.messages),
            "temperature": request.temperature,
            "top_p": request.top_p,
            "max_tokens": request.max_tokens or 4096,
            "system": self._extract_system_message(request.messages),
            "stream": True,
        }
        
        # Remove None values
        payload = {k: v for k, v in payload.items() if v is not None}
        
        # For streaming, we'll try once and let the caller handle retries
        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=self.timeout,
                stream=True,
            )
            
            if response.status_code != 200:
                raise handle_http_error(
                    response.status_code,
                    response.json(),
                    provider="anthropic",
                )
            
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data = line[6:]  # Remove 'data: ' prefix
                        if data == '[DONE]':
                            break
                        
                        try:
                            chunk_data = json.loads(data)
                            if chunk_data.get('type') == 'content_block_delta':
                                yield self._convert_stream_response(
                                    chunk_data, request.model
                                )
                        except json.JSONDecodeError:
                            continue
                            
        except requests.exceptions.Timeout:
            raise TimeoutError("Request timed out", provider="anthropic")
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Network error: {str(e)}", provider="anthropic")
    
    def _convert_messages(
        self,
        messages: List[ChatMessage],
    ) -> List[Dict[str, Any]]:
        """Convert UniLLM messages to Anthropic format."""
        converted = []
        for msg in messages:
            if msg.role == "system":
                # System messages are handled separately in Anthropic
                continue
            converted_msg = {
                "role": msg.role,
                "content": msg.content,
            }
            converted.append(converted_msg)
        return converted
    
    def _extract_system_message(self, messages: List[ChatMessage]) -> Optional[str]:
        """Extract system message from messages."""
        for msg in messages:
            if msg.role == "system":
                return msg.content
        return None
    
    def _convert_response(
        self,
        response_data: Dict[str, Any],
        model: str,
    ) -> ChatResponse:
        """Convert Anthropic response to UniLLM format."""
        content = response_data["content"][0]["text"]
        
        usage_data = response_data.get("usage", {})
        usage = TokenUsage(
            prompt_tokens=usage_data.get("input_tokens", 0),
            completion_tokens=usage_data.get("output_tokens", 0),
            total_tokens=usage_data.get("input_tokens", 0) + usage_data.get("output_tokens", 0),
        )
        
        return ChatResponse(
            content=content,
            model=model,
            provider="anthropic",
            usage=usage,
            finish_reason=response_data.get("stop_reason", "end_turn"),
            created_at=datetime.now(),
        )
    
    def _convert_stream_response(
        self,
        chunk_data: Dict[str, Any],
        model: str,
    ) -> ChatResponse:
        """Convert Anthropic streaming response chunk to UniLLM format."""
        content = chunk_data.get("delta", {}).get("text", "")
        
        return ChatResponse(
            content=content,
            model=model,
            provider="anthropic",
            usage=TokenUsage(prompt_tokens=0, completion_tokens=0, total_tokens=0),
            finish_reason=None,
            created_at=datetime.now(),
        )
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests."""
        return {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
        } 