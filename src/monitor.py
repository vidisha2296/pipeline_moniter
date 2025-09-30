# import time
# from datetime import datetime
# from typing import Dict, List, Optional
# from .models import PipelineStatus, FailureType, PipelineEvent, AlertLevel, RecoveryResult
# from .alert_system import AlertSystem
# from .recovery_engine import RecoveryEngine

# class PipelineMonitor:
#     def __init__(self, config: dict = None):
#         self.config = config or {}
#         self.alert_system = AlertSystem(self.config)
#         self.recovery_engine = RecoveryEngine(self.alert_system)
#         self.current_status = PipelineStatus.HEALTHY
#         self.failure_history: List[PipelineEvent] = []
#         self.recovery_history: List[RecoveryResult] = []
#         self.health_checks = {
#             'network': self._check_network_health,
#             'validation_service': self._check_validation_service_health,
#             'database': self._check_database_health
#         }
    
#     def check_pipeline_health(self) -> Dict:
#         """Perform comprehensive health check of publishing pipeline"""
#         health_results = {}
#         overall_healthy = True
#         detected_failure = None
        
#         for component, check_method in self.health_checks.items():
#             try:
#                 is_healthy, details = check_method()
#                 health_results[component] = {
#                     'healthy': is_healthy,
#                     'details': details
#                 }
                
#                 if not is_healthy:
#                     overall_healthy = False
#                     detected_failure = self._determine_failure_type(component, details)
                    
#             except Exception as e:
#                 health_results[component] = {
#                     'healthy': False,
#                     'details': f"Health check failed: {str(e)}"
#                 }
#                 overall_healthy = False
#                 detected_failure = FailureType.UNKNOWN
        
#         previous_status = self.current_status
#         self.current_status = PipelineStatus.HEALTHY if overall_healthy else PipelineStatus.FAILED
        
#         # Log failure if status changed to failed
#         if self.current_status == PipelineStatus.FAILED and previous_status != PipelineStatus.FAILED:
#             failure_event = self._log_failure(detected_failure, health_results)
#             self.trigger_auto_recovery(failure_event)
        
#         # Log recovery if status improved
#         if self.current_status == PipelineStatus.HEALTHY and previous_status == PipelineStatus.FAILED:
#             self._log_recovery()
        
#         return {
#             'status': self.current_status,
#             'timestamp': datetime.now(),
#             'components': health_results,
#             'failure_type': detected_failure
#         }
    
#     def _check_network_health(self) -> tuple:
#         """Check network connectivity"""
#         # Simulate network check - in real implementation, this would ping endpoints
#         import random
#         is_healthy = random.random() > 0.3  # 70% chance of being healthy
#         details = "Network connectivity normal" if is_healthy else "Network timeout or connection refused"
#         return is_healthy, details
    
#     def _check_validation_service_health(self) -> tuple:
#         """Check validation service status"""
#         import random
#         is_healthy = random.random() > 0.2  # 80% chance of being healthy
#         details = "Validation service responsive" if is_healthy else "Validation service unresponsive or crashing"
#         return is_healthy, details
    
#     def _check_database_health(self) -> tuple:
#         """Check database connectivity"""
#         import random
#         is_healthy = random.random() > 0.25  # 75% chance of being healthy
#         details = "Database connection stable" if is_healthy else "Database connection failed or slow queries"
#         return is_healthy, details
    
#     def _determine_failure_type(self, failed_component: str, details: str) -> FailureType:
#         """Map failed component to specific failure type"""
#         failure_map = {
#             'network': FailureType.NETWORK,
#             'validation_service': FailureType.VALIDATION_SERVICE,
#             'database': FailureType.DATABASE
#         }
#         return failure_map.get(failed_component, FailureType.UNKNOWN)
    
#     def _log_failure(self, failure_type: FailureType, health_results: Dict) -> PipelineEvent:
#         """Log pipeline failure event"""
#         event = PipelineEvent(
#             timestamp=datetime.now(),
#             event_type="pipeline_failure",
#             details=health_results,
#             status=PipelineStatus.FAILED,
#             failure_type=failure_type
#         )
        
#         self.failure_history.append(event)
        
#         self.alert_system.send_alert(
#             AlertLevel.CRITICAL,
#             f"Publishing pipeline failure detected: {failure_type.value}",
#             event
#         )
        
#         return event
    
