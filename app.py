from flask import Flask
import os
app = Flask(__name__)


@app.route("/")
def hello_world():
    return 'Hello world!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT') or 8080)
