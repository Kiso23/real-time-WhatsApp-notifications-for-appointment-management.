#!/usr/bin/env python3
"""
Hospital Management System - Main Runner
Run both Authentication and WhatsApp Notification APIs
"""

import subprocess
import sys
import time

def main():
    print("=" * 70)
    print("🏥 HOSPITAL MANAGEMENT SYSTEM")
    print("=" * 70)
    print("\nStarting servers...\n")
    
    try:
        # Start Authentication API
        print("Starting Authentication API on port 5000...")
        auth_process = subprocess.Popen(
            [sys.executable, "api/auth_api.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        time.sleep(2)
        
        # Start WhatsApp Notification API
        print("Starting WhatsApp Notification API on port 5005...")
        whatsapp_process = subprocess.Popen(
            [sys.executable, "api/notification_api.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        time.sleep(2)
        
        print("\n" + "=" * 70)
        print("✓ Both servers are running!")
        print("=" * 70)
        print("\n📡 API Endpoints:")
        print("   Authentication:  http://127.0.0.1:5000")
        print("   WhatsApp:        http://127.0.0.1:5005")
        print("\n📖 Documentation: docs/API_GUIDE.md")
        print("\nPress Ctrl+C to stop all servers")
        print("=" * 70 + "\n")
        
        # Keep running
        auth_process.wait()
        whatsapp_process.wait()
        
    except KeyboardInterrupt:
        print("\n\nStopping servers...")
        auth_process.terminate()
        whatsapp_process.terminate()
        print("✓ All servers stopped")
        sys.exit(0)

if __name__ == "__main__":
    main()