#     def _log_recovery(self):
#         """Log pipeline recovery"""
#         event = PipelineEvent(
#             timestamp=datetime.now(),
#             event_type="pipeline_recovery",
#             details={"message": "Pipeline restored to healthy state"},
#             status=PipelineStatus.HEALTHY,
#             failure_type=None
#         )
        
#         self.alert_system.send_alert(
#             AlertLevel.INFO,
#             "Publishing pipeline has recovered",
#             event
#         )
    
#     def trigger_auto_recovery(self, failure_event: PipelineEvent) -> RecoveryResult:
#         """Attempt automatic recovery based on failure type"""
#         if not failure_event.failure_type:
#             return RecoveryResult(
#                 success=False,
#                 message="Cannot attempt recovery: Unknown failure type",
#                 action_taken="None",
#                 timestamp=datetime.now()
#             )
        
#         self.alert_system.send_alert(
#             AlertLevel.WARNING,
#             f"Attempting auto-recovery for {failure_event.failure_type.value}",
#             failure_event
#         )
        
#         result = self.recovery_engine.attempt_recovery(
#             failure_event.failure_type, 
#             failure_event
#         )
        
#         self.recovery_history.append(result)
        
#         if result.success:
#             self.alert_system.send_alert(
#                 AlertLevel.INFO,
#                 f"Auto-recovery successful: {result.message}",
#                 failure_event
#             )
#         else:
#             self.alert_system.send_alert(
#                 AlertLevel.ERROR,
#                 f"Auto-recovery failed: {result.message}",
#                 failure_event
#             )
        
#         return result
    
#     def get_status_report(self) -> Dict:
#         """Generate comprehensive status report for API endpoint"""
#         latest_health = self.check_pipeline_health()
        
#         return {
#             'current_status': self.current_status,
#             'last_checked': datetime.now(),
#             'health_check_results': latest_health,
#             'recent_failures': self.failure_history[-5:],  # Last 5 failures
#             'recent_recoveries': self.recovery_history[-5:],  # Last 5 recovery attempts
#             'suggested_action': self._get_suggested_action()
#         }
    
#     def _get_suggested_action(self) -> str:
#         """Provide editor-facing recovery suggestions"""
#         if self.current_status == PipelineStatus.HEALTHY:
#             return "No action needed - pipeline is healthy"
        
#         latest_failure = self.failure_history[-1] if self.failure_history else None
#         latest_recovery = self.recovery_history[-1] if self.recovery_history else None
        
#         if not latest_failure:
#             return "Investigate pipeline components manually"
        
#         if latest_recovery and latest_recovery.success:
#             return "Recovery completed - monitor pipeline stability"
        
#         # Failure-specific suggestions
#         suggestions = {
#             FailureType.NETWORK: "Check network connectivity, VPN, and firewall settings. Contact IT if issues persist.",
#             FailureType.VALIDATION_SERVICE: "Restart validation service manually. Clear cache if necessary. Contact engineering if service won't start.",
#             FailureType.DATABASE: "Check database connection string and credentials. Verify database server status. Contact DBA if needed.",
#             FailureType.UNKNOWN: "Manual investigation required. Check all pipeline components and review logs for unusual activity."
#         }
        
#         base_suggestion = suggestions.get(latest_failure.failure_type, suggestions[FailureType.UNKNOWN])
        
#         if latest_recovery and not latest_recovery.success:
#             return f"Auto-recovery failed. {base_suggestion} Engineering team has been notified."
        
#         return f"Auto-recovery in progress. If not resolved soon: {base_suggestion}"



# import logging
# import time
# from datetime import datetime
# from typing import Dict, List, Optional, Any
# import random
# from .models import PipelineStatus, FailureType, PipelineEvent, AlertLevel, RecoveryResult, HealthCheckResponse
# from .alert_system import AlertSystem
# from .recovery_engine import RecoveryEngine

# class PipelineMonitor:
#     def __init__(self, config: dict = None):
#         self.config = config or {}
#         self.alert_system = AlertSystem(self.config)
#         self.recovery_engine = RecoveryEngine(self.alert_system)
#         self.current_status = PipelineStatus.HEALTHY
#         self.failure_history: List[PipelineEvent] = []
#         self.recovery_history: List[RecoveryResult] = []
#         self.setup_logging()
    
#     def setup_logging(self):
#         logging.basicConfig(
#             level=logging.INFO,
#             format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#             handlers=[
#                 logging.FileHandler('pipeline_audit.log'),
#                 logging.StreamHandler()
#             ]
#         )
#         self.logger = logging.getLogger("PipelineMonitor")
    
