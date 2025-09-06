"""
Authentication utilities and decorators
"""

from functools import wraps
from flask import current_app, request, jsonify, redirect, url_for, flash
from flask_login import current_user
from models import LoginAttempt
import requests
import os

def login_required_role(role):
    """Decorator to require specific role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('auth.login'))
            
            if current_user.role != role and role != 'user':
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('dashboard'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        
        if not current_user.is_admin:
            flash('Admin access required.', 'danger')
            return redirect(url_for('dashboard'))
        
        return f(*args, **kwargs)
    return decorated_function

def verified_required(f):
    """Decorator to require verified email"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        
        if not current_user.is_verified:
            flash('Please verify your email address to access this feature.', 'warning')
            return redirect(url_for('auth.resend_verification'))
        
        return f(*args, **kwargs)
    return decorated_function

def check_rate_limit(ip_address):
    """Check if IP is rate limited"""
    return LoginAttempt.is_blocked(ip_address)

def record_login_attempt(ip_address, email=None, success=False):
    """Record login attempt"""
    user_agent = request.headers.get('User-Agent', '')
    return LoginAttempt.record_attempt(
        ip_address=ip_address,
        email=email,
        success=success,
        user_agent=user_agent
    )

def get_client_ip():
    """Get client IP address"""
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.environ['REMOTE_ADDR']
    else:
        return request.environ['HTTP_X_FORWARDED_FOR']

class EmailService:
    """Email service using Gemini API for sending emails"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get('GEMINI_API_KEY')
        if not self.api_key:
            print("Warning: GEMINI_API_KEY not found. Email functionality will be limited.")
    
    def send_verification_email(self, user, token):
        """Send email verification email"""
        if not self.api_key:
            print(f"Email verification would be sent to {user.email}")
            print(f"Verification link: /auth/verify-email/{token}")
            return True
        
        subject = "Verify your XYL-PHOS-CURE account"
        verification_url = f"{request.host_url}auth/verify-email/{token}"
        
        body = f"""
        Dear {user.full_name},

        Welcome to the XYL-PHOS-CURE project management dashboard!

        Please verify your email address by clicking the link below:
        {verification_url}

        This link will expire in 24 hours.

        If you didn't create this account, please ignore this email.

        Best regards,
        XYL-PHOS-CURE Team
        """
        
        return self._send_email(user.email, subject, body)
    
    def send_password_reset_email(self, user, token):
        """Send password reset email"""
        if not self.api_key:
            print(f"Password reset would be sent to {user.email}")
            print(f"Reset link: /auth/reset-password/{token}")
            return True
        
        subject = "Reset your XYL-PHOS-CURE password"
        reset_url = f"{request.host_url}auth/reset-password/{token}"
        
        body = f"""
        Dear {user.full_name},

        You have requested to reset your password for your XYL-PHOS-CURE account.

        Please click the link below to reset your password:
        {reset_url}

        This link will expire in 1 hour.

        If you didn't request this password reset, please ignore this email.

        Best regards,
        XYL-PHOS-CURE Team
        """
        
        return self._send_email(user.email, subject, body)
    
    def send_welcome_email(self, user):
        """Send welcome email after registration"""
        if not self.api_key:
            print(f"Welcome email would be sent to {user.email}")
            return True
        
        subject = "Welcome to XYL-PHOS-CURE!"
        
        body = f"""
        Dear {user.full_name},

        Welcome to the XYL-PHOS-CURE project management dashboard!

        Your account has been successfully created. You can now access:
        - Project timeline and milestones
        - Consortium building tools
        - Document management
        - Real-time project updates

        Visit the dashboard: {request.host_url}

        If you have any questions, please don't hesitate to contact our team.

        Best regards,
        XYL-PHOS-CURE Project Team
        """
        
        return self._send_email(user.email, subject, body)
    
    def _send_email(self, to_email, subject, body):
        """Send email using Gemini API (simulated)"""
        try:
            # In a real implementation, you would integrate with an email service
            # For now, we'll simulate email sending
            print(f"Sending email to: {to_email}")
            print(f"Subject: {subject}")
            print(f"Body: {body[:100]}...")
            
            # Simulate API call delay
            import time
            time.sleep(0.1)
            
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False

# Country code to name mapping for display
COUNTRY_NAMES = {
    'AT': 'Austria', 'BE': 'Belgium', 'BG': 'Bulgaria', 'HR': 'Croatia',
    'CY': 'Cyprus', 'CZ': 'Czech Republic', 'DK': 'Denmark', 'EE': 'Estonia',
    'FI': 'Finland', 'FR': 'France', 'DE': 'Germany', 'GR': 'Greece',
    'HU': 'Hungary', 'IE': 'Ireland', 'IT': 'Italy', 'LV': 'Latvia',
    'LT': 'Lithuania', 'LU': 'Luxembourg', 'MT': 'Malta', 'NL': 'Netherlands',
    'PL': 'Poland', 'PT': 'Portugal', 'RO': 'Romania', 'SK': 'Slovakia',
    'SI': 'Slovenia', 'ES': 'Spain', 'SE': 'Sweden', 'NO': 'Norway',
    'CH': 'Switzerland', 'UK': 'United Kingdom', 'US': 'United States',
    'CA': 'Canada', 'AU': 'Australia', 'NZ': 'New Zealand', 'JP': 'Japan',
    'KR': 'South Korea', 'SG': 'Singapore', 'OTHER': 'Other'
}

def get_country_name(code):
    """Get country name from code"""
    return COUNTRY_NAMES.get(code, code)