"""
Configuration utilities for the MCP server.
"""
import os
from typing import Dict, Any, Optional


class Config:
    """Configuration manager for the MCP server."""
    
    @staticmethod
    def get_env_var(name: str, default: Any = None) -> Any:
        """
        Get an environment variable.
        
        Args:
            name: Name of the environment variable
            default: Default value if the environment variable is not set
            
        Returns:
            Value of the environment variable or default
        """
        return os.environ.get(name, default)
    
    @staticmethod
    def get_kubeconfig_path() -> Optional[str]:
        """
        Get the path to the kubeconfig file.
        
        Returns:
            Path to the kubeconfig file or None if not set
        """
        return Config.get_env_var("KUBECONFIG")
    
    @staticmethod
    def get_openweather_api_key() -> Optional[str]:
        """
        Get the OpenWeather API key.
        
        Returns:
            OpenWeather API key or None if not set
        """
        return Config.get_env_var("OPENWEATHER_API_KEY")
    
    @staticmethod
    def get_mongodb_uri() -> str:
        """
        Get the MongoDB URI.
        
        Returns:
            MongoDB URI or default localhost URI
        """
        return Config.get_env_var("MONGODB_URI", "mongodb://localhost:27017")
    
    @staticmethod
    def get_redis_uri() -> str:
        """
        Get the Redis URI.
        
        Returns:
            Redis URI or default localhost URI
        """
        return Config.get_env_var("REDIS_URI", "redis://localhost:6379")
    
    @staticmethod
    def get_mysql_config() -> Dict[str, Any]:
        """
        Get the MySQL configuration.
        
        Returns:
            MySQL configuration dictionary
        """
        return {
            "host": Config.get_env_var("MYSQL_HOST", "localhost"),
            "port": int(Config.get_env_var("MYSQL_PORT", "3306")),
            "user": Config.get_env_var("MYSQL_USER", "root"),
            "password": Config.get_env_var("MYSQL_PASSWORD", ""),
            "database": Config.get_env_var("MYSQL_DATABASE", ""),
        }