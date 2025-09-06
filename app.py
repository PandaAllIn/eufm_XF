#!/usr/bin/env python3
"""
XYL-PHOS-CURE Project Management Dashboard
A focused web interface for managing the Horizon Europe submission and consortium building
"""

from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from datetime import datetime, timedelta
import json
import os

# Import authentication components
from models import db, User, init_db
from auth import auth
from auth_utils import admin_required, verified_required

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'xyl-phos-cure-dev-key-2024')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///xyl_phos_cure.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_TIME_LIMIT'] = 3600  # 1 hour

# Initialize extensions
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

# Register blueprints
app.register_blueprint(auth)

# Initialize database
init_db(app)

@login_manager.user_loader
def load_user(user_id):
    """Load user for Flask-Login"""
    return User.query.get(int(user_id))

# Project configuration
PROJECT_CONFIG = {
    "name": "XYL-PHOS-CURE",
    "full_title": "Developing the First Curative Treatment for Xylella fastidiosa",
    "proposal_id": "101271185-1",
    "call": "HORIZON-CL6-2025-02-FARM2FORK-01-two-stage",
    "submitted_date": "2025-09-04",
    "budget": 6000000,  # €6M
    "duration_months": 42,
    "stage1_deadline": "2025-09-04",
    "stage1_results": "2026-01-15",  # Expected
    "stage2_deadline": "2026-02-18"
}

# Timeline milestones
MILESTONES = [
    {
        "id": 1,
        "title": "Stage 1 Submission",
        "date": "2025-09-04",
        "status": "completed",
        "description": "Stage 1 proposal successfully submitted",
        "progress": 100
    },
    {
        "id": 2,
        "title": "Consortium Building",
        "date": "2025-12-31",
        "status": "in_progress",
        "description": "Partner search and consortium agreements",
        "progress": 20
    },
    {
        "id": 3,
        "title": "Stage 1 Results",
        "date": "2026-01-15",
        "status": "pending",
        "description": "EU evaluation results announcement",
        "progress": 0
    },
    {
        "id": 4,
        "title": "Stage 2 Submission",
        "date": "2026-02-18",
        "status": "pending", 
        "description": "Full proposal submission (if Stage 1 approved)",
        "progress": 0
    }
]

# Consortium targets
CONSORTIUM_TARGETS = [
    {
        "role": "Research Partner - Plant Pathology",
        "target_country": "Spain",
        "status": "searching",
        "priority": "high",
        "description": "University/RTO with Xylella expertise and greenhouse facilities"
    },
    {
        "role": "Research Partner - Field Trials",
        "target_country": "Italy", 
        "status": "searching",
        "priority": "high",
        "description": "Research organization in Xylella-affected regions"
    },
    {
        "role": "Farmer Cooperative",
        "target_country": "Portugal",
        "status": "searching", 
        "priority": "high",
        "description": "Olive/almond growers for living lab trials"
    },
    {
        "role": "Industrial Formulation Partner",
        "target_country": "Germany/Netherlands",
        "status": "searching",
        "priority": "medium",
        "description": "Plant protection product formulation expertise"
    },
    {
        "role": "Regulatory/Policy Advisor",
        "target_country": "France",
        "status": "searching",
        "priority": "medium", 
        "description": "Plant health authority connections"
    }
]

@app.route('/')
@login_required
def dashboard():
    """Main dashboard view"""
    return render_template('dashboard.html', 
                         project=PROJECT_CONFIG,
                         milestones=MILESTONES,
                         consortium=CONSORTIUM_TARGETS,
                         user=current_user)

