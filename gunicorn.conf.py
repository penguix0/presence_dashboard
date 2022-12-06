import multiprocessing

bind = "0.0.0.0:8000"
## Using threads instead of workers because csrf gets messed up otherwise
workers = 1
threads = multiprocessing.cpu_count() * 2 + 1
wsgi_app = "dashboard:app"