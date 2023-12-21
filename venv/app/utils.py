from itsdangerous import URLSafeTimedSerializer
from flask import current_app

def generate_secure_url(data):
    # Generate a secure, time-limited URL using itsdangerous library
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(data, salt=current_app.config['SECURE_URL_SALT'])

def verify_secure_url(token, max_age):
    # Verify and load data from a secure URL token
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        data = serializer.loads(token, salt=current_app.config['SECURE_URL_SALT'], max_age=max_age)
        return data
    except Exception as e:
        # Handle verification failure (e.g., expired token)
        return None
