"""
Database models for XYL-PHOS-CURE Authentication System
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import secrets
import string

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication system"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Basic user information
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Profile information
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    organization = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(50), nullable=True)
    
    # Account status
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False)  # user, admin
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Verification and reset tokens
    verification_token = db.Column(db.String(100), nullable=True)
    verification_token_expires = db.Column(db.DateTime, nullable=True)
    reset_token = db.Column(db.String(100), nullable=True)
    reset_token_expires = db.Column(db.DateTime, nullable=True)
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            self.role = 'user'
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password"""
        return check_password_hash(self.password_hash, password)
    
    def generate_verification_token(self):
        """Generate email verification token"""
        self.verification_token = self._generate_token()
        self.verification_token_expires = datetime.utcnow() + timedelta(hours=24)
        return self.verification_token
    
    def generate_reset_token(self):
        """Generate password reset token"""
        self.reset_token = self._generate_token()
        self.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
        return self.reset_token
    
    def verify_email(self, token):
        """Verify email with token"""
        if (self.verification_token == token and 
            self.verification_token_expires and 
            datetime.utcnow() < self.verification_token_expires):
            self.is_verified = True
            self.verification_token = None
            self.verification_token_expires = None
            return True
        return False
    
    def verify_reset_token(self, token):
        """Verify password reset token"""
        if (self.reset_token == token and 
            self.reset_token_expires and 
            datetime.utcnow() < self.reset_token_expires):
            return True
        return False
    
    def clear_reset_token(self):
        """Clear password reset token"""
        self.reset_token = None
        self.reset_token_expires = None
    
    @staticmethod
    def _generate_token():
        """Generate secure random token"""
        return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))
    
    @property
    def full_name(self):
        """Get full name"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        return self.username
    
    @property
    def is_admin(self):
        """Check if user is admin"""
        return self.role == 'admin'
    
    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login = datetime.utcnow()
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'organization': self.organization,
            'country': self.country,
            'role': self.role,
            'is_verified': self.is_verified,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
    
    def __repr__(self):
        return f'<User {self.username}>'


class LoginAttempt(db.Model):
    """Track login attempts for security"""
    __tablename__ = 'login_attempts'
    
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(45), nullable=False, index=True)  # IPv6 support
    email = db.Column(db.String(120), nullable=True, index=True)
    success = db.Column(db.Boolean, default=False, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_agent = db.Column(db.String(255), nullable=True)
    
    @staticmethod
    def record_attempt(ip_address, email=None, success=False, user_agent=None):
        """Record login attempt"""
        attempt = LoginAttempt(
            ip_address=ip_address,
            email=email,
            success=success,
            user_agent=user_agent
        )
        db.session.add(attempt)
        db.session.commit()
        return attempt
    
    @staticmethod
    def get_recent_failures(ip_address, minutes=15):
        """Get recent failed attempts from IP"""
        cutoff = datetime.utcnow() - timedelta(minutes=minutes)
        return LoginAttempt.query.filter(
            LoginAttempt.ip_address == ip_address,
            LoginAttempt.success == False,
            LoginAttempt.timestamp > cutoff
        ).count()
    
    @staticmethod
    def is_blocked(ip_address, max_attempts=5, minutes=15):
        """Check if IP is blocked due to failed attempts"""
        return LoginAttempt.get_recent_failures(ip_address, minutes) >= max_attempts
    
    def __repr__(self):
        return f'<LoginAttempt {self.ip_address} - {self.success}>'


def init_db(app):
    """Initialize database"""
    db.init_app(app)
    
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Create default admin user if it doesn't exist
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@xyl-phos-cure.eu',
                first_name='System',
                last_name='Administrator',
                role='admin',
                is_verified=True,
                organization='XYL-PHOS-CURE Project',
                country='European Union'
            )
            admin.set_password('admin123')  # Default password - should be changed
            db.session.add(admin)
            db.session.commit()
            print("✓ Created default admin user (admin/admin123)")
        
        print("✓ Database initialized successfully")


def create_sample_users():
    """Create sample users for testing"""
    sample_users = [
        {
            'username': 'researcher1',
            'email': 'researcher@university.es',
            'password': 'research123',
            'first_name': 'Maria',
            'last_name': 'González',
            'organization': 'University of Córdoba',
            'country': 'Spain',
            'role': 'user',
            'is_verified': True
        },
        {
            'username': 'partner1',
            'email': 'partner@research.it',
            'password': 'partner123',
            'first_name': 'Marco',
            'last_name': 'Rossi',
            'organization': 'CNR-IPSP',
            'country': 'Italy',
            'role': 'user',
            'is_verified': True
        }
    ]
    
    for user_data in sample_users:
        existing = User.query.filter_by(username=user_data['username']).first()
        if not existing:
            password = user_data.pop('password')
            user = User(**user_data)
            user.set_password(password)
            db.session.add(user)
    
    db.session.commit()
    print("✓ Sample users created")