#!/usr/bin/env python
"""
Entry point for the DevOps MCP Server.
"""
import os
import sys
import asyncio
from mcp.server.fastmcp import FastMCP

from config.settings import SERVER_NAME, SERVER_VERSION, KUBECONFIG_PATH, PROMETHEUS_URL, VAULT_URL, VAULT_TOKEN, LOKI_URL
from config.settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, DATABASE_SETTINGS
from config.settings import AWS_PROFILE, AWS_REGION
from config.settings import GITHUB_ACCESS_TOKEN, GITHUB_BASE_URL
from utils.logging import setup_logger
from services.kubernetes.client import KubernetesService
from tools.kubernetes.generic_resource_tools import KubernetesGenericResourceTools
from tools.kubernetes.kubernetes_monitoring_tools import KubernetesMonitoringTools
from tools.kubernetes.kubernetes_security_tools import KubernetesSecurityTools
from resources.kubernetes_resources import KubernetesResources
from services.prometheus.service import PrometheusServiceManager
from tools.prometheus.prometheus_tools import PrometheusTools
from resources.prometheus_resources import PrometheusResources
from services.vault.service import VaultServiceManager
from tools.vault.vault_tools import VaultTools
from resources.vault_resources import VaultResources
from services.redis.service import RedisServiceManager
from tools.redis.redis_tools import RedisTools
from resources.redis_resources import RedisResources
from services.mongodb.service import MongoDBServiceManager
from tools.mongodb.mongodb_tools import MongoDBTools
from resources.mongodb_resources import MongoDBResources
from services.postgresql.service import PostgreSQLServiceManager
from tools.postgresql.postgresql_tools import PostgreSQLTools
from resources.postgresql_resources import PostgreSQLResources
from services.aws.service import AWSServiceManager
from tools.aws.aws_tools import AWSTools
from resources.aws_resources import AWSResources
from services.github.service import GitHubServiceManager
from tools.github.github_tools import GitHubTools
from resources.github_resources import GitHubResources
from services.loki.service import LokiServiceManager
from tools.loki.loki_tools import LokiTools
# Import LokiResources if/when created
# from resources.loki_resources import LokiResources


# Set up logger
logger = setup_logger("devops_mcp_server.main")


