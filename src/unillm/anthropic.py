# Anthropic-compatible interface for UniLLM

from unillm import UniLLM
import os

# Module-level variables to mimic anthropic
api_key = None
api_base = "https://web-production-70deb.up.railway.app"

DEFAULT_BASE_URL = "https://web-production-70deb.up.railway.app"

class Messages:
    @staticmethod
    def create(model, messages, max_tokens=None, temperature=None, api_key=None, api_base=None, **kwargs):
        """
        Drop-in replacement for anthropic.messages.create(...)
        """
        # Use passed-in or module-level api_key/api_base
        key = api_key or os.getenv("UNILLM_API_KEY")
        base = api_base or os.getenv("UNILLM_BASE_URL", DEFAULT_BASE_URL)
        client = UniLLM(api_key=key, base_url=base)
        response = client.chat(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        # Return Anthropic-style response object
        class Content:
            def __init__(self, text):
                self.text = text
        class Response:
            def __init__(self, content, model):
                self.content = [Content(content)]
                self.model = model
        return Response(response.content, response.model)

# Create messages instance for anthropic.messages.create()
messages = Messages()

class ChatCompletion:
    @staticmethod
    def create(model, messages, temperature=None, max_tokens=None, api_key=None, api_base=None, **kwargs):
        """
        Drop-in replacement for anthropic.ChatCompletion.create(...)
        """
        # Use passed-in or module-level api_key/api_base
        key = api_key or os.getenv("UNILLM_API_KEY")
        base = api_base or os.getenv("UNILLM_BASE_URL", DEFAULT_BASE_URL)
        client = UniLLM(api_key=key, base_url=base)
        response = client.chat(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        # Return Anthropic-style response dict (mimic OpenAI for consistency)
        return {
            "choices": [
                {
                    "message": {"content": response.content},
                    "finish_reason": response.finish_reason
                }
            ],
            "model": response.model,
            "usage": response.usage
        } 