@app.route('/api/project-status')
@login_required
def project_status():
    """API endpoint for project status data"""
    # Calculate days until key dates
    today = datetime.now().date()
    stage1_results_date = datetime.strptime(PROJECT_CONFIG["stage1_results"], "%Y-%m-%d").date()
    stage2_deadline_date = datetime.strptime(PROJECT_CONFIG["stage2_deadline"], "%Y-%m-%d").date()
    
    days_to_results = (stage1_results_date - today).days
    days_to_stage2 = (stage2_deadline_date - today).days
    
    return jsonify({
        "proposal_id": PROJECT_CONFIG["proposal_id"],
        "status": "Stage 1 Submitted - Awaiting Results",
        "days_to_results": days_to_results,
        "days_to_stage2": days_to_stage2,
        "stage1_success_odds": "60-70%",
        "overall_success_odds": "15-20%",
        "budget": f"€{PROJECT_CONFIG['budget']:,}",
        "innovation_level": "HIGH - First systemic cure for Xylella"
    })

@app.route('/api/milestones')
@login_required
def api_milestones():
    """API endpoint for milestone data"""
    return jsonify(MILESTONES)

@app.route('/api/consortium')
@login_required
def api_consortium():
    """API endpoint for consortium data"""
    return jsonify(CONSORTIUM_TARGETS)

@app.route('/api/documents')
@login_required
def api_documents():
    """API endpoint for project documents"""
    documents = []
    
    # Check for key files
    key_files = [
        {"name": "PROJECT_JOURNAL.md", "description": "Project status and milestones", "type": "status"},
        {"name": "Horizon_Xilella.md", "description": "Strategic analysis (76KB)", "type": "analysis"},
        {"name": "Stage1_proposal_final_clean.md", "description": "Final submission version", "type": "proposal"},
        {"name": "Stage1_Proposal_Cline_Enhanced.md", "description": "Proposal content", "type": "proposal"},
        {"name": "README.md", "description": "Project overview", "type": "overview"}
    ]
    
    for file_info in key_files:
        if os.path.exists(file_info["name"]):
            stat = os.stat(file_info["name"])
            documents.append({
                "name": file_info["name"],
                "description": file_info["description"],
                "type": file_info["type"],
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
            })
    
    return jsonify(documents)

@app.route('/timeline')
@login_required
def timeline():
    """Timeline view"""
    return render_template('timeline.html', 
                         project=PROJECT_CONFIG,
                         milestones=MILESTONES)

@app.route('/consortium')
@login_required
def consortium():
    """Consortium building view"""
    return render_template('consortium.html', 
                         consortium=CONSORTIUM_TARGETS)

@app.route('/documents')
@login_required
def documents():
    """Documents management view"""
    return render_template('documents.html')

# Phase 2: Codex Integration API Endpoints
@app.route('/api/codex-status')
@login_required
def codex_status():
    """API endpoint for Codex background task status"""
    try:
        from codex_monitor import CodexMonitor
        monitor = CodexMonitor()
        status = monitor.check_status()
        return jsonify({
            "status": status["status"] if "status" in status else "idle",
            "is_running": status["is_running"],
            "message": status["message"],
            "current_task": status.get("current_task", None),
            "log_file": status.get("log_file", None)
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "is_running": False,
            "message": f"Error checking Codex status: {str(e)}"
        })

@app.route('/api/codex-logs')
@login_required
def codex_logs():
    """API endpoint for recent Codex logs"""
    try:
        from codex_monitor import CodexMonitor
        monitor = CodexMonitor()
        lines = request.args.get('lines', 20, type=int)
        logs = monitor.get_log_tail(lines)
        return jsonify({
            "logs": logs,
            "lines": lines
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "logs": "Error retrieving logs"
        })

@app.route('/api/codex-start', methods=['POST'])
@admin_required
def codex_start():
    """API endpoint to start a Codex background task"""
    try:
        data = request.get_json()
        task_description = data.get('task', '')
        
        if not task_description:
            return jsonify({"error": "Task description required"}), 400
        
        from codex_monitor import CodexMonitor
        monitor = CodexMonitor()
        result = monitor.trigger_background_task(task_description)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Failed to start Codex task: {str(e)}"
        })

@app.route('/codex')
@admin_required
def codex_dashboard():
    """Codex management dashboard"""
    return render_template('codex.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)