# Redis Tools Documentation

This document provides detailed information about the Redis tools available in the DevOps MCP Server.

## Overview

The Redis integration allows you to interact with your Redis server through the MCP protocol. It provides tools for retrieving keys, values, and server information.

## Configuration

The Redis integration can be configured using the following environment variables:

- `REDIS_HOST`: The host of your Redis server (default: `localhost`)
- `REDIS_PORT`: The port of your Redis server (default: `6379`)
- `REDIS_PASSWORD`: The password for your Redis server (default: empty)
- `REDIS_TIMEOUT`: Timeout for API calls in seconds (default: `5`)

## Available Tools

The Redis integration provides the following tools:

### Key-Value Tools

#### `get_redis_keys`

Get Redis keys matching a pattern.

**Parameters:**
- `pattern` (optional): Pattern to match keys against (default: "*" for all keys)
- `limit` (optional): Maximum number of keys to return (default: 100, max: 500)

**Example:**
```
get_redis_keys("user:*")
get_redis_keys("session:*", 50)
```

#### `get_redis_value`

Get the value of a Redis key.

**Parameters:**
- `key` (required): Key to get the value of

**Example:**
```
get_redis_value("user:1001")
```

#### `get_redis_key_info`

Get information about a Redis key.

**Parameters:**
- `key` (required): Key to get information about

**Example:**
```
get_redis_key_info("user:1001")
```

#### `scan_redis_keys`

Scan Redis keys matching a pattern.

**Parameters:**
- `pattern` (optional): Pattern to match keys against (default: "*" for all keys)
- `count` (optional): Number of keys to scan per iteration (default: 10)
- `cursor` (optional): Cursor position to start scanning from (default: 0)
- `limit` (optional): Maximum number of keys to return (default: 100, max: 500)

**Example:**
```
scan_redis_keys("user:*", 20, 0, 50)
```

### Information Tools

#### `get_redis_info`

Get Redis server information.

**Parameters:**
- `section` (optional): Specific section of information to retrieve
  - Valid sections include: server, clients, memory, persistence, stats, replication, cpu, commandstats, cluster, keyspace

**Example:**
```
get_redis_info()
get_redis_info("memory")
```

#### `get_redis_stats`

Get Redis server statistics.

**Example:**
```
get_redis_stats()
```

#### `get_redis_config`

Get Redis server configuration.

**Parameters:**
- `parameter` (optional): Specific configuration parameter to retrieve

**Example:**
```
get_redis_config()
get_redis_config("maxmemory")
```

#### `get_redis_slow_log`

Get Redis slow log.

**Parameters:**
- `count` (optional): Maximum number of entries to return (default: 10, max: 100)

**Example:**
```
get_redis_slow_log()
get_redis_slow_log(20)
```

#### `get_redis_client_list`

Get Redis client list.

**Parameters:**
- `limit` (optional): Maximum number of clients to return (default: 100, max: 500)

**Example:**
```
get_redis_client_list()
```

#### `get_redis_memory_stats`

Get Redis memory statistics.

**Example:**
```
get_redis_memory_stats()
```

## Available Resources

The Redis integration provides the following resources:

- `redis://info`: Get Redis server information
- `redis://stats`: Get Redis server statistics
- `redis://config`: Get Redis server configuration
- `redis://clients`: Get Redis client list
- `redis://key/{key}`: Get the value of a Redis key
- `redis://keys/{pattern}`: Get Redis keys matching a pattern

## Examples

### Working with Keys and Values

```
# Get all keys matching the pattern "user:*"
get_redis_keys("user:*")

# Get the value of the key "user:1001"
get_redis_value("user:1001")

# Get information about the key "user:1001"
get_redis_key_info("user:1001")
```

### Working with Server Information

```
# Get Redis server information
get_redis_info()

# Get Redis server statistics
get_redis_stats()

# Get Redis server configuration
get_redis_config()

# Get Redis memory statistics
get_redis_memory_stats()
```

### Working with Clients and Slow Log

```
# Get Redis client list
get_redis_client_list()

# Get Redis slow log
get_redis_slow_log()