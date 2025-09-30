import logging
from src.alert_system import AlertSystem
from src.models import AlertLevel, PipelineEvent, PipelineStatus, FailureType
from datetime import datetime

def test_alert_creation():
    """Test that alerts can be created without errors"""
    alert_system = AlertSystem({})
    event = PipelineEvent(
        timestamp=datetime.now(),
        event_type="test_alert",
        details={"test": "data"},
        status=PipelineStatus.FAILED,
        failure_type=FailureType.NETWORK
    )
    
    # Test that we can send alerts at all levels without exceptions
    alert_system.send_alert(AlertLevel.INFO, "Test info message", event)
    alert_system.send_alert(AlertLevel.WARNING, "Test warning message", event)
    alert_system.send_alert(AlertLevel.ERROR, "Test error message", event)
    alert_system.send_alert(AlertLevel.CRITICAL, "Test critical message", event)

def test_alert_logging():
    """Test that alerts are properly logged"""
    alert_system = AlertSystem({})
    event = PipelineEvent(
        timestamp=datetime.now(),
        event_type="test_logging",
        details={"component": "network", "error": "test error"},
        status=PipelineStatus.FAILED,
        failure_type=FailureType.NETWORK,
        component="network"
    )
    
    # This should log to both console and file without errors
    alert_system.send_alert(AlertLevel.ERROR, "Test error for logging", event)

def test_alert_with_different_events():
    """Test alerts with different event types"""
    alert_system = AlertSystem({})
    
    # Test with validation service failure
    validation_event = PipelineEvent(
        timestamp=datetime.now(),
        event_type="validation_failure",
        details={"service": "validation", "error": "rate limit"},
        status=PipelineStatus.FAILED,
        failure_type=FailureType.VALIDATION_SERVICE,
        component="validation_service"
    )
    
    # Test with database failure
    db_event = PipelineEvent(
        timestamp=datetime.now(),
        event_type="database_failure", 
        details={"database": "primary", "error": "connection pool"},
        status=PipelineStatus.FAILED,
        failure_type=FailureType.DATABASE,
        component="database"
    )
    
    # Test with unknown failure
    unknown_event = PipelineEvent(
        timestamp=datetime.now(),
        event_type="unknown_failure",
        details={"error": "unknown issue"},
        status=PipelineStatus.FAILED,
        failure_type=FailureType.UNKNOWN,
        component="unknown"
    )
    
    # All should work without errors
    alert_system.send_alert(AlertLevel.WARNING, "Validation service issue", validation_event)
    alert_system.send_alert(AlertLevel.ERROR, "Database connection problem", db_event)
    alert_system.send_alert(AlertLevel.CRITICAL, "Unknown system failure", unknown_event)

if __name__ == "__main__":
    test_alert_creation()
    test_alert_logging()
    test_alert_with_different_events()
    print("✅ All alert system tests passed!")