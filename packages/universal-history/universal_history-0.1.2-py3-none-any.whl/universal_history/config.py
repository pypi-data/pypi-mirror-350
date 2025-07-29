"""
Configuration module for the Universal History system.
"""
import os
from enum import Enum
from typing import Dict, Any, Optional

class StorageType(str, Enum):
    """Type of storage backend."""
    MEMORY = "memory"
    FILE = "file"
    MONGODB = "mongodb"

class Config:
    """Configuration class for the Universal History system."""
    
    # Default values
    DEFAULT_STORAGE_TYPE = StorageType.MEMORY
    DEFAULT_STORAGE_DIR = "./universal_history_data"
    DEFAULT_MONGODB_CONNECTION = "mongodb://localhost:27017/"
    DEFAULT_MONGODB_DATABASE = "universal_history"
    
    def __init__(self, config_dict: Optional[Dict[str, Any]] = None):
        """
        Initialize the configuration.
        
        Args:
            config_dict (Optional[Dict[str, Any]]): Configuration dictionary
        """
        self.config = {}
        
        # Set default values
        self.config["storage_type"] = self._get_env_or_default(
            "UNIVERSAL_HISTORY_STORAGE_TYPE", 
            self.DEFAULT_STORAGE_TYPE.value
        )
        
        self.config["storage_dir"] = self._get_env_or_default(
            "UNIVERSAL_HISTORY_STORAGE_DIR", 
            self.DEFAULT_STORAGE_DIR
        )
        
        self.config["mongodb_connection"] = self._get_env_or_default(
            "UNIVERSAL_HISTORY_MONGODB_CONNECTION", 
            self.DEFAULT_MONGODB_CONNECTION
        )
        
        self.config["mongodb_database"] = self._get_env_or_default(
            "UNIVERSAL_HISTORY_MONGODB_DATABASE", 
            self.DEFAULT_MONGODB_DATABASE
        )
        
        # Update with provided config dictionary
        if config_dict:
            self.config.update(config_dict)
    
    def _get_env_or_default(self, env_var: str, default: str) -> str:
        """
        Get a value from environment variable or use default.
        
        Args:
            env_var (str): Environment variable name
            default (str): Default value
            
        Returns:
            str: The value
        """
        return os.environ.get(env_var, default)
    
    @property
    def storage_type(self) -> StorageType:
        """Get the storage type."""
        return StorageType(self.config["storage_type"])
    
    @storage_type.setter
    def storage_type(self, value: StorageType):
        """Set the storage type."""
        self.config["storage_type"] = value.value
    
    @property
    def storage_dir(self) -> str:
        """Get the storage directory."""
        return self.config["storage_dir"]
    
    @storage_dir.setter
    def storage_dir(self, value: str):
        """Set the storage directory."""
        self.config["storage_dir"] = value
    
    @property
    def mongodb_connection(self) -> str:
        """Get the MongoDB connection string."""
        return self.config["mongodb_connection"]
    
    @mongodb_connection.setter
    def mongodb_connection(self, value: str):
        """Set the MongoDB connection string."""
        self.config["mongodb_connection"] = value
    
    @property
    def mongodb_database(self) -> str:
        """Get the MongoDB database name."""
        return self.config["mongodb_database"]
    
    @mongodb_database.setter
    def mongodb_database(self, value: str):
        """Set the MongoDB database name."""
        self.config["mongodb_database"] = value
    
    def get_repository_args(self) -> Dict[str, Any]:
        """
        Get arguments for initializing a repository based on the configuration.
        
        Returns:
            Dict[str, Any]: Repository initialization arguments
        """
        if self.storage_type == StorageType.MEMORY:
            return {}
        elif self.storage_type == StorageType.FILE:
            return {"storage_dir": self.storage_dir}
        elif self.storage_type == StorageType.MONGODB:
            return {
                "connection_string": self.mongodb_connection,
                "database_name": self.mongodb_database
            }
        else:
            raise ValueError(f"Unsupported storage type: {self.storage_type}")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the configuration to a dictionary.
        
        Returns:
            Dict[str, Any]: The configuration dictionary
        """
        return self.config.copy()

# Global configuration instance
config = Config()

def configure(config_dict: Dict[str, Any]) -> None:
    """
    Configure the Universal History system.
    
    Args:
        config_dict (Dict[str, Any]): Configuration dictionary
    """
    global config
    config = Config(config_dict)