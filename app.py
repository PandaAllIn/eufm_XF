#!/usr/bin/env python3
"""
XYL-PHOS-CURE Project Management Dashboard
A focused web interface for managing the Horizon Europe submission and consortium building
"""

from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)

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
def dashboard():
    """Main dashboard view"""
    return render_template('dashboard.html', 
                         project=PROJECT_CONFIG,
                         milestones=MILESTONES,
                         consortium=CONSORTIUM_TARGETS)

@app.route('/api/project-status')
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
def api_milestones():
    """API endpoint for milestone data"""
    return jsonify(MILESTONES)

@app.route('/api/consortium')
def api_consortium():
    """API endpoint for consortium data"""
    return jsonify(CONSORTIUM_TARGETS)

@app.route('/api/documents')
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
def timeline():
    """Timeline view"""
    return render_template('timeline.html', 
                         project=PROJECT_CONFIG,
                         milestones=MILESTONES)

@app.route('/consortium')
def consortium():
    """Consortium building view"""
    return render_template('consortium.html', 
                         consortium=CONSORTIUM_TARGETS)

@app.route('/documents')
def documents():
    """Documents management view"""
    return render_template('documents.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)