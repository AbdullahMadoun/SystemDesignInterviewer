# Capacity Estimation Constants

Use these to **validate** the candidate's math during Phase 2. Never hand them to the candidate during the interview. Accept anything within the same order of magnitude unless the error changes a design decision.

## Time
| Unit | Exact | Working approximation |
| :--- | :--- | :--- |
| 1 day | 86,400 s | ≈ 10⁵ s |
| 1 month | ~2.6 × 10⁶ s | ≈ 2.5 × 10⁶ s |
| 1 year | ~3.15 × 10⁷ s | ≈ 3 × 10⁷ s |

**QPS shortcut:** 1M requests/day ≈ 12 QPS average. Peak ≈ 2–10× average (10× is the conservative interview heuristic).

## Storage
| Rule | Value |
| :--- | :--- |
| 1M × 1 KB | 1 GB |
| 1B × 1 KB | 1 TB |
| 1B × 1 MB | 1 PB |
| Typical DB row / metadata | 100 B – 1 KB |
| Image | 200 KB – 2 MB |
| Short video (compressed, per minute of HD) | ~5 – 50 MB |

## Latency (orders of magnitude)
| Operation | Approx. |
| :--- | :--- |
| L1 cache / main memory reference | ~1 ns / ~100 ns |
| Read 1 MB sequentially from memory | ~10 µs |
| SSD random read | ~100 µs |
| Round trip within a datacenter | ~0.5 ms |
| Read 1 MB sequentially from SSD | ~1 ms |
| Disk seek (HDD) | ~10 ms |
| Cross-continent round trip | ~100–150 ms |

## Throughput rules of thumb (single node, order of magnitude)
| Component | Approx. |
| :--- | :--- |
| Stateless app server | 1k – 10k+ RPS (workload dependent) |
| Relational DB (well-indexed simple queries) | ~1k – 10k QPS writes, more for reads |
| In-memory cache node | ~100k+ ops/s |
| Log/stream broker partition | ~10 MB/s – 100 MB/s |

## Typical read:write ratios
| Workload | Ratio |
| :--- | :--- |
| Social feeds, URL shortener, video | 10:1 – 100:1 |
| Chat / messaging | ~1:1 – 5:1 |
| Metrics, telemetry, logging | ~1:100 (write-heavy) |
