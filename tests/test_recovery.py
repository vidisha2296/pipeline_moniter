from datetime import datetime
from src.recovery_engine import RecoveryEngine
from src.alert_system import AlertSystem
from src.models import PipelineEvent, FailureType, PipelineStatus

def test_network_recovery():
    """Test network recovery functionality"""
    alert_system = AlertSystem({})
    recovery_engine = RecoveryEngine(alert_system)
    
    event = PipelineEvent(
        timestamp=datetime.now(),
        event_type="test",
        details={},
        status=PipelineStatus.FAILED,
        failure_type=FailureType.NETWORK
    )
    
    result = recovery_engine.attempt_recovery(FailureType.NETWORK, event)
    
    assert result.failure_type == FailureType.NETWORK
    assert isinstance(result.success, bool), "Success should be boolean"
    assert isinstance(result.message, str), "Message should be string"
    assert isinstance(result.action_taken, str), "Action taken should be string"

def test_validation_service_recovery():
    """Test validation service recovery functionality"""
    alert_system = AlertSystem({})
    recovery_engine = RecoveryEngine(alert_system)
    
    event = PipelineEvent(
        timestamp=datetime.now(),
        event_type="test",
        details={},
        status=PipelineStatus.FAILED,
        failure_type=FailureType.VALIDATION_SERVICE
    )
    
    result = recovery_engine.attempt_recovery(FailureType.VALIDATION_SERVICE, event)
    
    assert result.failure_type == FailureType.VALIDATION_SERVICE
    assert isinstance(result.success, bool), "Success should be boolean"
    assert isinstance(result.message, str), "Message should be string"
    assert isinstance(result.action_taken, str), "Action taken should be string"

def test_database_recovery():
    """Test database recovery functionality"""
    alert_system = AlertSystem({})
    recovery_engine = RecoveryEngine(alert_system)
    
    event = PipelineEvent(
        timestamp=datetime.now(),
        event_type="test",
        details={},
        status=PipelineStatus.FAILED,
        failure_type=FailureType.DATABASE
    )
    
    result = recovery_engine.attempt_recovery(FailureType.DATABASE, event)
    
    assert result.failure_type == FailureType.DATABASE
    assert isinstance(result.success, bool), "Success should be boolean"
    assert isinstance(result.message, str), "Message should be string"
    assert isinstance(result.action_taken, str), "Action taken should be string"

def test_unknown_recovery():
    """Test unknown failure type recovery functionality"""
    alert_system = AlertSystem({})
    recovery_engine = RecoveryEngine(alert_system)
    
    event = PipelineEvent(
        timestamp=datetime.now(),
        event_type="test",
        details={},
        status=PipelineStatus.FAILED,
        failure_type=FailureType.UNKNOWN
    )
    
    result = recovery_engine.attempt_recovery(FailureType.UNKNOWN, event)
    
    assert result.failure_type == FailureType.UNKNOWN
    assert isinstance(result.success, bool), "Success should be boolean"
    assert isinstance(result.message, str), "Message should be string"
    assert isinstance(result.action_taken, str), "Action taken should be string"

def test_all_recovery_types():
    """Test all recovery types in one function"""
    alert_system = AlertSystem({})
    recovery_engine = RecoveryEngine(alert_system)
    
    failure_types = [
        FailureType.NETWORK,
        FailureType.VALIDATION_SERVICE, 
        FailureType.DATABASE,
        FailureType.UNKNOWN
    ]
    
    for failure_type in failure_types:
        event = PipelineEvent(
            timestamp=datetime.now(),
            event_type=f"test_{failure_type.value}",
            details={},
            status=PipelineStatus.FAILED,
            failure_type=failure_type
        )
        
        result = recovery_engine.attempt_recovery(failure_type, event)
        
        # Verify basic structure
        assert result.failure_type == failure_type
        assert isinstance(result.success, bool), f"Success for {failure_type} should be boolean"
        assert isinstance(result.message, str), f"Message for {failure_type} should be string"
        assert isinstance(result.action_taken, str), f"Action taken for {failure_type} should be string"
        assert hasattr(result, 'timestamp'), f"Result for {failure_type} should have timestamp"

if __name__ == "__main__":
    test_network_recovery()
    test_validation_service_recovery()
    test_database_recovery()
    test_unknown_recovery()
    test_all_recovery_types()
    print("✅ All recovery engine tests passed!")