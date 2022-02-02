from . import bp as api
from flask import jsonify, request
from app.models import User
from .auth import basic_auth, token_auth

# Get token
@api.route('/token', methods=['POST'])
@basic_auth.login_required
def get_token():
    user = basic_auth.current_user()
    token = user.get_token()
    return jsonify({'token': token})

# Get all users
@api.route('/users')
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])


# Get a single user by id
@api.route('/users/<id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())


# Create a user
@api.route('/users', methods=['POST'])
def create_user():
    data = request.json
    # Validate the data
    for field in ['username', 'email', 'password']:
        if field not in data:
            return jsonify({'error': f"You are missing the {field} field"}), 400

    # Grab the data from the request body
    username = data['username']
    email = data['email']
    password = data['password']

    # Check if the username or email already exists
    user_exists = User.query.filter((User.username == username)|(User.email == email)).all()
    # if it is, return back to register
    if user_exists:
        return jsonify({'error': f"User with username {username} or email {email} already exists"}), 400

    # Create the new user
    # new_user = User(username=username, email=email, password=password)
    new_user = User(**data)

    return jsonify(new_user.to_dict())

# Update a user by id
@api.route('/users/<id>', methods=['PUT'])
@token_auth.login_required
def updated_user(id):
    pass


# Delete a user by id
@api.route('/users/<id>', methods=['DELETE'])
@token_auth.login_required
def delete_user(id):
    pass

