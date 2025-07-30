# Vault Tools Documentation

This document provides detailed information about the Vault tools available in the DevOps MCP Server.

## Overview

The Vault integration allows you to interact with your HashiCorp Vault server through the MCP protocol. It provides tools for retrieving secrets, authentication information, and system status.

## Configuration

The Vault integration can be configured using the following environment variables:

- `VAULT_URL`: The URL of your Vault server (default: `http://localhost:8200`)
- `VAULT_TOKEN`: The token to use for authentication
- `VAULT_TIMEOUT`: Timeout for API calls in seconds (default: `10`)

## Available Tools

The Vault integration provides the following tools:

### Secret Tools

#### `list_vault_secrets`

List secrets at a path in Vault.

**Parameters:**
- `path` (required): Path to list secrets from (e.g., "my-app")
- `mount_point` (optional): The secret engine mount point (default: "secret")
- `limit` (optional): Maximum number of secrets to return (default: 100, max: 500)

**Example:**
```
list_vault_secrets("my-app")
list_vault_secrets("my-app", "kv")
```

#### `get_vault_secret`

Get a secret from Vault.

**Parameters:**
- `path` (required): Path to the secret (e.g., "my-app/database")
- `mount_point` (optional): The secret engine mount point (default: "secret")
- `version` (optional): Specific version to retrieve

**Example:**
```
get_vault_secret("my-app/database")
get_vault_secret("my-app/database", "kv", 2)
```

#### `get_vault_secret_metadata`

Get metadata for a secret in Vault.

**Parameters:**
- `path` (required): Path to the secret (e.g., "my-app/database")
- `mount_point` (optional): The secret engine mount point (default: "secret")

**Example:**
```
get_vault_secret_metadata("my-app/database")
```

### Auth Tools

#### `list_vault_auth_methods`

List authentication methods in Vault.

**Parameters:**
- `limit` (optional): Maximum number of methods to return (default: 100, max: 500)

**Example:**
```
list_vault_auth_methods()
```

#### `get_vault_token_info`

Get information about the current token.

**Example:**
```
get_vault_token_info()
```

#### `list_vault_token_accessors`

List token accessors in Vault.

**Parameters:**
- `limit` (optional): Maximum number of accessors to return (default: 100, max: 500)

**Example:**
```
list_vault_token_accessors()
```

### System Tools

#### `get_vault_health_status`

Get Vault health status.

**Example:**
```
get_vault_health_status()
```

#### `get_vault_seal_status`

Get Vault seal status.

**Example:**
```
get_vault_seal_status()
```

#### `list_vault_policies`

List policies in Vault.

**Parameters:**
- `limit` (optional): Maximum number of policies to return (default: 100, max: 500)

**Example:**
```
list_vault_policies()
```

#### `get_vault_policy`

Get a policy from Vault.

**Parameters:**
- `name` (required): Policy name

**Example:**
```
get_vault_policy("admin")
```

#### `list_vault_audit_devices`

List audit devices in Vault.

**Parameters:**
- `limit` (optional): Maximum number of devices to return (default: 100, max: 500)

**Example:**
```
list_vault_audit_devices()
```

## Available Resources

The Vault integration provides the following resources:

- `vault://status`: Get Vault server status
- `vault://auth`: Get Vault authentication information
- `vault://secret/{path}`: Get a secret from Vault
- `vault://policies`: List Vault policies

## Examples

### Working with Secrets

```
# List secrets in the "my-app" path
list_vault_secrets("my-app")

# Get the "database" secret from the "my-app" path
get_vault_secret("my-app/database")

# Get metadata for the "database" secret
get_vault_secret_metadata("my-app/database")
```

### Working with Authentication

```
# List all authentication methods
list_vault_auth_methods()

# Get information about the current token
get_vault_token_info()
```

### Working with System Information

```
# Get Vault health status
get_vault_health_status()

# List all policies
list_vault_policies()

# Get the "admin" policy
get_vault_policy("admin")