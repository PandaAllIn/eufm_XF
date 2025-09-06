"""
Authentication routes for XYL-PHOS-CURE project
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from models import User, LoginAttempt, db
from forms import LoginForm, RegistrationForm, ForgotPasswordForm, ResetPasswordForm, ChangePasswordForm, ProfileForm
from auth_utils import (
    admin_required, verified_required, check_rate_limit, record_login_attempt, 
    get_client_ip, EmailService, get_country_name
)
from datetime import datetime

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        ip_address = get_client_ip()
        
        # Check rate limiting
        if check_rate_limit(ip_address):
            flash('Too many failed login attempts. Please try again later.', 'danger')
            return render_template('auth/login.html', form=form)
        
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and user.check_password(form.password.data):
            if not user.is_active:
                record_login_attempt(ip_address, form.email.data, False)
                flash('Your account has been deactivated. Please contact support.', 'danger')
                return render_template('auth/login.html', form=form)
            
            # Successful login
            login_user(user, remember=form.remember_me.data)
            user.update_last_login()
            db.session.commit()
            
            record_login_attempt(ip_address, form.email.data, True)
            
            flash(f'Welcome back, {user.full_name}!', 'success')
            
            # Redirect to intended page or dashboard
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('dashboard'))
        else:
            # Failed login
            record_login_attempt(ip_address, form.email.data, False)
            flash('Invalid email or password.', 'danger')
    
    return render_template('auth/login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        # Create new user
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            organization=form.organization.data,
            country=form.country.data
        )
        user.set_password(form.password.data)
        
        # Generate verification token
        token = user.generate_verification_token()
        
        db.session.add(user)
        db.session.commit()
        
        # Send verification email
        email_service = EmailService()
        if email_service.send_verification_email(user, token):
            flash('Registration successful! Please check your email to verify your account.', 'success')
        else:
            flash('Registration successful! However, we couldn\'t send the verification email. Please contact support.', 'warning')
        
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    """User logout"""
    username = current_user.username
    logout_user()
    flash(f'You have been logged out successfully. Goodbye, {username}!', 'info')
    return redirect(url_for('auth.login'))

@auth.route('/verify-email/<token>')
def verify_email(token):
    """Email verification"""
    user = User.query.filter_by(verification_token=token).first()
    
    if not user:
        flash('Invalid or expired verification token.', 'danger')
        return redirect(url_for('auth.login'))
    
    if user.verify_email(token):
        db.session.commit()
        
        # Send welcome email
        email_service = EmailService()
        email_service.send_welcome_email(user)
        
        flash('Your email has been verified successfully! You can now log in.', 'success')
    else:
        flash('Invalid or expired verification token.', 'danger')
    
    return redirect(url_for('auth.login'))

@auth.route('/resend-verification')
@login_required
def resend_verification():
    """Resend verification email"""
    if current_user.is_verified:
        flash('Your email is already verified.', 'info')
        return redirect(url_for('dashboard'))
    
    token = current_user.generate_verification_token()
    db.session.commit()
    
    email_service = EmailService()
    if email_service.send_verification_email(current_user, token):
        flash('A new verification email has been sent to your address.', 'success')
    else:
        flash('Failed to send verification email. Please try again later.', 'danger')
    
    return redirect(url_for('dashboard'))

@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Password reset request"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = ForgotPasswordForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user:
            token = user.generate_reset_token()
            db.session.commit()
            
            email_service = EmailService()
            if email_service.send_password_reset_email(user, token):
                flash('Password reset instructions have been sent to your email.', 'info')
            else:
                flash('Failed to send reset email. Please try again later.', 'danger')
        else:
            # For security, don't reveal if email exists
            flash('If that email address exists, password reset instructions have been sent.', 'info')
        
        return redirect(url_for('auth.login'))
    
    return render_template('auth/forgot_password.html', form=form)

@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Password reset with token"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    user = User.query.filter_by(reset_token=token).first()
    
    if not user or not user.verify_reset_token(token):
        flash('Invalid or expired reset token.', 'danger')
        return redirect(url_for('auth.forgot_password'))
    
    form = ResetPasswordForm()
    
    if form.validate_on_submit():
        user.set_password(form.password.data)
        user.clear_reset_token()
        db.session.commit()
        
        flash('Your password has been reset successfully. You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', form=form)

@auth.route('/profile')
@login_required
def profile():
    """User profile view"""
    return render_template('auth/profile.html', user=current_user)

@auth.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Edit user profile"""
    form = ProfileForm(obj=current_user)
    
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.organization = form.organization.data
        current_user.country = form.country.data
        current_user.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Your profile has been updated successfully.', 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('auth/edit_profile.html', form=form)

@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change password"""
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash('Current password is incorrect.', 'danger')
            return render_template('auth/change_password.html', form=form)
        
        current_user.set_password(form.new_password.data)
        current_user.updated_at = datetime.utcnow()
        db.session.commit()
        
        flash('Your password has been changed successfully.', 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('auth/change_password.html', form=form)

@auth.route('/users')
@admin_required
def manage_users():
    """Admin: Manage users"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    role_filter = request.args.get('role', '')
    
    query = User.query
    
    if search:
        query = query.filter(
            User.username.contains(search) | 
            User.email.contains(search) |
            User.first_name.contains(search) |
            User.last_name.contains(search) |
            User.organization.contains(search)
        )
    
    if role_filter:
        query = query.filter(User.role == role_filter)
    
    users = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('auth/manage_users.html', users=users, search=search, role_filter=role_filter)

@auth.route('/users/<int:user_id>/toggle-status', methods=['POST'])
@admin_required
def toggle_user_status(user_id):
    """Admin: Toggle user active status"""
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        return jsonify({'success': False, 'message': 'Cannot deactivate your own account'})
    
    user.is_active = not user.is_active
    db.session.commit()
    
    status = 'activated' if user.is_active else 'deactivated'
    return jsonify({
        'success': True, 
        'message': f'User {user.username} has been {status}',
        'is_active': user.is_active
    })

@auth.route('/users/<int:user_id>/toggle-role', methods=['POST'])
@admin_required
def toggle_user_role(user_id):
    """Admin: Toggle user admin role"""
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        return jsonify({'success': False, 'message': 'Cannot change your own role'})
    
    user.role = 'admin' if user.role == 'user' else 'user'
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': f'User {user.username} is now a {user.role}',
        'role': user.role
    })

@auth.route('/api/profile')
@login_required
def api_profile():
    """API: Get user profile data"""
    return jsonify({
        'success': True,
        'user': current_user.to_dict()
    })

@auth.route('/api/users')
@admin_required
def api_users():
    """API: Get users list"""
    users = User.query.order_by(User.created_at.desc()).all()
    return jsonify({
        'success': True,
        'users': [user.to_dict() for user in users]
    })

# Context processor to make auth utilities available in templates
@auth.app_context_processor
def inject_auth_utils():
    """Inject auth utilities into template context"""
    return {
        'get_country_name': get_country_name
    }