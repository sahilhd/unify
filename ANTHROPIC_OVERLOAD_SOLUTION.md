# 🔄 Anthropic Server Overload Solution

## 🚨 Problem Identified

The error `Server error: Overloaded` is coming from **Anthropic's servers**, not your UniLLM backend. This is a temporary issue on Anthropic's side when their servers are under heavy load.

### Error Details:
```
[UniLLM] Exception in /chat/completions: Server error: Overloaded
Traceback (most recent call last):
  File "/app/api_gateway/main_phase2.py", line 267, in chat_completion
    response = llm_client.chat(
               ^^^^^^^^^^^^^^^^
  File "/app/api_gateway/phase2_llm_client.py", line 152, in chat
    return adapter.chat(request)
           ^^^^^^^^^^^^^^
  File "/app/src/unillm/adapters/anthropic_adapter.py", line 64, in chat
    raise handle_http_error(
unillm.exceptions.ServerError: Server error: Overloaded
```

## ✅ Solution Implemented

### 1. **Retry Logic with Exponential Backoff**
Added intelligent retry logic to the Anthropic adapter:

```python
def _make_request_with_retry(self, url: str, headers: Dict[str, str], payload: Dict[str, Any], max_retries: int = 3) -> requests.Response:
    """Make a request with exponential backoff retry logic for server overloads."""
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=self.timeout)
            
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
```

### 2. **Improved Error Messages**
Enhanced error handling to provide clearer messages:

```python
elif status_code >= 500:
    # Check for specific overload messages
    if "overloaded" in error_message.lower():
        return ServerError(
            f"Anthropic servers are temporarily overloaded. Please try again in a few moments. Error: {error_message}",
            provider=provider,
            status_code=status_code,
            response_data=response_data,
        )
    else:
        return ServerError(
            f"Server error: {error_message}",
            provider=provider,
            status_code=status_code,
            response_data=response_data,
        )
```

## 🔧 How It Works

### **Retry Strategy:**
1. **First attempt**: Immediate request
2. **Second attempt**: Wait 1 second, then retry
3. **Third attempt**: Wait 2.1 seconds, then retry
4. **Final failure**: Return the error

### **What Triggers Retries:**
- HTTP 500+ status codes
- Error messages containing: "overloaded", "server error", "internal error", "service unavailable"
- Network timeouts

### **What Doesn't Retry:**
- Authentication errors (401)
- Rate limit errors (429)
- Invalid request errors (400)
- Model not found errors (404)

## 🧪 Testing

Run the retry logic test:
```bash
python3 test_retry_logic.py
```

## 📊 Benefits

### **For Users:**
- ✅ Automatic handling of temporary server overloads
- ✅ Better user experience with fewer failed requests
- ✅ Clear error messages when retries are exhausted

### **For Your System:**
- ✅ Reduced support tickets for temporary issues
- ✅ Better reliability metrics
- ✅ Graceful degradation during peak usage

## 🚀 Deployment

The changes are in:
- `src/unillm/adapters/anthropic_adapter.py` - Retry logic
- `src/unillm/exceptions.py` - Improved error messages

### **To Deploy:**
1. Commit the changes
2. Deploy to Railway
3. The retry logic will automatically handle future overloads

## 📈 Monitoring

### **Logs to Watch:**
```
[AnthropicAdapter] Server overloaded, retrying in 1.0s (attempt 1/3)
[AnthropicAdapter] Server overloaded, retrying in 2.1s (attempt 2/3)
```

### **Success Metrics:**
- Reduced 500 errors from Anthropic
- Better success rates for claude-3-haiku requests
- Improved user satisfaction

## 🔮 Future Improvements

### **Potential Enhancements:**
1. **Circuit Breaker Pattern**: Temporarily disable Anthropic if too many failures
2. **Fallback Models**: Automatically switch to alternative models during overloads
3. **Queue System**: Queue requests during overload periods
4. **Health Checks**: Proactively check Anthropic server status

### **Configuration Options:**
```python
# Future: Make retry parameters configurable
MAX_RETRIES = 3
BASE_WAIT_TIME = 1.0
MAX_WAIT_TIME = 10.0
```

## ✅ Summary

**Problem**: Anthropic servers occasionally return "Overloaded" errors
**Solution**: Intelligent retry logic with exponential backoff
**Result**: Automatic handling of temporary server issues
**Status**: ✅ Implemented and ready for deployment

Your UniLLM system will now gracefully handle Anthropic server overloads! 🎉 