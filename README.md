# TerraSync — Milestone 2

# TerraSync Milestone 2

Milestone 2 connects the Milestone 1 role/device foundation to the field workflow and refreshes all three application surfaces.

## Working flow

1. Coordinator signs in and publishes an assignment.
2. Field technician activates a phone once with username + OTP.
3. The phone keeps its registered session and opens directly on later launches.
4. Assignments are cached locally.
5. Technician starts/continues an assignment.
6. Client-supplied inventory is downloaded when online.
7. Missing assets can be created on-site with manufacturer, model, serial, quantity, height/elevation, dimensions, position, condition and notes.
8. On-site assets require a live-camera full-picture capture.
9. Inspection drafts and the sync outbox are persisted in IndexedDB.
10. Evidence is captured by live camera, resized/compressed and watermarked with GPS + time only.
11. Asset changes synchronize before report submission.
12. Report sync is authenticated and idempotent.
13. Submission runs AI pre-screening.
14. Coordinator receives the report in the AI review queue and can approve or return it.
15. Supervisor dashboard reflects completion, pending review, critical reports and escalations.
16. PDF report generation remains available.

## Routes

- Field: `/app/`
- Coordinator: `/coordinator/`
- Supervisor: `/supervisor/`
- API: `/docs`

## Demo access

Field technician:
- username: `field.tech`
- activation code: `246810`

Coordinator:
- username: `coordinator`
- password: `demo123`

Supervisor:
- username: `supervisor`
- password: `demo123`

## Local database

The schema now includes the `assets` table. For a local SQLite demo, delete the old database before first launch of this build. Production should use Alembic migrations rather than dropping a database.

## Tested

- one-time device activation
- persistent device session
- RBAC
- coordinator assignment publication
- technician assignment receipt
- technician assignment start
- asset creation with assignment authorization
- report synchronization
- idempotency
- AI screening
- coordinator review
- supervisor metrics
- PDF generation
- JavaScript syntax


---

# TerraSync MVP

TerraSync is an offline-first, AI-assisted field surveying, inspection and reporting platform.

## What works in this MVP

- FastAPI REST backend with SQLite for zero-config demos and PostgreSQL for Docker deployments.
- Sites, work orders, inspection reports, defects, AI findings and change events persisted with SQLAlchemy.
- Installable responsive PWA served by the backend.
- Offline app shell plus a persistent local outbox for inspection submissions.
- Idempotent push sync and cursor-based pull sync.
- Conflict detection through report revisions.
- Local hybrid AI/rules pre-screening for completeness, inconsistent values, abnormal readings, safety risks and critical conditions.
- Human-review oriented AI findings and risk score.
- PDF report generation including inspection data, AI findings and evidence manifest.
- Demo seed data and automated end-to-end tests.

## Fastest demo

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:

- App: http://localhost:8000/app/
- API docs: http://localhost:8000/docs

The default database is `backend/terrasync.db` and demo data is created automatically.

## PostgreSQL demo

```bash
cd docker
docker compose up --build
```

Then open http://localhost:8000/app/.

## Offline demonstration

1. Open the app while online once.
2. Open **New inspection**.
3. Use browser devtools to switch the network to Offline.
4. Submit an inspection. It remains in the local outbox.
5. Re-enable network access and press **Sync**.
6. Open **Reports** to see the server AI risk score and download the generated PDF.

## AI safety model

The MVP intentionally uses a local deterministic pre-screening engine. It never autonomously approves reports. It flags issues for a human coordinator and works without internet access. The engine is designed to be replaced or augmented by a model provider later while preserving the same `AIFinding` contract.

## Production gaps after MVP

Authentication/authorization, encrypted evidence object storage, signed evidence provenance, background job processing, schema migrations, richer template authoring, device enrollment, telemetry, and production-grade observability remain follow-on work.
