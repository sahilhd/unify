"""
UniLLM API Gateway

A FastAPI server that provides a unified interface for multiple LLM providers.
"""

import os
import time
from typing import Dict, List, Optional, Any
from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="UniLLM API Gateway",
    description="A unified API for accessing multiple LLM providers",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Provider API keys (in production, these would be stored securely)
PROVIDER_KEYS = {
    "openai": os.getenv("OPENAI_API_KEY"),
    "anthropic": os.getenv("ANTHROPIC_API_KEY"),
    "gemini": os.getenv("GEMINI_API_KEY"),
    "mistral": os.getenv("MISTRAL_API_KEY"),
    "cohere": os.getenv("COHERE_API_KEY"),
}

# Model to provider mapping
MODEL_PROVIDER_MAP = {
    # OpenAI models
    "gpt-4": "openai",
    "gpt-4-turbo": "openai",
    "gpt-4-turbo-preview": "openai",
    "gpt-4-32k": "openai",
    "gpt-4-32k-turbo": "openai",
    "gpt-3.5-turbo": "openai",
    "gpt-3.5-turbo-16k": "openai",
    "gpt-3.5-turbo-instruct": "openai",
    
    # Anthropic models
    "claude-3-opus": "anthropic",
    "claude-3-sonnet": "anthropic",
    "claude-3-haiku": "anthropic",
    "claude-2.1": "anthropic",
    "claude-2.0": "anthropic",
    "claude-instant-1.2": "anthropic",
    
    # Google Gemini models
    "gemini-pro": "gemini",
    "gemini-pro-vision": "gemini",
    "gemini-1.5-pro": "gemini",
    "gemini-1.5-flash": "gemini",
    
    # Mistral models
    "mistral-large": "mistral",
    "mistral-medium": "mistral",
    "mistral-small": "mistral",
    "mistral-7b-instruct": "mistral",
    
    # Cohere models
    "command": "cohere",
    "command-light": "cohere",
    "command-nightly": "cohere",
    "command-light-nightly": "cohere",
}

# Pydantic models
class ChatMessage(BaseModel):
    role: str = Field(..., description="The role of the message sender")
    content: str = Field(..., description="The content of the message")
    name: Optional[str] = Field(None, description="Optional name for the message sender")

class ChatRequest(BaseModel):
    model: str = Field(..., description="The model to use")
    messages: List[ChatMessage] = Field(..., description="The conversation messages")
    temperature: Optional[float] = Field(1.0, ge=0.0, le=2.0, description="Sampling temperature")
    top_p: Optional[float] = Field(1.0, ge=0.0, le=1.0, description="Nucleus sampling parameter")
    n: Optional[int] = Field(1, ge=1, le=10, description="Number of completions to generate")
    stream: Optional[bool] = Field(False, description="Whether to stream the response")
    max_tokens: Optional[int] = Field(None, ge=1, description="Maximum number of tokens to generate")
    presence_penalty: Optional[float] = Field(0.0, ge=-2.0, le=2.0, description="Presence penalty")
    frequency_penalty: Optional[float] = Field(0.0, ge=-2.0, le=2.0, description="Frequency penalty")
    user: Optional[str] = Field(None, description="User identifier for tracking")

class TokenUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class ChatResponse(BaseModel):
    content: str
    model: str
    provider: str
    usage: TokenUsage
    finish_reason: str
    created_at: datetime

class ErrorResponse(BaseModel):
    error: str
    provider: Optional[str] = None
    status_code: Optional[int] = None

