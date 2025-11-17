# Hospital SMS Notification System - DEMO VERSION
# Shows SMS in response (simulated for demonstration)
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# In-memory storage
appointments = []
sms_log = []

def send_sms_demo(phone_number, message):
    """Simulate SMS and log it"""
    sms_record = {
        'id': len(sms_log) + 1,
        'to': phone_number,
        'message': message,
        'status': 'sent',
        'timestamp': datetime.now().isoformat()
    }
    sms_log.append(sms_record)
    
    # Print to console
    print(f"\n{'='*60}")
    print("📱 SMS SENT")
    print(f"{'='*60}")
    print(f"To: {phone_number}")
    print(f"Message: {message}")
    print(f"Time: {sms_record['timestamp']}")
    print(f"{'='*60}\n")
    
    return sms_record

@app.route('/')
def home():
    return jsonify({
        'message': 'Hospital SMS Notification System - DEMO',
        'status': 'running',
        'total_sms_sent': len(sms_log),
        'endpoints': {
            'POST /api/book-appointment': 'Book appointment and send SMS',
            'POST /api/send-reminder': 'Send appointment reminder',
            'POST /api/send-prescription': 'Send prescription notification',
            'POST /api/cancel-appointment': 'Cancel appointment',
            'GET /api/appointments': 'Get all appointments',
            'GET /api/sms-log': 'View all SMS sent'
        }
    })

@app.route('/api/book-appointment', methods=['POST'])
def book_appointment():
    """Book appointment and send confirmation SMS"""
    data = request.get_json()
    
    required = ['patient_name', 'phone_number', 'doctor_name', 'appointment_date', 'appointment_time']
    for field in required:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    # Create appointment
    appointment = {
        'id': len(appointments) + 1,
        'patient_name': data['patient_name'],
        'phone_number': data['phone_number'],
        'doctor_name': data['doctor_name'],
        'appointment_date': data['appointment_date'],
        'appointment_time': data['appointment_time'],
        'status': 'confirmed',
        'created_at': datetime.now().isoformat()
    }
    
    appointments.append(appointment)
    
    # Send SMS
    message = f"""Hello {appointment['patient_name']}!

Your appointment has been CONFIRMED:
Doctor: Dr. {appointment['doctor_name']}
Date: {appointment['appointment_date']}
Time: {appointment['appointment_time']}

Please arrive 15 minutes early.
Bring your ID and insurance card.

For changes, call: +91-1800-HOSPITAL

Thank you,
Hospital Management"""
    
    sms_result = send_sms_demo(appointment['phone_number'], message)
    
    return jsonify({
        'success': True,
        'message': 'Appointment booked successfully!',
        'appointment': appointment,
        'sms_sent': {
            'to': sms_result['to'],
            'message': sms_result['message'],
            'status': sms_result['status'],
            'sent_at': sms_result['timestamp']
        }
    }), 201

@app.route('/api/send-reminder', methods=['POST'])
def send_reminder():
    """Send appointment reminder SMS"""
    data = request.get_json()
    
    if not data.get('phone_number') or not data.get('patient_name'):
        return jsonify({'error': 'phone_number and patient_name required'}), 400
    
    message = f"""REMINDER: {data['patient_name']}

Your appointment is tomorrow:
Time: {data.get('time', '10:00 AM')}
Doctor: Dr. {data.get('doctor_name', 'Smith')}

Reply YES to confirm or call to reschedule.

- Hospital Management"""
    
    sms_result = send_sms_demo(data['phone_number'], message)
    
    return jsonify({
        'success': True,
        'message': 'Reminder sent successfully',
        'sms_sent': sms_result
    }), 200

@app.route('/api/send-prescription', methods=['POST'])
def send_prescription():
    """Send prescription ready notification"""
    data = request.get_json()
    
    if not data.get('phone_number') or not data.get('patient_name'):
        return jsonify({'error': 'phone_number and patient_name required'}), 400
    
    message = f"""Hello {data['patient_name']}!

Your PRESCRIPTION is ready for pickup:

Medication: {data.get('medication', 'As prescribed')}
Location: Hospital Pharmacy, Ground Floor
Hours: 9:00 AM - 6:00 PM

Please bring your ID.

- Hospital Pharmacy"""
    
    sms_result = send_sms_demo(data['phone_number'], message)
    
    return jsonify({
        'success': True,
        'message': 'Prescription notification sent',
        'sms_sent': sms_result
    }), 200

@app.route('/api/cancel-appointment', methods=['POST'])
def cancel_appointment():
    """Cancel appointment and send notification"""
    data = request.get_json()
    
    if not data.get('phone_number') or not data.get('patient_name'):
        return jsonify({'error': 'phone_number and patient_name required'}), 400
    
    message = f"""Hello {data['patient_name']},

Your appointment on {data.get('date', 'the scheduled date')} has been CANCELLED.

To reschedule, please call:
+91-1800-HOSPITAL

Or visit our website.

- Hospital Management"""
    
    sms_result = send_sms_demo(data['phone_number'], message)
    
    return jsonify({
        'success': True,
        'message': 'Cancellation notification sent',
        'sms_sent': sms_result
    }), 200

@app.route('/api/appointments', methods=['GET'])
def get_appointments():
    """Get all appointments"""
    return jsonify({
        'success': True,
        'total': len(appointments),
        'appointments': appointments
    }), 200

@app.route('/api/sms-log', methods=['GET'])
def get_sms_log():
    """Get all SMS sent"""
    return jsonify({
        'success': True,
        'total_sms': len(sms_log),
        'sms_log': sms_log
    }), 200

if __name__ == '__main__':
    print("=" * 70)
    print("🏥 HOSPITAL SMS NOTIFICATION SYSTEM - DEMO VERSION")
    print("=" * 70)
    print("\n✓ Server running on: http://127.0.0.1:5003")
    print("\n📱 SMS Feature: ACTIVE (Demo Mode)")
    print("   All SMS will be logged and displayed in responses")
    print("\n🔗 API Endpoints:")
    print("   POST   http://127.0.0.1:5003/api/book-appointment")
    print("   POST   http://127.0.0.1:5003/api/send-reminder")
    print("   POST   http://127.0.0.1:5003/api/send-prescription")
    print("   POST   http://127.0.0.1:5003/api/cancel-appointment")
    print("   GET    http://127.0.0.1:5003/api/appointments")
    print("   GET    http://127.0.0.1:5003/api/sms-log")
    print("\n" + "=" * 70)
    print("Ready to accept requests! Test in Postman now.")
    print("=" * 70 + "\n")
    app.run(debug=True, port=5003)
