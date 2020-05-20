from flask import Flask
from flask_restful import reqparse, Resource, Api, abort
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


parser = reqparse.RequestParser()
parser.add_argument("task")

class Todo(Resource):
    def get(self, todo_id):
        abort_if_docker_file_exits(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_docker_file_exits(todo_id)
        del TODOS[todo_id]
        return "", 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {"task": args["task"]}
        TODOS[todo_id] = task
        return task, 201


@api.resource('/info', methods=["POST"], endpoint="/info")
class TodoList(Resource):
    def post(self):
        return {"task 1": doc.docker_container_inspect()}

@api.resource("/information", methods=["GET"], endpoint="/information")
class docker_list(Resource):
    def post(self):
        args = parser.parse_args()
        todo_id = "todo%d" % (len(TODOS) + 1)
        TODOS[todo_id] = {"task": args["task"]}
        return TODOS[todo_id], 201

    def get(self):
        return TODOS

api.add_resource(TodoList, "/todos/")
api.add_resource(Todo, "/todos/<string:todo_id>")



if __name__ == "__main__":
    app.run(debug=True)
