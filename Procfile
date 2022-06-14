release: alembic upgrade head
web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker grocerystore.main:app
