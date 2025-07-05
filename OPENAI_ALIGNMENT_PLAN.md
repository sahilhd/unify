# UniLLM OpenAI Alignment Plan

## Current State vs. Desired State

### Current UniLLM Structure:
```python
from unillm import UniLLM
client = UniLLM(api_key='your-key')
response = client.chat(model='gpt-4', messages=[...])
print(response.content)  # Custom ChatResponse object
```

### Desired OpenAI-Aligned Structure:
```python
from unillm import UniLLM
client = UniLLM(api_key='your-key')
response = client.chat.completions.create(model='gpt-4', messages=[...])
print(response.choices[0].message.content)  # OpenAI-style response
```

## Key Changes Needed

### 1. Main Client Structure
**Current:**
- `client.chat(model, messages, ...)` - direct method call
- Returns custom `ChatResponse` object

**Desired:**
- `client.chat.completions.create(model, messages, ...)` - nested object structure
- Returns OpenAI-style response object with `choices`, `model`, `usage` attributes

### 2. Response Object Structure
**Current:**
```python
class ChatResponse:
    def __init__(self, content, model, usage, finish_reason):
        self.content = content
        self.model = model
        self.usage = usage
        self.finish_reason = finish_reason
```

**Desired:**
```python
class ChatCompletionResponse:
    def __init__(self, choices, model, usage, ...):
        self.choices = choices  # List of Choice objects
        self.model = model
        self.usage = usage
        # ... other OpenAI attributes

class Choice:
    def __init__(self, message, finish_reason, index=0):
        self.message = message
        self.finish_reason = finish_reason
        self.index = index

class ChatMessage:
    def __init__(self, content, role="assistant"):
        self.content = content
        self.role = role
```

### 3. Client Architecture
**Current:**
```python
class UniLLM:
    def chat(self, model, messages, ...):
        # Direct implementation
```

**Desired:**
```python
class UniLLM:
    def __init__(self, api_key=None, base_url=None, ...):
        self.chat = Chat(self)
        self.models = Models(self)
        # ... other OpenAI-style resources

class Chat:
    def __init__(self, client):
        self.completions = ChatCompletions(client)

class ChatCompletions:
    def __init__(self, client):
        self._client = client
    
    def create(self, model, messages, ...):
        # Implementation here
```

### 4. Configuration and Environment
**Current:**
- Custom environment variables: `UNILLM_API_KEY`, `UNILLM_BASE_URL`
- Custom parameter names

**Desired:**
- OpenAI-compatible: `OPENAI_API_KEY`, `OPENAI_API_BASE`
- Support both UniLLM and OpenAI environment variables
- Fallback to UniLLM-specific variables

### 5. Error Handling
**Current:**
- Custom `UniLLMError` exceptions

**Desired:**
- OpenAI-compatible error classes
- Support for OpenAI-style error handling patterns

### 6. Additional Features
**Current:**
- Basic chat completions only

**Desired:**
- Models listing: `client.models.list()`
- Files support: `client.files.list()`
- Streaming support: `stream=True`
- Async support: `await client.chat.completions.create(...)`

## Implementation Strategy

### Phase 1: Core Structure (Priority 1)
1. Refactor main client to use nested object structure
2. Update response objects to match OpenAI format
3. Maintain backward compatibility with deprecation warnings

### Phase 2: Configuration (Priority 2)
1. Add OpenAI-compatible environment variable support
2. Update parameter handling to match OpenAI patterns

### Phase 3: Advanced Features (Priority 3)
1. Add models listing endpoint
2. Add streaming support
3. Add async support

### Phase 4: Full Compatibility (Priority 4)
1. Add files support
2. Add embeddings support
3. Add other OpenAI endpoints

## Backward Compatibility

To maintain existing code, we should:
1. Keep the old `client.chat()` method with deprecation warnings
2. Provide migration guide from old to new API
3. Support both response formats during transition period

## Example Migration

**Old Code:**
```python
from unillm import UniLLM
client = UniLLM(api_key='your-key')
response = client.chat('gpt-4', [{'role': 'user', 'content': 'Hello!'}])
print(response.content)
```

**New Code:**
```python
from unillm import UniLLM
client = UniLLM(api_key='your-key')
response = client.chat.completions.create(
    model='gpt-4', 
    messages=[{'role': 'user', 'content': 'Hello!'}]
)
print(response.choices[0].message.content)
```

## Benefits of This Approach

1. **Familiarity**: Developers already know OpenAI's API
2. **Migration Path**: Easy to switch from OpenAI to UniLLM
3. **Consistency**: Same patterns across different LLM libraries
4. **Future-Proof**: Can easily add more OpenAI-compatible features
5. **Documentation**: Can leverage existing OpenAI documentation patterns 