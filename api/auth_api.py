# REST API for Authentication System - Test with Postman
from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import hashlib
import secrets
from datetime import datetime, timedelta
from functools import wraps
from enum import Enum

app = Flask(__name__)
CORS(app)

# Configuration
SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Role definitions
class Role(Enum):
    ADMIN = "admin"
    DOCTOR = "doctor"
    PATIENT = "patient"

# In-memory user database
users_db = {
    "admin@hospital.com": {
        "id": 1,
        "email": "admin@hospital.com",
        "password_hash": hashlib.sha256("admin123".encode()).hexdigest(),
        "role": Role.ADMIN.value,
        "name": "Admin User"
    },
    "doctor@hospital.com": {
        "id": 2,
        "email": "doctor@hospital.com",
        "password_hash": hashlib.sha256("doctor123".encode()).hexdigest(),
        "role": Role.DOCTOR.value,
        "name": "Dr. Smith"
    },
    "patient@hospital.com": {
        "id": 3,
        "email": "patient@hospital.com",
        "password_hash": hashlib.sha256("patient123".encode()).hexdigest(),
        "role": Role.PATIENT.value,
        "name": "John Doe"
    }
}

# Helper functions
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Authentication decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'message': 'Token format invalid'}), 401
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        # Decode token
        payload = decode_access_token(token)
        if not payload:
            return jsonify({'message': 'Token is invalid or expired'}), 401
        
        return f(payload, *args, **kwargs)
    
    return decorated

# Role-based access decorator
def role_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated(current_user, *args, **kwargs):
            user_role = current_user.get('role')
            if user_role not in [role.value for role in allowed_roles]:
                return jsonify({
                    'message': 'Access denied',
                    'required_roles': [role.value for role in allowed_roles],
                    'your_role': user_role
                }), 403
            return f(current_user, *args, **kwargs)
        return decorated
    return decorator

# Routes
@app.route('/')
def home():
    return jsonify({
        'message': 'Hospital Authentication API',
        'endpoints': {
            'POST /api/login': 'Login with email and password',
            'GET /api/profile': 'Get user profile (All roles)',
            'GET /api/admin/dashboard': 'Admin dashboard (Admin only)',
            'GET /api/medical-records': 'Medical records (Admin, Doctor)',
            'POST /api/prescribe': 'Prescribe medication (Doctor only)',
            'GET /api/my-records': 'View own records (Patient only)'
        },
        'test_credentials': {
            'admin': {'email': 'admin@hospital.com', 'password': 'admin123'},
            'doctor': {'email': 'doctor@hospital.com', 'password': 'doctor123'},
            'patient': {'email': 'patient@hospital.com', 'password': 'patient123'}
        }
    })

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Email and password required'}), 400
    
    email = data.get('email')
    password = data.get('password')
    
    user = users_db.get(email)
    if not user or not verify_password(password, user['password_hash']):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    # Create token
    token_data = {
        'sub': user['email'],
        'user_id': user['id'],
        'role': user['role'],
        'name': user['name']
    }
    access_token = create_access_token(token_data)
    
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'token_type': 'Bearer',
        'user': {
            'id': user['id'],
            'email': user['email'],
            'role': user['role'],
            'name': user['name']
        }
    }), 200

@app.route('/api/profile', methods=['GET'])
@token_required
def profile(current_user):
    return jsonify({
        'message': 'User Profile',
        'user': {
            'id': current_user['user_id'],
            'email': current_user['sub'],
            'role': current_user['role'],
            'name': current_user['name']
        }
    }), 200

@app.route('/api/admin/dashboard', methods=['GET'])
@token_required
@role_required(Role.ADMIN)
def admin_dashboard(current_user):
    return jsonify({
        'message': 'Welcome to Admin Dashboard',
        'user': current_user['name'],
        'role': current_user['role'],
        'data': {
            'total_users': len(users_db),
            'total_doctors': 1,
            'total_patients': 1,
            'system_status': 'operational'
        }
    }), 200

@app.route('/api/medical-records', methods=['GET'])
@token_required
@role_required(Role.ADMIN, Role.DOCTOR)
def medical_records(current_user):
    return jsonify({
        'message': 'Medical Records Access',
        'accessed_by': current_user['name'],
        'role': current_user['role'],
        'records': [
            {'patient_id': 3, 'name': 'John Doe', 'diagnosis': 'Flu', 'status': 'Recovering'},
            {'patient_id': 4, 'name': 'Jane Smith', 'diagnosis': 'Diabetes', 'status': 'Stable'}
        ]
    }), 200

@app.route('/api/prescribe', methods=['POST'])
@token_required
@role_required(Role.DOCTOR)
def prescribe_medication(current_user):
    data = request.get_json()
    
    if not data or not data.get('patient_id') or not data.get('medication'):
        return jsonify({'message': 'patient_id and medication required'}), 400
    
    return jsonify({
        'message': 'Prescription created successfully',
        'doctor': current_user['name'],
        'doctor_id': current_user['user_id'],
        'prescription': {
            'patient_id': data['patient_id'],
            'medication': data['medication'],
            'dosage': data.get('dosage', 'As prescribed'),
            'date': datetime.utcnow().isoformat()
        }
    }), 201

@app.route('/api/my-records', methods=['GET'])
@token_required
@role_required(Role.PATIENT)
def view_my_records(current_user):
    return jsonify({
        'message': 'Your Medical Records',
        'patient': current_user['name'],
        'patient_id': current_user['user_id'],
        'records': {
            'diagnoses': ['Flu - 2024-11-10'],
            'prescriptions': ['Paracetamol 500mg'],
            'appointments': ['Dr. Smith - 2024-11-20 10:00 AM'],
            'test_results': 'All normal'
        }
    }), 200

if __name__ == '__main__':
    print("=" * 60)
    print("Hospital Authentication API Server")
    print("=" * 60)
    print("\nServer running on: http://127.0.0.1:5000")
    print("\nTest Credentials:")
    print("  Admin:   admin@hospital.com / admin123")
    print("  Doctor:  doctor@hospital.com / doctor123")
    print("  Patient: patient@hospital.com / patient123")
    print("\nAPI Endpoints:")
    print("  POST   http://127.0.0.1:5000/api/login")
    print("  GET    http://127.0.0.1:5000/api/profile")
    print("  GET    http://127.0.0.1:5000/api/admin/dashboard")
    print("  GET    http://127.0.0.1:5000/api/medical-records")
    print("  POST   http://127.0.0.1:5000/api/prescribe")
    print("  GET    http://127.0.0.1:5000/api/my-records")
    print("\n" + "=" * 60)
    app.run(debug=True, port=5000)
