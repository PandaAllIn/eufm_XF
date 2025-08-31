# 🔬 EUFM Assistant - European Funds Management System

**CRITICAL DEADLINE: Stage 1 Proposal Due September 4, 2025**

An intelligent AI-powered project assistant for managing the Horizon Europe Xylella Fastidiosa research project. This system automates proposal generation, partner discovery, timeline tracking, and project management for the **HORIZON-CL6-2025-02-FARM2FORK-01-two-stage** call.

## 🚨 Tier 1 - Ready for September 4th Deadline

### Quick Start (URGENT - 3 Days Remaining!)

```bash
# 1. Install dependencies
python3 -m pip install pyyaml requests ruff pytest PyGithub Flask openai

# 2. Launch the system
python3 launch_eufm.py
```

**Access the system at: http://localhost:8080**
- **Username:** `admin`
- **Password:** `eufm2025!`

### 🎯 Critical Actions for September 4th

1. **Generate Stage 1 Proposal** ⚠️ URGENT
   - Go to "Proposal" tab in the dashboard
   - Click "Generate Stage 1 Proposal" 
   - Review and customize the 10-page proposal
   - Download and prepare for submission

2. **Configure OpenAI API** (Optional but recommended)
   - Edit: `src/eufm_assistant/ai_assistant/config/settings.yaml`
   - Replace `"dummy"` with your OpenAI API key

3. **Review Project Strategy**
   - Check the "Strategy" tab for the complete Xylella solution approach
   - Ensure all technical details are current

## 🏗️ System Architecture

### Core Components
- **🔐 Authentication System** - Secure access control
- **📝 Proposal Generator** - AI-powered Stage 1 proposal creation
- **🔍 Research Agent** - Partner discovery and research
- **📊 Monitoring Dashboard** - Real-time project tracking
- **⚠️ Alerts System** - Deadline and risk management
- **📋 WBS Management** - Work breakdown structure tracking

### Key Features
- **Two-Stage Proposal Support** - Horizon Europe compliant
- **Blind Evaluation Ready** - Anonymous submission format
- **Multi-Actor Approach** - Stakeholder integration
- **Real-time Monitoring** - Project health tracking
- **Automated Alerts** - Deadline notifications

## 📋 Project Overview

### Scientific Approach
Novel **phosphinic acid derivatives** as systemic bactericides against *Xylella fastidiosa* - potentially the first effective cure for this devastating plant pathogen affecting European agriculture.

### Horizon Europe Call Details
- **Call ID:** HORIZON-CL6-2025-02-FARM2FORK-01-two-stage
- **Title:** Emerging and future risks to plant health
- **Type:** Research and Innovation Action (RIA)
- **Budget:** ~€6 million EU contribution
- **Duration:** 48 months
- **Stage 1 Deadline:** September 4, 2025 ⚠️
- **Stage 2 Deadline:** February 18, 2026

## 🛠️ Technical Implementation

### Directory Structure
```
eufm/
├── src/eufm_assistant/
│   ├── agents/                 # AI agents
│   │   ├── proposal_agent.py   # Proposal generation
│   │   ├── research_agent.py   # Partner discovery
│   │   └── monitor/            # Monitoring system
│   ├── dashboard/              # Web interface
│   ├── auth/                   # Authentication
│   └── ai_assistant/           # Core AI components
├── wbs/                        # Work breakdown structure
├── docs/                       # Documentation
└── launch_eufm.py             # Launch script
```

### Database & Configuration
- **WBS Data:** `wbs/wbs.yaml` - Tasks, deadlines, owners
- **Milestones:** `wbs/milestones.yaml` - Key project gates
- **Settings:** `src/eufm_assistant/ai_assistant/config/settings.yaml`

## 🚀 Deployment Options

### Local Development (Current - Tier 1)
```bash
python3 launch_eufm.py
```

### Production Deployment (Future - Tier 2)
- Docker containerization ready
- Cloud deployment scripts available
- CI/CD pipeline configured

## 📊 Monitoring & Alerts

### Daily Monitoring
- Automated deadline tracking
- Progress compliance scoring
- Risk identification
- GitHub integration for issue management

### Alert Levels
- 🔴 **EMERGENCY** - <24 hours remaining (CRITICAL priority)
- 🟡 **CRITICAL** - 1-3 days remaining  
- 🔵 **WARNING** - 3-7 days remaining
- ⚫ **OVERDUE** - Past deadline

## 🤝 Multi-Actor Approach

Ready to integrate:
- **Research Organizations** - Universities, RTOs
- **Industry Partners** - SMEs, formulation companies
- **End Users** - Farmer cooperatives
- **Advisory Bodies** - Plant health authorities

## 📈 Success Metrics

### Tier 1 (Complete - Sept 4)
- ✅ Stage 1 proposal generated and submitted
- ✅ System operational with monitoring
- ✅ Authentication and security active

### Tier 2 (Post-funding)
- Partner consortium confirmed
- Stage 2 proposal submitted
- Project execution begins

## 🔧 Configuration

### Environment Variables
```bash
export EUFM_ADMIN_USER="admin"
export EUFM_ADMIN_PASS_HASH="your_hash"
export EUFM_SECRET_KEY="your_secret_key"
export GITHUB_TOKEN="your_github_token"  # For issue management
```

### OpenAI Integration
Edit `src/eufm_assistant/ai_assistant/config/settings.yaml`:
```yaml
openai_api_key: "your-api-key-here"
llm_model: "gpt-4o"
```

## 🆘 Emergency Support

### Critical Issue Resolution
1. **System Won't Start** - Check Python path and dependencies
2. **Login Issues** - Use default admin/eufm2025!
3. **Proposal Generation Fails** - Check OpenAI API key
4. **Missing Deadlines** - Check WBS dates in `wbs/wbs.yaml`

### Contact Information
- **Technical Support:** System administrator
- **Project Lead:** CSO (your brother)
- **Emergency:** Check system health in dashboard

## 📜 Legal & Compliance

- **EU GDPR Compliant** - Data protection built-in
- **Horizon Europe Rules** - IP management ready
- **Open Source Components** - All dependencies cleared
- **Security Protocols** - Authentication and encryption

---

**⚠️ REMEMBER: Stage 1 Proposal Due September 4, 2025**

*This system is your collaborative partner in securing €6M EU funding for solving the Xylella crisis. Use it strategically and act decisively.*
