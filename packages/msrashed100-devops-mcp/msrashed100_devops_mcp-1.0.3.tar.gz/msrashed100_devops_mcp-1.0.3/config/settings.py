"""
Global settings and configuration for the DevOps MCP Server.
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Server settings
SERVER_NAME = "devops-server"
SERVER_VERSION = "0.1.0"

# Kubernetes settings
KUBECONFIG_PATH = os.environ.get("KUBECONFIG")
KUBERNETES_TIMEOUT = 15  # seconds

# Prometheus settings
PROMETHEUS_URL = os.environ.get("PROMETHEUS_URL", "http://localhost:9090")
PROMETHEUS_TIMEOUT = 10  # seconds

# Vault settings
VAULT_URL = os.environ.get("VAULT_ADDR", "http://localhost:8200")
VAULT_TOKEN = os.environ.get("VAULT_TOKEN")
VAULT_TIMEOUT = 10  # seconds

# Grafana settings
GRAFANA_URL = os.environ.get("GRAFANA_URL", "http://localhost:3000")
GRAFANA_API_KEY = os.environ.get("GRAFANA_API_KEY")
GRAFANA_TIMEOUT = 10  # seconds

# Loki settings
LOKI_URL = os.environ.get("LOKI_URL", "http://localhost:3100") # Default to localhost
LOKI_TIMEOUT = 10 # seconds

# Database settings
DATABASE_SETTINGS = {
    "mysql": {
        "host": os.environ.get("MYSQL_HOST", "localhost"),
        "port": int(os.environ.get("MYSQL_PORT", 3306)),
        "user": os.environ.get("MYSQL_USER", "root"),
        "password": os.environ.get("MYSQL_PASSWORD", ""),
        "timeout": 10,  # seconds
    },
    "postgres": {
        "host": os.environ.get("POSTGRES_HOST", "localhost"),
        "port": int(os.environ.get("POSTGRES_PORT", 5432)),
        "user": os.environ.get("POSTGRES_USER", "postgres"),
        "password": os.environ.get("POSTGRES_PASSWORD", ""),
        "timeout": 10,  # seconds
    },
    "mongodb": {
        "uri": os.environ.get("MONGODB_URI", "mongodb://localhost:27017"),
        "timeout": 10,  # seconds
    },
}

# Redis settings
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "")
REDIS_TIMEOUT = 5  # seconds

# AWS settings
AWS_PROFILE = os.environ.get("AWS_PROFILE", "default")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
AWS_TIMEOUT = 15  # seconds

# GitHub settings
GITHUB_ACCESS_TOKEN = os.environ.get("GITHUB_ACCESS_TOKEN")
GITHUB_BASE_URL = os.environ.get("GITHUB_BASE_URL", "https://api.github.com")
GITHUB_TIMEOUT = 10  # seconds

# Logging settings
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"