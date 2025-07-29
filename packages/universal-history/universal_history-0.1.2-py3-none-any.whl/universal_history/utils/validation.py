"""
Utility functions for validating data in the Universal History system.
"""
from datetime import datetime
from typing import Any, Dict, List, Optional, Union, Set

from ..models.event_record import DomainType, ContentType, SourceType, ConfidentialityLevel

def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> List[str]:
    """
    Validate that all required fields are present in the data.
    
    Args:
        data (Dict[str, Any]): The data to validate
        required_fields (List[str]): List of required field names
        
    Returns:
        List[str]: List of missing field names, empty if all required fields are present
    """
    missing_fields = []
    
    for field in required_fields:
        if field not in data or data[field] is None:
            missing_fields.append(field)
    
    return missing_fields

def validate_event_record(event_data: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Validate the data for an Event Record.
    
    Args:
        event_data (Dict[str, Any]): The event data to validate
        
    Returns:
        Dict[str, List[str]]: Dictionary of validation errors by field, empty if valid
    """
    errors: Dict[str, List[str]] = {}
    
    # Required fields
    required_fields = ["subject_id", "domain_type", "event_type", "raw_input", "source"]
    missing_fields = validate_required_fields(event_data, required_fields)
    if missing_fields:
        errors["required_fields"] = [f"Missing required field: {field}" for field in missing_fields]
    
    # Validate domain_type
    if "domain_type" in event_data and event_data["domain_type"] is not None:
        domain_type = event_data["domain_type"]
        if isinstance(domain_type, str):
            try:
                DomainType(domain_type)
            except ValueError:
                if "domain_type" not in errors:
                    errors["domain_type"] = []
                errors["domain_type"].append(f"Invalid domain type: {domain_type}")
    
    # Validate raw_input
    if "raw_input" in event_data and event_data["raw_input"] is not None:
        raw_input = event_data["raw_input"]
        
        # Check if raw_input is a dictionary
        if not isinstance(raw_input, dict):
            if "raw_input" not in errors:
                errors["raw_input"] = []
            errors["raw_input"].append("Raw input must be a dictionary")
        else:
            # Check required fields in raw_input
            raw_input_required = ["type", "content"]
            raw_input_missing = validate_required_fields(raw_input, raw_input_required)
            if raw_input_missing:
                if "raw_input" not in errors:
                    errors["raw_input"] = []
                errors["raw_input"].extend([f"Missing required field in raw_input: {field}" for field in raw_input_missing])
            
            # Validate content type
            if "type" in raw_input and raw_input["type"] is not None:
                content_type = raw_input["type"]
                if isinstance(content_type, str):
                    try:
                        ContentType(content_type)
                    except ValueError:
                        if "raw_input" not in errors:
                            errors["raw_input"] = []
                        errors["raw_input"].append(f"Invalid content type: {content_type}")
    
    # Validate source
    if "source" in event_data and event_data["source"] is not None:
        source = event_data["source"]
        
        # Check if source is a dictionary
        if not isinstance(source, dict):
            if "source" not in errors:
                errors["source"] = []
            errors["source"].append("Source must be a dictionary")
        else:
            # Check required fields in source
            source_required = ["type", "id", "name"]
            source_missing = validate_required_fields(source, source_required)
            if source_missing:
                if "source" not in errors:
                    errors["source"] = []
                errors["source"].extend([f"Missing required field in source: {field}" for field in source_missing])
            
            # Validate source type
            if "type" in source and source["type"] is not None:
                source_type = source["type"]
                if isinstance(source_type, str):
                    try:
                        SourceType(source_type)
                    except ValueError:
                        if "source" not in errors:
                            errors["source"] = []
                        errors["source"].append(f"Invalid source type: {source_type}")
    
    # Validate metadata if present
    if "metadata" in event_data and event_data["metadata"] is not None:
        metadata = event_data["metadata"]
        
        # Check if metadata is a dictionary
        if not isinstance(metadata, dict):
            if "metadata" not in errors:
                errors["metadata"] = []
            errors["metadata"].append("Metadata must be a dictionary")
        else:
            # Validate confidentiality level
            if "confidentiality_level" in metadata and metadata["confidentiality_level"] is not None:
                confidentiality_level = metadata["confidentiality_level"]
                if isinstance(confidentiality_level, str):
                    try:
                        ConfidentialityLevel(confidentiality_level)
                    except ValueError:
                        if "metadata" not in errors:
                            errors["metadata"] = []
                        errors["metadata"].append(f"Invalid confidentiality level: {confidentiality_level}")
    
    return errors

def validate_synthesis(synthesis_data: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Validate the data for a Trajectory Synthesis.
    
    Args:
        synthesis_data (Dict[str, Any]): The synthesis data to validate
        
    Returns:
        Dict[str, List[str]]: Dictionary of validation errors by field, empty if valid
    """
    errors: Dict[str, List[str]] = {}
    
    # Required fields
    required_fields = ["subject_id", "domain_type", "time_frame", "summary"]
    missing_fields = validate_required_fields(synthesis_data, required_fields)
    if missing_fields:
        errors["required_fields"] = [f"Missing required field: {field}" for field in missing_fields]
    
    # Validate domain_type
    if "domain_type" in synthesis_data and synthesis_data["domain_type"] is not None:
        domain_type = synthesis_data["domain_type"]
        if isinstance(domain_type, str):
            try:
                DomainType(domain_type)
            except ValueError:
                if "domain_type" not in errors:
                    errors["domain_type"] = []
                errors["domain_type"].append(f"Invalid domain type: {domain_type}")
    
    # Validate time_frame
    if "time_frame" in synthesis_data and synthesis_data["time_frame"] is not None:
        time_frame = synthesis_data["time_frame"]
        
        # Check if time_frame is a dictionary
        if not isinstance(time_frame, dict):
            if "time_frame" not in errors:
                errors["time_frame"] = []
            errors["time_frame"].append("Time frame must be a dictionary")
        else:
            # Check required fields in time_frame
            time_frame_required = ["start", "end"]
            time_frame_missing = validate_required_fields(time_frame, time_frame_required)
            if time_frame_missing:
                if "time_frame" not in errors:
                    errors["time_frame"] = []
                errors["time_frame"].extend([f"Missing required field in time_frame: {field}" for field in time_frame_missing])
            
            # Validate dates
            try:
                if "start" in time_frame and time_frame["start"] is not None:
                    if isinstance(time_frame["start"], str):
                        start_date = datetime.fromisoformat(time_frame["start"])
                    else:
                        if "time_frame" not in errors:
                            errors["time_frame"] = []
                        errors["time_frame"].append("Start date must be an ISO format string")
                
                if "end" in time_frame and time_frame["end"] is not None:
                    if isinstance(time_frame["end"], str):
                        end_date = datetime.fromisoformat(time_frame["end"])
                    else:
                        if "time_frame" not in errors:
                            errors["time_frame"] = []
                        errors["time_frame"].append("End date must be an ISO format string")
                
                # Check that end date is after start date
                if "start" in time_frame and "end" in time_frame and time_frame["start"] is not None and time_frame["end"] is not None:
                    if isinstance(time_frame["start"], str) and isinstance(time_frame["end"], str):
                        start_date = datetime.fromisoformat(time_frame["start"])
                        end_date = datetime.fromisoformat(time_frame["end"])
                        if end_date < start_date:
                            if "time_frame" not in errors:
                                errors["time_frame"] = []
                            errors["time_frame"].append("End date must be after start date")
            
            except ValueError as e:
                if "time_frame" not in errors:
                    errors["time_frame"] = []
                errors["time_frame"].append(f"Invalid date format: {e}")
    
    return errors

def validate_state_document(state_data: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Validate the data for a State Document.
    
    Args:
        state_data (Dict[str, Any]): The state document data to validate
        
    Returns:
        Dict[str, List[str]]: Dictionary of validation errors by field, empty if valid
    """
    errors: Dict[str, List[str]] = {}
    
    # Required fields
    required_fields = ["subject_id", "general_summary", "domains"]
    missing_fields = validate_required_fields(state_data, required_fields)
    if missing_fields:
        errors["required_fields"] = [f"Missing required field: {field}" for field in missing_fields]
    
    # Validate domains
    if "domains" in state_data and state_data["domains"] is not None:
        domains = state_data["domains"]
        
        # Check if domains is a dictionary
        if not isinstance(domains, dict):
            if "domains" not in errors:
                errors["domains"] = []
            errors["domains"].append("Domains must be a dictionary")
        else:
            # Validate each domain
            for domain_key, domain_state in domains.items():
                # Check if domain_state is a dictionary
                if not isinstance(domain_state, dict):
                    if "domains" not in errors:
                        errors["domains"] = []
                    errors["domains"].append(f"Domain state for {domain_key} must be a dictionary")
                    continue
                
                # Check required fields in domain_state
                domain_required = ["last_updated", "current_status"]
                domain_missing = validate_required_fields(domain_state, domain_required)
                if domain_missing:
                    if "domains" not in errors:
                        errors["domains"] = []
                    errors["domains"].extend([f"Missing required field in domain {domain_key}: {field}" for field in domain_missing])
    
    return errors

def validate_domain_catalog(catalog_data: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Validate the data for a Domain Catalog.
    
    Args:
        catalog_data (Dict[str, Any]): The domain catalog data to validate
        
    Returns:
        Dict[str, List[str]]: Dictionary of validation errors by field, empty if valid
    """
    errors: Dict[str, List[str]] = {}
    
    # Required fields
    required_fields = ["domain_type", "organization"]
    missing_fields = validate_required_fields(catalog_data, required_fields)
    if missing_fields:
        errors["required_fields"] = [f"Missing required field: {field}" for field in missing_fields]
    
    # Validate domain_type
    if "domain_type" in catalog_data and catalog_data["domain_type"] is not None:
        domain_type = catalog_data["domain_type"]
        if isinstance(domain_type, str):
            try:
                DomainType(domain_type)
            except ValueError:
                if "domain_type" not in errors:
                    errors["domain_type"] = []
                errors["domain_type"].append(f"Invalid domain type: {domain_type}")
    
    # Validate organization
    if "organization" in catalog_data and catalog_data["organization"] is not None:
        organization = catalog_data["organization"]
        
        # Check if organization is a dictionary
        if not isinstance(organization, dict):
            if "organization" not in errors:
                errors["organization"] = []
            errors["organization"].append("Organization must be a dictionary")
        else:
            # Check required fields in organization
            org_required = ["id", "name"]
            org_missing = validate_required_fields(organization, org_required)
            if org_missing:
                if "organization" not in errors:
                    errors["organization"] = []
                errors["organization"].extend([f"Missing required field in organization: {field}" for field in org_missing])
    
    return errors

def is_valid_iso_date(date_str: str) -> bool:
    """
    Check if a string is a valid ISO format date.
    
    Args:
        date_str (str): The date string to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        datetime.fromisoformat(date_str)
        return True
    except (ValueError, TypeError):
        return False

def is_valid_domain_type(domain_type: str) -> bool:
    """
    Check if a string is a valid domain type.
    
    Args:
        domain_type (str): The domain type to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        DomainType(domain_type)
        return True
    except ValueError:
        return False

def get_valid_domain_types() -> Set[str]:
    """
    Get the set of valid domain types.
    
    Returns:
        Set[str]: Set of valid domain type values
    """
    return {domain_type.value for domain_type in DomainType}