from flask import Flask
from flask_pymongo import PyMongo
from flasgger import Swagger

def create_app():
    app = Flask(__name__)
    Swagger(app)

    return app

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongo'
mongo = PyMongo(app)


if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Here we use port 5001 instead of the default port 5000

