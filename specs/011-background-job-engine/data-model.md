# Data Model: Background Job Engine

**Feature**: 011-background-job-engine
**Date**: 2025-12-15

## Overview

This document defines the data model for the Background Job Engine, including Frappe doctypes, their fields, relationships, and state transitions.

---

## Entity Relationship Diagram

```
┌─────────────────┐       ┌─────────────────┐
│    Job Type     │       │  Organization   │
│  (Configuration)│       │   (Existing)    │
└────────┬────────┘       └────────┬────────┘
         │                         │
         │ 1:N                     │ 1:N
         ▼                         ▼
┌─────────────────────────────────────────────┐
│              Background Job                  │
│  (Core entity - tracks all async work)       │
└─────────────────────┬───────────────────────┘
                      │
                      │ 1:N
                      ▼
┌─────────────────────────────────────────────┐
│           Job Execution Log                  │
│  (Audit trail of state transitions)          │
└─────────────────────────────────────────────┘
```

---

## Doctype: Background Job

The core entity representing a single unit of asynchronous work.

### Fields

| Field Name | Type | Required | Options/Default | Description |
|------------|------|----------|-----------------|-------------|
| `naming_series` | Select | Yes | `JOB-.YYYY.-` | Auto-generated job ID |
| `job_type` | Link | Yes | Job Type | Category of work |
| `organization` | Link | Yes | Organization | Multi-tenant scoping |
| `owner_user` | Link | Yes | User | User who submitted the job |
| `status` | Select | Yes | See state machine | Current job state |
| `priority` | Select | Yes | Normal | Low/Normal/High/Critical |
| `progress` | Percent | No | 0 | Completion percentage (0-100) |
| `progress_message` | Data | No | | Current step description |
| `input_parameters` | JSON | No | | Job-specific input data |
| `output_reference` | Data | No | | Result reference (file URL, docname) |
| `error_message` | Text | No | | Last error message |
| `error_type` | Select | No | | Transient/Permanent |
| `retry_count` | Int | No | 0 | Number of retry attempts |
| `max_retries` | Int | No | 5 | Maximum retry attempts |
| `next_retry_at` | Datetime | No | | Scheduled retry time |
| `depends_on` | Link | No | Background Job | Parent job dependency |
| `job_hash` | Data | No | | Hash for duplicate detection |
| `timeout_seconds` | Int | No | 300 | Execution timeout |
| `created_at` | Datetime | Yes | Now | Job creation time |
| `started_at` | Datetime | No | | Execution start time |
| `completed_at` | Datetime | No | | Execution end time |
| `canceled_at` | Datetime | No | | Cancellation time |
| `canceled_by` | Link | No | User | User who canceled |

### Indexes

| Index Name | Fields | Purpose |
|------------|--------|---------|
| `idx_org_status` | organization, status | Filter jobs by org and state |
| `idx_job_hash` | job_hash, creation | Duplicate detection |
| `idx_next_retry` | next_retry_at, status | Retry scheduler |
| `idx_depends_on` | depends_on, status | Dependency resolution |

### Permissions

```json
{
  "permissions": [
    {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
    {"role": "Dartwing Admin", "read": 1, "write": 1, "create": 1},
    {"role": "Dartwing User", "read": 1, "write": 0, "if_owner": 1}
  ],
  "user_permission_dependant_doctype": "Organization"
}
```

### Validation Rules

1. `organization` must exist and be active
2. `job_type` must exist and be enabled
3. `depends_on` cannot reference self (no circular dependency)
4. `depends_on` must be in same organization
5. `priority` validated against allowed values
6. `input_parameters` must be valid JSON if provided

---

## Doctype: Job Type

Configuration doctype defining categories of background work.

### Fields

| Field Name | Type | Required | Options/Default | Description |
|------------|------|----------|-----------------|-------------|
| `type_name` | Data | Yes | | Unique identifier (e.g., "pdf_generation") |
| `display_name` | Data | Yes | | Human-readable name |
| `description` | Text | No | | Purpose and usage notes |
| `handler_method` | Data | Yes | | Python method path to execute |
| `default_timeout` | Int | No | 300 | Default timeout in seconds |
| `default_priority` | Select | No | Normal | Default priority level |
| `max_retries` | Int | No | 5 | Default max retry attempts |
| `is_enabled` | Check | No | 1 | Can new jobs be created? |
| `requires_permission` | Data | No | | Frappe permission to check |
| `deduplication_window` | Int | No | 300 | Seconds for duplicate detection |

### Naming

Auto-name by `type_name` field (unique identifier).

### Permissions

```json
{
  "permissions": [
    {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}
  ]
}
```

### Seed Data (Fixtures)

```json
[
  {
    "doctype": "Job Type",
    "type_name": "sample_job",
    "display_name": "Sample Background Job",
    "handler_method": "dartwing.dartwing_core.background_jobs.samples.execute_sample_job",
    "default_timeout": 60,
    "default_priority": "Normal",
    "max_retries": 3,
    "is_enabled": 1
  }
]
```

---

## Doctype: Job Execution Log

Audit trail recording all job state transitions.

### Fields

| Field Name | Type | Required | Options/Default | Description |
|------------|------|----------|-----------------|-------------|
| `background_job` | Link | Yes | Background Job | Parent job reference |
| `from_status` | Data | No | | Previous status (null for creation) |
| `to_status` | Data | Yes | | New status |
| `timestamp` | Datetime | Yes | Now | When transition occurred |
| `actor` | Link | No | User | Who triggered change (system if null) |
| `message` | Text | No | | Additional context (error details) |
| `retry_attempt` | Int | No | | Which retry attempt (if retry) |

