# Full-Stack Observability Specification

**Objective:** Define comprehensive observability strategy spanning metrics, logging, and alerting across all Dartwing system layers.

## Goals

- Unified visibility across HTTP, background jobs, database, and integrations
- Actionable alerts with low noise-to-signal ratio
- Troubleshooting capability from symptom to root cause
- Capacity planning data for scaling decisions

## Problem Statement

Without unified observability:

- Issues are discovered by users, not monitoring
- Debugging requires log spelunking across multiple systems
- Performance degradation goes unnoticed until critical
- Capacity limits are hit unexpectedly

## Architecture

### Observability Stack

```
┌─────────────────────────────────────────────────────────────────┐
│                    OBSERVABILITY ARCHITECTURE                    │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    Data Sources                              ││
│  │                                                              ││
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       ││
│  │  │  HTTP    │ │Background│ │ Database │ │Integration│       ││
│  │  │ Requests │ │   Jobs   │ │  Queries │ │   Calls  │       ││
│  │  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘       ││
│  └───────┼────────────┼────────────┼────────────┼──────────────┘│
│          │            │            │            │                │
│          └────────────┴─────┬──────┴────────────┘                │
│                             ▼                                    │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                 Collection Layer                             ││
│  │                                                              ││
│  │  ┌──────────────────┐    ┌──────────────────┐              ││
│  │  │ Prometheus Client│    │  Structured JSON │              ││
│  │  │    (Metrics)     │    │     (Logging)    │              ││
│  │  └────────┬─────────┘    └────────┬─────────┘              ││
│  └───────────┼───────────────────────┼──────────────────────────┘│
│              │                       │                           │
│              ▼                       ▼                           │
│  ┌─────────────────────┐  ┌─────────────────────┐               │
│  │    Prometheus       │  │  Log Aggregator     │               │
│  │    (Time Series)    │  │  (Loki/ELK/etc)     │               │
│  └──────────┬──────────┘  └──────────┬──────────┘               │
│             │                        │                           │
│             └────────────┬───────────┘                           │
│                          ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    Visualization                             ││
│  │                                                              ││
│  │  ┌──────────────────┐    ┌──────────────────┐              ││
│  │  │    Grafana       │    │   AlertManager   │              ││
│  │  │   Dashboards     │    │    (Alerts)      │              ││
│  │  └──────────────────┘    └──────────────────┘              ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Metrics

### HTTP Layer Metrics

| Metric | Type | Labels | Description |
|--------|------|--------|-------------|
| `http_requests_total` | counter | `method`, `endpoint`, `status`, `org` | Total HTTP requests |
| `http_request_duration_seconds` | histogram | `method`, `endpoint` | Request latency distribution |
| `http_request_size_bytes` | histogram | `endpoint` | Request payload size |
| `http_response_size_bytes` | histogram | `endpoint` | Response payload size |
| `http_active_requests` | gauge | `method` | Currently processing requests |

### Background Job Metrics

| Metric | Type | Labels | Description |
|--------|------|--------|-------------|
| `jobs_enqueued_total` | counter | `queue`, `method`, `org` | Jobs enqueued |
| `jobs_completed_total` | counter | `queue`, `method`, `org`, `status` | Jobs completed (success/failure) |
| `jobs_duration_seconds` | histogram | `queue`, `method` | Job execution duration |
| `queue_depth` | gauge | `queue` | Current jobs in queue |
| `dlq_depth` | gauge | - | Dead letter queue depth |
| `org_job_count` | gauge | `org`, `queue` | Jobs per org per queue |
| `jobs_retried_total` | counter | `queue`, `method` | Job retry count |

### Database Metrics

| Metric | Type | Labels | Description |
|--------|------|--------|-------------|
| `db_queries_total` | counter | `doctype`, `operation` | Database queries |
| `db_query_duration_seconds` | histogram | `doctype`, `operation` | Query latency |
| `db_connections_active` | gauge | - | Active database connections |
| `db_connections_pool_size` | gauge | - | Connection pool size |
| `db_slow_queries_total` | counter | `doctype` | Queries exceeding threshold |

### Integration Metrics

| Metric | Type | Labels | Description |
|--------|------|--------|-------------|
| `integration_requests_total` | counter | `integration`, `endpoint`, `status` | External API calls |
| `integration_duration_seconds` | histogram | `integration`, `endpoint` | External call latency |
| `integration_token_refresh_total` | counter | `integration`, `status` | Token refresh operations |
| `integration_token_expiry_seconds` | gauge | `integration`, `org` | Time until token expiry |
| `integration_circuit_breaker_state` | gauge | `integration` | Circuit breaker state (0=closed, 1=half-open, 2=open) |

### Sync Layer Metrics

| Metric | Type | Labels | Description |
|--------|------|--------|-------------|
| `sync_deltas_total` | counter | `doctype`, `org`, `operation` | Sync deltas processed |
| `sync_conflicts_total` | counter | `doctype`, `strategy` | Conflict occurrences |
| `sync_lag_seconds` | gauge | `org` | Time since last successful sync |
| `sync_queue_depth` | gauge | `org` | Pending sync operations |

### Socket.IO Metrics

| Metric | Type | Labels | Description |
|--------|------|--------|-------------|
| `socketio_connections_total` | gauge | `server_id` | Current connection count |
| `socketio_rooms_total` | gauge | `server_id` | Active rooms count |
| `socketio_messages_published` | counter | `event_type` | Messages published via Redis |
| `socketio_messages_delivered` | counter | `event_type` | Messages delivered to clients |
| `socketio_redis_latency_ms` | histogram | - | Redis pub/sub latency |

## Implementation

### Prometheus Client Setup

```python
# dartwing_core/observability/metrics.py

