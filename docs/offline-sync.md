# Offline Synchronization

TerraSync is built for environments where connectivity is unreliable.

## Sync Flow

```text
1. Engineer captures data offline
2. Data is saved to SQLite
3. Changes are added to a local queue
4. Connectivity returns
5. Sync engine uploads changes to FastAPI
6. Backend validates and stores data in PostgreSQL
7. Dashboard updates for supervisors
```

## What Syncs

- Work order status
- Check-in and check-out records
- Inspection checklist results
- Measurements
- Remarks
- Defects
- Report summaries
- Photo evidence metadata

## Photo Metadata

Each photo stores only:

- GPS coordinates
- Timestamp
- Site ID

Photos are evidence inside a report, not separate report records.

## Conflict Handling

Initial conflict handling can follow simple rules:

- Latest update wins for non-critical draft data
- Server validation rejects incomplete submitted reports
- Supervisor review handles disputed reports
- Audit logs preserve change history

## Reliability Goals

- No data loss during offline work
- Retry failed sync operations
- Queue changes in order
- Validate data before submission
- Keep engineers productive without internet
