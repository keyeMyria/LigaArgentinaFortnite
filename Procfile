web: gunicorn --pythonpath="$PWD/torneo" config.wsgi:application
worker: python manage.py rqworker default
