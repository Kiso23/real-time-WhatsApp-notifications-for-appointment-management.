# Twilio Configuration Example
# Copy this file to twilio_config.py and add your actual credentials

# Get these values from: https://console.twilio.com

# Step 1: Sign up at https://www.twilio.com/try-twilio
# Step 2: Get your credentials from the console
# Step 3: Replace the values below with your actual credentials

TWILIO_ACCOUNT_SID = 'ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'  # Your Account SID (starts with AC)
TWILIO_AUTH_TOKEN = 'your_auth_token_here'                 # Your Auth Token
TWILIO_PHONE_NUMBER = '+1234567890'                        # Your Twilio phone number

# Your verified phone number (where you want to receive messages)
YOUR_PHONE_NUMBER = '+919876543210'  # Replace with your mobile number (include country code)

# WhatsApp Setup:
# 1. Go to: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
# 2. Get your sandbox code (e.g., "join happy-dog")
# 3. On WhatsApp, message +1 415 523 8886
# 4. Send: "join your-code-here"
# 5. Wait for confirmation
# 6. Now you can receive WhatsApp notifications!
