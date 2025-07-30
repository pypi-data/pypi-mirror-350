"""
Constants used in the PM Studio MCP server.
"""

# =====================
# File patterns
# =====================
QUERY_RESULT_PATTERN = "query_result.csv"
UNWRAP_FEEDBACK_PATTERN = "Unwrap_Feedback*.csv"

# =====================
# Output file names
# =====================
OCV_CLEANED_FILE = "ocv_data_cleaned.csv"
UNWRAP_CLEANED_FILE = "unwrap_data_cleaned.csv"
ALL_DATA_CLEANED_FILE = "all_data_cleaned.csv"
FINAL_RESULT_FILE = "final_result.csv"

# =====================
# Column indexes and names
# =====================
OCV_COLUMN_INDEX = 38  # 39th column (0-based index)
UNWRAP_DEFAULT_COLUMN_INDEX = 2  # 3rd column (0-based index)
UNWRAP_COLUMN_NAME = "Entry Text"
OCV_COLUMN_NAME = "Issue[0].Title"  # For OCV clean tool

# =====================
# Greeting message template
# =====================
GREETING_TEMPLATE = "hello, {name}! How can I help you today? I can help you to do competitor analysis, user feedback summary, write docs and more!"

# =====================
# Configuration constants (placeholders, please update with real values as needed)
# =====================

# Reddit API configuration
REDDIT_CLIENT_ID = "your_reddit_client_id"  # Reddit API client ID

# Data.ai API configuration
DATA_AI_GOOGLE_PLAY_ID = "20600008137685"  # Data.ai Google Play app ID
DATA_AI_APP_STORE_ID = "1288723196"  # Data.ai App Store app ID

# User configuration
USER_ALIAS = "your_user_alias"  # Default user alias

# Azure AI configuration
AZURE_MODEL_NAME = "your_azure_model_name"  # Azure AI model name

# Titan API configuration
TITAN_CLIENT_ID = "dcca0492-ea09-452c-bf98-3750d4331d33"  # Titan API client ID
MICROSOFT_TENANT_ID = "72f988bf-86f1-41af-91ab-2d7cd011db47"  # Microsoft tenant ID
TITAN_ENDPOINT = "https://titanapi.westus2.cloudapp.azure.com/v2/query"  # Titan API endpoint
TITAN_SCOPE = "api://dcca0492-ea09-452c-bf98-3750d4331d33/signin"  # Titan API scope

# Graph API configuration 
GRAPH_CLIENT_ID = "684f658a-cdb0-4ef5-a087-a54c064751b2"
GRAPH_TENANT_ID = "72f988bf-86f1-41af-91ab-2d7cd011db47"
