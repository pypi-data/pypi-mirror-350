"""
Prometheus formatting utilities for the DevOps MCP Server.
"""
from typing import Dict, Any, List, Optional
from utils.formatting import format_text_response, format_json_response, format_error_response


def format_prometheus_query_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format a Prometheus query result.
    
    Args:
        result: The query result from Prometheus
        
    Returns:
        Formatted response
    """
    return format_json_response(result)


def format_prometheus_series(series: List[Dict[str, Any]], limit: Optional[int] = None) -> Dict[str, Any]:
    """
    Format Prometheus series data.
    
    Args:
        series: List of series data
        limit: Maximum number of series to include
        
    Returns:
        Formatted response
    """
    if limit and len(series) > limit:
        series = series[:limit]
        limited = True
    else:
        limited = False
    
    result = {
        "status": "success",
        "data": series
    }
    
    if limited:
        result["resultLimited"] = True
    
    return format_json_response(result)


def format_prometheus_labels(labels: List[str], limit: Optional[int] = None) -> Dict[str, Any]:
    """
    Format Prometheus labels.
    
    Args:
        labels: List of label names
        limit: Maximum number of labels to include
        
    Returns:
        Formatted response
    """
    if limit and len(labels) > limit:
        labels = labels[:limit]
        limited = True
    else:
        limited = False
    
    result = {
        "status": "success",
        "data": labels
    }
    
    if limited:
        result["resultLimited"] = True
    
    return format_json_response(result)


def format_prometheus_alerts(alerts: List[Dict[str, Any]], limit: Optional[int] = None) -> Dict[str, Any]:
    """
    Format Prometheus alerts.
    
    Args:
        alerts: List of alerts
        limit: Maximum number of alerts to include
        
    Returns:
        Formatted response
    """
    if limit and len(alerts) > limit:
        alerts = alerts[:limit]
        limited = True
    else:
        limited = False
    
    result = {
        "status": "success",
        "data": {
            "alerts": alerts
        }
    }
    
    if limited:
        result["data"]["resultLimited"] = True
    
    return format_json_response(result)


def format_prometheus_rules(rules: List[Dict[str, Any]], limit: Optional[int] = None) -> Dict[str, Any]:
    """
    Format Prometheus rules.
    
    Args:
        rules: List of rules
        limit: Maximum number of rules to include
        
    Returns:
        Formatted response
    """
    if limit and len(rules) > limit:
        rules = rules[:limit]
        limited = True
    else:
        limited = False
    
    result = {
        "status": "success",
        "data": {
            "groups": rules
        }
    }
    
    if limited:
        result["data"]["resultLimited"] = True
    
    return format_json_response(result)


def format_prometheus_targets(targets: Dict[str, Any], limit: Optional[int] = None) -> Dict[str, Any]:
    """
    Format Prometheus targets.
    
    Args:
        targets: Target data
        limit: Maximum number of targets to include
        
    Returns:
        Formatted response
    """
    result = {
        "status": "success",
        "data": targets
    }
    
    # Apply limit to active targets if needed
    if limit and "activeTargets" in targets and len(targets["activeTargets"]) > limit:
        targets["activeTargets"] = targets["activeTargets"][:limit]
        targets["resultLimited"] = True
    
    # Apply limit to dropped targets if needed
    if limit and "droppedTargets" in targets and len(targets["droppedTargets"]) > limit:
        targets["droppedTargets"] = targets["droppedTargets"][:limit]
        targets["resultLimited"] = True
    
    return format_json_response(result)


def format_prometheus_status(status: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format Prometheus status.
    
    Args:
        status: Status data
        
    Returns:
        Formatted response
    """
    return format_json_response(status)