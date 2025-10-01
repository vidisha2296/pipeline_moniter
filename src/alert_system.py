import logging
from typing import Optional
from .models import AlertLevel, PipelineEvent

class AlertSystem:
    def __init__(self, config: dict):
        self.config = config
        self.logger = logging.getLogger("PipelineMonitor")
    
    def send_alert(self, level: AlertLevel, message: str, event: PipelineEvent):
        log_message = f"[{level.upper()}] {message} | Failure: {event.failure_type} | Component: {event.component}"
        
        if level == AlertLevel.INFO:
            self.logger.info(log_message)
        elif level == AlertLevel.WARNING:
            self.logger.warning(log_message)
        elif level == AlertLevel.ERROR:
            self.logger.error(log_message)
        elif level == AlertLevel.CRITICAL:
            self.logger.critical(log_message)