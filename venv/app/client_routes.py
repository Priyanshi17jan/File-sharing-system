from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import mongo
from bson import ObjectId
from app.utils import generate_secure_url, verify_secure_url

client_bp = Blueprint('client', __name__)

# ... (previous code)

@client_bp.route('/download-file/<file_id>', methods=['GET'])
@jwt_required()
def client_download_file(file_id):
    # Implement secure file download logic
    current_user = get_jwt_identity()
    user_id = current_user.get('user_id')

    # Check if the user has permission to download the file
    if mongo.db.client_users.find_one({'_id': user_id, 'verified': True}):
        # Generate a secure download link for the file with file_id
        download_link = generate_secure_url({'file_id': file_id, 'user_id': user_id})
        return jsonify({'download-link': download_link, 'message': 'success'}), 200
    else:
        return jsonify({'error': 'Unauthorized access'}), 403

@client_bp.route('/verify-download/<token>', methods=['GET'])
def verify_download(token):
    # Verify the secure download link
    max_age = 3600  # Set the maximum age of the link (in seconds), adjust as needed
    data = verify_secure_url(token, max_age)

    if data:
        # Successfully verified, return the file or perform additional logic
        file_id = data.get('file_id')
        user_id = data.get('user_id')

        # Check if the user has permission to download the file
        if mongo.db.client_users.find_one({'_id': user_id, 'verified': True}):
            # Perform additional logic, e.g., retrieve file from MongoDB GridFS
            # ...

            return jsonify({'message': 'Download verified successfully'}), 200
    else:
        # Verification failed
        return jsonify({'error': 'Invalid or expired download link'}), 401
