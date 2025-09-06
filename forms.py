"""
Authentication forms for XYL-PHOS-CURE project
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, TextAreaField
from wtforms.validators import (
    DataRequired, Email, Length, EqualTo, ValidationError, Optional, Regexp
)
from models import User

class LoginForm(FlaskForm):
    """User login form"""
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address')
    ], render_kw={
        'class': 'form-control',
        'placeholder': 'Enter your email',
        'autocomplete': 'email'
    })
    
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=6, message='Password must be at least 6 characters long')
    ], render_kw={
        'class': 'form-control',
        'placeholder': 'Enter your password',
        'autocomplete': 'current-password'
    })
    
    remember_me = BooleanField('Keep me signed in', render_kw={
        'class': 'form-check-input'
    })

class RegistrationForm(FlaskForm):
    """User registration form"""
    username = StringField('Username', validators=[
        DataRequired(message='Username is required'),
        Length(min=3, max=20, message='Username must be between 3 and 20 characters'),
        Regexp(r'^[a-zA-Z0-9_]+$', message='Username can only contain letters, numbers, and underscores')
    ], render_kw={
        'class': 'form-control',
        'placeholder': 'Choose a username',
        'autocomplete': 'username'
    })
    
    email = StringField('Email Address', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address')
    ], render_kw={
        'class': 'form-control',
        'placeholder': 'Enter your email address',
        'autocomplete': 'email'
    })
    
    first_name = StringField('First Name', validators=[
        DataRequired(message='First name is required'),
        Length(min=2, max=50, message='First name must be between 2 and 50 characters')
    ], render_kw={
        'class': 'form-control',
        'placeholder': 'Enter your first name',
        'autocomplete': 'given-name'
    })
    
    last_name = StringField('Last Name', validators=[
        DataRequired(message='Last name is required'),
        Length(min=2, max=50, message='Last name must be between 2 and 50 characters')
    ], render_kw={
        'class': 'form-control',
        'placeholder': 'Enter your last name',
        'autocomplete': 'family-name'
    })
    
    organization = StringField('Organization', validators=[
        DataRequired(message='Organization is required'),
        Length(max=100, message='Organization name cannot exceed 100 characters')
    ], render_kw={
        'class': 'form-control',
        'placeholder': 'University, Company, or Institution',
        'autocomplete': 'organization'
    })
    
    country = SelectField('Country', validators=[
        DataRequired(message='Please select your country')
    ], choices=[
        ('', 'Select your country'),
        ('AT', 'Austria'),
        ('BE', 'Belgium'),
        ('BG', 'Bulgaria'),
        ('HR', 'Croatia'),
        ('CY', 'Cyprus'),
        ('CZ', 'Czech Republic'),
        ('DK', 'Denmark'),
        ('EE', 'Estonia'),
        ('FI', 'Finland'),
        ('FR', 'France'),
        ('DE', 'Germany'),
        ('GR', 'Greece'),
        ('HU', 'Hungary'),
        ('IE', 'Ireland'),
        ('IT', 'Italy'),
        ('LV', 'Latvia'),
        ('LT', 'Lithuania'),
        ('LU', 'Luxembourg'),
        ('MT', 'Malta'),
        ('NL', 'Netherlands'),
        ('PL', 'Poland'),
        ('PT', 'Portugal'),
        ('RO', 'Romania'),
        ('SK', 'Slovakia'),
        ('SI', 'Slovenia'),
        ('ES', 'Spain'),
        ('SE', 'Sweden'),
        ('NO', 'Norway'),
        ('CH', 'Switzerland'),
        ('UK', 'United Kingdom'),
        ('US', 'United States'),
        ('CA', 'Canada'),
        ('AU', 'Australia'),
        ('NZ', 'New Zealand'),
        ('JP', 'Japan'),
        ('KR', 'South Korea'),
        ('SG', 'Singapore'),
        ('OTHER', 'Other')
    ], render_kw={
        'class': 'form-select'
    })
    
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=8, message='Password must be at least 8 characters long'),
        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)', 
               message='Password must contain at least one lowercase letter, one uppercase letter, and one number')
    ], render_kw={
        'class': 'form-control',
        'placeholder': 'Create a strong password',
        'autocomplete': 'new-password'
    })
    
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message='Please confirm your password'),
        EqualTo('password', message='Passwords do not match')
    ], render_kw={
        'class': 'form-control',
        'placeholder': 'Confirm your password',
        'autocomplete': 'new-password'
    })
    
    agree_terms = BooleanField('I agree to the Terms of Service and Privacy Policy', validators=[
        DataRequired(message='You must agree to the terms of service')
    ], render_kw={
        'class': 'form-check-input'
    })
    
    def validate_username(self, username):
        """Check if username is already taken"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already taken. Please choose a different one.')
    
    def validate_email(self, email):
        """Check if email is already registered"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already registered. Please use a different email or try logging in.')

class ForgotPasswordForm(FlaskForm):
    """Password reset request form"""
    email = StringField('Email Address', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address')
    ], render_kw={
        'class': 'form-control',
        'placeholder': 'Enter your registered email address',
        'autocomplete': 'email'
    })
    
    def validate_email(self, email):
        """Check if email exists in database"""
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('No account found with this email address.')

class ResetPasswordForm(FlaskForm):
    """Password reset form"""
    password = PasswordField('New Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=8, message='Password must be at least 8 characters long'),
        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)', 
               message='Password must contain at least one lowercase letter, one uppercase letter, and one number')
    ], render_kw={
        'class': 'form-control',
        'placeholder': 'Enter your new password',
        'autocomplete': 'new-password'
    })
    
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(message='Please confirm your new password'),
        EqualTo('password', message='Passwords do not match')
    ], render_kw={
        'class': 'form-control',
        'placeholder': 'Confirm your new password',
        'autocomplete': 'new-password'
    })

class ChangePasswordForm(FlaskForm):
    """Change password form for logged-in users"""
    current_password = PasswordField('Current Password', validators=[
        DataRequired(message='Current password is required')
    ], render_kw={
        'class': 'form-control',
        'placeholder': 'Enter your current password',
        'autocomplete': 'current-password'
    })
    
    new_password = PasswordField('New Password', validators=[
        DataRequired(message='New password is required'),
        Length(min=8, message='Password must be at least 8 characters long'),
        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)', 
               message='Password must contain at least one lowercase letter, one uppercase letter, and one number')
    ], render_kw={
        'class': 'form-control',
        'placeholder': 'Enter your new password',
        'autocomplete': 'new-password'
    })
    
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(message='Please confirm your new password'),
        EqualTo('new_password', message='Passwords do not match')
    ], render_kw={
        'class': 'form-control',
        'placeholder': 'Confirm your new password',
        'autocomplete': 'new-password'
    })

class ProfileForm(FlaskForm):
    """User profile edit form"""
    first_name = StringField('First Name', validators=[
        DataRequired(message='First name is required'),
        Length(min=2, max=50, message='First name must be between 2 and 50 characters')
    ], render_kw={
        'class': 'form-control',
        'autocomplete': 'given-name'
    })
    
    last_name = StringField('Last Name', validators=[
        DataRequired(message='Last name is required'),
        Length(min=2, max=50, message='Last name must be between 2 and 50 characters')
    ], render_kw={
        'class': 'form-control',
        'autocomplete': 'family-name'
    })
    
    organization = StringField('Organization', validators=[
        DataRequired(message='Organization is required'),
        Length(max=100, message='Organization name cannot exceed 100 characters')
    ], render_kw={
        'class': 'form-control',
        'autocomplete': 'organization'
    })
    
    country = SelectField('Country', validators=[
        DataRequired(message='Please select your country')
    ], choices=[
        ('AT', 'Austria'),
        ('BE', 'Belgium'),
        ('BG', 'Bulgaria'),
        ('HR', 'Croatia'),
        ('CY', 'Cyprus'),
        ('CZ', 'Czech Republic'),
        ('DK', 'Denmark'),
        ('EE', 'Estonia'),
        ('FI', 'Finland'),
        ('FR', 'France'),
        ('DE', 'Germany'),
        ('GR', 'Greece'),
        ('HU', 'Hungary'),
        ('IE', 'Ireland'),
        ('IT', 'Italy'),
        ('LV', 'Latvia'),
        ('LT', 'Lithuania'),
        ('LU', 'Luxembourg'),
        ('MT', 'Malta'),
        ('NL', 'Netherlands'),
        ('PL', 'Poland'),
        ('PT', 'Portugal'),
        ('RO', 'Romania'),
        ('SK', 'Slovakia'),
        ('SI', 'Slovenia'),
        ('ES', 'Spain'),
        ('SE', 'Sweden'),
        ('NO', 'Norway'),
        ('CH', 'Switzerland'),
        ('UK', 'United Kingdom'),
        ('US', 'United States'),
        ('CA', 'Canada'),
        ('AU', 'Australia'),
        ('NZ', 'New Zealand'),
        ('JP', 'Japan'),
        ('KR', 'South Korea'),
        ('SG', 'Singapore'),
        ('OTHER', 'Other')
    ], render_kw={
        'class': 'form-select'
    })