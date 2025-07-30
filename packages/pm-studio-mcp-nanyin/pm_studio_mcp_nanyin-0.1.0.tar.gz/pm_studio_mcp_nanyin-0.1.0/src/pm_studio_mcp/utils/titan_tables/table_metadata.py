"""
Titan Table Metadata Dictionary Definition File
"""

# Import table metadata
from pm_studio_mcp.utils.titan_tables.edgemacecsretentionv1 import (
    SAMPLE as EDGE_MAC_ECS_RETENTION_SAMPLE,
    DESCRIPTION as EDGE_MAC_ECS_RETENTION_DESC,
    FILTER_COLUMNS as EDGE_MAC_ECS_RETENTION_FILTER_COLUMNS,
    SQL_TEMPLATES as EDGE_MAC_ECS_RETENTION_SQL_TEMPLATES
)
from pm_studio_mcp.utils.titan_tables.KPI_DailyUser import (
    SAMPLE as KPI_DAILY_USER_SAMPLE,
    DESCRIPTION as KPI_DAILY_USER_DESC,
    FILTER_COLUMNS as KPI_DAILY_USER_FILTER_COLUMNS,
    SQL_TEMPLATES as KPI_DAILY_USER_SQL_TEMPLATES
)
from pm_studio_mcp.utils.titan_tables.KPI_BrowserMinutes_All import (
    SAMPLE as KPI_BROWSER_MINUTES_ALL_SAMPLE,
    DESCRIPTION as KPI_BROWSER_MINUTES_ALL_DESC,
    FILTER_COLUMNS as KPI_BROWSER_MINUTES_ALL_FILTER_COLUMNS,
    SQL_TEMPLATES as KPI_BROWSER_MINUTES_ALL_SQL_TEMPLATES
)

# Define table metadata dictionary
# Each table entry contains:
# - sample: Sample data showing the table structure
# - description: Detailed description of the table's purpose and contents
# - filter_columns: Available filters and their configurations
# - sql_templates: Pre-defined SQL query templates with:
#   * name: Unique identifier for the template
#   * description: Brief explanation of the query purpose
#   * template: SQL query with placeholders
#   * required_filters: List of filters that must be provided
#   * optional_filters: List of filters that are optional
#   * template_params: Dynamic parameter processing functions for complex filters
TABLE_METADATA = {
    # Edge Mac retention data table
    # Contains user retention metrics for Edge browser on Mac
    "EdgeMacECSRetentionV1": {
        "sample": EDGE_MAC_ECS_RETENTION_SAMPLE,
        "description": EDGE_MAC_ECS_RETENTION_DESC,
        "filter_columns": EDGE_MAC_ECS_RETENTION_FILTER_COLUMNS,
        "sql_templates": EDGE_MAC_ECS_RETENTION_SQL_TEMPLATES
    },
    # Daily active user metrics table
    # Contains user activity data across different platforms and regions
    "KPI_DailyUser": {
        "sample": KPI_DAILY_USER_SAMPLE,
        "description": KPI_DAILY_USER_DESC,
        "filter_columns": KPI_DAILY_USER_FILTER_COLUMNS,
        "sql_templates": KPI_DAILY_USER_SQL_TEMPLATES
    },
    # Browser usage minutes table
    # Contains detailed browser usage metrics with various filtering options
    "KPI_BrowserMinutes_All": {
        "sample": KPI_BROWSER_MINUTES_ALL_SAMPLE,
        "description": KPI_BROWSER_MINUTES_ALL_DESC,
        "filter_columns": KPI_BROWSER_MINUTES_ALL_FILTER_COLUMNS,
        "sql_templates": KPI_BROWSER_MINUTES_ALL_SQL_TEMPLATES
    }
}

# Define template metadata dictionary for quick template lookup
# This dictionary is populated with:
# - Full template names as keys
# - Individual keywords from template names as additional keys
# Each key points to the complete template information including:
# - table: The source table name
# - template_info: The complete template definition
# - table_description: Description of the source table
# - filter_columns: Available filters for the template
TEMPLATE_METADATA = {}

# Populate template metadata
for table_name, table_info in TABLE_METADATA.items():
    if "sql_templates" in table_info:
        for template in table_info["sql_templates"]:
            if "name" in template:
                template_name = template["name"].lower()
                template_info = {
                    "table": table_name,
                    "template_info": template,
                    "table_description": table_info["description"],
                    "filter_columns": table_info.get("filter_columns", {})
                }
                # Store the main template entry
                TEMPLATE_METADATA[template_name] = template_info
                
                # Add keywords for fuzzy matching, but only store references
                for keyword in template_name.split():
                    if keyword not in TEMPLATE_METADATA:
                        TEMPLATE_METADATA[keyword] = template_info
