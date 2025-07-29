"""
Utility functions for hashing and integrity verification.
"""
import hashlib
import json
from typing import Any, Dict, Optional

def calculate_hash(data: Dict[str, Any]) -> str:
    """
    Calculate a SHA-256 hash of a dictionary.
    
    Args:
        data (Dict[str, Any]): The data to hash
        
    Returns:
        str: Hexadecimal representation of the hash
    """
    # Convert to a canonical string representation
    data_str = json.dumps(data, sort_keys=True, default=str)
    
    # Calculate the hash
    return hashlib.sha256(data_str.encode()).hexdigest()

def verify_hash(data: Dict[str, Any], expected_hash: str) -> bool:
    """
    Verify that a dictionary matches an expected hash.
    
    Args:
        data (Dict[str, Any]): The data to verify
        expected_hash (str): The expected hash
        
    Returns:
        bool: True if the hash matches, False otherwise
    """
    # Calculate the hash
    actual_hash = calculate_hash(data)
    
    # Compare with the expected hash
    return actual_hash == expected_hash

def verify_hash_chain(items: list, hash_getter, previous_hash_getter) -> bool:
    """
    Verify the integrity of a hash chain.
    
    Args:
        items (list): List of items in the chain, ordered by time
        hash_getter: Function to get the current hash from an item
        previous_hash_getter: Function to get the previous hash from an item
        
    Returns:
        bool: True if the chain is valid, False otherwise
    """
    if not items:
        return True  # Empty chain is valid
    
    # First item should have no previous hash (or it's None)
    first_item = items[0]
    previous_hash = previous_hash_getter(first_item)
    if previous_hash and previous_hash.strip():
        return False
    
    # Check the chain
    for i in range(1, len(items)):
        current_item = items[i]
        previous_item = items[i-1]
        
        # The current item's previous hash should match the previous item's hash
        if previous_hash_getter(current_item) != hash_getter(previous_item):
            return False
    
    return True

def create_hash_chain(items: list, hash_generator, previous_hash_setter) -> None:
    """
    Create a hash chain from a list of items.
    
    Args:
        items (list): List of items to chain, ordered by time
        hash_generator: Function to generate a hash for an item
        previous_hash_setter: Function to set the previous hash on an item
    """
    if not items:
        return  # Nothing to do
    
    previous_hash = None
    
    for item in items:
        # Set the previous hash
        previous_hash_setter(item, previous_hash)
        
        # Generate the current hash
        current_hash = hash_generator(item)
        
        # Update previous hash for the next item
        previous_hash = current_hash