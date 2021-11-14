import os
from typing import TYPE_CHECKING


from flask import Flask
from werkzeug.serving import run_simple
from werkzeug.wsgi import get_path_info, wrap_file
from werkzeug.http import parse_accept_header
from werkzeug.datastructures import EnvironHeaders


if TYPE_CHECKING:
    from typing import Iterable
    from _typeshed.wsgi import WSGIApplication, WSGIEnvironment, StartResponse


class ContentNegotiatorMiddleware:
    def __init__(self, app: "WSGIApplication"):
        self.app = app

    def __call__(self, environ: "WSGIEnvironment", start_response: "StartResponse") -> "Iterable[bytes]":
        # This file path handling code is meant as an example and is not secure.
        path = get_path_info(environ)
        local_path = os.path.join(os.getcwd() + path)
        local_path_gz = os.path.join(local_path + ".gz")

        parsed_headers = EnvironHeaders(environ)
        accepted_encodings = parse_accept_header(parsed_headers.get("accept-encoding"))
        resp_headers = []

        if 'gzip' in accepted_encodings and os.path.exists(local_path_gz):
            serve_path = local_path_gz
            resp_headers.append(("Content-Encoding", "gzip"))
        elif os.path.exists(local_path):
            serve_path = local_path
        else:
            raise Exception("No.")

        resp_headers.extend([
            ("Content-Type", "text/plain; charset=UTF-8"),
            ("Content-Length", str(os.stat(serve_path).st_size))
        ])

        start_response("200 OK", resp_headers)
        return wrap_file(environ, open(serve_path, 'rb'))


app = Flask(__name__)
content_negotiator = ContentNegotiatorMiddleware(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


if __name__ == "__main__":
    run_simple('localhost', 5000, content_negotiator)
