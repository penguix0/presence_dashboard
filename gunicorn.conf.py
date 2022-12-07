import multiprocessing

bind = "unix:dashboard.sock"
## Using threads instead of workers because csrf gets messed up otherwise
workers = 1
threads = multiprocessing.cpu_count() * 2 + 1
wsgi_app = "dashboard:app"
umask = "007"