from prometheus_client import Counter, Histogram, Gauge, CollectorRegistry
import frappe

# Custom registry to avoid conflicts
REGISTRY = CollectorRegistry()

# HTTP Metrics
http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status", "org"],
    registry=REGISTRY
)

http_request_duration = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["method", "endpoint"],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
    registry=REGISTRY
)

# Job Metrics
jobs_enqueued = Counter(
    "jobs_enqueued_total",
    "Jobs enqueued",
    ["queue", "method", "org"],
    registry=REGISTRY
)

jobs_completed = Counter(
    "jobs_completed_total",
    "Jobs completed",
    ["queue", "method", "org", "status"],
    registry=REGISTRY
)

queue_depth = Gauge(
    "queue_depth",
    "Current jobs in queue",
    ["queue"],
    registry=REGISTRY
)

# Database Metrics
db_queries = Counter(
    "db_queries_total",
    "Database queries",
    ["doctype", "operation"],
    registry=REGISTRY
)

db_query_duration = Histogram(
    "db_query_duration_seconds",
    "Query latency",
    ["doctype", "operation"],
    buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0, 5.0],
    registry=REGISTRY
)

# Integration Metrics
integration_requests = Counter(
    "integration_requests_total",
    "External API calls",
    ["integration", "endpoint", "status"],
    registry=REGISTRY
)

integration_token_expiry = Gauge(
    "integration_token_expiry_seconds",
    "Time until token expiry",
    ["integration", "org"],
    registry=REGISTRY
)
```

### Request Instrumentation

```python
# dartwing_core/observability/middleware.py

import time
import frappe
from dartwing_core.observability.metrics import (
    http_requests_total,
    http_request_duration
)


def instrument_request():
    """Middleware to instrument HTTP requests. Call from hooks."""
    start_time = time.time()

    def after_request():
        duration = time.time() - start_time

        # Extract labels
        method = frappe.request.method if frappe.request else "UNKNOWN"
        endpoint = frappe.request.path if frappe.request else "UNKNOWN"
        status = str(frappe.response.get("status_code", 200))
        org = frappe.flags.get("current_organization", "system")

        # Record metrics
        http_requests_total.labels(
            method=method,
            endpoint=endpoint,
            status=status,
            org=org
        ).inc()

        http_request_duration.labels(
            method=method,
            endpoint=endpoint
        ).observe(duration)

    frappe.db.after_commit.add(after_request)
```

### Job Instrumentation

```python
# dartwing_core/observability/job_metrics.py

import time
import functools
from dartwing_core.observability.metrics import (
    jobs_enqueued,
    jobs_completed,
    queue_depth
)


