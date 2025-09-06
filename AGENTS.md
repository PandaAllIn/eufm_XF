# AGENTS.md - AI Agent Configuration for XYL-PHOS-CURE Project

## Project Overview
**XYL-PHOS-CURE**: €6M Horizon Europe RIA developing the first curative treatment for Xylella fastidiosa
- **Stage**: Awaiting Stage 1 results (Jan 2026), preparing Stage 2 proposal (Feb 18, 2026)
- **TRL**: 2-3 → 5-6 progression
- **Technology**: Phosphinic acid derivatives for systemic plant therapeutics

## Codebase Architecture

### Core Application Structure
```
├── app.py              # Main Flask application with routes
├── auth.py             # Authentication system (JWT-based)
├── auth_utils.py       # Authentication utilities
├── models.py           # Data models and database schemas
├── forms.py            # WTForms definitions
├── templates/          # Jinja2 HTML templates
├── static/
│   ├── css/           # Stylesheets
│   ├── js/            # JavaScript files
│   └── images/        # Static assets
└── logs/              # Application and agent logs
```

### Agent Infrastructure
```
├── codex_monitor.py           # Background task monitoring
├── scripts/
│   ├── codex-helper.sh       # Bash wrapper for Codex tasks
│   └── real-codex-helper.py  # Python Codex executor
├── smart_task_detector.py    # Task classification system
└── logs/                     # Agent execution logs
```

## Development Standards

### Code Style
- **Python**: Follow PEP 8, use type hints where possible
- **JavaScript**: ES6+, consistent indentation (2 spaces)
- **HTML**: Semantic markup, accessibility attributes
- **CSS**: Mobile-first responsive design, CSS Grid/Flexbox

### Framework Conventions
- **Flask**: Blueprint organization, error handling with try/catch
- **Frontend**: Progressive enhancement, no heavy JS frameworks
- **Database**: SQLAlchemy ORM, migration-based schema changes
- **Authentication**: JWT tokens, role-based access control

### File Naming
- **Templates**: snake_case.html (e.g., `project_dashboard.html`)
- **Static files**: kebab-case (e.g., `main-dashboard.css`)
- **Python modules**: snake_case.py
- **JavaScript**: camelCase variables, kebab-case files

## Project-Specific Context

### Critical Deadlines
- **January 15, 2026**: Stage 1 evaluation results announcement
- **February 18, 2026**: Stage 2 proposal submission deadline (if selected)
- **September 2026**: Project start (if funded)

### Key Stakeholders
- **EU Commission**: HORIZON-CL6-2025-02-FARM2FORK-01-two-stage call
- **Target Partners**: Spanish/Italian/Portuguese research institutions + farmer cooperatives
- **Regulatory**: EU plant protection product registration pathway

### Domain Knowledge
- **Xylella fastidiosa**: Gram-negative bacteria, xylem-limited pathogen
- **Target crops**: Olive, citrus, almond trees
- **Technology**: Phosphinic acid derivatives (Fosfomycin analogs)
- **Market impact**: €5.5B annual threat, 300K jobs at risk

## Agent Instructions

### For Dashboard Development
- **Priority**: Professional, executive-level interface suitable for €6M project
- **Visual standards**: Corporate pharmaceutical/research sector aesthetics
- **Data focus**: Real-time KPIs, milestone tracking, budget monitoring
- **Responsive**: Desktop + tablet optimized

### For Authentication System
- **Security**: JWT-based, role separation (coordinator/partner/viewer)
- **Integration**: Connect with existing Flask-Login patterns
- **Features**: Registration, password reset, email verification

### For Data Visualization
- **Charts**: Progress tracking, budget allocation, timeline views
- **Alerts**: Deadline countdowns, budget variance warnings
- **Maps**: Partner consortium geographical distribution

### Command Execution
```bash
# Development server
python3 app.py

# Run tests (when available)
python3 -m pytest

# Monitor agents
python3 codex_monitor.py

# Start background task
python3 codex_monitor.py start "task description"
```

### Environment Setup
- **Python 3.9+** required
- **Virtual environment** recommended
- **Dependencies**: Flask, SQLAlchemy, WTForms, JWT libraries
- **Development**: Use local SQLite, production PostgreSQL ready

## Quality Standards

### Code Review Checklist
- [ ] Follows project naming conventions
- [ ] Includes proper error handling
- [ ] Mobile responsive (CSS)
- [ ] Accessible (ARIA labels, semantic HTML)
- [ ] Secure (input validation, CSRF protection)
- [ ] Performance optimized (<2s load times)

### Testing Requirements
- Unit tests for critical business logic
- Integration tests for authentication flows
- UI tests for dashboard functionality
- Performance tests for data visualization

### Documentation
- Inline comments for complex business logic
- Docstrings for public functions
- README updates for new features
- API documentation for endpoints

---

**Agent Success Criteria**: Deliver production-ready code that reflects the professionalism and scale of a €6M EU research initiative, with particular attention to executive-level presentation quality and regulatory compliance readiness.