#     def check_pipeline_health(self) -> HealthCheckResponse:
#         """Perform comprehensive health check of publishing pipeline"""
#         self.logger.info("Performing pipeline health check")
        
#         # Simulate health checks
#         components = {
#             'network': {'healthy': True, 'response_time': '45ms', 'details': 'Network connectivity normal'},
#             'validation_service': {'healthy': True, 'version': '2.1.0', 'details': 'Validation service responsive'},
#             'database': {'healthy': True, 'connections': 5, 'details': 'Database connection stable'}
#         }
        
#         # Simulate occasional failures for testing (30% chance)
#         failure_type = None
#         if random.random() < 0.3:
#             failed_component = random.choice(['network', 'validation_service', 'database'])
#             components[failed_component]['healthy'] = False
#             components[failed_component]['error'] = f"{failed_component} failure simulated"
            
#             failure_type = self._determine_failure_type(failed_component)
#             status = PipelineStatus.FAILED
            
#             # Log the failure
#             failure_event = PipelineEvent(
#                 timestamp=datetime.now(),
#                 event_type="pipeline_failure",
#                 details=components,
#                 status=status,
#                 failure_type=failure_type,
#                 component=failed_component
#             )
#             self.failure_history.append(failure_event)
            
#             # Send alert
#             self.alert_system.send_alert(
#                 AlertLevel.ERROR,
#                 f"Pipeline failure detected in {failed_component}",
#                 failure_event
#             )
            
#             self.logger.error(f"Pipeline failure detected: {failed_component}")
#         else:
#             status = PipelineStatus.HEALTHY
#             self.logger.info("Pipeline health check passed")
        
#         return HealthCheckResponse(
#             status=status,
#             timestamp=datetime.now(),
#             components=components,
#             failure_type=failure_type
#         )
    
#     def _determine_failure_type(self, failed_component: str) -> FailureType:
#         """Map failed component to specific failure type"""
#         failure_map = {
#             'network': FailureType.NETWORK,
#             'validation_service': FailureType.VALIDATION_SERVICE,
#             'database': FailureType.DATABASE
#         }
#         return failure_map.get(failed_component, FailureType.UNKNOWN)
    
#     def get_status_report(self) -> Dict[str, Any]:
#         """Generate comprehensive status report for API endpoint"""
#         health_result = self.check_pipeline_health()
        
#         return {
#             'current_status': health_result.status,
#             'last_checked': health_result.timestamp,
#             'health_check_results': health_result.dict(),
#             'recent_failures': [event.dict() for event in self.failure_history[-5:]],
#             'recent_recoveries': [result.dict() for result in self.recovery_history[-5:]],
#             'suggested_action': self._get_suggested_action(health_result)
#         }
    
#     def _get_suggested_action(self, health_result: HealthCheckResponse) -> str:
#         """Provide editor-facing recovery suggestions"""
#         if health_result.status == PipelineStatus.HEALTHY:
#             return "No action needed - pipeline is healthy"
        
#         if health_result.failure_type == FailureType.NETWORK:
#             return "Check network connectivity, VPN, and firewall settings. Contact IT if issues persist."
#         elif health_result.failure_type == FailureType.VALIDATION_SERVICE:
#             return "Restart validation service manually. Clear cache if necessary. Contact engineering if service won't start."
#         elif health_result.failure_type == FailureType.DATABASE:
#             return "Check database connection string and credentials. Verify database server status. Contact DBA if needed."
#         else:
#             return "Manual investigation required. Check all pipeline components and review logs for unusual activity."
    
#     def trigger_auto_recovery(self, failure_event: PipelineEvent) -> RecoveryResult:
#         """Attempt automatic recovery based on failure type"""
#         self.alert_system.send_alert(
#             AlertLevel.WARNING,
#             f"Attempting auto-recovery for {failure_event.failure_type}",
#             failure_event
#         )
        
#         result = self.recovery_engine.attempt_recovery(failure_event.failure_type, failure_event)
#         self.recovery_history.append(result)
        
#         if result.success:
#             self.alert_system.send_alert(
#                 AlertLevel.INFO,
#                 f"Auto-recovery successful: {result.message}",
#                 failure_event
#             )
#             self.logger.info(f"Auto-recovery successful: {result.message}")
#         else:
#             self.alert_system.send_alert(
#                 AlertLevel.ERROR,
#                 f"Auto-recovery failed: {result.message}",
#                 failure_event
#             )
#             self.logger.error(f"Auto-recovery failed: {result.message}")
        
#         return result


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