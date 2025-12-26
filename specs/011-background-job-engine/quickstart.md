# Quickstart: Background Job Engine

**Feature**: 011-background-job-engine
**Date**: 2025-12-15

## Overview

This guide provides a quick introduction to using the Background Job Engine in Dartwing. After completing this guide, you'll be able to submit jobs, track progress, and handle results.

---

## Prerequisites

- Dartwing backend running with Redis
- User authenticated with access to an Organization
- Basic understanding of Frappe whitelisted methods

---

## 1. Submit a Job (Python)

### From Server-Side Code

```python
from dartwing.dartwing_core.background_jobs import submit_job

# Submit a simple job
job = submit_job(
    job_type="pdf_generation",
    organization="ORG-2025-00001",
    parameters={
        "template": "monthly_report",
        "date_range": ["2025-01-01", "2025-01-31"]
    }
)

print(f"Job submitted: {job.name}")  # JOB-2025-00001
```

### With Priority and Dependencies

```python
# Submit a high-priority job
urgent_job = submit_job(
    job_type="fax_send",
    organization="ORG-2025-00001",
    parameters={"fax_number": "+15551234567", "document": "doc.pdf"},
    priority="High"
)

# Submit a job that depends on another
followup_job = submit_job(
    job_type="email_notification",
    organization="ORG-2025-00001",
    parameters={"template": "fax_sent_confirmation"},
    depends_on=urgent_job.name
)
```

---

## 2. Submit a Job (API)

### Using curl

```bash
curl -X POST \
  'https://your-site.com/api/method/dartwing.dartwing_core.api.jobs.submit_job' \
  -H 'Authorization: token api_key:api_secret' \
  -H 'Content-Type: application/json' \
  -d '{
    "job_type": "pdf_generation",
    "organization": "ORG-2025-00001",
    "parameters": {
      "template": "monthly_report"
    }
  }'
```

### Response

```json
{
  "message": {
    "job_id": "JOB-2025-00001",
    "status": "Queued",
    "message": "Job submitted successfully"
  }
}
```

---

## 3. Check Job Status

### Python

```python
from dartwing.dartwing_core.background_jobs import get_job_status

status = get_job_status("JOB-2025-00001")
print(f"Status: {status.status}, Progress: {status.progress}%")
```

### API

```bash
curl 'https://your-site.com/api/method/dartwing.dartwing_core.api.jobs.get_job_status?job_id=JOB-2025-00001' \
  -H 'Authorization: token api_key:api_secret'
```

---

## 4. Listen for Real-Time Updates (Flutter)

```dart
import 'package:socket_io_client/socket_io_client.dart' as IO;

class JobProgressListener {
  late IO.Socket socket;

  void connect(String organizationId) {
    socket = IO.io('https://your-site.com', <String, dynamic>{
      'transports': ['websocket'],
      'autoConnect': false,
    });

    socket.connect();

    // Join organization room
    socket.emit('join_room', 'org:$organizationId');

    // Listen for progress updates
    socket.on('job_progress', (data) {
      print('Job ${data['job_id']}: ${data['progress']}%');
      print('Status: ${data['progress_message']}');
    });

    // Listen for status changes
    socket.on('job_status_changed', (data) {
      print('Job ${data['job_id']} changed to ${data['to_status']}');
      if (data['output_reference'] != null) {
        print('Result: ${data['output_reference']}');
      }
    });
  }

  void disconnect() {
    socket.disconnect();
  }
}
```

---

## 5. Create a Custom Job Type

### Step 1: Define the Handler

```python
# dartwing/dartwing_core/background_jobs/handlers/my_handler.py

from dartwing.dartwing_core.background_jobs import JobContext, TransientError, PermanentError

def execute_my_job(context: JobContext):
    """
    Custom job handler.

    Args:
        context: Contains job parameters, progress callback, and metadata
    """
    params = context.parameters

    # Update progress
    context.update_progress(10, "Starting processing...")

    try:
        # Do work
        result = process_data(params.get("input_data"))

        context.update_progress(50, "Processing complete, saving...")

        # Save result
        output_path = save_result(result)

        context.update_progress(100, "Done!")

        # Return output reference
        return {"output_reference": output_path}

    except ConnectionError as e:
        # Transient error - will retry
        raise TransientError(f"Connection failed: {e}")

    except ValueError as e:
        # Permanent error - fail immediately
        raise PermanentError(f"Invalid input: {e}")
```

