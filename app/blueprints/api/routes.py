from xml.sax.handler import property_dom_node
from . import bp as api
from flask import jsonify, request
from app.models import User, Product
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
@api.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def updated_user(id):
    current_user = token_auth.current_user()
    if current_user.id != id:
        return jsonify({'error': 'You do not have access to update this user'}), 403
    user = User.query.get_or_404(id)
    data = request.json
    user.update(data)
    return jsonify(user.to_dict())

# Delete a user by id
@api.route('/users/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_user(id):
    current_user = token_auth.current_user()
    if current_user.id != id:
        return jsonify({'error': 'You do not have access to delete this user'}), 403
    user_to_delete = User.query.get_or_404(id)
    user_to_delete.delete()
    return jsonify({}), 204



# Get all Products
@api.route('/products')
def get_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])


# Get one Product by id
@api.route('/products/<int:id>')
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify(product.to_dict())


# Update a Product by id
@api.route('/products/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_product(id):
    user = token_auth.current_user()
    if not user.is_admin:
        return jsonify({'error': 'You are not allowed to update products'}), 403
    data = request.json
    product = Product.query.get_or_404(id)
    product.update(data)
    return jsonify(product.to_dict())


# Delete a Product by id
@api.route('/products/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_product(id):
    user = token_auth.current_user()
    if not user.is_admin:
        return jsonify({'error': 'You are not allowed to delete products'}), 403
    product = Product.query.get_or_404(id)
    product.delete()
    return jsonify({}), 204

