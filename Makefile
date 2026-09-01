.PHONY: demo test docker

demo:
	cd backend && python -m uvicorn app.main:app --reload

test:
	cd backend && python -m pytest -q

docker:
	cd docker && docker compose up --build
