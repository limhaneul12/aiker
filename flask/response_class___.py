from flask import Response, make_response, Flask


app = Flask(__name__)



@app.route("/", methods=["GET", "POST"])
def response_test():
    custom_response = Response('Custom Response', 200,
                               {"Program": "Flask Web Application"})
    return make_response(custom_response)


@app.route("/str")
def response():
    return make_response("Custom Response")


@app.route("/ohyes")
def custom_response():
    def application(environ, start_response):
        response_body = "The request method was %s" % environ["REQUEST_METHOD"]

        status = '200 OK'
        response_header = [("Content-Type", "text/plain"),
                           ("Content-Length", str(len(response_body)))]

        start_response(status, response_header)

        return [response_body]
    return make_response(application)


if __name__ == "__main__":
    app.run(debug=True)