import random
import string
from typing import Optional
from app.core.config import settings

def generate_otp() -> str:
    """Generate a 6-digit OTP code."""
    return ''.join(random.choices(string.digits, k=6))

def send_otp_email(email: str, otp_code: str) -> bool:
    """
    Mock email sending for OTP verification.
    In production, replace with actual email service (SendGrid, Mailgun, etc.)
    """
    print(f"📧 MOCK EMAIL SENT TO: {email}")
    print(f"🔐 OTP CODE: {otp_code}")
    print(f"📝 Subject: Your Influbazzar Verification Code")
    print(f"📄 Body: Your verification code is: {otp_code}. This code expires in 5 minutes.")
    print("-" * 50)
    
    # In production, implement actual email sending here
    # Example with SendGrid, Mailgun, or SMTP
    return True

def send_welcome_email(email: str, role: str) -> bool:
    """Send welcome email after successful verification."""
    print(f"🎉 WELCOME EMAIL SENT TO: {email}")
    print(f"👤 Role: {role.title()}")
    print(f"📝 Subject: Welcome to Influbazzar!")
    print("-" * 50)
    return True