### Naming

Hash-based auto-naming.

### Permissions

```json
{
  "permissions": [
    {"role": "System Manager", "read": 1},
    {"role": "Dartwing Admin", "read": 1}
  ]
}
```

### Indexes

| Index Name | Fields | Purpose |
|------------|--------|---------|
| `idx_job_timestamp` | background_job, timestamp | Job history queries |

---

## State Machine: Background Job Status

```
                    ┌──────────────┐
                    │   Pending    │ (Initial state)
                    └──────┬───────┘
                           │ enqueue()
                           ▼
                    ┌──────────────┐
        ┌───────────│    Queued    │───────────┐
        │           └──────┬───────┘           │
        │                  │ worker picks up   │ cancel()
        │                  ▼                   │
        │           ┌──────────────┐           │
        │           │   Running    │───────────┤
        │           └──────┬───────┘           │
        │                  │                   │
        │    ┌─────────────┼─────────────┐     │
        │    │             │             │     │
        │    ▼             ▼             ▼     ▼
   ┌─────────────┐  ┌───────────┐  ┌─────────────┐
   │  Completed  │  │  Failed   │  │  Canceled   │
   └─────────────┘  └─────┬─────┘  └─────────────┘
        (Terminal)        │             (Terminal)
                          │ retry
                          ▼
                   ┌──────────────┐
                   │    Queued    │ (Back to queue)
                   └──────┬───────┘
                          │ exhausted retries
                          ▼
                   ┌──────────────┐
                   │ Dead Letter  │
                   └──────────────┘
                        (Terminal)

   ┌──────────────┐
   │  Timed Out   │ (From Running, may retry)
   └──────────────┘
```

### State Transitions

| From | To | Trigger | Conditions |
|------|----|---------|------------|
| - | Pending | Job created | Valid job type and organization |
| Pending | Queued | enqueue() | Job type enabled |
| Queued | Running | Worker picks up | Worker available |
| Running | Completed | Success | Handler returns without error |
| Running | Failed | Transient error | is_retryable = True |
| Running | Dead Letter | Permanent error | is_retryable = False |
| Running | Timed Out | Timeout exceeded | timeout_seconds reached |
| Failed | Queued | Retry | retry_count < max_retries |
| Failed | Dead Letter | Exhausted | retry_count >= max_retries |
| Timed Out | Queued | Retry | retry_count < max_retries |
| Timed Out | Dead Letter | Exhausted | retry_count >= max_retries |
| Pending | Canceled | cancel() | User owns job or is admin |
| Queued | Canceled | cancel() | User owns job or is admin |
| Running | Canceled | cancel() | Graceful stop at checkpoint |

---

## Relationships

### Background Job → Organization
- **Type**: Many-to-One (required)
- **Constraint**: Organization must exist and be active
- **On Delete**: Fail job with "Organization not found" (don't cascade delete)

### Background Job → Job Type
- **Type**: Many-to-One (required)
- **Constraint**: Job Type must exist
- **On Delete**: Prevent deletion if jobs reference it

### Background Job → Background Job (depends_on)
- **Type**: Many-to-One (optional)
- **Constraint**: Same organization, no circular references
- **Behavior**: Child job waits until parent is "Completed"

### Job Execution Log → Background Job
- **Type**: Many-to-One (required)
- **On Delete**: Cascade delete logs with job

---

## Data Retention

| Entity | Retention | Cleanup Trigger |
|--------|-----------|-----------------|
| Background Job (terminal) | 30 days | Scheduled cleanup job |
| Background Job (non-terminal) | Indefinite | Until completed/canceled |
| Job Execution Log | Same as parent job | Cascade with job |
| Job Type | Indefinite | Manual admin action |

### Cleanup Query

```sql
DELETE FROM `tabBackground Job`
WHERE status IN ('Completed', 'Dead Letter', 'Canceled')
AND modified < DATE_SUB(NOW(), INTERVAL 30 DAY);
```

---

## Sample Data Scenarios

### Scenario 1: Successful Job
```json
{
  "name": "JOB-2025-00001",
  "job_type": "pdf_generation",
  "organization": "ORG-2025-00001",
  "status": "Completed",
  "progress": 100,
  "progress_message": "PDF generated successfully",
  "output_reference": "/files/report-2025-001.pdf",
  "retry_count": 0,
  "created_at": "2025-12-15 10:00:00",
  "started_at": "2025-12-15 10:00:01",
  "completed_at": "2025-12-15 10:00:05"
}
```

### Scenario 2: Job in Dead Letter
```json
{
  "name": "JOB-2025-00002",
  "job_type": "fax_send",
  "organization": "ORG-2025-00001",
  "status": "Dead Letter",
  "progress": 0,
  "error_message": "Invalid fax number format: +1-INVALID",
  "error_type": "Permanent",
  "retry_count": 0,
  "created_at": "2025-12-15 11:00:00",
  "started_at": "2025-12-15 11:00:01",
  "completed_at": "2025-12-15 11:00:02"
}
```

### Scenario 3: Job with Retries
```json
{
  "name": "JOB-2025-00003",
  "job_type": "ocr_processing",
  "organization": "ORG-2025-00001",
  "status": "Queued",
  "progress": 0,
  "error_message": "Connection timeout to OCR service",
  "error_type": "Transient",
  "retry_count": 2,
  "max_retries": 5,
  "next_retry_at": "2025-12-15 11:04:00",
  "created_at": "2025-12-15 11:00:00"
}
```
