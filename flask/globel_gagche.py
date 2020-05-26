from flask import Flask
from flask_restful import Api, Resource, abort
import dokcer__ as doc

app = Flask(__name__)
api = Api(app)

TODOS = {
    "todo1": {"task": doc.docker_container_cleaner()},
    "todo2": {"task": doc.docker_container_inspect()}
}


def abort_if_docker_file_exits(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn`t exit".format(todo_id))


@api.app.route("/docker", methods=["POST"])
def POST():
    TODOS = {
        "todo1": {"task": doc.docker_container_cleaner()},
        "todo2": {"task": doc.docker_container_inspect()}
    }
    return TODOS


if __name__ == "__main__":
    api.app.run(debug=True)