def initialize_server():
    """Initialize the MCP server with tools and resources."""
    # Create MCP server
    mcp = FastMCP(SERVER_NAME, version=SERVER_VERSION)
    
    # Initialize Kubernetes tools
    try:
        kubeconfig_path = KUBECONFIG_PATH or os.environ.get("KUBECONFIG")
        if kubeconfig_path:
            logger.info(f"Using kubeconfig from: {kubeconfig_path}")
        else:
            logger.warning("No kubeconfig path provided. Kubernetes tools may not work correctly.")
        
        # Initialize Kubernetes service
        k8s_service = KubernetesService(kubeconfig_path)
        logger.info("Kubernetes service initialized successfully")
        
        # Initialize Kubernetes generic resource tools
        # This single tool can handle any Kubernetes resource type dynamically
        KubernetesGenericResourceTools(mcp, k8s_service)
        logger.info("Kubernetes generic resource tools initialized successfully")
        
        # Initialize Kubernetes monitoring tools
        KubernetesMonitoringTools(mcp, k8s_service)
        logger.info("Kubernetes monitoring tools initialized successfully")
        
        # Initialize Kubernetes security tools
        KubernetesSecurityTools(mcp, k8s_service)
        logger.info("Kubernetes security tools initialized successfully")
        
        # Initialize Kubernetes resources - commented out for now
        # KubernetesResources(mcp, k8s_service)
        # logger.info("Kubernetes resources initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Kubernetes components: {e}")
    # Initialize Prometheus tools
    try:
        prometheus_url = PROMETHEUS_URL or os.environ.get("PROMETHEUS_URL")
        if prometheus_url:
            logger.info(f"Using Prometheus URL: {prometheus_url}")
        else:
            logger.warning("No Prometheus URL provided. Prometheus tools may not work correctly.")
        
        # Initialize Prometheus service
        prometheus_service = PrometheusServiceManager(prometheus_url)
        logger.info("Prometheus service initialized successfully")
        
        # Initialize Prometheus tools
        PrometheusTools(mcp, prometheus_service)
        logger.info("Prometheus tools initialized successfully")
        
        # Initialize Prometheus resources
        PrometheusResources(mcp, prometheus_service)
        logger.info("Prometheus resources initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Prometheus components: {e}")
    # Initialize Vault tools
    try:
        # Check if hvac is available
        try:
            import importlib
            importlib.import_module('hvac')
            hvac_available = True
        except ImportError:
            hvac_available = False
            logger.warning("hvac module is not installed. Vault tools will not be available. Install with 'pip install hvac'")
        
        if hvac_available:
            vault_url = VAULT_URL or os.environ.get("VAULT_URL")
            vault_token = VAULT_TOKEN or os.environ.get("VAULT_TOKEN")
            
            if vault_url:
                logger.info(f"Using Vault URL: {vault_url}")
            else:
                logger.warning("No Vault URL provided. Vault tools may not work correctly.")
            
            if not vault_token:
                logger.warning("No Vault token provided. Vault tools may not work correctly.")
            
            # Initialize Vault service
            vault_service = VaultServiceManager(vault_url, vault_token)
            logger.info("Vault service initialized successfully")
            
            # Initialize Vault tools
            VaultTools(mcp, vault_service)
            logger.info("Vault tools initialized successfully")
            
            # Initialize Vault resources
            VaultResources(mcp, vault_service)
            logger.info("Vault resources initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Vault components: {e}")
    # Initialize Redis tools
    try:
        # Check if redis is available
        try:
            import importlib
            importlib.import_module('redis')
            redis_available = True
        except ImportError:
            redis_available = False
            logger.warning("redis module is not installed. Redis tools will not be available. Install with 'pip install redis'")
        
        if redis_available:
            redis_host = REDIS_HOST or os.environ.get("REDIS_HOST")
            redis_port = REDIS_PORT or int(os.environ.get("REDIS_PORT", 6379))
            redis_password = REDIS_PASSWORD or os.environ.get("REDIS_PASSWORD")
            
            if redis_host:
                logger.info(f"Using Redis host: {redis_host}, port: {redis_port}")
            else:
                logger.warning("No Redis host provided. Redis tools may not work correctly.")
            
            # Initialize Redis service
            redis_service = RedisServiceManager(redis_host, redis_port, redis_password)
            logger.info("Redis service initialized successfully")
            
            # Initialize Redis tools
            RedisTools(mcp, redis_service)
            logger.info("Redis tools initialized successfully")
            
            # Initialize Redis resources
            RedisResources(mcp, redis_service)
            logger.info("Redis resources initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Redis components: {e}")
    # Initialize MongoDB tools
    try:
        # Check if pymongo is available
        try:
            import importlib
            importlib.import_module('pymongo')
            pymongo_available = True
        except ImportError:
            pymongo_available = False
            logger.warning("pymongo module is not installed. MongoDB tools will not be available. Install with 'pip install pymongo'")
        
        if pymongo_available:
            mongodb_uri = DATABASE_SETTINGS.get("mongodb", {}).get("uri") or os.environ.get("MONGODB_URI")
            
            if mongodb_uri:
                logger.info(f"Using MongoDB URI: {mongodb_uri}")
            else:
                logger.warning("No MongoDB URI provided. MongoDB tools may not work correctly.")
            
            # Initialize MongoDB service
            mongodb_service = MongoDBServiceManager(mongodb_uri)
            logger.info("MongoDB service initialized successfully")
            
            # Initialize MongoDB tools
            MongoDBTools(mcp, mongodb_service)
            logger.info("MongoDB tools initialized successfully")
            
            # Initialize MongoDB resources
            MongoDBResources(mcp, mongodb_service)
            logger.info("MongoDB resources initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize MongoDB components: {e}")
    # Initialize PostgreSQL tools
    try:
        # Check if psycopg2 is available
        try:
            import importlib
            importlib.import_module('psycopg2')
            psycopg2_available = True
        except ImportError:
            psycopg2_available = False
            logger.warning("psycopg2 module is not installed. PostgreSQL tools will not be available. Install with 'pip install psycopg2-binary'")
        
        if psycopg2_available:
            postgres_settings = DATABASE_SETTINGS.get("postgres", {})
            postgres_host = postgres_settings.get("host") or os.environ.get("POSTGRES_HOST")
            postgres_port = postgres_settings.get("port") or int(os.environ.get("POSTGRES_PORT", 5432))
            postgres_user = postgres_settings.get("user") or os.environ.get("POSTGRES_USER")
            postgres_password = postgres_settings.get("password") or os.environ.get("POSTGRES_PASSWORD")
            
            if postgres_host:
                logger.info(f"Using PostgreSQL host: {postgres_host}, port: {postgres_port}")
            else:
                logger.warning("No PostgreSQL host provided. PostgreSQL tools may not work correctly.")
            
            # Initialize PostgreSQL service
            postgresql_service = PostgreSQLServiceManager(
                postgres_host, postgres_port, postgres_user, postgres_password
            )
            logger.info("PostgreSQL service initialized successfully")
            
            # Initialize PostgreSQL tools
            PostgreSQLTools(mcp, postgresql_service)
            logger.info("PostgreSQL tools initialized successfully")
            
            # Initialize PostgreSQL resources
            PostgreSQLResources(mcp, postgresql_service)
            logger.info("PostgreSQL resources initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize PostgreSQL components: {e}")
    
    # Initialize AWS tools
    try:
        # Check if boto3 is available
        try:
            import importlib
            importlib.import_module('boto3')
            boto3_available = True
        except ImportError:
            boto3_available = False
            logger.warning("boto3 module is not installed. AWS tools will not be available. Install with 'pip install boto3'")
        
        if boto3_available:
            aws_profile = AWS_PROFILE or os.environ.get("AWS_PROFILE")
            aws_region = AWS_REGION or os.environ.get("AWS_REGION")
            
            logger.info(f"Using AWS profile: {aws_profile} and region: {aws_region}")
            
            # Initialize AWS service
            aws_service = AWSServiceManager(aws_region, aws_profile)
            logger.info("AWS service initialized successfully")
            
            # Initialize AWS tools
            AWSTools(mcp, aws_service)
            logger.info("AWS tools initialized successfully")
            
            # Initialize AWS resources
            AWSResources(mcp, aws_service)
            logger.info("AWS resources initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize AWS components: {e}")
    
    # Initialize GitHub tools
    try:
        # Check if PyGithub is available
        try:
            import importlib
            importlib.import_module('github')
            pygithub_available = True
        except ImportError:
            pygithub_available = False
            logger.warning("PyGithub module is not installed. GitHub tools will not be available. Install with 'pip install PyGithub'")
        
        if pygithub_available:
            github_access_token = GITHUB_ACCESS_TOKEN or os.environ.get("GITHUB_ACCESS_TOKEN")
            github_base_url = GITHUB_BASE_URL or os.environ.get("GITHUB_BASE_URL")
            
            if github_access_token:
                logger.info("GitHub access token provided")
            else:
                logger.warning("No GitHub access token provided. GitHub tools may not work correctly.")
            
            # Initialize GitHub service
            github_service = GitHubServiceManager(github_access_token, github_base_url)
            logger.info("GitHub service initialized successfully")
            
            # Initialize GitHub tools
            GitHubTools(mcp, github_service)
            logger.info("GitHub tools initialized successfully")
            
            # Initialize GitHub resources
            GitHubResources(mcp, github_service)
            logger.info("GitHub resources initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize GitHub components: {e}")

    # Initialize Loki tools
    try:
        # Check if requests is available (Loki client uses it)
        try:
            import importlib
            importlib.import_module('requests')
            requests_available = True
        except ImportError:
            requests_available = False
            logger.warning("requests module is not installed. Loki tools will not be available. Install with 'pip install requests'")

        if requests_available:
            loki_url = LOKI_URL or os.environ.get("LOKI_URL")
            if loki_url:
                logger.info(f"Using Loki URL: {loki_url}")
            else:
                logger.warning("No Loki URL provided. Loki tools may not work correctly.")

            # Initialize Loki service
            loki_service = LokiServiceManager(loki_url)
            logger.info("Loki service initialized successfully")

            # Initialize Loki tools
            LokiTools(mcp, loki_service)
            logger.info("Loki tools initialized successfully")

            # Initialize Loki resources (if/when created)
            # LokiResources(mcp, loki_service)
            # logger.info("Loki resources initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Loki components: {e}")
    
    # Initialize other tools here as they are implemented
    # Example:
    # GrafanaTools(mcp)
    # MySQLTools(mcp)
    # MSSQLTools(mcp)
    
    return mcp


def main():
    """Main entry point for the DevOps MCP Server."""
    try:
        logger.info(f"Starting {SERVER_NAME} v{SERVER_VERSION}...")
        
        # Initialize server
        mcp = initialize_server()
        
        # Run server
        logger.info("Server initialized successfully")
        logger.info("Running server...")
        mcp.run()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Error running server: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
