# app.py

from flask import Flask
from flask_cors import CORS
from database import init_db
from routes import routes

app = Flask(__name__)
CORS(app)

# Initialize the database
init_db()

# Register the blueprint for routes
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=3001)

