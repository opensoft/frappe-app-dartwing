# Socket.IO Horizontal Scaling Specification

**Objective:** Enable Socket.IO real-time messaging across multiple Frappe/Gunicorn worker processes and server nodes.

## Goals

- Deliver real-time events to users connected to any server node
- Support horizontal scaling without sticky sessions requirement
- Maintain room-based messaging across distributed nodes
- Provide observability into connection state and message delivery

## Problem Statement

Frappe's default `frappe.publish_realtime()` broadcasts to the local Socket.IO process only. In a multi-node deployment:

```
User A (Server 1) publishes to room "org_123"
User B (Server 2) is in room "org_123" but NEVER receives the message
```

## Architecture

### Redis Pub/Sub Adapter Pattern

```
┌─────────────────────────────────────────────────────────────────┐
│                    HORIZONTAL SCALING ARCHITECTURE               │
│                                                                  │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐       │
│  │  Server 1   │     │  Server 2   │     │  Server N   │       │
│  │  Gunicorn   │     │  Gunicorn   │     │  Gunicorn   │       │
│  │  Socket.IO  │     │  Socket.IO  │     │  Socket.IO  │       │
│  └──────┬──────┘     └──────┬──────┘     └──────┬──────┘       │
│         │                   │                   │               │
│         └───────────────────┼───────────────────┘               │
│                             │                                    │
│                             ▼                                    │
│         ┌─────────────────────────────────────────┐             │
│         │              Redis Pub/Sub               │             │
│         │                                          │             │
│         │  Channel: dartwing:realtime             │             │
│         │  - All Socket.IO nodes subscribe        │             │
│         │  - Python publishes via redis.publish() │             │
│         └─────────────────────────────────────────┘             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Implementation

### 1. Python Side: Patch `frappe.publish_realtime`

```python
# dartwing_core/realtime/redis_adapter.py

import json
import redis
import frappe

_redis_client = None

def get_redis_client():
    """Get Redis client for Socket.IO pub/sub."""
    global _redis_client
    if _redis_client is None:
        redis_url = frappe.conf.get("redis_socketio") or frappe.conf.get("redis_cache")
        _redis_client = redis.from_url(redis_url)
    return _redis_client


def patch_frappe_realtime():
    """
    Monkey-patch frappe.publish_realtime to use Redis pub/sub.
    Call this on app startup via hooks.py.
    """
    import frappe.realtime

    original_publish = frappe.realtime.publish_realtime

    def redis_publish_realtime(
        event,
        message=None,
        room=None,
        user=None,
        doctype=None,
        docname=None,
        after_commit=True
    ):
        """Enhanced publish that goes through Redis for cross-node delivery."""
        if after_commit:
            frappe.db.after_commit.add(
                lambda: _redis_emit(event, message, room, user, doctype, docname)
            )
        else:
            _redis_emit(event, message, room, user, doctype, docname)

    frappe.realtime.publish_realtime = redis_publish_realtime


def _redis_emit(event, message, room, user, doctype, docname):
    """Publish to Redis channel for all Socket.IO nodes."""
    redis_client = get_redis_client()

    payload = {
        "event": event,
        "message": message,
        "room": room,
        "user": user,
        "doctype": doctype,
        "docname": docname,
    }

    redis_client.publish("dartwing:realtime", json.dumps(payload))
```

### 2. Hooks Configuration

```python
# dartwing_core/hooks.py

# Patch realtime on app startup
on_startup = [
    "dartwing_core.realtime.redis_adapter.patch_frappe_realtime"
]
```

### 3. Node.js Socket.IO Configuration

```javascript
// frappe-bench/apps/dartwing_core/socketio_patch.js

const { createAdapter } = require("@socket.io/redis-adapter");
const { createClient } = require("redis");

