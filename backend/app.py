from flask import Flask, make_response, jsonify
from routes import auth_bp

app = Flask(__name__)

app.register_blueprint(auth_bp)

app.run(debug=True)
