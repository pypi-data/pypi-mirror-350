"""
Test script for Azure AI Inference Client.

This module provides testing functionality for the AzureInferenceClient class.

Usage:
    export AZURE_INFERENCE_API_KEY="your-api-key"
    python -m src.utils.azure_ai.test_azure_inference_client
"""

import os
from .azure_inference_client import AzureInferenceClient
from pm_studio_mcp.config import config

def test_azure_inference_client(
    api_key=None, 
    model_name="DeepSeek-R1"
):
    """
    Test the AzureInferenceClient functionality.
    
    Args:
        api_key: Azure API key. If None, will attempt to read from AZURE_INFERENCE_API_KEY environment variable.
        model_name: The name of the model to use.
    """
    try:
        # Get API key from environment variable if not provided
        if not api_key:
            api_key = config.AZURE_INFERENCE_API_KEY
            if not api_key:
                raise ValueError("API key must be provided either as a parameter or as environment variable AZURE_INFERENCE_API_KEY")
        
        # Initialize the client with credentials
        client = AzureInferenceClient(
            api_key=api_key,
            model_name=model_name
        )
        
        # Test the get_response method
        response = client.get_response("say something to me")
        print(f"Response: {response}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing Azure Inference Client...")
    try:
        if test_azure_inference_client():
            print("Test completed successfully.")
        else:
            print("Test failed.")
    except ValueError as e:
        print(f"Error: {e}")
        print("Hint: You can set the AZURE_INFERENCE_API_KEY environment variable or pass the API key as an argument.")