async function setupRedisAdapter(io) {
    const redisUrl = process.env.REDIS_SOCKETIO_URL || "redis://localhost:6379";

    // Create pub/sub clients for Socket.IO adapter
    const pubClient = createClient({ url: redisUrl });
    const subClient = pubClient.duplicate();

    await Promise.all([pubClient.connect(), subClient.connect()]);

    // Enable Redis adapter for room synchronization
    io.adapter(createAdapter(pubClient, subClient));

    console.log("Socket.IO Redis adapter connected");

    // Subscribe to Python-published messages
    const messageClient = pubClient.duplicate();
    await messageClient.connect();

    await messageClient.subscribe("dartwing:realtime", (message) => {
        const payload = JSON.parse(message);

        // Route message based on target
        if (payload.room) {
            io.to(payload.room).emit(payload.event, payload.message);
        } else if (payload.user) {
            io.to(`user:${payload.user}`).emit(payload.event, payload.message);
        } else if (payload.doctype && payload.docname) {
            io.to(`doc:${payload.doctype}:${payload.docname}`).emit(
                payload.event,
                payload.message
            );
        } else {
            // Broadcast to all
            io.emit(payload.event, payload.message);
        }
    });
}

module.exports = { setupRedisAdapter };
```

### 4. Room Naming Convention

Consistent room naming across Python and Node.js:

| Target | Room Name | Example |
|--------|-----------|---------|
| User | `user:{email}` | `user:john@example.com` |
| Document | `doc:{doctype}:{name}` | `doc:Task:TASK-00001` |
| Organization | `org:{org_name}` | `org:ORG-2025-00001` |
| Sync Channel | `sync:{doctype}:{org}` | `sync:Task:ORG-2025-00001` |
| Custom | `room:{name}` | `room:dashboard_updates` |

### 5. Nginx Configuration (Optional Sticky Sessions)

While Redis adapter eliminates the need for sticky sessions, they can improve performance by reducing cross-node chatter:

```nginx
# nginx.conf - upstream configuration

upstream socketio {
    ip_hash;  # Sticky sessions by client IP
    server 127.0.0.1:9000;
    server 127.0.0.1:9001;
    server 127.0.0.1:9002;
}

server {
    location /socket.io/ {
        proxy_pass http://socketio;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_read_timeout 86400;
    }
}
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `REDIS_SOCKETIO_URL` | `redis://localhost:6379` | Redis URL for Socket.IO pub/sub |
| `SOCKETIO_WORKERS` | `1` | Number of Socket.IO worker processes |

### site_config.json

```json
{
    "redis_socketio": "redis://localhost:6379/2",
    "socketio_scaling": {
        "enabled": true,
        "sticky_sessions": false
    }
}
```

## Observability

### Metrics

| Metric | Type | Labels | Description |
|--------|------|--------|-------------|
| `socketio_connections_total` | gauge | `server_id` | Current connection count |
| `socketio_rooms_total` | gauge | `server_id` | Active rooms count |
| `socketio_messages_published` | counter | `event_type` | Messages published via Redis |
| `socketio_messages_delivered` | counter | `event_type` | Messages delivered to clients |
| `socketio_redis_latency_ms` | histogram | - | Redis pub/sub latency |

### Logging

```python
# Log format for debugging
frappe.logger().info(
    "realtime_publish",
    event=event,
    room=room,
    user=user,
    server_id=os.environ.get("HOSTNAME"),
)
```

### Alerts

| Alert | Condition | Severity |
|-------|-----------|----------|
| Connection spike | `connections > baseline * 2` for 5m | Warning |
| Redis latency | `p99 latency > 100ms` for 5m | Warning |
| Message backlog | `published - delivered > 1000` for 5m | Critical |
| Redis disconnected | Connection failed for 1m | Critical |

## Test Matrix

| Scenario | Test Method | Expected Result |
|----------|-------------|-----------------|
| Cross-node delivery | Publish from Server 1, verify receipt on Server 2 | Message received |
| User room targeting | Send to `user:X`, verify only X receives | Targeted delivery |
| Document subscription | Subscribe to doc, verify updates received | Real-time updates |
| Redis failover | Kill Redis, verify reconnection | Auto-reconnect |
| High volume | 1000 messages/sec across 3 nodes | All delivered, < 100ms latency |
| Connection cleanup | Disconnect client, verify room cleanup | No orphan rooms |

## Migration Path

### From Single-Node to Multi-Node

1. **Phase 1:** Install Redis adapter, test in staging
2. **Phase 2:** Deploy patch to production with single node
3. **Phase 3:** Add additional Socket.IO nodes behind load balancer
4. **Phase 4:** Enable sticky sessions if performance requires

### Rollback

Disable by removing `on_startup` hook and restarting workers.

---

*Specification version: 1.0*
*Last updated: November 2025*
