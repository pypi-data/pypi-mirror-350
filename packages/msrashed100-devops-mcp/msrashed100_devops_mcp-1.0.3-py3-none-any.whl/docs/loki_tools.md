# Loki Tools for DevOps MCP Server

This document provides an overview of the Loki tools available in the DevOps MCP Server. These tools allow interaction with a configured Loki instance for log querying and label inspection.

## Configuration

The Loki tools require the `LOKI_URL` to be configured. This can be set as an environment variable or in the `config/settings.py` file. The default is `http://localhost:3100` if not otherwise specified. The `LOKI_TIMEOUT` (default 10 seconds) can also be configured.

## Available Tools

### 1. `query_loki_range`

Queries logs from Loki within a given time range using a LogQL query.

**Arguments:**

*   `query` (str, required): The LogQL query string.
    *   Example: `{cluster="platformlive", namespace="console"} |= "error"`
*   `start` (str, required): The start of the query range. Can be a relative time string (e.g., "1h", "30m"), a Unix timestamp (seconds), or an RFC3339 formatted timestamp.
    *   Example: `"1h"` (for one hour ago)
*   `end` (str, required): The end of the query range. Can be a relative time string (e.g., "now"), a Unix timestamp (seconds), or an RFC3339 formatted timestamp.
    *   Example: `"now"`
*   `limit` (int, optional): Maximum number of log lines to return.
    *   Default: `100`
    *   Max: `5000`
*   `direction` (str, optional): Search direction.
    *   Allowed values: `"forward"`, `"backward"`
    *   Default: `"backward"`
*   `step` (str, optional): Query resolution step width for metric queries (e.g., "15s", "1m"). Not typically used for log stream queries.

**Returns:**

*   (str): A JSON string containing the query result from Loki. The structure includes `status`, `data` (with `resultType` and `result` containing log streams or matrix data, and `stats`).

**Example Usage (MCP Tool Call):**

```json
{
  "tool_name": "query_loki_range",
  "arguments": {
    "query": "{app=\\"your-app\\"} |= \\"error\\"",
    "start": "15m",
    "end": "now",
    "limit": 50
  }
}
```

### 2. `get_loki_labels`

Retrieves a list of all label names known to Loki within a given time range.

**Arguments:**

*   `start` (str, optional): The start of the time range to consider for labels. Can be a relative time string, Unix timestamp, or RFC3339. If omitted, recent labels are typically returned based on Loki's default.
    *   Example: `"24h"`
*   `end` (str, optional): The end of the time range. Can be a relative time string, Unix timestamp, or RFC3339.
    *   Example: `"now"`

**Returns:**

*   (str): A JSON string containing a list of label names.
    *   Example: `{"status": "success", "data": ["app", "namespace", "pod", "job", ...]}`

**Example Usage (MCP Tool Call):**

```json
{
  "tool_name": "get_loki_labels",
  "arguments": {
    "start": "7d"
  }
}
```

### 3. `get_loki_label_values`

Retrieves all unique values for a specific label name within a given time range.

**Arguments:**

*   `label_name` (str, required): The name of the label for which to fetch values.
    *   Example: `"namespace"`
*   `start` (str, optional): The start of the time range to consider for label values. Can be a relative time string, Unix timestamp, or RFC3339.
    *   Example: `"24h"`
*   `end` (str, optional): The end of the time range. Can be a relative time string, Unix timestamp, or RFC3339.
    *   Example: `"now"`

**Returns:**

*   (str): A JSON string containing a list of unique values for the specified label.
    *   Example: `{"status": "success", "data": ["default", "kube-system", "monitoring", "loki", ...]}`

**Example Usage (MCP Tool Call):**

```json
{
  "tool_name": "get_loki_label_values",
  "arguments": {
    "label_name": "app",
    "start": "3h",
    "end": "now"
  }
}