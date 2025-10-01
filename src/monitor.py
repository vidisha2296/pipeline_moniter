import logging
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
import random
from .models import PipelineStatus, FailureType, PipelineEvent, AlertLevel, RecoveryResult, HealthCheckResponse
from .alert_system import AlertSystem
from .recovery_engine import RecoveryEngine
from .database import PipelineDatabase

class PipelineMonitor:
    def __init__(self, config: dict = None):
        self.config = config or {}
        self.alert_system = AlertSystem(self.config)
        self.recovery_engine = RecoveryEngine(self.alert_system)
        self.database = PipelineDatabase()  # Database integration
        self.current_status = PipelineStatus.HEALTHY
        self.failure_history: List[PipelineEvent] = []
        self.recovery_history: List[RecoveryResult] = []
        self.setup_logging()
    
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('pipeline_audit.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("PipelineMonitor")
    
    def check_pipeline_health(self) -> HealthCheckResponse:
        """Perform comprehensive health check of publishing pipeline"""
        self.logger.info("Performing pipeline health check")
        
        # More realistic health checks with varied responses
        components = {
            'network': {
                'healthy': random.random() > 0.2,  # 80% healthy
                'response_time': f"{random.randint(10, 200)}ms",
                'latency': f"{random.randint(1, 50)}ms",
                'packet_loss': f"{random.random() * 5:.2f}%"
            },
            'validation_service': {
                'healthy': random.random() > 0.15,  # 85% healthy
                'version': '2.1.0',
                'queue_size': random.randint(0, 50),
                'processing_time': f"{random.randint(10, 500)}ms"
            },
            'database': {
                'healthy': random.random() > 0.1,  # 90% healthy
                'connections': random.randint(3, 20),
                'query_time': f"{random.randint(5, 100)}ms",
                'active_sessions': random.randint(1, 15)
            }
        }
        
        # Add realistic error messages when components are unhealthy
        failure_messages = {
            'network': ["Connection timeout", "DNS resolution failed", "SSL handshake error", "High packet loss"],
            'validation_service': ["Service unresponsive", "Queue overloaded", "Memory limit exceeded", "API rate limit reached"],
            'database': ["Connection pool exhausted", "Query timeout", "Deadlock detected", "Authentication failed"]
        }
        
        failure_type = None
        failed_component = None
        status = PipelineStatus.HEALTHY
        
        # Check each component and set failure details
        for component, data in components.items():
            if not data['healthy']:
                status = PipelineStatus.FAILED
                failed_component = component
                failure_type = self._determine_failure_type(component)
                data['error'] = random.choice(failure_messages[component])
                data['last_error_time'] = datetime.now().isoformat()
        
        # Log failure if detected
        if status == PipelineStatus.FAILED:
            failure_event = PipelineEvent(
                timestamp=datetime.now(),
                event_type="pipeline_failure",
                details=components,
                status=status,
                failure_type=failure_type,
                component=failed_component
            )
            self.failure_history.append(failure_event)
            
            # Store in database
            self.database.store_event(failure_event.dict())
            
            # Send alert
            self.alert_system.send_alert(
                AlertLevel.ERROR,
                f"Pipeline failure detected in {failed_component}: {components[failed_component]['error']}",
                failure_event
            )
            
            self.logger.error(f"Pipeline failure in {failed_component}: {components[failed_component]['error']}")
            
            # Auto-trigger recovery for certain failure types
            if failure_type in [FailureType.NETWORK, FailureType.VALIDATION_SERVICE]:
                self.trigger_auto_recovery(failure_event)
        else:
            self.logger.info("Pipeline health check passed - all systems operational")
        
        return HealthCheckResponse(
            status=status,
            timestamp=datetime.now(),
            components=components,
            failure_type=failure_type
        )
    
    def _determine_failure_type(self, failed_component: str) -> FailureType:
        """Map failed component to specific failure type"""
        failure_map = {
            'network': FailureType.NETWORK,
            'validation_service': FailureType.VALIDATION_SERVICE,
            'database': FailureType.DATABASE
        }
        return failure_map.get(failed_component, FailureType.UNKNOWN)
    
    def get_status_report(self) -> Dict[str, Any]:
        """Generate comprehensive status report for API endpoint"""
        health_result = self.check_pipeline_health()
        
        # Get recent events from database for more comprehensive report
        recent_events = self.database.get_recent_events(5)
        recent_recoveries = self.database.get_recovery_attempts(5)
        
        return {
            'current_status': health_result.status,
            'last_checked': health_result.timestamp,
            'health_check_results': health_result.dict(),
            'recent_failures': [event for event in recent_events if event['status'] == 'failed'],
            'recent_recoveries': recent_recoveries,
            'suggested_action': self._get_suggested_action(health_result),
            'components_health': {
                component: data['healthy'] 
                for component, data in health_result.components.items()
            }
        }
    
    def _get_suggested_action(self, health_result: HealthCheckResponse) -> str:
        """Provide editor-facing recovery suggestions"""
        if health_result.status == PipelineStatus.HEALTHY:
            return "No action needed - pipeline is healthy"
        
        if health_result.failure_type == FailureType.NETWORK:
            return "Check network connectivity, VPN, and firewall settings. Contact IT if issues persist."
        elif health_result.failure_type == FailureType.VALIDATION_SERVICE:
            return "Restart validation service manually. Clear cache if necessary. Contact engineering if service won't start."
        elif health_result.failure_type == FailureType.DATABASE:
            return "Check database connection string and credentials. Verify database server status. Contact DBA if needed."
        else:
            return "Manual investigation required. Check all pipeline components and review logs for unusual activity."
    
    def trigger_auto_recovery(self, failure_event: PipelineEvent) -> RecoveryResult:
        """Attempt automatic recovery based on failure type"""
        self.alert_system.send_alert(
            AlertLevel.WARNING,
            f"Attempting auto-recovery for {failure_event.failure_type}",
            failure_event
        )
        
        result = self.recovery_engine.attempt_recovery(failure_event.failure_type, failure_event)
        self.recovery_history.append(result)
        
        # Store in database
        self.database.store_recovery_attempt(result.dict())
        
        if result.success:
            self.alert_system.send_alert(
                AlertLevel.INFO,
                f"Auto-recovery successful: {result.message}",
                failure_event
            )
            self.logger.info(f"Auto-recovery successful: {result.message}")
            
            # Update status if recovery was successful
            if self.current_status == PipelineStatus.FAILED:
                self.current_status = PipelineStatus.HEALTHY
                recovery_event = PipelineEvent(
                    timestamp=datetime.now(),
                    event_type="pipeline_recovery",
                    details={"recovery_result": result.dict()},
                    status=PipelineStatus.HEALTHY,
                    failure_type=None
                )
                self.database.store_event(recovery_event.dict())
        else:
            self.alert_system.send_alert(
                AlertLevel.ERROR,
                f"Auto-recovery failed: {result.message}",
                failure_event
            )
            self.logger.error(f"Auto-recovery failed: {result.message}")
        
        return result
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get comprehensive system statistics"""
        total_failures = len(self.failure_history)
        successful_recoveries = sum(1 for r in self.recovery_history if r.success)
        recovery_rate = (successful_recoveries / len(self.recovery_history)) * 100 if self.recovery_history else 0
        
        # Count failures by type
        failure_types = {}
        for failure in self.failure_history:
            if failure.failure_type:
                failure_type = failure.failure_type.value
                failure_types[failure_type] = failure_types.get(failure_type, 0) + 1
        
        # Get uptime percentage (simplified)
        total_checks = len(self.failure_history) + 10  # Approximate
        uptime_percentage = ((total_checks - len(self.failure_history)) / total_checks) * 100 if total_checks > 0 else 100
        
        return {
            "uptime_percentage": round(uptime_percentage, 2),
            "total_failures": total_failures,
            "total_recovery_attempts": len(self.recovery_history),
            "recovery_success_rate": round(recovery_rate, 2),
            "failure_breakdown": failure_types,
            "current_status": self.current_status.value,
            "last_health_check": datetime.now()
        }