def instrument_job(queue_name: str):
    """Decorator to instrument background jobs."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            method_name = f"{func.__module__}.{func.__name__}"
            org = kwargs.get("organization", "system")

            start_time = time.time()
            status = "success"

            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                status = "failure"
                raise
            finally:
                duration = time.time() - start_time

                jobs_completed.labels(
                    queue=queue_name,
                    method=method_name,
                    org=org,
                    status=status
                ).inc()

        return wrapper
    return decorator


def record_enqueue(queue: str, method: str, org: str):
    """Record job enqueue event."""
    jobs_enqueued.labels(
        queue=queue,
        method=method,
        org=org
    ).inc()


def update_queue_depths():
    """Scheduled job to update queue depth gauges."""
    from frappe.utils.background_jobs import get_queue

    for queue_name in ["critical", "default", "bulk", "short", "long"]:
        try:
            q = get_queue(queue_name)
            queue_depth.labels(queue=queue_name).set(len(q))
        except Exception:
            pass
```

### Metrics Endpoint

```python
# dartwing_core/observability/api.py

import frappe
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from dartwing_core.observability.metrics import REGISTRY


@frappe.whitelist(allow_guest=True)
def metrics():
    """
    Prometheus metrics endpoint.

    GET /api/method/dartwing_core.observability.api.metrics
    """
    # Optional: Add authentication for production
    frappe.response["content_type"] = CONTENT_TYPE_LATEST
    frappe.response["message"] = generate_latest(REGISTRY).decode("utf-8")
```

## Structured Logging

### Log Format

All logs MUST use JSON format for aggregation:

```python
# dartwing_core/observability/logging.py

import json
import frappe
from frappe.utils import now_datetime


def structured_log(
    level: str,
    message: str,
    **context
):
    """
    Emit a structured log entry.

    Args:
        level: Log level (debug, info, warning, error)
        message: Human-readable message
        **context: Additional context fields
    """
    log_entry = {
        "timestamp": now_datetime().isoformat(),
        "level": level.upper(),
        "message": message,
        "trace_id": frappe.flags.get("trace_id"),
        "user": frappe.session.user if frappe.session else None,
        "organization": frappe.flags.get("current_organization"),
        "site": frappe.local.site,
        **context
    }

    logger = frappe.logger()
    log_method = getattr(logger, level, logger.info)
    log_method(json.dumps(log_entry))


def log_info(message: str, **context):
    structured_log("info", message, **context)


def log_warning(message: str, **context):
    structured_log("warning", message, **context)


def log_error(message: str, **context):
    structured_log("error", message, **context)
```

### Request Context

```python
# dartwing_core/observability/context.py

import uuid
import frappe


def init_request_context():
    """Initialize observability context for a request. Call from hooks."""
    # Generate trace ID
    trace_id = frappe.request.headers.get("X-Trace-ID") if frappe.request else None
    if not trace_id:
        trace_id = str(uuid.uuid4())[:8]

    frappe.flags.trace_id = trace_id

    # Extract organization from request context
    if hasattr(frappe.local, "form_dict"):
        org = frappe.local.form_dict.get("organization")
        if org:
            frappe.flags.current_organization = org


def get_trace_id() -> str:
    """Get current request trace ID."""
    return frappe.flags.get("trace_id", "no-trace")
```

### Standard Log Fields

| Field | Required | Description |
|-------|----------|-------------|
| `timestamp` | Yes | ISO 8601 format |
| `level` | Yes | DEBUG, INFO, WARNING, ERROR |
| `message` | Yes | Human-readable description |
| `trace_id` | Yes | Request correlation ID |
| `user` | No | Authenticated user email |
| `organization` | No | Current org context |
| `site` | Yes | Frappe site name |
| `doctype` | No | Related DocType |
| `docname` | No | Related document name |
| `duration_ms` | No | Operation duration |
| `error_type` | No | Exception class name |
| `stack_trace` | No | Full traceback (errors only) |

## Alerting

### Alert Definitions

| Alert | Condition | Severity | Channel |
|-------|-----------|----------|---------|
| **High Error Rate** | `rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.05` | Critical | PagerDuty + Slack |
| **Slow Requests** | `histogram_quantile(0.95, http_request_duration_seconds) > 5` for 10m | Warning | Slack |
| **Queue Backlog** | `queue_depth{queue="critical"} > 100` for 5m | Critical | PagerDuty |
| **Queue Backlog** | `queue_depth{queue="default"} > 1000` for 15m | Warning | Slack |
| **DLQ Growing** | `dlq_depth > 50` | Warning | Slack |
| **Integration Failing** | `rate(integration_requests_total{status="error"}[5m]) > 10` | Warning | Slack |
| **Token Expiring** | `integration_token_expiry_seconds < 3600` | Warning | Slack |
| **Token Expired** | `integration_token_expiry_seconds <= 0` | Critical | PagerDuty |
| **DB Connection Pool** | `db_connections_active / db_connections_pool_size > 0.9` for 5m | Warning | Slack |
| **Sync Lag** | `sync_lag_seconds > 300` for 10m | Warning | Slack |
| **Socket.IO Disconnect** | `changes(socketio_connections_total[5m]) > 100` | Warning | Slack |

### Alert Configuration

```yaml
# alertmanager.yml

groups:
  - name: dartwing-core
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m]))
          / sum(rate(http_requests_total[5m])) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High HTTP error rate"
          description: "Error rate is {{ $value | humanizePercentage }}"

      - alert: CriticalQueueBacklog
        expr: queue_depth{queue="critical"} > 100
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Critical queue backlog"
          description: "{{ $value }} jobs pending in critical queue"

      - alert: TokenExpiringSoon
        expr: integration_token_expiry_seconds < 3600
        for: 0m
        labels:
          severity: warning
        annotations:
          summary: "Integration token expiring"
          description: "Token for {{ $labels.integration }}:{{ $labels.org }} expires in {{ $value | humanizeDuration }}"
```

## Dashboard Requirements

### Overview Dashboard

Panels:
1. Request rate and error rate (time series)
2. P50/P95/P99 latency (time series)
3. Active connections (gauge)
4. Queue depths by queue (bar chart)
5. Top endpoints by request count (table)
6. Top errors by message (table)

### Jobs Dashboard

Panels:
1. Job throughput by queue (time series)
2. Job success/failure rate (time series)
3. Queue depth trends (time series)
4. DLQ depth (gauge with threshold)
5. Slowest jobs (table)
6. Jobs by organization (pie chart)

### Integrations Dashboard

Panels:
1. External call rate by integration (time series)
2. External call latency P95 (time series)
3. Token expiry countdown (table)
4. Circuit breaker states (status map)
5. Failed calls by integration (bar chart)

### Sync Dashboard

Panels:
1. Sync operations by doctype (time series)
2. Conflict rate by strategy (time series)
3. Sync lag by organization (heatmap)
4. Active sync connections (gauge)

## Hooks Configuration

```python
# dartwing_core/hooks.py

# Initialize observability on each request
before_request = [
    "dartwing_core.observability.context.init_request_context",
    "dartwing_core.observability.middleware.instrument_request",
]

# Scheduled metrics collection
scheduler_events = {
    "cron": {
        # Update queue depths every minute
        "* * * * *": [
            "dartwing_core.observability.job_metrics.update_queue_depths"
        ],
    }
}
```

## Health Check Endpoint

```python
# dartwing_core/observability/health.py

import frappe
from frappe.utils.background_jobs import get_queue


@frappe.whitelist(allow_guest=True)
def health():
    """
    Health check endpoint for load balancers.

    GET /api/method/dartwing_core.observability.health.health

    Returns:
        200: All systems healthy
        503: One or more systems unhealthy
    """
    checks = {
        "database": check_database(),
        "redis": check_redis(),
        "workers": check_workers(),
    }

    all_healthy = all(c["status"] == "healthy" for c in checks.values())

    frappe.response["http_status_code"] = 200 if all_healthy else 503
    return {
        "status": "healthy" if all_healthy else "unhealthy",
        "checks": checks
    }


def check_database() -> dict:
    try:
        frappe.db.sql("SELECT 1")
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


def check_redis() -> dict:
    try:
        frappe.cache().ping()
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


def check_workers() -> dict:
    try:
        queue = get_queue("default")
        worker_count = len(queue.workers)
        if worker_count == 0:
            return {"status": "unhealthy", "error": "No workers available"}
        return {"status": "healthy", "workers": worker_count}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
```

## Test Matrix

| Scenario | Test Method | Expected Result |
|----------|-------------|-----------------|
| Metrics collection | Make requests, check Prometheus | Metrics incremented correctly |
| Request tracing | Verify trace_id in logs | Consistent ID across request |
| Error logging | Trigger error, check log format | JSON with stack trace |
| Alert firing | Exceed threshold | Alert received in channel |
| Health check | Call endpoint | 200 with component status |
| Queue metrics | Enqueue jobs, check gauges | Accurate depth reported |
| Token expiry | Set near-expiry token | Alert fires before expiry |

---

*Specification version: 1.0*
*Last updated: November 2025*
