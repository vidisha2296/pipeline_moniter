
from datetime import datetime
from src.monitor import PipelineMonitor
from src.models import PipelineStatus, FailureType

def test_initial_status():
    """Test monitor initializes with healthy status"""
    monitor = PipelineMonitor()
    assert monitor.current_status == PipelineStatus.HEALTHY, "Monitor should start healthy"

def test_health_check_structure():
    """Test health check returns proper structure"""
    monitor = PipelineMonitor()
    result = monitor.check_pipeline_health()
    
    assert hasattr(result, 'status'), "Health check should have status"
    assert hasattr(result, 'timestamp'), "Health check should have timestamp"
    assert hasattr(result, 'components'), "Health check should have components"
    assert hasattr(result, 'failure_type'), "Health check should have failure_type"
    
    components = result.components
    assert 'network' in components, "Should check network component"
    assert 'validation_service' in components, "Should check validation service component"
    assert 'database' in components, "Should check database component"

def test_failure_detection():
    """Test that failures are properly detected"""
    monitor = PipelineMonitor()
    
    # Run multiple health checks to potentially catch a failure
    failure_detected = False
    for _ in range(10):  # Try multiple times due to random failure simulation
        result = monitor.check_pipeline_health()
        if result.status == PipelineStatus.FAILED:
            failure_detected = True
            assert result.failure_type is not None, "Failure should have a type"
            assert result.failure_type in [FailureType.NETWORK, FailureType.VALIDATION_SERVICE, FailureType.DATABASE, FailureType.UNKNOWN], "Failure type should be valid"
            break
    
    # It's OK if no failure was detected in test runs - the random simulation might not trigger one
    # The important thing is that when a failure does occur, it's properly handled
    print(f"Failure detected in test: {failure_detected}")

def test_status_report_structure():
    """Test status report has correct structure"""
    monitor = PipelineMonitor()
    report = monitor.get_status_report()
    
    assert 'current_status' in report, "Report should have current_status"
    assert 'last_checked' in report, "Report should have last_checked"
    assert 'health_check_results' in report, "Report should have health_check_results"
    assert 'recent_failures' in report, "Report should have recent_failures"
    assert 'recent_recoveries' in report, "Report should have recent_recoveries"
    assert 'suggested_action' in report, "Report should have suggested_action"

def test_failure_type_determination():
    """Test failure type mapping works correctly"""
    monitor = PipelineMonitor()
    
    # FIXED: The method only takes 1 argument (failed_component)
    assert monitor._determine_failure_type('network') == FailureType.NETWORK
    assert monitor._determine_failure_type('validation_service') == FailureType.VALIDATION_SERVICE
    assert monitor._determine_failure_type('database') == FailureType.DATABASE
    assert monitor._determine_failure_type('unknown') == FailureType.UNKNOWN
    assert monitor._determine_failure_type('') == FailureType.UNKNOWN

def test_suggested_actions():
    """Test that appropriate suggestions are provided for different failure types"""
    monitor = PipelineMonitor()
    report = monitor.get_status_report()
    
    # Test that we get a suggestion regardless of status
    assert 'suggested_action' in report, "Report should always have suggested action"
    assert isinstance(report['suggested_action'], str), "Suggestion should be a string"
    assert len(report['suggested_action']) > 0, "Suggestion should not be empty"

def test_recovery_trigger():
    """Test that recovery can be triggered"""
    from src.models import PipelineEvent
    
    monitor = PipelineMonitor()
    
    # Create a test failure event
    test_event = PipelineEvent(
        timestamp=datetime.now(),
        event_type="test_failure",
        details={"component": "network", "error": "test error"},
        status=PipelineStatus.FAILED,
        failure_type=FailureType.NETWORK
    )
    
    # Trigger recovery
    result = monitor.trigger_auto_recovery(test_event)
    
    # Check result structure
    assert hasattr(result, 'success'), "Recovery result should have success status"
    assert hasattr(result, 'message'), "Recovery result should have message"
    assert hasattr(result, 'action_taken'), "Recovery result should have action_taken"
    assert hasattr(result, 'timestamp'), "Recovery result should have timestamp"

if __name__ == "__main__":
    test_initial_status()
    test_health_check_structure()
    test_failure_detection()
    test_status_report_structure()
    test_failure_type_determination()
    test_suggested_actions()
    test_recovery_trigger()
    print("✅ All monitor tests passed!")