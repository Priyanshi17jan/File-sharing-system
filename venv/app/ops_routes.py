from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from app import mongo

ops_bp = Blueprint('ops', __name__)

@ops_bp.route('/login', methods=['POST'])
def ops_login():
    # Implement Ops User login logic
    # Example: Check credentials in the request and return a JWT token
    username = request.json.get('username')
    password = request.json.get('password')

    # Your authentication logic here (this is a simplified example)
    if username == 'ops_user' and password == 'password':
        # Generate and return a JWT token
        return jsonify({'token': 'your_generated_token'}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@ops_bp.route('/upload', methods=['POST'])
def ops_upload():
    # Implement file upload logic
    # Example: Save uploaded file to MongoDB GridFS

    # Check if the POST request has the file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    # Check if the file is selected
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Check if the file type is allowed (pptx, docx, xlsx)
    allowed_extensions = {'pptx', 'docx', 'xlsx'}
    if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
        return jsonify({'error': 'Invalid file type. Allowed types: pptx, docx, xlsx'}), 400

    # Save the file to MongoDB GridFS
    filename = secure_filename(file.filename)
    file_id = mongo.save_file(filename, file)

    return jsonify({'file_id': str(file_id)}), 201
