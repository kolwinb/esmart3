#!/bin/bash
#uwsgi --http :9090 --wsgi-file wsgi.py --master --processes 4 --threads 2 --stats 127.0.0.1:9191

#django
#uwsgi --socket 127.0.0.1:3031 --chdir /home/foobar/myproject/ --wsgi-file myproject/wsgi.py --master --processes 4 --threads 2 --stats 127.0.0.1:9191

#flask
#uwsgi --socket 127.0.0.1:5000 --wsgi-file wsgi.py --callable app --processes 4 --threads 2 --stats 127.0.0.1:9191
uwsgi --socket 0.0.0.0:5000 --protocol=http --wsgi-file wsgi:app 

