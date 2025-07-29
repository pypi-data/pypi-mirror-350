"""
Validation utility functions for Taskinity.

This module contains utilities for validating JSON data and schemas.
"""
import json
from typing import Any, Dict, Optional, Union

def validate_json(data: str) -> Dict[str, Any]:
    """
    Validate that a string is valid JSON and return the parsed data.
    
    Args:
        data: JSON string to validate.
        
    Returns:
        Parsed JSON data as a dictionary.
        
    Raises:
        ValueError: If the data is not valid JSON.
    """
    try:
        return json.loads(data)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON data: {str(e)}")

def validate_schema(data: Dict[str, Any], schema: Dict[str, Any]) -> bool:
    """
    Validate that a JSON object conforms to a schema.
    
    This is a simple schema validator that checks for required fields and their types.
    For more complex validation, consider using a library like jsonschema.
    
    Args:
        data: JSON data to validate.
        schema: Schema definition with field names and expected types.
        
    Returns:
        True if the data conforms to the schema, False otherwise.
    """
    for field, field_schema in schema.items():
        # Check if required field is present
        if field_schema.get("required", False) and field not in data:
            raise ValueError(f"Required field '{field}' is missing")
        
        # Skip validation if field is not present and not required
        if field not in data:
            continue
        
        # Validate field type
        expected_type = field_schema.get("type")
        if expected_type:
            # Handle special case for null type
            if expected_type == "null" and data[field] is not None:
                raise ValueError(f"Field '{field}' should be null")
            
            # Map JSON schema types to Python types
            type_map = {
                "string": str,
                "number": (int, float),
                "integer": int,
                "boolean": bool,
                "object": dict,
                "array": list
            }
            
            if expected_type in type_map:
                python_type = type_map[expected_type]
                if not isinstance(data[field], python_type):
                    raise ValueError(f"Field '{field}' should be of type {expected_type}")
        
        # Validate nested objects
        if field_schema.get("type") == "object" and "properties" in field_schema:
            if field in data and isinstance(data[field], dict):
                validate_schema(data[field], field_schema["properties"])
        
        # Validate array items
        if field_schema.get("type") == "array" and "items" in field_schema:
            if field in data and isinstance(data[field], list):
                for item in data[field]:
                    if isinstance(item, dict) and isinstance(field_schema["items"], dict):
                        validate_schema(item, field_schema["items"].get("properties", {}))
    
    return True
