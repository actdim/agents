# Backend & Service Engineering Guidelines & Best Practices

Strict architectural and reliability standards for backend services, APIs, and microservices.

---

## 1. API Contract Design & Validation

1. **Explicit API Contracts**:
   - Define API contracts using formal schemas (OpenAPI / JSON Schema, Protocol Buffers / gRPC).
   - Validate all incoming request payloads at the controller boundary before invoking domain handlers.

2. **Error Envelope Consistency**:
   - Return standard RFC 7807 (Problem Details) or consistent structured JSON error responses containing `code`, `message`, and optional validation details.

---

## 2. Statelessness & Distributed Concurrency

1. **Stateless Service Layer**:
   - Design application nodes as stateless processes (12-Factor App); store session state in distributed caches (e.g. Redis) or signed tokens (JWT).

2. **Idempotent Operations**:
   - Enforce idempotency keys on payment, order placement, and critical mutating endpoints to prevent duplicate processing on network retries.

---

## 3. Database Transactions & Connection Hygiene

1. **Atomic Transactions**:
   - Wrap multi-table domain mutations in explicit ACID database transactions. Keep transaction scopes short to minimize row locking.

2. **Connection Pooling & Query Optimization**:
   - Always configure bounded connection pools with health checks and query timeouts.
   - Prevent N+1 query patterns by using eager loading, batch joins, or data loaders.

---

## 4. Observability & Health Probes

1. **Structured Logging & Correlation**:
   - Emit structured JSON logs containing timestamp, log level, message, and distributed `trace_id` / `correlation_id`.

2. **Standard Health Endpoints**:
   - Provide `/health/liveness` (service process is running) and `/health/readiness` (database and downstream dependencies are connected) endpoints for orchestrators.

