import os
from typing import Optional

class Config:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._initialized = True
            self._initialize_config()

    def _initialize_config(self):
        # Key Vault related
        self.key_vault_url = os.environ.get('AZURE_KEY_VAULT_URL')
        self.key_vault_client_id = os.environ.get('AZURE_KEY_VAULT_CLIENT_ID')
        self.key_vault_tenant_id = os.environ.get('AZURE_KEY_VAULT_TENANT_ID')
        self.key_vault_client_secret = os.environ.get('AZURE_KEY_VAULT_CLIENT_SECRET')

        self.key_vault_utils = None
        if self.key_vault_url and self.key_vault_client_id and self.key_vault_client_secret and self.key_vault_tenant_id:
            try:
                from pm_studio_mcp.utils.key_vault_utils import KeyVaultUtils
                self.key_vault_utils = KeyVaultUtils(vault_url=self.key_vault_url)
                self.key_vault_utils.initialize_with_client_secret(
                    client_id=self.key_vault_client_id,
                    client_secret=self.key_vault_client_secret,
                    tenant_id=self.key_vault_tenant_id
                )
            except Exception as e:
                print(f"Warning: KeyVaultUtils init failed: {e}")
                self.key_vault_utils = None
        else:
            print("Warning: Key Vault config not set, skip KeyVaultUtils initialization.")

        # Working directory configuration
        self.WORKING_PATH = os.environ.get('WORKING_PATH', os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../temp'))
        os.makedirs(self.WORKING_PATH, exist_ok=True)

        # Reddit API configuration
        self.REDDIT_CLIENT_ID = self._get_config_value('REDDIT_CLIENT_ID', 'reddit-client-id', 'REDDIT_CLIENT_ID', '')
        self.REDDIT_CLIENT_SECRET = self._get_config_value('REDDIT_CLIENT_SECRET', 'reddit-client-secret', None, '')

        # Data.ai API configuration
        self.DATA_AI_API_KEY = self._get_config_value('DATA_AI_API_KEY', 'data-ai-api-key', None, '')
        self.DATA_AI_GOOGLE_PLAY_ID = self._get_config_value('DATA_AI_GOOGLE_PLAY_ID', 'data-ai-google-play-id', 'DATA_AI_GOOGLE_PLAY_ID', 'com.example.app')
        self.DATA_AI_APP_STORE_ID = self._get_config_value('DATA_AI_APP_STORE_ID', 'data-ai-app-store-id', 'DATA_AI_APP_STORE_ID', '123456789')

        # User configuration
        self.USER_ALIAS = self._get_config_value('USER_ALIAS', None, 'USER_ALIAS', 'default_user')

        # Azure AI configuration
        self.AZURE_INFERENCE_API_KEY = self._get_config_value('AZURE_INFERENCE_API_KEY', 'azure-inference-api-key', None, '')
        self.AZURE_MODEL_NAME = self._get_config_value('AZURE_MODEL_NAME', None, 'AZURE_MODEL_NAME', 'DeepSeek-R1')

        # Titan API configuration
        self.TITAN_CLIENT_ID = self._get_config_value('TITAN_CLIENT_ID', 'titan-client-id', 'TITAN_CLIENT_ID', '')
        self.MICROSOFT_TENANT_ID = self._get_config_value('MICROSOFT_TENANT_ID', 'microsoft-tenant-id', 'MICROSOFT_TENANT_ID', '')
        self.TITAN_ENDPOINT = self._get_config_value('TITAN_ENDPOINT', 'titan-endpoint', 'TITAN_ENDPOINT', '')
        self.TITAN_SCOPE = self._get_config_value('TITAN_SCOPE', 'titan-scope', 'TITAN_SCOPE', '')

    def _get_config_value(self, env_var: str, key_vault_key: Optional[str], constant_attr: Optional[str], default_value: str) -> str:
        value = os.environ.get(env_var)
        if value:
            print(f"Using {env_var} from environment")
            return value
        if constant_attr:
            try:
                from pm_studio_mcp.constant import __dict__ as consts
                value = consts.get(constant_attr)
                if value is not None:
                    print(f"Using {env_var} from constant.py")
                    return value
            except Exception as e:
                print(f"Warning: Failed to get {env_var} from constant.py: {e}")
        if key_vault_key and self.key_vault_utils:
            try:
                value = self.key_vault_utils.get_secret(key_vault_key)
                if value:
                    print(f"Using {env_var} from Key Vault")
                    return value
            except Exception as e:
                print(f"Warning: Failed to get {env_var} from Key Vault: {e}")
        print(f"Using default value for {env_var}")
        return default_value

# Create global config instance
config = Config() 