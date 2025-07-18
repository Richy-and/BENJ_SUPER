# Configuration Gunicorn optimisée pour Render
import os
import multiprocessing

# Bind configuration
bind = f"0.0.0.0:{os.environ.get('PORT', 5000)}"

# Worker configuration
workers = min(multiprocessing.cpu_count() * 2 + 1, 4)  # Max 4 workers pour le plan gratuit
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 2
max_requests = 1000
max_requests_jitter = 100

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Performance
preload_app = True
enable_stdio_inheritance = True

# Process naming
proc_name = "benj-inside"

# Graceful timeout
graceful_timeout = 30

# Memory optimization
max_worker_memory = 200  # MB

def when_ready(server):
    server.log.info("BENJ INSIDE Server is ready. Listening on %s", server.address)

def worker_int(worker):
    worker.log.info("Worker received INT or QUIT signal")

def pre_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)