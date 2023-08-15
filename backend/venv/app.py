from routes.auth import auth_bp
from flask import Flask
app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)





app.register_blueprint(auth_bp, url_prefix='/auth')
