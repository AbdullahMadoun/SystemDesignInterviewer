# Topic Bank, Archetype Rotation & Weak-Point Mapping

Read this file in Phase 0 to pick the session's topic. Never reveal the archetype or why you chose it.

## Archetype Rotation Matrix

| # | Archetype | Core forces | Example topics |
| :-: | :--- | :--- | :--- |
| 1 | **Storage Engines & Distributed Consensus** | LSM vs. B-tree, WAL, replication, quorums, leader election, consistent hashing | Distributed KV store, distributed lock service, distributed SQL database, unique ID generator |
| 2 | **Search, Indexing & Retrieval** | Inverted indexes, tries, ranking, index sharding, segment merging | Web search, typeahead autocomplete, log search platform, Yelp/nearby places |
| 3 | **Large-Scale File & Blob Storage** | Metadata/data separation, chunking, replication vs. erasure coding, CDNs | Dropbox/Google Drive, object store (S3), YouTube upload & streaming |
| 4 | **Real-Time Collaborative & Stateful** | WebSocket fan-out, presence, OT/CRDTs, connection management | Google Docs, Slack/WhatsApp chat, live comments, multiplayer game lobby |
| 5 | **Graph Systems & Feed Ranking** | Fan-out on write vs. read, celebrity problem, graph partitioning, ranking | Twitter/X news feed, LinkedIn connections, recommendation engine |
| 6 | **Async Streaming & Queuing** | Brokers, partitioning, windowing, consumer groups, retries/DLQs, idempotency | Webhook delivery, job scheduler, ad click aggregator, notification service |
| 7 | **Transactions & Contention** | Inventory contention, distributed transactions, idempotent payments, rate limiting | Ticketmaster, flash sale, payment system, distributed rate limiter, Uber ride matching |

## Selection Rules (in order of precedence)

1. **Anti-Repetition Rule (hard):** never pick the same archetype as the immediately previous session in `candidate_profile.md`.
2. **No repeat topics:** never re-run a topic already in the session log unless the candidate asks for it.
3. **Weak-point mode:** choose from the mapping below, subject to rules 1–2.
4. **Otherwise:** prefer the archetype the candidate has practiced least.

## Weak-Point Mapping

| Weak dimension in the profile | Good topic choices (choose a different archetype from last session) |
| :--- | :--- |
| Concurrency / race conditions | Ticketmaster or flash sale (7), distributed lock service (1), Google Docs (4) |
| Board completeness / ingress / failure paths | Webhook delivery (6), payment system (7), Dropbox (3) |
| High-throughput storage & math | Ad click aggregator (6), metrics/telemetry platform (6), YouTube (3) |
| Data modeling & indexing | Yelp/nearby places (2), typeahead (2), LinkedIn connections (5) |
| Read-scaling & caching | News feed (5), URL shortener (1), YouTube streaming (3) |
| Consistency & replication | Distributed KV store (1), chat with message ordering (4), payment system (7) |

## Prompt Style

Deliver the topic as one sentence, with no requirements attached, e.g.:
> "Design a service that lets users buy tickets for popular live events. You have 45 minutes."
