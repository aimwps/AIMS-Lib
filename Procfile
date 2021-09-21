web: gunicorn AimsLib.wsgi
worker: celery -A AimsLib.celery worker -B --loglevel=info
