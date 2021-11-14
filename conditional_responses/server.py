import datetime

from flask import Flask, jsonify, request, abort


app = Flask(__name__, static_folder="static")

boot_time = datetime.datetime.utcnow()
_database = []


@app.route("/")
def index_html():
    return app.send_static_file("index.html")


@app.route("/api/heroes")
def get_heroes():
    return jsonify(_database)


@app.route("/api/heroes/<int:hero_id>")
def get_hero(hero_id: int):
    resp_obj = [x for x in _database if x.get("id") == hero_id]
    if len(resp_obj) == 0:
        abort(404)

    json_response = jsonify(resp_obj[0])

    json_response.cache_control.public = True
    json_response.cache_control.must_revalidate = True
    json_response.cache_control.max_age = 5
    json_response.last_modified = boot_time
    json_response.add_etag()

    json_response = json_response.make_conditional(request.environ)

    return json_response


@app.route("/api/heroes", methods=["POST"])
def post_hero():
    if not request.is_json:
        abort(500)
    integer = 1
    for integer in range(1, 1000):
        if integer not in [x["id"] for x in _database]:
            break
    hero_obj = request.json
    hero_obj["id"] = integer
    _database.append(hero_obj)
    return jsonify(hero_obj)


if __name__ == "__main__":
    app.run()