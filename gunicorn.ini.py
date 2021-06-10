"""gunicorn flask server configuration."""
from os import environ, path, getcwd
workers = 1
daemon = True
loglevel = 'info'
capture_output = True
worker_class = "eventlet"
bind = f"0.0.0.0:{environ.get('PORT', '8000')}"
errorlog = path.join(getcwd(), "server", "logs", "gunicorn.info.log")
accesslog = path.join(getcwd(), "server", "logs", "gunicorn.access.log")