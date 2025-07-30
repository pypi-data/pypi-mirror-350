import os
import sys
import json
from pathlib import Path
from msal import PublicClientApplication
from pm_studio_mcp.config import config
from pm_studio_mcp.constant import __dict__ as consts

# Ensure the environment are set, use constant values as default if not

def get_secret_safe(utils, key):
    try:
        return utils.get_secret(key) if utils else None
    except Exception:
        return None

class AuthUtils:
    # Class variables for script mode and token storage
    temp_token_dir = os.environ.get('TEMP_TOKEN_DIR')
    SCRIPT_MODE = False if temp_token_dir is None else True
    token_file = Path(temp_token_dir) / "auth_token.json" if temp_token_dir else None
    
    # Graph API Configuration, used for auth and sending messages
    client_id = (
        os.environ.get('GRAPH_CLIENT_ID')
        or consts.get('GRAPH_CLIENT_ID')
        or get_secret_safe(config.key_vault_utils, "graph-client-id")
    )
    tenant_id = (
        os.environ.get('GRAPH_TENANT_ID')
        or consts.get('GRAPH_TENANT_ID')
        or get_secret_safe(config.key_vault_utils, "graph-tenant-id")
    )
    scopes = os.environ.get('GRAPH_SCOPE') if os.environ.get('GRAPH_SCOPE') else ["https://graph.microsoft.com/.default"]
    authority = f"https://login.microsoftonline.com/{tenant_id}"

    app = PublicClientApplication(
        client_id=client_id,
        authority=authority,
        # enable_broker_on_mac=True if sys.platform == "darwin" else False, #needed for broker-based flow
        # enable_broker_on_windows=True if sys.platform == "win32" else False, #needed for broker-based flow
    )

    @classmethod
    def save_token(cls, token_data):
        """
        Save the token data to a temporary file.
        
        Args:
            token_data (dict): The token data to save
        """
        if not cls.temp_token_dir or not cls.token_file:
            raise ValueError("Cannot save token: temp_token_dir is not set")
            
        # Create temp directory if it doesn't exist
        os.makedirs(cls.temp_token_dir, exist_ok=True) 

        # Write token data to file
        with open(cls.token_file, 'w') as f:
            json.dump({"access_token": token_data}, f)
        
        print(f"Token saved to {cls.token_file}")

    
    @classmethod
    def load_token(cls):
        """
        Load the token data from the temporary file.
        
        Returns:
            str or None: The access token if available, None otherwise
        """
        if not cls.token_file:
            print("Cannot load token: token_file is not set")
            return None
            
        try:
            if cls.token_file.exists():
                with open(cls.token_file, 'r') as f:
                    data = json.load(f)
                    return data.get("access_token")
        except Exception as e:
            print(f"Error loading token: {str(e)}")
        return None
    

    @classmethod
    def validate_token(cls, token=None):
        """
        Validate the access token to ensure it's still valid.
        
        Args:
            token (str, optional): The token to validate. If None, load from file.
            
        Returns:
            bool: True if token is valid, False otherwise
        """
        if not token:
            token = cls.load_token()
            
        if not token:
            print("No token found to validate")
            return False
            
        try:
            # The simplest way to validate a token is to try using it
            # Try a lightweight call to Microsoft Graph API
            import requests
            
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            # Make a simple call to the /me endpoint
            response = requests.get(
                'https://graph.microsoft.com/v1.0/me',
                headers=headers
            )
            
            if response.status_code == 200:
                print("Token is valid")
                return True
            else:
                print(f"Token validation failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"Error validating token: {str(e)}")
            return False

    @staticmethod
    def login():
        """
        Authenticate with MSAL and return the access token.

        Returns:
            str: The access token
        """
        
        # if app is not None: print("Using MSAL app instance:", app)

        try:
            print("Authenticating...")

            if AuthUtils.SCRIPT_MODE:
                print("Running in script mode, using file cached token.")
                # In script mode, we use the file cached token
                if AuthUtils.validate_token():
                    token = AuthUtils.load_token()

                    headers = {
                        'Authorization': f'Bearer {token}',
                        'Content-Type': 'application/json'
                    }
                    
                    # Get user info from Microsoft Graph
                    import requests
                    response = requests.get(
                        'https://graph.microsoft.com/v1.0/me',
                        headers=headers
                    )

                    # userPrincipalName = response.json().get('userPrincipalName', 'Unknown User')
                    account = response.json()

                    result = AuthUtils.app.acquire_token_silent(
                        AuthUtils.scopes, 
                        account=account,
                        force_refresh=True # Get new token even if the cached one is not expired
                    )

                    if result: 
                        AuthUtils.save_token(result['access_token'])
                        print("Token refreshed and saved.")
                    
                    print("Token loaded from file.")
                    return token
                else:
                    print("No valid token found, please authenticate interactively.")
                    # In script mode, we need to authenticate interactively
                    result = AuthUtils.app.acquire_token_interactive(
                        AuthUtils.scopes
                    )

                    if "access_token" not in result:
                        print(f"Authentication failed: {result.get('error_description', 'Unknown error')}")
                        sys.exit(1)

                    print("Authentication successful!")
                    AuthUtils.save_token(result["access_token"])
                    return result["access_token"]

            # In interactive mode, we try to get the token silently first
            print("Running in interactive mode, trying to get token silently.", flush=True)
            accounts = AuthUtils.app.get_accounts()
            print(f"Found {len(accounts)} cached accounts.")
            if accounts:
                print ("Found cached account: ")
                for account in accounts:
                    print(f"  {account['username']}")
                
                result = AuthUtils.app.acquire_token_silent(
                    AuthUtils.scopes, 
                    account=accounts[0],
                    force_refresh=True # Get new token even if the cached one is not expired
                )
                                                            
                if result:
                    return result['access_token']

            # If no cached token, do interactive authentication
            result = AuthUtils.app.acquire_token_interactive(
                AuthUtils.scopes
                # port=0,  # Specify the port if needed
                # parent_window_handle=msal.PublicClientApplication.CONSOLE_WINDOW_HANDLE #needed for broker-based flow
            )

            if "access_token" not in result:
                print(f"Authentication failed: {result.get('error_description', 'Unknown error')}")
                sys.exit(1)

            print("Authentication successful!")
            return result["access_token"]

        except Exception as e:
            print(f"Authentication error: {str(e)}")
            sys.exit(1)
