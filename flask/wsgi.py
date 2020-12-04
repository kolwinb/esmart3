#!venv/bin/python3
#def application(env, start_response):
#    start_response('200 OK', [('Content-Type','text/html')])
#    return [b"Hello World"]

from api import app

if __name__ == "__main__":
    app.run()
