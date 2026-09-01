.PHONY: demo test docker

demo:
	cd backend && python -m uvicorn app.main:app --reload

test:
	cd backend && python -m pytest -q

docker:
	cd docker && docker compose up --build

db-status:
	cd backend && python -m app.db.migrate status

db-bootstrap:
	cd backend && python -m app.db.migrate bootstrap

db-upgrade:
	cd backend && python -m app.db.migrate upgrade

db-check:
	cd backend && python -m app.db.migrate check
