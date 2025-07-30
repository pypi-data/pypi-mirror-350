"""
Azure Key Vault utility functions for retrieving secrets.
"""
import os
from typing import Optional, Dict, Any

from azure.identity import DefaultAzureCredential, ClientSecretCredential
from azure.keyvault.secrets import SecretClient


class KeyVaultUtils:
    """
    Utility class for Azure Key Vault operations.
    This class provides methods to retrieve secrets from Azure Key Vault.
    """
    
    def __init__(self, vault_url: Optional[str] = None):
        """
        Initialize the KeyVaultUtils class.
        
        Args:
            vault_url (Optional[str]): The URL of the Azure Key Vault. 
                                      If not provided, will use AZURE_KEY_VAULT_URL from environment.
        """
        self.vault_url = vault_url or os.environ.get('AZURE_KEY_VAULT_URL')
        
        if not self.vault_url:
            raise ValueError("Key Vault URL must be provided either as a parameter or "
                            "as the AZURE_KEY_VAULT_URL environment variable.")
        
        # Initialize the credential and client
        self.credential = None
        self.client = None
    
    def initialize_with_default_credential(self) -> None:
        """
        Initialize using DefaultAzureCredential.
        This uses environment variables, managed identity, or developer tools for authentication.
        """
        self.credential = DefaultAzureCredential()
        self.client = SecretClient(vault_url=self.vault_url, credential=self.credential)
    
    def initialize_with_client_secret(self, client_id: str, client_secret: str, tenant_id: str) -> None:
        """
        Initialize using client secret authentication.
        
        Args:
            client_id (str): Azure AD application client ID
            client_secret (str): Azure AD application client secret
            tenant_id (str): Azure AD tenant ID
        """
        self.credential = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret
        )
        self.client = SecretClient(vault_url=self.vault_url, credential=self.credential)
    
    def get_secret(self, secret_name: str) -> str:
        """
        Get a secret from Azure Key Vault.
        
        Args:
            secret_name (str): The name of the secret to retrieve
            
        Returns:
            str: The secret value, or None if not found or error occurs
            
        Raises:
            ValueError: If the client is not initialized
        """
        if not self.client:
            raise ValueError("Key Vault client is not initialized. Call initialize_with_default_credential() or "
                           "initialize_with_client_secret() before getting secrets.")
        
        try:
            secret = self.client.get_secret(secret_name)
            return secret.value
        except Exception as e:
            print(f"Error retrieving secret '{secret_name}': {str(e)}")
            return None
    
    def get_secrets(self, secret_names: list) -> Dict[str, Any]:
        """
        Get multiple secrets from Azure Key Vault.
        
        Args:
            secret_names (list): List of secret names to retrieve
            
        Returns:
            Dict[str, Any]: Dictionary of secret names and their values
            
        Raises:
            ValueError: If the client is not initialized
        """
        if not self.client:
            raise ValueError("Key Vault client is not initialized. Call initialize_with_default_credential() or "
                           "initialize_with_client_secret() before getting secrets.")
        
        secrets = {}
        for name in secret_names:
            try:
                secret = self.client.get_secret(name)
                secrets[name] = secret.value
            except Exception as e:
                # Log the error but continue with other secrets
                print(f"Error retrieving secret '{name}': {str(e)}")
                secrets[name] = None
        
        return secrets


# Helper functions for easier usage
def get_secret(secret_name: str, vault_url: Optional[str] = None, 
               client_id: Optional[str] = None, 
               client_secret: Optional[str] = None,
               tenant_id: Optional[str] = None) -> str:
    """
    Helper function to get a single secret from Azure Key Vault.
    
    Args:
        secret_name (str): The name of the secret to retrieve
        vault_url (Optional[str]): The URL of the Azure Key Vault
        client_id (Optional[str]): Azure AD application client ID
        client_secret (Optional[str]): Azure AD application client secret
        tenant_id (Optional[str]): Azure AD tenant ID
        
    Returns:
        str: The secret value
        
    Usage:
        # Using environment variables for authentication:
        api_key = get_secret('my-api-key', 'https://myvault.vault.azure.net')
        
        # Using client credentials:
        api_key = get_secret('my-api-key', 
                            'https://myvault.vault.azure.net',
                            client_id='app-id', 
                            client_secret='app-secret', 
                            tenant_id='tenant-id')
    """
    vault = KeyVaultUtils(vault_url)
    
    if client_id and client_secret and tenant_id:
        vault.initialize_with_client_secret(client_id, client_secret, tenant_id)
    else:
        vault.initialize_with_default_credential()
    
    return vault.get_secret(secret_name)


def get_secrets(secret_names: list, vault_url: Optional[str] = None,
                client_id: Optional[str] = None, 
                client_secret: Optional[str] = None,
                tenant_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Helper function to get multiple secrets from Azure Key Vault.
    
    Args:
        secret_names (list): List of secret names to retrieve
        vault_url (Optional[str]): The URL of the Azure Key Vault
        client_id (Optional[str]): Azure AD application client ID
        client_secret (Optional[str]): Azure AD application client secret
        tenant_id (Optional[str]): Azure AD tenant ID
        
    Returns:
        Dict[str, Any]: Dictionary of secret names and their values
        
    Usage:
        # Using environment variables for authentication:
        secrets = get_secrets(['api-key', 'db-password'], 'https://myvault.vault.azure.net')
        
        # Using client credentials:
        secrets = get_secrets(['api-key', 'db-password'], 
                             'https://myvault.vault.azure.net',
                             client_id='app-id', 
                             client_secret='app-secret', 
                             tenant_id='tenant-id')
        
        api_key = secrets['api-key']
        db_pass = secrets['db-password']
    """
    vault = KeyVaultUtils(vault_url)
    
    if client_id and client_secret and tenant_id:
        vault.initialize_with_client_secret(client_id, client_secret, tenant_id)
    else:
        vault.initialize_with_default_credential()
    
    return vault.get_secrets(secret_names)