# Authentication
def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Verify the API key and return the user ID."""
    # In production, you would validate against a database
    # For now, we'll accept any valid Bearer token
    if not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    return credentials.credentials

# Provider adapters
class OpenAIAdapter:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1"
    
    def chat(self, request: ChatRequest) -> ChatResponse:
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": request.model,
            "messages": [{"role": msg.role, "content": msg.content} for msg in request.messages],
            "temperature": request.temperature,
            "top_p": request.top_p,
            "n": request.n,
            "stream": False,
            "max_tokens": request.max_tokens,
            "presence_penalty": request.presence_penalty,
            "frequency_penalty": request.frequency_penalty,
            "user": request.user,
        }
        
        # Remove None values
        payload = {k: v for k, v in payload.items() if v is not None}
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"OpenAI API error: {response.text}"
            )
        
        data = response.json()
        choice = data["choices"][0]
        message = choice["message"]
        usage_data = data.get("usage", {})
        
        return ChatResponse(
            content=message["content"],
            model=request.model,
            provider="openai",
            usage=TokenUsage(
                prompt_tokens=usage_data.get("prompt_tokens", 0),
                completion_tokens=usage_data.get("completion_tokens", 0),
                total_tokens=usage_data.get("total_tokens", 0)
            ),
            finish_reason=choice.get("finish_reason", "stop"),
            created_at=datetime.fromtimestamp(data.get("created", time.time()))
        )

class AnthropicAdapter:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.anthropic.com/v1"
    
    def chat(self, request: ChatRequest) -> ChatResponse:
        url = f"{self.base_url}/messages"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        # Extract system message
        system_message = None
        messages = []
        for msg in request.messages:
            if msg.role == "system":
                system_message = msg.content
            else:
                messages.append({"role": msg.role, "content": msg.content})
        
        payload = {
            "model": request.model,
            "messages": messages,
            "temperature": request.temperature,
            "top_p": request.top_p,
            "max_tokens": request.max_tokens or 4096,
        }
        
        if system_message:
            payload["system"] = system_message
        
        # Remove None values
        payload = {k: v for k, v in payload.items() if v is not None}
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Anthropic API error: {response.text}"
            )
        
        data = response.json()
        content = data["content"][0]["text"]
        usage_data = data.get("usage", {})
        
        return ChatResponse(
            content=content,
            model=request.model,
            provider="anthropic",
            usage=TokenUsage(
                prompt_tokens=usage_data.get("input_tokens", 0),
                completion_tokens=usage_data.get("output_tokens", 0),
                total_tokens=usage_data.get("input_tokens", 0) + usage_data.get("output_tokens", 0)
            ),
            finish_reason=data.get("stop_reason", "end_turn"),
            created_at=datetime.now()
        )

class GeminiAdapter:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
    
    def chat(self, request: ChatRequest) -> ChatResponse:
        url = f"{self.base_url}/models/{request.model}:generateContent"
        headers = {"Content-Type": "application/json"}
        
        # Convert messages to Gemini format
        contents = []
        system_content = None
        
        for msg in request.messages:
            if msg.role == "system":
                system_content = msg.content
            else:
                contents.append({
                    "role": "user" if msg.role == "user" else "model",
                    "parts": [{"text": msg.content}]
                })
        
        # Prepend system message to first user message if present
        if system_content and contents:
            contents[0]["parts"][0]["text"] = f"{system_content}\n\n{contents[0]['parts'][0]['text']}"
        
        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": request.temperature,
                "topP": request.top_p,
                "maxOutputTokens": request.max_tokens,
            }
        }
        
        # Remove None values from generationConfig
        payload["generationConfig"] = {
            k: v for k, v in payload["generationConfig"].items() if v is not None
        }
        
        response = requests.post(
            url, 
            headers=headers, 
            json=payload, 
            params={"key": self.api_key},
            timeout=30
        )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Gemini API error: {response.text}"
            )
        
        data = response.json()
        candidate = data["candidates"][0]
        content = candidate["content"]["parts"][0]["text"]
        usage_data = data.get("usageMetadata", {})
        
        return ChatResponse(
            content=content,
            model=request.model,
            provider="gemini",
            usage=TokenUsage(
                prompt_tokens=usage_data.get("promptTokenCount", 0),
                completion_tokens=usage_data.get("candidatesTokenCount", 0),
                total_tokens=usage_data.get("totalTokenCount", 0)
            ),
            finish_reason=candidate.get("finishReason", "STOP"),
            created_at=datetime.now()
        )

# Adapter factory
def get_adapter(provider: str):
    api_key = PROVIDER_KEYS.get(provider)
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"API key not configured for provider: {provider}"
        )
    
    if provider == "openai":
        return OpenAIAdapter(api_key)
    elif provider == "anthropic":
        return AnthropicAdapter(api_key)
    elif provider == "gemini":
        return GeminiAdapter(api_key)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported provider: {provider}"
        )

# API endpoints
@app.get("/")
async def root():
    return {"message": "UniLLM API Gateway", "version": "1.0.0"}

@app.get("/models")
async def list_models():
    """List all available models."""
    return {
        "models": list(MODEL_PROVIDER_MAP.keys()),
        "providers": list(set(MODEL_PROVIDER_MAP.values())),
        "model_provider_map": MODEL_PROVIDER_MAP
    }

@app.post("/chat/completions", response_model=ChatResponse)
async def chat_completions(
    request: ChatRequest,
    api_key: str = Depends(verify_api_key)
):
    """Send a chat completion request."""
    
    # Get provider for the model
    provider = MODEL_PROVIDER_MAP.get(request.model)
    if not provider:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Model '{request.model}' not supported. Available models: {list(MODEL_PROVIDER_MAP.keys())}"
        )
    
    try:
        # Get adapter and make request
        adapter = get_adapter(provider)
        response = adapter.chat(request)
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing request: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 