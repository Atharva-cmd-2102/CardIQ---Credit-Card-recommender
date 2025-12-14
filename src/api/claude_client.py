"""Claude API client wrapper"""
from anthropic import Anthropic
from src.config import ANTHROPIC_API_KEY, HAIKU_MODEL, SONNET_MODEL

class ClaudeClient:
    """Wrapper for Claude API calls"""
    
    def __init__(self, api_key: str = ANTHROPIC_API_KEY):
        self.client = Anthropic(api_key=api_key)
        self.haiku_model = HAIKU_MODEL
        self.sonnet_model = SONNET_MODEL
    
    def call_haiku(self, system_prompt: str, user_message: str, max_tokens: int = 2000) -> str:
        """Call Claude Haiku (faster, cheaper)"""
        message = self.client.messages.create(
            model=self.haiku_model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        return message.content[0].text
    
    def call_sonnet(self, system_prompt: str, user_message: str, max_tokens: int = 3000) -> str:
        """Call Claude Sonnet (better quality)"""
        message = self.client.messages.create(
            model=self.sonnet_model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        return message.content[0].text
