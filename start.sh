source simpleappenv/bin/activate
gunicorn --workers 5 --bind unix:dashboard.sock -m 007 src:app
deactivate