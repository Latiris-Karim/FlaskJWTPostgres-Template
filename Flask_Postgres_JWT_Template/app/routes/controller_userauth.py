from flask import Blueprint, request, jsonify
from ..services.db import Database
from ..services.user_handling import create_user, user_exist, valid_user_query

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from datetime import timedelta

users = Blueprint('users', __name__)
db = Database()



@users.route('/login', methods=['POST'])
def user_login():
    # Get JSON data with more robust error handling
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400

    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Validate required fields
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    
    try:
        # Get query and check if user exists
        query = valid_user_query()
        result = user_exist(query, email, password)

        if not result:
            return jsonify({'error': 'Invalid email or password',
                            "information": result}), 401

        # Get the first (and should be only) user from results
        user = result[0]
        
        # Create JWT token with user information
        access_token = create_access_token(
            identity=user['email'],
            additional_claims={
                'user_id': user['user_id']  # Make sure this matches your DB column name
            },
            expires_delta=timedelta(hours=1)
        )
        
        # Fixed indentation and added return statement inside try block
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': {
                'id': user['user_id'],  # Using UUID from your response
                'email': user['email']
            }
        }), 200
        
    except Exception as e:
        # Added more detailed error logging
        print(f"Login error: {str(e)}")
        return jsonify({'error': 'An error occurred during login'}), 500

#only return jsonify in this route call multiple jsonifies give error
@users.route('/register', methods=['POST'])
def user_register():
    data = request.json #as post request it's inside the 'body' get request uses route parameters.
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    
    try:
        response = create_user(email, password)
        return jsonify(response), 201
    except Exception as e:
        print(f"Error during user registration: {e}")
        return jsonify({"error": "Internal server error"}), 500
        

@users.route('/tokentest', methods=['GET'])
@jwt_required()
def tokentester():
    current_user = get_jwt_identity()
    return jsonify({
        "message": "You accessed a protected route",
        "your_email": current_user
    })
