# Mock application logs -- stands in for a real log aggregator (Datadog/CloudWatch/etc.)
LOGS = [
    "2026-08-15 10:02:11 ERROR PaymentService timeout while contacting gateway",
    "2026-08-15 10:02:45 WARN Redis connection retry (attempt 1/3)",
    "2026-08-15 10:05:03 ERROR Database connection pool exhausted",
    "2026-08-16 09:12:00 ERROR AuthService 401 invalid token for user_id=12",
    "2026-08-16 14:30:22 WARN High latency detected on /api/v1/chat (2.3s)",
    "2026-08-17 08:00:00 INFO Scheduled backup completed successfully",
    "2026-08-17 11:45:10 ERROR RefundService failed to reach OrderAPI (connection refused)",
]