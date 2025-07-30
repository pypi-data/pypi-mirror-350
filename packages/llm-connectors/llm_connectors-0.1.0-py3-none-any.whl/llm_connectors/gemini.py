from typing import Dict, Any, Optional, List
import google.generativeai as genai
from .base import BaseConnector

class GeminiConnector(BaseConnector):
    """Connector for Google's Gemini API."""
    
    def __init__(self, api_key: str, **kwargs):
        """Initialize the Gemini connector.
        
        Args:
            api_key (str): Google API key
            **kwargs: Additional Gemini configuration
        """
        super().__init__(api_key, **kwargs)
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name=kwargs.get("model", "gemini-pro"),
            **kwargs
        )
    
    async def chat(self,
                  messages: List[Dict[str, str]],
                  temperature: float = 0.7,
                  max_tokens: Optional[int] = None,
                  **kwargs) -> Dict[str, Any]:
        """Send a chat request to Gemini.
        
        Args:
            messages (List[Dict[str, str]]): List of message dictionaries
            temperature (float): Controls randomness in the response
            max_tokens (Optional[int]): Maximum number of tokens in the response
            **kwargs: Additional Gemini API parameters
            
        Returns:
            Dict[str, Any]: The response from Gemini
        """
        chat = self.model.start_chat(history=[])
        response = await chat.send_message(
            messages[-1]["content"],
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
                **kwargs
            )
        )
        return {
            "content": response.text,
            "candidates": [{"content": response.text}]
        }
    
    async def generate_text(self,
                          prompt: str,
                          temperature: float = 0.7,
                          max_tokens: Optional[int] = None,
                          **kwargs) -> str:
        """Generate text using Gemini.
        
        Args:
            prompt (str): The input prompt
            temperature (float): Controls randomness in the response
            max_tokens (Optional[int]): Maximum number of tokens in the response
            **kwargs: Additional Gemini API parameters
            
        Returns:
            str: The generated text
        """
        response = await self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
                **kwargs
            )
        )
        return response.text
    
    async def get_embeddings(self,
                           text: str,
                           **kwargs) -> List[float]:
        """Get embeddings for the input text using Gemini's embedding model.
        
        Args:
            text (str): The input text
            **kwargs: Additional Gemini API parameters
            
        Returns:
            List[float]: The embedding vector
        """
        embedding_model = genai.GenerativeModel(
            model_name=kwargs.get("model", "embedding-001")
        )
        result = await embedding_model.embed_content(text)
        return result.embedding 