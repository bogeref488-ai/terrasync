# TerraSync Architecture

TerraSync is designed as an offline-first field operations platform. The architecture separates field data capture, synchronization, backend processing, reporting, and dashboard visibility.

## Core Layers

```text
Mobile App
↓
SQLite Local Database
↓
Offline Sync Queue
↓
FastAPI Backend
↓
PostgreSQL Central Database
↓
Operations Dashboard
```

## Mobile Layer

The mobile app is used by field engineers to:

- Receive assigned work orders
- Check in and check out on site
- Complete safety readiness
- Load inspection templates
- Capture measurements, remarks, defects, and photo evidence
- Save data offline
- Synchronize when connectivity returns

## API and Backend Layer

The backend is built around Python and FastAPI. It provides services for:

- Authentication
- Work orders
- Inspection templates
- Reports
- Defects
- Users and roles
- Assets and sites
- Synchronization
- Reporting and exports

## Data Layer

TerraSync uses:

- SQLite for local offline data storage on the field device
- PostgreSQL for centralized operational data
- Redis for queues, background tasks, and caching where needed
- Object storage for report files and media evidence

## Design Principles

- Offline-first by design
- Template-driven inspections
- Secure synchronization
- Data integrity and auditability
- Modular and extensible services
- Open-source and community-driven
