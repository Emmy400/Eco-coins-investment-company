from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize database and login manager
db = SQLAlchemy(app)
login_manager = LoginManager(app)

# User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Load user for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Authentication routes
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and user.password == data['password']:
        login_user(user)
        return jsonify({'message': 'Logged in successfully!'}), 200
    return jsonify({'message': 'Invalid username or password!'}), 401

@app.route('/logout')
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully!'}), 200

# Investment endpoints
@app.route('/invest', methods=['POST'])
@login_required
def invest():
    data = request.json
    # Placeholder logic for investments
    return jsonify({'message': 'Investment successful!'}), 200

@app.route('/api/crypto_price', methods=['GET'])
def get_crypto_price():
    response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')
    return jsonify(response.json()), 200

if __name__ == '__main__':
    app.run(debug=True)