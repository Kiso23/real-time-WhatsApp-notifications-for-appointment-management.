# Secure Authentication System with JWT and Role-Based Access Control
import jwt
import hashlib
import secrets
from datetime import datetime, timedelta
from functools import wraps
from enum import Enum

# Configuration
SECRET_KEY = secrets.token_hex(32)  # Generate secure secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Role definitions
class Role(Enum):
    ADMIN = "admin"
    DOCTOR = "doctor"
    PATIENT = "patient"

# In-memory user database (replace with actual database in production)
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

# Password hashing
def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return hash_password(plain_password) == hashed_password

# JWT Token functions
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    """Decode and verify JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")

# Authentication
def authenticate_user(email: str, password: str) -> dict:
    """Authenticate user and return user data"""
    user = users_db.get(email)
    if not user:
        return None
    if not verify_password(password, user["password_hash"]):
        return None
    return user

def login(email: str, password: str) -> dict:
    """Login user and generate JWT token"""
    user = authenticate_user(email, password)
    if not user:
        raise Exception("Invalid credentials")
    
    # Create token with user info
    token_data = {
        "sub": user["email"],
        "user_id": user["id"],
        "role": user["role"],
        "name": user["name"]
    }
    access_token = create_access_token(token_data)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "email": user["email"],
            "role": user["role"],
            "name": user["name"]
        }
    }

# Role-based access control decorators
def require_role(*allowed_roles):
    """Decorator to check if user has required role"""
    def decorator(func):
        @wraps(func)
        def wrapper(token: str, *args, **kwargs):
            try:
                payload = decode_access_token(token)
                user_role = payload.get("role")
                
                if user_role not in [role.value for role in allowed_roles]:
                    raise Exception(f"Access denied. Required roles: {[r.value for r in allowed_roles]}")
                
                # Pass user info to the function
                return func(payload, *args, **kwargs)
            except Exception as e:
                raise Exception(f"Authorization failed: {str(e)}")
        return wrapper
    return decorator

# Protected resource examples
@require_role(Role.ADMIN)
def admin_dashboard(user_info: dict):
    """Admin-only resource"""
    return {
        "message": "Welcome to Admin Dashboard",
        "user": user_info["name"],
        "role": user_info["role"],
        "data": "All system data and user management"
    }

@require_role(Role.ADMIN, Role.DOCTOR)
def medical_records(user_info: dict):
    """Admin and Doctor accessible resource"""
    return {
        "message": "Medical Records Access",
        "user": user_info["name"],
        "role": user_info["role"],
        "data": "Patient medical records and history"
    }

@require_role(Role.DOCTOR)
def prescribe_medication(user_info: dict, patient_id: int, medication: str):
    """Doctor-only resource"""
    return {
        "message": "Prescription created",
        "doctor": user_info["name"],
        "patient_id": patient_id,
        "medication": medication
    }

@require_role(Role.PATIENT)
def view_my_records(user_info: dict):
    """Patient-only resource"""
    return {
        "message": "Your Medical Records",
        "patient": user_info["name"],
        "patient_id": user_info["user_id"],
        "data": "Your personal medical history"
    }

@require_role(Role.ADMIN, Role.DOCTOR, Role.PATIENT)
def profile(user_info: dict):
    """All authenticated users can access"""
    return {
        "message": "User Profile",
        "user": user_info["name"],
        "email": user_info["sub"],
        "role": user_info["role"]
    }

# Demo usage
if __name__ == "__main__":
    print("=" * 60)
    print("SECURE AUTHENTICATION SYSTEM - JWT & ROLE-BASED ACCESS")
    print("=" * 60)
    print()
    
    # Test credentials
    test_users = [
        ("admin@hospital.com", "admin123", "Admin"),
        ("doctor@hospital.com", "doctor123", "Doctor"),
        ("patient@hospital.com", "patient123", "Patient")
    ]
    
    for email, password, role_name in test_users:
        print(f"\n{'='*60}")
        print(f"Testing {role_name} Login")
        print(f"{'='*60}")
        
        try:
            # Login
            result = login(email, password)
            print(f"✓ Login successful!")
            print(f"  User: {result['user']['name']}")
            print(f"  Role: {result['user']['role']}")
            print(f"  Token: {result['access_token'][:50]}...")
            
            token = result['access_token']
            
            # Test access to different resources
            print(f"\nTesting Resource Access:")
            
            # Profile (all can access)
            try:
                response = profile(token)
                print(f"  ✓ Profile: {response['message']}")
            except Exception as e:
                print(f"  ✗ Profile: {str(e)}")
            
            # Admin dashboard
            try:
                response = admin_dashboard(token)
                print(f"  ✓ Admin Dashboard: {response['message']}")
            except Exception as e:
                print(f"  ✗ Admin Dashboard: Access denied")
            
            # Medical records
            try:
                response = medical_records(token)
                print(f"  ✓ Medical Records: {response['message']}")
            except Exception as e:
                print(f"  ✗ Medical Records: Access denied")
            
            # Prescribe medication
            try:
                response = prescribe_medication(token, 123, "Aspirin")
                print(f"  ✓ Prescribe Medication: {response['message']}")
            except Exception as e:
                print(f"  ✗ Prescribe Medication: Access denied")
            
            # View patient records
            try:
                response = view_my_records(token)
                print(f"  ✓ My Records: {response['message']}")
            except Exception as e:
                print(f"  ✗ My Records: Access denied")
                
        except Exception as e:
            print(f"✗ Login failed: {str(e)}")
    
    print(f"\n{'='*60}")
    print("Testing Invalid Credentials")
    print(f"{'='*60}")
    try:
        login("invalid@hospital.com", "wrongpass")
    except Exception as e:
        print(f"✓ Correctly rejected: {str(e)}")
    
    print(f"\n{'='*60}")
    print("Testing Expired/Invalid Token")
    print(f"{'='*60}")
    try:
        admin_dashboard("invalid_token_here")
    except Exception as e:
        print(f"✓ Correctly rejected: Authorization failed")
    
    print(f"\n{'='*60}")
    print("Demo Complete!")
    print(f"{'='*60}")
