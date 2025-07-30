"""
Titan Table Metadata Definition File
"""

import re
import difflib
from typing import Dict, List, Tuple, Optional
from pm_studio_mcp.utils.titan_tables.table_metadata import TABLE_METADATA, TEMPLATE_METADATA
from pm_studio_mcp.utils.matching_utils import normalize_string, word_match, find_best_match, find_all_matches

def find_table_by_template_name(template_name):
    """
    Find tables that contain a SQL template with the given name

    Args:
        template_name (str): Template name or keyword to search for

    Returns:
        list: List of (table_name, template_name, template_description) tuples for matching templates
              Returns empty list if no matches found
    """
    results = []
    template_name = template_name.lower()
    
    # First try exact match in TEMPLATE_METADATA
    if template_name in TEMPLATE_METADATA:
        template_info = TEMPLATE_METADATA[template_name]
        template = template_info["template_info"]
        results.append((
            template_info["table"],
            template["name"],
            template.get("description", "")
        ))
        # Do not return directly, continue to find fuzzy matches to avoid missing any.
    
    # Fuzzy match, return all related templates (deduplicated)
    matches = find_all_matches(template_name, TEMPLATE_METADATA, match_types=['word', 'pattern', 'fuzzy'], threshold=0.6)
    seen = set((r[0], r[1]["template_info"]["name"]) for r in results)  # (table, template_name)
    for match_name, match_info, score, match_type in matches:
        key = (match_info["table"], match_info["template_info"]["name"])
        if key not in seen:
            template = match_info["template_info"]
            results.append((
                match_info["table"],
                template["name"],
                template.get("description", "")
            ))
            seen.add(key)
    return results

def get_table_metadata(table_name):
    """
    Get metadata information for a specified table

    Args:
        table_name (str): Table name or keyword

    Returns:
        dict: Dictionary containing table metadata, including:
              - sample: Sample data showing the table structure
              - description: Table structure description
              - sample_query: Example query (for legacy tables)
              - filter_columns: Filter configurations (for template-based tables)
              - sql_templates: SQL templates with placeholders (for template-based tables)
              Returns None if table doesn't exist
    """
    # Convert TABLE_METADATA to a format suitable for matching functions
    metadata_dict = {key: value for key, value in TABLE_METADATA.items()}
    
    # Find the best match using our generic matching utility
    best_match = find_best_match(table_name, metadata_dict, match_type='auto', threshold=0.6)
    
    if best_match[0] is not None:
        return best_match[1]  # Return the metadata for the matched table
    
    return None

def get_table_metadata_extended(table_name):
    """
    Get extended metadata information for a specified table, including SQL templates and filter configurations

    Args:
        table_name (str): Table name or keyword

    Returns:
        dict: Dictionary containing extended table metadata including SQL_TEMPLATES and FILTER_COLUMNS if available
              Returns None if table doesn't exist or has no extended metadata
    """
    # First, find the matching table using standard method
    standard_metadata = get_table_metadata(table_name)

    if not standard_metadata:
        return None

    # Find the actual table name that was matched
    actual_table_name = None
    for key in TABLE_METADATA.keys():
        if TABLE_METADATA[key] == standard_metadata:
            actual_table_name = key
            break

    if not actual_table_name:
        return None

    # Initialize result dictionary
    extended_metadata = {}

    # Check if extended metadata is available in TABLE_METADATA
    table_meta = TABLE_METADATA[actual_table_name]
    if 'sql_templates' in table_meta:
        extended_metadata['sql_templates'] = table_meta['sql_templates']

    if 'filter_columns' in table_meta:
        extended_metadata['filter_columns'] = table_meta['filter_columns']

    return extended_metadata if extended_metadata else None
