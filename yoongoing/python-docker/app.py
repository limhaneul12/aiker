from flask import Flask

app = Flask('app')


@app.route('/')
def index():
    return "I'm from docker"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
