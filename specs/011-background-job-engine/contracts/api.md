# API Contract: Background Job Engine

**Feature**: 011-background-job-engine
**Date**: 2025-12-15
**Base Path**: `/api/method/dartwing.dartwing_core.api.jobs`

## Overview

This document defines the REST API contracts for the Background Job Engine. All endpoints require authentication and respect organization-based permissions.

---

## Authentication

All endpoints require a valid Frappe session or API key/secret.

```http
Authorization: token api_key:api_secret
```

Or session cookie from Frappe login.

---

## Endpoints

### 1. Submit Job

**POST** `/api/method/dartwing.dartwing_core.api.jobs.submit_job`

Submit a new background job for execution.

#### Request

```json
{
  "job_type": "pdf_generation",
  "organization": "ORG-2025-00001",
  "parameters": {
    "template": "monthly_report",
    "date_range": ["2025-01-01", "2025-01-31"]
  },
  "priority": "Normal",
  "depends_on": null
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `job_type` | string | Yes | Job Type identifier |
| `organization` | string | Yes | Organization name |
| `parameters` | object | No | Job-specific input parameters |
| `priority` | string | No | Low/Normal/High/Critical (default: Normal) |
| `depends_on` | string | No | Parent job ID to wait for |

#### Response (Success - 200)

```json
{
  "message": {
    "job_id": "JOB-2025-00001",
    "status": "Queued",
    "message": "Job submitted successfully"
  }
}
```

#### Response (Duplicate - 409)

```json
{
  "message": {
    "error": "Duplicate job detected",
    "existing_job_id": "JOB-2025-00001",
    "status": "Running"
  }
}
```

#### Response (Error - 400/403)

```json
{
  "exc_type": "ValidationError",
  "message": "Invalid job type: unknown_type"
}
```

---

### 2. Get Job Status

**GET** `/api/method/dartwing.dartwing_core.api.jobs.get_job_status`

Retrieve current status and progress of a job.

#### Request

```
?job_id=JOB-2025-00001
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `job_id` | string | Yes | Background Job ID |

#### Response (Success - 200)

```json
{
  "message": {
    "job_id": "JOB-2025-00001",
    "job_type": "pdf_generation",
    "status": "Running",
    "progress": 45,
    "progress_message": "Processing page 5 of 11...",
    "created_at": "2025-12-15T10:00:00Z",
    "started_at": "2025-12-15T10:00:01Z",
    "retry_count": 0,
    "output_reference": null
  }
}
```

#### Response (Completed with Output)

```json
{
  "message": {
    "job_id": "JOB-2025-00001",
    "job_type": "pdf_generation",
    "status": "Completed",
    "progress": 100,
    "progress_message": "PDF generated successfully",
    "created_at": "2025-12-15T10:00:00Z",
    "started_at": "2025-12-15T10:00:01Z",
    "completed_at": "2025-12-15T10:00:05Z",
    "retry_count": 0,
    "output_reference": "/files/report-2025-001.pdf"
  }
}
```

#### Response (Failed)

```json
{
  "message": {
    "job_id": "JOB-2025-00002",
    "job_type": "fax_send",
    "status": "Dead Letter",
    "progress": 0,
    "error_message": "Invalid fax number format",
    "error_type": "Permanent",
    "retry_count": 0,
    "output_reference": null
  }
}
```

---

### 3. List Jobs

**GET** `/api/method/dartwing.dartwing_core.api.jobs.list_jobs`

List jobs with filtering and pagination.

#### Request

```
?organization=ORG-2025-00001&status=Running&job_type=pdf_generation&limit=20&offset=0
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization` | string | No* | Filter by organization (*required for non-admin) |
| `status` | string | No | Filter by status |
| `job_type` | string | No | Filter by job type |
| `limit` | int | No | Page size (default: 20, max: 100) |
| `offset` | int | No | Pagination offset (default: 0) |

#### Response (Success - 200)

```json
{
  "message": {
    "jobs": [
      {
        "job_id": "JOB-2025-00001",
        "job_type": "pdf_generation",
        "status": "Running",
        "progress": 45,
        "created_at": "2025-12-15T10:00:00Z"
      },
      {
        "job_id": "JOB-2025-00002",
        "job_type": "ocr_processing",
        "status": "Queued",
        "progress": 0,
        "created_at": "2025-12-15T10:01:00Z"
      }
    ],
    "total": 42,
    "limit": 20,
    "offset": 0
  }
}
```

---

### 4. Cancel Job

**POST** `/api/method/dartwing.dartwing_core.api.jobs.cancel_job`

