from flask import request, jsonify
from .db import Database
from werkzeug.security import generate_password_hash, check_password_hash

db = Database()

def create_user(email, password):
    try:
        # Check if the user already exists
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        query = valid_user_query()
        if user_exist(query, email, password):
            return {"error": "User already exists"}, 400
        # Hash the password
       

        # Insert user into the database
        insert_query = """
        INSERT INTO users (email, password_hash) 
        VALUES (%s, %s)
        """
        db.execute_query(insert_query, (email, hashed_password))

        return {"message": "User registered successfully"}, 201
    except Exception as e:
        print("Error during registration:", e)
        return {"error": "Internal server error"}, 500


def user_exist(query, email, password):
    try:
        # Get user by email only
        existing_user = db.fetch_query(query, (email,))  # Note: only passing email
        
        if not existing_user:
            return None
            
        user = existing_user[0]
        
        # Verify password against stored hash
        if check_password_hash(user['password_hash'], password):
            return existing_user  # Return the full user data if password matches
            
        return None  # Return None if password doesn't match
        
    except Exception as e:
        print(f"Error checking user existence: {e}")
        raise

def valid_user_query():
    # Changed to only query by email
    return "SELECT user_id, email, password_hash FROM users WHERE email = %s"
