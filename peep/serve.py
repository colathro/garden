from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/")
def hello():
    message = "Hello, World"
    return render_template('index.html', message=message)


@app.route("/startuplogs")
def hello():
    with open("/tmp/rc.local.log", "r") as logfile:
        message = logfile.read()
        return render_template('logs.html', message=message)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
