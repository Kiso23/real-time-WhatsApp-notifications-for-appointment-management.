# WhatsApp Notification System using Twilio Template
from flask import Flask, request, jsonify
from flask_cors import CORS
from twilio.rest import Client
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Import Twilio configuration
try:
    from twilio_config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
    twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    print("✓ Twilio configured for WhatsApp!")
except Exception as e:
    twilio_client = None
    print(f"⚠ Twilio not configured: {e}")

# Twilio WhatsApp Sandbox number
TWILIO_WHATSAPP_NUMBER = 'whatsapp:+14155238886'
TEMPLATE_SID = 'HXb5b62575e6e4ff6129ad7c8efe1f983e'

# In-memory storage
appointments = []
whatsapp_log = []

def send_whatsapp_formatted(to_number, patient_name, doctor_name, date, time):
    """Send formatted WhatsApp message"""
    
    # Format phone number for WhatsApp
    if not to_number.startswith('whatsapp:'):
        to_number = f'whatsapp:{to_number}'
    
    # Create formatted message
    message = f"""🏥 *Appointment Confirmed*

Hello *{patient_name}*! 👋

Your appointment has been successfully booked:

👨‍⚕️ *Doctor:* {doctor_name}
📅 *Date:* {date}
🕐 *Time:* {time}

📌 *Important:*
• Please arrive 15 minutes early
• Bring your ID and insurance card
• Wear a mask

For any changes, call: +91-1800-HOSPITAL

_Thank you for choosing our hospital!_"""
    
    if twilio_client is None:
        print(f"\n{'='*60}")
        print("📱 WHATSAPP SIMULATION")
        print(f"{'='*60}")
        print(f"To: {to_number}")
        print(message)
        print(f"{'='*60}\n")
        return {
            'status': 'simulated',
            'to': to_number,
            'message': message
        }
    
    try:
        msg = twilio_client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=message,
            to=to_number
        )
        
        result = {
            'status': 'sent',
            'sid': msg.sid,
            'to': to_number,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
        
        whatsapp_log.append(result)
        
        print(f"\n{'='*60}")
        print("✓ WHATSAPP MESSAGE SENT")
        print(f"{'='*60}")
        print(f"To: {to_number}")
        print(f"SID: {msg.sid}")
        print(f"{'='*60}\n")
        
        return result
        
    except Exception as e:
        return {
            'status': 'failed',
            'error': str(e),
            'to': to_number
        }

@app.route('/')
def home():
    return jsonify({
        'message': 'Hospital WhatsApp Notification System',
        'status': 'running',
        'total_messages': len(whatsapp_log),
        'endpoints': {
            'POST /api/book-appointment': 'Book appointment and send WhatsApp',
            'POST /api/send-reminder': 'Send appointment reminder',
            'POST /api/send-test': 'Send test message',
            'GET /api/appointments': 'Get all appointments',
            'GET /api/whatsapp-log': 'View all messages sent'
        }
    })

@app.route('/api/send-test', methods=['POST'])
def send_test():
    """Send test WhatsApp message"""
    data = request.get_json()
    
    if not data.get('phone_number'):
        return jsonify({'error': 'phone_number required'}), 400
    
    date = data.get('date', 'December 1')
    time = data.get('time', '3:00 PM')
    
    result = send_whatsapp_template(data['phone_number'], date, time)
    
    return jsonify({
        'success': True,
        'message': 'Test WhatsApp sent',
        'whatsapp_result': result
    }), 200

@app.route('/api/book-appointment', methods=['POST'])
def book_appointment():
    """Book appointment and send WhatsApp confirmation"""
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
    
    # Send formatted WhatsApp message
    result = send_whatsapp_formatted(
        appointment['phone_number'],
        appointment['patient_name'],
        appointment['doctor_name'],
        appointment['appointment_date'],
        appointment['appointment_time']
    )
    
    return jsonify({
        'success': True,
        'message': 'Appointment booked successfully!',
        'appointment': appointment,
        'whatsapp_sent': result
    }), 201

@app.route('/api/send-reminder', methods=['POST'])
def send_reminder():
    """Send appointment reminder via WhatsApp"""
    data = request.get_json()
    
    if not data.get('phone_number'):
        return jsonify({'error': 'phone_number required'}), 400
    
    date = data.get('date', 'tomorrow')
    time = data.get('time', '10:00 AM')
    
    result = send_whatsapp_template(data['phone_number'], date, time)
    
    return jsonify({
        'success': True,
        'message': 'Reminder sent',
        'whatsapp_sent': result
    }), 200

@app.route('/api/appointments', methods=['GET'])
def get_appointments():
    """Get all appointments"""
    return jsonify({
        'success': True,
        'total': len(appointments),
        'appointments': appointments
    }), 200

@app.route('/api/whatsapp-log', methods=['GET'])
def get_whatsapp_log():
    """Get all WhatsApp messages sent"""
    return jsonify({
        'success': True,
        'total': len(whatsapp_log),
        'messages': whatsapp_log
    }), 200

if __name__ == '__main__':
    print("=" * 70)
    print("📱 HOSPITAL WHATSAPP NOTIFICATION SYSTEM")
    print("=" * 70)
    print("\n✓ Server running on: http://127.0.0.1:5005")
    print("\n📋 Using Twilio Template:")
    print("   Message: 'Your appointment is coming up on {date} at {time}'")
    print("\n🔗 API Endpoints:")
    print("   POST   http://127.0.0.1:5005/api/send-test")
    print("   POST   http://127.0.0.1:5005/api/book-appointment")
    print("   POST   http://127.0.0.1:5005/api/send-reminder")
    print("   GET    http://127.0.0.1:5005/api/appointments")
    print("   GET    http://127.0.0.1:5005/api/whatsapp-log")
    print("\n" + "=" * 70)
    app.run(debug=True, port=5005)