Request cancellation of a pending or running job.

#### Request

```json
{
  "job_id": "JOB-2025-00001"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `job_id` | string | Yes | Job to cancel |

#### Response (Success - 200)

```json
{
  "message": {
    "job_id": "JOB-2025-00001",
    "status": "Canceled",
    "message": "Job canceled successfully"
  }
}
```

#### Response (Cannot Cancel - 400)

```json
{
  "exc_type": "ValidationError",
  "message": "Cannot cancel job in status: Completed"
}
```

---

### 5. Retry Job

**POST** `/api/method/dartwing.dartwing_core.api.jobs.retry_job`

Manually retry a failed or dead letter job (admin only).

#### Request

```json
{
  "job_id": "JOB-2025-00002"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `job_id` | string | Yes | Job to retry |

#### Response (Success - 200)

```json
{
  "message": {
    "job_id": "JOB-2025-00002",
    "status": "Queued",
    "message": "Job re-queued for execution"
  }
}
```

---

### 6. Get Job Metrics

**GET** `/api/method/dartwing.dartwing_core.api.jobs.get_job_metrics`

Retrieve operational metrics for monitoring.

#### Request

```
?organization=ORG-2025-00001
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization` | string | No | Filter by org (admin sees all if omitted) |

#### Response (Success - 200)

```json
{
  "message": {
    "job_count_by_status": {
      "Pending": 2,
      "Queued": 15,
      "Running": 8,
      "Completed": 1250,
      "Failed": 3,
      "Dead Letter": 12,
      "Canceled": 5
    },
    "queue_depth_by_priority": {
      "Critical": 1,
      "High": 5,
      "Normal": 8,
      "Low": 3
    },
    "processing_time": {
      "average_seconds": 4.5,
      "p95_seconds": 12.3
    },
    "failure_rate_by_type": {
      "pdf_generation": 0.02,
      "ocr_processing": 0.05,
      "fax_send": 0.08
    },
    "timestamp": "2025-12-15T10:30:00Z"
  }
}
```

---

### 7. Get Job History

**GET** `/api/method/dartwing.dartwing_core.api.jobs.get_job_history`

Retrieve execution log for a specific job.

#### Request

```
?job_id=JOB-2025-00001
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `job_id` | string | Yes | Job to get history for |

#### Response (Success - 200)

```json
{
  "message": {
    "job_id": "JOB-2025-00001",
    "history": [
      {
        "from_status": null,
        "to_status": "Pending",
        "timestamp": "2025-12-15T10:00:00Z",
        "actor": "user@example.com",
        "message": "Job created"
      },
      {
        "from_status": "Pending",
        "to_status": "Queued",
        "timestamp": "2025-12-15T10:00:00Z",
        "actor": null,
        "message": "Job enqueued"
      },
      {
        "from_status": "Queued",
        "to_status": "Running",
        "timestamp": "2025-12-15T10:00:01Z",
        "actor": null,
        "message": "Worker started execution"
      },
      {
        "from_status": "Running",
        "to_status": "Completed",
        "timestamp": "2025-12-15T10:00:05Z",
        "actor": null,
        "message": "Job completed successfully"
      }
    ]
  }
}
```

---

## Socket.IO Events

### Real-Time Progress Updates

**Room**: `org:{organization_name}`

**Event**: `job_progress`

```json
{
  "job_id": "JOB-2025-00001",
  "status": "Running",
  "progress": 45,
  "progress_message": "Processing page 5 of 11...",
  "updated_at": "2025-12-15T10:00:03Z"
}
```

### Job State Change

**Room**: `org:{organization_name}`

**Event**: `job_status_changed`

```json
{
  "job_id": "JOB-2025-00001",
  "from_status": "Running",
  "to_status": "Completed",
  "output_reference": "/files/report-2025-001.pdf",
  "updated_at": "2025-12-15T10:00:05Z"
}
```

---

## Error Codes

| HTTP Status | Error Type | Description |
|-------------|------------|-------------|
| 400 | ValidationError | Invalid input parameters |
| 403 | PermissionError | User lacks permission for this action |
| 404 | DoesNotExistError | Job or resource not found |
| 409 | DuplicateError | Duplicate job submission detected |
| 500 | InternalError | Server error during processing |

---

## Rate Limits

| Endpoint | Limit | Window |
|----------|-------|--------|
| submit_job | 100 | per minute per user |
| get_job_status | 600 | per minute per user |
| list_jobs | 60 | per minute per user |
| cancel_job | 30 | per minute per user |
| get_job_metrics | 30 | per minute per user |
