# import logging
# import smtplib
# from email.mime.text import MimeText
# from typing import List
# from .models import AlertLevel, PipelineEvent, FailureType

# class AlertSystem:
#     def __init__(self, config: dict):
#         self.config = config
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
    
#     def send_alert(self, level: AlertLevel, message: str, event: PipelineEvent):
#         log_message = f"[{level.upper()}] {message} | Failure: {event.failure_type} | Details: {event.details}"
        
#         if level == AlertLevel.INFO:
#             self.logger.info(log_message)
#         elif level == AlertLevel.WARNING:
#             self.logger.warning(log_message)
#         elif level == AlertLevel.ERROR:
#             self.logger.error(log_message)
#         elif level == AlertLevel.CRITICAL:
#             self.logger.critical(log_message)
        
#         # Send email for critical alerts
#         if level in [AlertLevel.CRITICAL, AlertLevel.ERROR]:
#             self._send_email_alert(level, message, event)
    
#     def _send_email_alert(self, level: AlertLevel, message: str, event: PipelineEvent):
#         # This is a simplified email sender - in production, use proper email service
#         try:
#             if self.config.get('email_enabled', False):
#                 # Implementation for email sending would go here
#                 self.logger.info(f"Email alert prepared for {level}: {message}")
#         except Exception as e:
#             self.logger.error(f"Failed to send email alert: {e}")



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