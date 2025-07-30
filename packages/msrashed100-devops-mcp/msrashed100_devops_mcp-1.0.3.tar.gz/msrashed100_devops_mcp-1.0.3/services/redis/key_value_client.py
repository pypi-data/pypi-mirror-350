"""
Redis key-value client for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List, Union

from services.redis.client import RedisService


class RedisKeyValueClient:
    """Client for Redis key-value operations."""
    
    def __init__(self, redis_service: RedisService):
        """
        Initialize the Redis key-value client.
        
        Args:
            redis_service: The base Redis service
        """
        self.redis = redis_service
        self.logger = redis_service.logger
    
    def get_keys(self, pattern: str = "*", limit: int = 100) -> List[str]:
        """
        Get keys matching a pattern.
        
        Args:
            pattern: Pattern to match keys against
            limit: Maximum number of keys to return
            
        Returns:
            List of matching keys
        """
        try:
            # Get keys matching the pattern
            keys = self.redis.client.keys(pattern)
            
            # Apply limit
            if len(keys) > limit:
                keys = keys[:limit]
            
            return keys
        except Exception as e:
            self.redis._handle_error(f"get_keys({pattern})", e)
    
    def get_value(self, key: str) -> Union[str, List[str], Dict[str, str], None]:
        """
        Get the value of a key.
        
        Args:
            key: Key to get the value of
            
        Returns:
            Value of the key, or None if the key does not exist
        """
        try:
            # Check the type of the key
            key_type = self.redis.client.type(key)
            
            if key_type == "string":
                # Get string value
                return self.redis.client.get(key)
            elif key_type == "list":
                # Get list value
                return self.redis.client.lrange(key, 0, -1)
            elif key_type == "set":
                # Get set value
                return list(self.redis.client.smembers(key))
            elif key_type == "hash":
                # Get hash value
                return self.redis.client.hgetall(key)
            elif key_type == "zset":
                # Get sorted set value with scores
                return {member: score for member, score in self.redis.client.zrange(key, 0, -1, withscores=True)}
            else:
                # Key does not exist or has an unsupported type
                return None
        except Exception as e:
            self.redis._handle_error(f"get_value({key})", e)
    
    def get_key_info(self, key: str) -> Dict[str, Any]:
        """
        Get information about a key.
        
        Args:
            key: Key to get information about
            
        Returns:
            Information about the key
        """
        try:
            # Check if the key exists
            if not self.redis.client.exists(key):
                return {"exists": False}
            
            # Get key type
            key_type = self.redis.client.type(key)
            
            # Get key TTL
            ttl = self.redis.client.ttl(key)
            
            # Get key size
            if key_type == "string":
                size = self.redis.client.strlen(key)
            elif key_type == "list":
                size = self.redis.client.llen(key)
            elif key_type == "set":
                size = self.redis.client.scard(key)
            elif key_type == "hash":
                size = self.redis.client.hlen(key)
            elif key_type == "zset":
                size = self.redis.client.zcard(key)
            else:
                size = 0
            
            return {
                "exists": True,
                "type": key_type,
                "ttl": ttl,
                "size": size
            }
        except Exception as e:
            self.redis._handle_error(f"get_key_info({key})", e)
    
    def get_key_ttl(self, key: str) -> int:
        """
        Get the TTL of a key.
        
        Args:
            key: Key to get the TTL of
            
        Returns:
            TTL of the key in seconds, -1 if the key has no TTL, -2 if the key does not exist
        """
        try:
            return self.redis.client.ttl(key)
        except Exception as e:
            self.redis._handle_error(f"get_key_ttl({key})", e)