Overview
A comprehensive monitoring and recovery system for the EssentiallySports article publishing pipeline. Automatically detects failures, attempts auto-recovery, and provides clear editor guidance to restore publishing with minimal engineering involvement.

🚀 Quick Start
Prerequisites
Python 3.8+

pip (Python package manager)

Installation
Clone and setup:

bash
# Navigate to project directory
cd pipeline_moniter

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
Run the application:

bash
# Development mode with auto-reload
uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Or run directly
python app.py
Access the system:

API Documentation: http://localhost:8000/docs

Status Dashboard: http://localhost:8000/pipeline/status

Health Check: http://localhost:8000/health

📊 Key Features
Automated Monitoring
Continuous Health Checks: Monitors network, validation service, and database

Real-time Failure Detection: Identifies issues before they impact publishing

Smart Alerting: Different severity levels (INFO, WARNING, ERROR, CRITICAL)

Auto-Recovery System
Automatic Repair: Attempts to fix common issues without human intervention

Intelligent Recovery: Different strategies for different failure types

Recovery Tracking: Logs all recovery attempts and outcomes

Editor-Friendly Interface
Clear Status Reports: Simple "healthy/failed" status with explanations

Actionable Guidance: Step-by-step recovery instructions for editors

No Technical Jargon: Plain language that anyone can understand

Comprehensive Analytics
Failure Trends: Identify recurring issues and patterns

Recovery Success Rates: Measure auto-recovery effectiveness

Historical Data: Track pipeline performance over time

🔧 API Endpoints
Core Monitoring
GET /pipeline/status - Current pipeline status + recovery suggestions

POST /pipeline/health-check - Force immediate health check

GET /pipeline/components - Detailed component status

Historical Data
GET /pipeline/history - Recent events and recovery attempts

GET /pipeline/failures - Failure patterns and summaries

GET /pipeline/analytics - System statistics and success rates

Testing & Recovery
POST /pipeline/trigger-recovery - Manual recovery test

POST /pipeline/reset-stats - Clear test data (development)

📝 How Editors Use This System
Scenario 1: Pipeline Goes Down
Editor notices publishing is stuck

Visits http://localhost:8000/pipeline/status

Sees clear status:

json
{
  "current_status": "failed",
  "suggested_action": "Restart validation service manually...",
  "components_health": {
    "validation_service": false
  }
}
Follows instructions - no engineering help needed

Scenario 2: Auto-Recovery Works
Temporary network glitch occurs

System detects → auto-recovers → logs event

Editor sees status is "healthy" - no action needed

📋 Interpreting Logs
Log File Location
Audit Log: pipeline_audit.log

Database: pipeline_events.db

Log Levels
INFO: Normal operations, successful recoveries

WARNING: Recovery attempts, degraded performance

ERROR: Recovery failures, non-critical issues

CRITICAL: Pipeline failures requiring immediate attention

Common Log Patterns
Failure Detected
text
2025-09-30 22:09:07,403 - PipelineMonitor - ERROR - [ERROR] Pipeline failure detected in network: DNS resolution failed | Failure: FailureType.NETWORK | Component: network
2025-09-30 22:09:07,403 - PipelineMonitor - ERROR - Pipeline failure in network: DNS resolution failed
Recovery Attempt
text
2025-09-30 22:09:07,403 - PipelineMonitor - WARNING - [WARNING] Attempting auto-recovery for FailureType.NETWORK | Failure: FailureType.NETWORK | Component: network
Recovery Successful
text
2025-09-30 22:09:08,410 - PipelineMonitor - INFO - [INFO] Auto-recovery successful: Network connectivity restored | Failure: FailureType.NETWORK | Component: network
2025-09-30 22:09:08,410 - PipelineMonitor - INFO - Auto-recovery successful: Network connectivity restored
Health Check Passed
text
2025-09-30 22:09:08,412 - PipelineMonitor - INFO - Pipeline health check passed - all systems operational
🧪 Testing
Run All Tests
bash
python run_tests.py
Test Specific Components
bash
# Basic functionality
python tests/test_basic.py

# Monitor logic
python tests/test_monitor.py

# Alert system
python tests/test_alerts.py

# Recovery engine
python tests/test_recovery.py
Generate Test Data
bash
# Run multiple health checks to see different states
for i in {1..5}; do
  curl -X POST http://localhost:8000/pipeline/health-check
  sleep 2
done

# Check results
curl http://localhost:8000/pipeline/analytics
curl http://localhost:8000/pipeline/history
🗄️ Database
Schema
The system uses SQLite with two main tables:

pipeline_events

id, timestamp, event_type, status, failure_type, component, details

recovery_attempts

id, timestamp, failure_type, success, message, action_taken, related_event_id

Query Examples
bash
# View recent events
sqlite3 pipeline_events.db "SELECT event_type, status, component FROM pipeline_events ORDER BY timestamp DESC LIMIT 10;"

# Check recovery success rate
sqlite3 pipeline_events.db "SELECT failure_type, COUNT(*), AVG(success) FROM recovery_attempts GROUP BY failure_type;"
🛠️ Configuration
Environment Variables (.env)
env
DATABASE_URL=sqlite:///./pipeline_monitor.db
ENVIRONMENT=development
HEALTH_CHECK_INTERVAL=30
EMAIL_ENABLED=false
Monitor Configuration
The system can be configured via the PipelineMonitor constructor:

python
monitor = PipelineMonitor({
    'health_check_interval': 30,
    'email_enabled': False,
    'auto_recovery_enabled': True
})
📈 Monitoring in Production
Integration with Real Infrastructure
Replace simulated health checks with real checks:

python
# Example: Real network check
def _check_network_health(self):
    try:
        response = requests.get('https://api.essentiallysports.com/health', timeout=5)
        return response.status_code == 200, f"Status: {response.status_code}"
    except Exception as e:
        return False, f"Network error: {str(e)}"
Alert Notifications
Configure email/Slack alerts for critical failures:

python
# In alert_system.py
def _send_email_alert(self, level, message, event):
    # Implement email/Slack/webhook notifications
    pass
🆘 Troubleshooting
Common Issues
Port already in use:

bash
# Use different port
uvicorn app:app --reload --host 0.0.0.0 --port 8001
Import errors:

bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
Database issues:

bash
# Reset database (development only)
rm pipeline_events.db
# The system will recreate it on next run
Getting Help
Check the audit logs: tail -f pipeline_audit.log

Verify API status: curl http://localhost:8000/health

Check test results: python run_tests.py

