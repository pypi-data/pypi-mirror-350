"""
Azure AI Inference Client utility class for PM Studio MCP.

This module provides a singleton class to interact with Azure AI Inference services.
"""

import os
from typing import List, Optional, Dict, Any, Union

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import (
    SystemMessage, 
    UserMessage
)
from azure.core.credentials import AzureKeyCredential
from pm_studio_mcp.config import config


class AzureInferenceClient:
    """
    A singleton class for Azure AI Inference API calls.
    
    This class provides methods to interact with Azure AI models for chat completions.
    """
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        """Ensure only one instance of the client exists."""
        if cls._instance is None:
            cls._instance = super(AzureInferenceClient, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(
        self,
        api_key: str,
        model_name: str,
        system_message: Optional[str] = 'You are a helpful assistant. Say hello to me first. And ask "what I can do for you."',
    ):
        """
        Initialize the Azure Inference Client.
        
        Args:
            api_key: Azure API key. If None, will try to read from AZURE_INFERENCE_API_KEY environment variable.
            model_name: Azure model name. If None, will try to read from DEPLOYMENT_NAME environment variable.
            system_message: Default system message to use for chat completions.
        """
        if self._initialized:
            return
            
        self.endpoint = 'https://EdgeMobileDataAiServices.services.ai.azure.com/models'
        self.api_key = api_key
        if not self.api_key:
            self.api_key = config.AZURE_INFERENCE_API_KEY
            
        self.model_name = model_name
        self.system_message = system_message
        
        self.client = ChatCompletionsClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.api_key)
        )
        
    def get_response(
        self,
        user_message: str,
    ) -> str:
        """
        Get a completion from the Azure AI Inference API.
        
        Args:
            messages: A list of message objects to send to the API.
            model: The model to use. If None, the default model will be used.
            temperature: The temperature to use for the completion.
            max_tokens: The maximum number of tokens to generate.
            top_p: The top_p value to use for the completion.
            **kwargs: Additional parameters to pass to the API.
            
        Returns:
            The completion text.
        """
        response = self.client.complete(
            messages=[
                SystemMessage(content=self.system_message),
                UserMessage(content=user_message)
            ],
            model=self.model_name,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
