# 🏥 Hospital Management System

A comprehensive hospital management system with secure JWT authentication, role-based access control, and real-time WhatsApp notifications for appointment management.

## ✨ Features

- **🔐 Secure Authentication**: JWT/OAuth2 implementation with token-based authentication
- **👥 Role-Based Access Control (RBAC)**: Three user roles with different permissions
  - **Admin**: Full system access, user management, dashboard
  - **Doctor**: Medical records access, prescription management
  - **Patient**: Personal records access only
- **📱 WhatsApp Notifications**: Real-time appointment confirmations and reminders via Twilio
- **🚀 RESTful API**: Clean and well-documented API endpoints
- **💊 Prescription Management**: Doctors can prescribe medications
- **📊 Medical Records**: Secure access to patient medical history
- **📅 Appointment Booking**: Easy appointment scheduling with instant WhatsApp confirmation

## Project Structure

```
hospital_management/
├── api/                    # API endpoints
│   ├── auth_api.py        # Authentication API
│   └── notification_api.py # WhatsApp notification API
├── config/                 # Configuration files
│   └── twilio_config.py   # Twilio credentials
├── demo/                   # Demo and test files
│   ├── auth_demo.py       # Authentication demo
│   └── sms_demo.py        # SMS simulation demo
├── docs/                   # Documentation
│   └── API_GUIDE.md       # API usage guide
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure Twilio credentials in `config/twilio_config.py`

3. Run the authentication API:
```bash
python api/auth_api.py
```

4. Run the WhatsApp notification API:
```bash
python api/notification_api.py
```

## API Endpoints

### Authentication API (Port 5000)
- `POST /api/login` - User login
- `GET /api/profile` - Get user profile
- `GET /api/admin/dashboard` - Admin dashboard (Admin only)
- `GET /api/medical-records` - Medical records (Admin, Doctor)
- `POST /api/prescribe` - Prescribe medication (Doctor only)
- `GET /api/my-records` - Patient records (Patient only)

### WhatsApp Notification API (Port 5005)
- `POST /api/book-appointment` - Book appointment with WhatsApp notification
- `POST /api/send-reminder` - Send appointment reminder
- `POST /api/send-test` - Send test message
- `GET /api/appointments` - Get all appointments
- `GET /api/whatsapp-log` - View message log

## Test Credentials

- **Admin**: admin@hospital.com / admin123
- **Doctor**: doctor@hospital.com / doctor123
- **Patient**: patient@hospital.com / patient123

## 🛠️ Technologies Used

- **Backend**: Python 3.x, Flask
- **Authentication**: PyJWT (JSON Web Tokens)
- **Notifications**: Twilio API (WhatsApp)
- **API**: RESTful architecture with Flask-CORS

## 🚀 Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/hospital-management-system.git
cd hospital-management-system
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure Twilio** (for WhatsApp notifications)
   - Sign up at [Twilio](https://www.twilio.com/)
   - Get your Account SID and Auth Token
   - Update `config/twilio_config.py` with your credentials

4. **Run the servers**
```bash
# Run authentication API
python api/auth_api.py

# Run WhatsApp notification API (in another terminal)
python api/notification_api.py
```

5. **Test with Postman**
   - Import the API endpoints from `docs/API_GUIDE.md`
   - Start testing!

## 📸 Screenshots

### Authentication Flow
- Login with role-based access
- JWT token generation
- Protected routes

### WhatsApp Notifications
- Appointment confirmation messages
- Formatted messages with emojis
- Real-time delivery

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

Created with ❤️ for modern healthcare management

## 🙏 Acknowledgments

- Twilio for WhatsApp API
- Flask community
- All contributors
