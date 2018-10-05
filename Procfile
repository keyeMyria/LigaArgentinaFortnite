web: gunicorn torneo.wsgi --log-file -
worker: python torneo/manage.py rqworker high default low
