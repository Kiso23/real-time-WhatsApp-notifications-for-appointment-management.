# API Usage Guide

## Authentication API

### Base URL
```
http://127.0.0.1:5000
```

### 1. Login
**Endpoint:** `POST /api/login`

**Request Body:**
```json
{
  "email": "admin@hospital.com",
  "password": "admin123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "admin@hospital.com",
    "role": "admin",
    "name": "Admin User"
  }
}
```

### 2. Get Profile
**Endpoint:** `GET /api/profile`

**Headers:**
```
Authorization: Bearer YOUR_TOKEN_HERE
```

**Response:**
```json
{
  "message": "User Profile",
  "user": {
    "id": 1,
    "email": "admin@hospital.com",
    "role": "admin",
    "name": "Admin User"
  }
}
```

### 3. Admin Dashboard (Admin Only)
**Endpoint:** `GET /api/admin/dashboard`

**Headers:**
```
Authorization: Bearer ADMIN_TOKEN
```

### 4. Medical Records (Admin, Doctor)
**Endpoint:** `GET /api/medical-records`

**Headers:**
```
Authorization: Bearer ADMIN_OR_DOCTOR_TOKEN
```

### 5. Prescribe Medication (Doctor Only)
**Endpoint:** `POST /api/prescribe`

**Headers:**
```
Authorization: Bearer DOCTOR_TOKEN
```

**Request Body:**
```json
{
  "patient_id": 3,
  "medication": "Aspirin",
  "dosage": "500mg twice daily"
}
```

---

## WhatsApp Notification API

### Base URL
```
http://127.0.0.1:5005
```

### 1. Book Appointment
**Endpoint:** `POST /api/book-appointment`

**Request Body:**
```json
{
  "patient_name": "John Doe",
  "phone_number": "+918473010850",
  "doctor_name": "Dr. Smith",
  "appointment_date": "2024-11-20",
  "appointment_time": "10:00 AM"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Appointment booked successfully!",
  "appointment": {
    "id": 1,
    "patient_name": "John Doe",
    "phone_number": "+918473010850",
    "doctor_name": "Dr. Smith",
    "appointment_date": "2024-11-20",
    "appointment_time": "10:00 AM",
    "status": "confirmed"
  },
  "whatsapp_sent": {
    "status": "sent",
    "sid": "MM3bc0b799d14feed449c9f9c1295457f8"
  }
}
```

### 2. Send Reminder
**Endpoint:** `POST /api/send-reminder`

**Request Body:**
```json
{
  "phone_number": "+918473010850",
  "date": "tomorrow",
  "time": "10:00 AM"
}
```

### 3. Send Test Message
**Endpoint:** `POST /api/send-test`

**Request Body:**
```json
{
  "phone_number": "+918473010850",
  "date": "December 1",
  "time": "3:00 PM"
}
```

### 4. Get All Appointments
**Endpoint:** `GET /api/appointments`

**Response:**
```json
{
  "success": true,
  "total": 5,
  "appointments": [...]
}
```

### 5. Get WhatsApp Log
**Endpoint:** `GET /api/whatsapp-log`

**Response:**
```json
{
  "success": true,
  "total": 10,
  "messages": [...]
}
```

---

## Test Credentials

### Admin
- Email: `admin@hospital.com`
- Password: `admin123`
- Access: Full system access

### Doctor
- Email: `doctor@hospital.com`
- Password: `doctor123`
- Access: Medical records, prescriptions

### Patient
- Email: `patient@hospital.com`
- Password: `patient123`
- Access: Own records only

---

## WhatsApp Setup

1. Go to: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
2. Get your sandbox code (e.g., "join happy-dog")
3. On WhatsApp, message +1 415 523 8886
4. Send: "join your-code-here"
5. Wait for confirmation
6. Now you can receive WhatsApp notifications!

---

## Error Codes

- `400` - Bad Request (missing required fields)
- `401` - Unauthorized (invalid or missing token)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found (endpoint doesn't exist)
- `500` - Internal Server Error
