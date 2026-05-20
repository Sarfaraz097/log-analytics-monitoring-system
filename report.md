# System Health Intelligence Report

**Period:** 2026-04-01 00:00 to 2026-04-07 22:29

## KPI Summary

| Metric | Value |
|--------|-------|
| Total Events | 200000 |
| Total Errors | 50252 |
| Error Rate | 25.13% |
| Error Density | 5.03 errors/min |
| Uptime Score | 74.87% |
| Suspicious Users | 899 |
| Unauthorized IPs | 6631 |

## Top 5 Failing Components

| Rank | Component | Errors |
|------|-----------|--------|
| 1 | CacheService | 2368 |
| 2 | QueueService | 2360 |
| 3 | NotificationService | 2336 |
| 4 | InventoryService | 2336 |
| 5 | SecurityService | 2313 |

## Failure Nature Breakdown

| Event Type | Count |
|------------|-------|
| Other | 86792 |
| Queue Backlog | 6794 |
| Disk Space Low | 6768 |
| Login Failure | 6723 |
| Suspicious Activity | 6709 |
| Third-party API Failure | 6689 |
| Login Success | 6680 |
| Service Restart | 6674 |
| Slow Query | 6664 |
| Deadlock | 6657 |

## Anomaly Insights

- OrderService is in a crash-restart loop
- Deadlock storm detected — ~1 per minute
- Distributed brute-force attack on /admin
- Queue saturation on orderQueue
- Resource exhaustion — CPU, Memory, Disk alerts