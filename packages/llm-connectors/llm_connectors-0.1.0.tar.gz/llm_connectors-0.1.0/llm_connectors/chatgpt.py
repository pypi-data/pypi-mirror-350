from typing import Dict, Any, Optional, List
import openai
from .base import BaseConnector

class ChatGPTConnector(BaseConnector):
    """Connector for OpenAI's ChatGPT API."""
    
    def __init__(self, api_key: str, **kwargs):
        """Initialize the ChatGPT connector.
        
        Args:
            api_key (str): OpenAI API key
            **kwargs: Additional OpenAI client configuration
        """
        super().__init__(api_key, **kwargs)
        self.client = openai.OpenAI(api_key=api_key, **kwargs)
    
    async def chat(self,
                  messages: List[Dict[str, str]],
                  temperature: float = 0.7,
                  max_tokens: Optional[int] = None,
                  **kwargs) -> Dict[str, Any]:
        """Send a chat request to ChatGPT.
        
        Args:
            messages (List[Dict[str, str]]): List of message dictionaries
            temperature (float): Controls randomness in the response
            max_tokens (Optional[int]): Maximum number of tokens in the response
            **kwargs: Additional OpenAI API parameters
            
        Returns:
            Dict[str, Any]: The response from ChatGPT
        """
        response = await self.client.chat.completions.create(
            model=kwargs.get("model", "gpt-3.5-turbo"),
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        return await response.model_dump()
    
    async def generate_text(self,
                          prompt: str,
                          temperature: float = 0.7,
                          max_tokens: Optional[int] = None,
                          **kwargs) -> str:
        """Generate text using ChatGPT.
        
        Args:
            prompt (str): The input prompt
            temperature (float): Controls randomness in the response
            max_tokens (Optional[int]): Maximum number of tokens in the response
            **kwargs: Additional OpenAI API parameters
            
        Returns:
            str: The generated text
        """
        response = await self.client.chat.completions.create(
            model=kwargs.get("model", "gpt-3.5-turbo"),
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        return response.choices[0].message.content
    
    async def get_embeddings(self,
                           text: str,
                           **kwargs) -> List[float]:
        """Get embeddings for the input text using OpenAI's embedding model.
        
        Args:
            text (str): The input text
            **kwargs: Additional OpenAI API parameters
            
        Returns:
            List[float]: The embedding vector
        """
        response = await self.client.embeddings.create(
            model=kwargs.get("model", "text-embedding-ada-002"),
            input=text,
            **kwargs
        )
        return response.data[0].embedding 