### Step 2: Register the Job Type

Create a fixture or use the desk to add a Job Type record:

```json
{
  "doctype": "Job Type",
  "type_name": "my_custom_job",
  "display_name": "My Custom Job",
  "handler_method": "dartwing.dartwing_core.background_jobs.handlers.my_handler.execute_my_job",
  "default_timeout": 120,
  "default_priority": "Normal",
  "max_retries": 3,
  "is_enabled": 1
}
```

### Step 3: Use Your Job Type

```python
job = submit_job(
    job_type="my_custom_job",
    organization="ORG-2025-00001",
    parameters={"input_data": "..."}
)
```

---

## 6. Handle Job Results

### Poll for Completion

```python
import time
from dartwing.dartwing_core.background_jobs import get_job_status

def wait_for_job(job_id, timeout=300):
    """Wait for job completion with timeout."""
    start = time.time()
    while time.time() - start < timeout:
        status = get_job_status(job_id)

        if status.status == "Completed":
            return status.output_reference
        elif status.status in ["Failed", "Dead Letter", "Canceled"]:
            raise Exception(f"Job failed: {status.error_message}")

        time.sleep(2)

    raise TimeoutError(f"Job {job_id} did not complete in {timeout}s")

# Usage
result_path = wait_for_job("JOB-2025-00001")
print(f"Result available at: {result_path}")
```

### Callback Pattern (Recommended)

```python
# When submitting, include a callback URL or doctype
job = submit_job(
    job_type="pdf_generation",
    organization="ORG-2025-00001",
    parameters={
        "template": "report",
        "callback_doctype": "Report Request",
        "callback_name": "REQ-2025-00001"
    }
)

# In your job handler, update the callback on completion
def execute_pdf_generation(context: JobContext):
    # ... generate PDF ...

    # Update the requesting document
    if context.parameters.get("callback_doctype"):
        frappe.db.set_value(
            context.parameters["callback_doctype"],
            context.parameters["callback_name"],
            "pdf_file", output_path
        )
```

---

## 7. Cancel a Job

### Python

```python
from dartwing.dartwing_core.background_jobs import cancel_job

cancel_job("JOB-2025-00001")
```

### API

```bash
curl -X POST \
  'https://your-site.com/api/method/dartwing.dartwing_core.api.jobs.cancel_job' \
  -H 'Authorization: token api_key:api_secret' \
  -H 'Content-Type: application/json' \
  -d '{"job_id": "JOB-2025-00001"}'
```

---

## 8. View Job Metrics (Admin)

### API

```bash
curl 'https://your-site.com/api/method/dartwing.dartwing_core.api.jobs.get_job_metrics' \
  -H 'Authorization: token api_key:api_secret'
```

### Response

```json
{
  "message": {
    "job_count_by_status": {
      "Running": 8,
      "Queued": 15,
      "Dead Letter": 3
    },
    "queue_depth_by_priority": {
      "Critical": 1,
      "High": 5,
      "Normal": 8,
      "Low": 1
    },
    "processing_time": {
      "average_seconds": 4.5,
      "p95_seconds": 12.3
    }
  }
}
```

---

## Common Patterns

### Pattern 1: Fire and Forget

```python
# Submit job and don't wait
submit_job(job_type="send_welcome_email", organization=org, parameters={...})
# Continue with other work immediately
```

### Pattern 2: Job Chain

```python
# Job A generates data
job_a = submit_job(job_type="generate_report", ...)

# Job B emails the report (waits for A)
job_b = submit_job(job_type="email_report", depends_on=job_a.name, ...)
```

### Pattern 3: Bulk Operations

```python
# Submit many jobs at once
job_ids = []
for item in items:
    job = submit_job(
        job_type="process_item",
        organization=org,
        parameters={"item_id": item.name},
        priority="Low"  # Low priority for bulk
    )
    job_ids.append(job.name)
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Job stuck in "Pending" | Check that workers are running: `bench worker` |
| Job fails immediately | Check error_type - if "Permanent", fix input data |
| Progress not updating | Ensure Socket.IO is connected and joined correct room |
| Duplicate job rejected | Wait for deduplication window (default: 5 min) or use different parameters |
| Job timeout | Increase timeout in Job Type or optimize handler |

---

## Next Steps

- Read the full [API Contract](./contracts/api.md) for all endpoints
- Review [Data Model](./data-model.md) for doctype details
- Check [Research](./research.md) for architectural decisions
