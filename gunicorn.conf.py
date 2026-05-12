import multiprocessing
import os

# Server socket
port = os.environ.get("PORT", "5000")
bind = f"0.0.0.0:{port}"
backlog = 2048

# Worker processes
# A typical rule of thumb is (2 x $num_cores) + 1
workers = int(os.environ.get("GUNICORN_WORKERS", multiprocessing.cpu_count() * 2 + 1))
worker_class = "sync"
threads = int(os.environ.get("GUNICORN_THREADS", 2))
worker_connections = 1000
timeout = int(os.environ.get("GUNICORN_TIMEOUT", 120))
keepalive = 2

# Logging
errorlog = "-"
loglevel = "info"
accesslog = "-"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "pc_mlra"

# Environment variables
raw_env = [
    "FLASK_ENV=production"
]
