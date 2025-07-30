from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential
from datetime import datetime
import requests
import pandas as pd
import os
import importlib.util
import sys
import re

# Import table metadata module
from pm_studio_mcp.utils.titan_table_metadata import get_table_metadata
from pm_studio_mcp.config import config

class TitanQuery:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(TitanQuery, cls).__new__(cls)
        return cls._instance

    def __init__(self, titan_client_id, microsoft_tenant_id, titan_endpoint, titan_scope, user_alias=None, ):
        if self._initialized:
            return

        # Read USER_ALIAS from environment variables
        if user_alias is not None:
            self.user_alias = user_alias
        elif 'USER_ALIAS' in os.environ:
            self.user_alias = os.environ['USER_ALIAS']
            print(f"Using configured user alias from environment: {self.user_alias}")
        else:
            # Set default value for testing
            self.user_alias = config.USER_ALIAS
            print(f"Using default user alias for testing: {self.user_alias}")

        # Use credentials from constant.py
        self.titan_client_id = titan_client_id
        self.microsoft_tenant_id = microsoft_tenant_id

        self.endpoint = titan_endpoint
        self.titan_scope = titan_scope
        self.credential = InteractiveBrowserCredential(
            client_id=self.titan_client_id, tenant_id=self.microsoft_tenant_id
        )
        self.access_token = (
            "Bearer " + self.credential.get_token(self.titan_scope).token
        )
        self._initialized = True

    def query_data_from_titan_tool(self, query_str, table, output_dir=None):
        """
        Query data from Titan tool and save directly to file

        Args:
            query_str (str): Query string
            table (str): Table name, can be in format "{database_name}.{table_name}"
            output_dir (str, optional): Output directory path, defaults to config.WORKING_PATH

        Returns:
            dict: Dictionary containing:
                - 'file_path': Path to the output file
                - 'row_count': Total number of rows
                - 'message': Status message
        """
        # Use default working path from config if output_dir is not provided
        if output_dir is None:
            output_dir = config.WORKING_PATH
            
        try:
            # Extract table name if it's in format {database_name}.{table_name}
            simple_table_name = table.split('.')[-1] if '.' in table else table
            
            # Clean up quotes if they exist
            simple_table_name = simple_table_name.strip("'").strip('"')
            
            # Clean up the query string to ensure it uses the simple table name
            # Replace patterns like: 'database'.'table' or "database"."table" or database.table with just the table name
            if '.' in query_str:
                # Various database.table pattern replacements
                patterns = [
                    r"'[^']+'\.'[^']+'",  # 'database'.'table'
                    r'"[^"]+"\."[^"]+"',   # "database"."table"
                    r'`[^`]+`\.`[^`]+`',   # `database`.`table`
                    r"\b\w+\.\w+\b"        # database.table (without quotes)
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, query_str)
                    for match in matches:
                        # Extract the table part from the match
                        table_part = match.split('.')[-1].strip("'").strip('"').strip('`')
                        # Only replace if this looks like our target table
                        if table_part.lower() == simple_table_name.lower():
                            query_str = query_str.replace(match, simple_table_name)
            
            api_headers = {
                "Authorization": self.access_token,
                "Content-Type": "application/json",
            }
            api_body = {
                "query": query_str,
                "TableName": simple_table_name,
                "UserAlias": self.user_alias,
                "CreatedTimeUtc": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                "UseCache": True,
                "UseDefaultDatabaseName": True,
            }

            response = requests.post(self.endpoint, json=api_body, headers=api_headers)

            # Check response status code
            if response.status_code != 200:
                return {
                    'file_path': None,
                    'row_count': 0,
                    'message': f"API request failed with status code {response.status_code}: {response.text}"
                }

            # Try to parse JSON response
            try:
                response_json = response.json()
            except ValueError as e:
                return {
                    'file_path': None,
                    'row_count': 0,
                    'message': f"Failed to parse API response as JSON: {str(e)}"
                }

            # Check response structure
            if "Result" not in response_json or "data" not in response_json["Result"]:
                return {
                    'file_path': None,
                    'row_count': 0,
                    'message': f"Invalid API response structure: {response_json}"
                }

            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)

            # Generate output file path
            output_file = os.path.join(output_dir, f"titan_query_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")

            # Convert data to DataFrame and get information
            try:
                data = pd.DataFrame(response_json["Result"]["data"])
                # Save to CSV
                data.to_csv(output_file, index=False)

                # Prepare return information
                result = {
                    'file_path': output_file,
                    'row_count': len(data),
                    'message': 'Successfully retrieved data from Titan'
                }

                print(f"Successfully saved query results to: {output_file}")
                print(f"Total rows: {result['row_count']}")
                return result

            except Exception as e:
                return {
                    'file_path': None,
                    'row_count': 0,
                    'message': f"Failed to save data to CSV: {str(e)}"
                }

        except requests.exceptions.RequestException as e:
            return {
                'file_path': None,
                'row_count': 0,
                'message': f"API request failed: {str(e)}"
            }
        except Exception as e:
            return {
                'file_path': None,
                'row_count': 0,
                'message': f"Unexpected error: {str(e)}"
            }

