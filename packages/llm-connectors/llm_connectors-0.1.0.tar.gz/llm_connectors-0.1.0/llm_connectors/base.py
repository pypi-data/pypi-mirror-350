from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List

class BaseConnector(ABC):
    """Base class for all AI platform connectors."""
    
    def __init__(self, api_key: str, **kwargs):
        """Initialize the connector with API key and optional parameters.
        
        Args:
            api_key (str): The API key for the AI platform
            **kwargs: Additional platform-specific parameters
        """
        self.api_key = api_key
        self.config = kwargs
    
    @abstractmethod
    async def chat(self, 
                  messages: List[Dict[str, str]], 
                  temperature: float = 0.7,
                  max_tokens: Optional[int] = None,
                  **kwargs) -> Dict[str, Any]:
        """Send a chat request to the AI platform.
        
        Args:
            messages (List[Dict[str, str]]): List of message dictionaries with 'role' and 'content'
            temperature (float): Controls randomness in the response
            max_tokens (Optional[int]): Maximum number of tokens in the response
            **kwargs: Additional platform-specific parameters
            
        Returns:
            Dict[str, Any]: The response from the AI platform
        """
        pass
    
    @abstractmethod
    async def generate_text(self,
                          prompt: str,
                          temperature: float = 0.7,
                          max_tokens: Optional[int] = None,
                          **kwargs) -> str:
        """Generate text based on a prompt.
        
        Args:
            prompt (str): The input prompt
            temperature (float): Controls randomness in the response
            max_tokens (Optional[int]): Maximum number of tokens in the response
            **kwargs: Additional platform-specific parameters
            
        Returns:
            str: The generated text
        """
        pass
    
    @abstractmethod
    async def get_embeddings(self,
                           text: str,
                           **kwargs) -> List[float]:
        """Get embeddings for the input text.
        
        Args:
            text (str): The input text
            **kwargs: Additional platform-specific parameters
            
        Returns:
            List[float]: The embedding vector
        """
        pass 