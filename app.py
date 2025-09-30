# from fastapi import FastAPI, HTTPException
# from datetime import datetime
# import uvicorn
# import os
# from dotenv import load_dotenv
# from src.monitor import PipelineMonitor

# # Load environment variables
# load_dotenv()

# app = FastAPI(
#     title="EssentiallySports Pipeline Monitor",
#     description="Monitoring and recovery system for publishing pipeline",
#     version="1.0.0"
# )

# # Initialize monitor
# monitor = PipelineMonitor()

# @app.get("/")
# async def root():
#     return {
#         "message": "EssentiallySports Pipeline Monitor API",
#         "status": "operational",
#         "timestamp": datetime.now()
#     }

# @app.get("/health")
# async def health_check():
#     return {
#         "status": "healthy",
#         "service": "pipeline_monitor",
#         "timestamp": datetime.now(),
#         "version": "1.0.0"
#     }

# @app.get("/pipeline/status")
# async def pipeline_status():
#     """Get current pipeline status and health information"""
#     try:
#         report = monitor.get_status_report()
#         return report
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error checking pipeline status: {str(e)}")

# @app.post("/pipeline/health-check")
# async def force_health_check():
#     """Force an immediate pipeline health check"""
#     try:
#         health_result = monitor.check_pipeline_health()
#         return {
#             "message": "Health check completed",
#             "result": health_result.dict(),
#             "timestamp": datetime.now()
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

# @app.post("/pipeline/trigger-recovery")
# async def trigger_recovery():
#     """Manually trigger recovery process"""
#     try:
#         # Create a simulated failure event for testing recovery
#         from src.models import PipelineEvent, FailureType
#         import random
        
#         failure_types = [FailureType.NETWORK, FailureType.VALIDATION_SERVICE, FailureType.DATABASE]
#         simulated_failure = PipelineEvent(
#             timestamp=datetime.now(),
#             event_type="manual_recovery_trigger",
#             details={"trigger": "manual", "components": "all"},
#             status="failed",
#             failure_type=random.choice(failure_types)
#         )
        
#         result = monitor.trigger_auto_recovery(simulated_failure)
        
#         return {
#             "message": "Recovery process triggered",
#             "recovery_result": result.dict(),
#             "timestamp": datetime.now()
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Recovery trigger failed: {str(e)}")

# if __name__ == "__main__":
#     uvicorn.run(
#         app,
#         host="0.0.0.0",
#         port=8000,
#         reload=True
#     )



from fastapi import FastAPI, HTTPException
from datetime import datetime
import uvicorn
import os
from dotenv import load_dotenv
from src.monitor import PipelineMonitor

# Load environment variables
load_dotenv()

app = FastAPI(
    title="EssentiallySports Pipeline Monitor",
    description="Monitoring and recovery system for publishing pipeline",
    version="1.0.0"
)

# Initialize monitor
monitor = PipelineMonitor()

@app.get("/")
async def root():
    return {
        "message": "EssentiallySports Pipeline Monitor API",
        "status": "operational",
        "timestamp": datetime.now()
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "pipeline_monitor",
        "timestamp": datetime.now(),
        "version": "1.0.0"
    }

@app.get("/pipeline/status")
async def pipeline_status():
    """Get current pipeline status and health information"""
    try:
        report = monitor.get_status_report()
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking pipeline status: {str(e)}")

@app.post("/pipeline/health-check")
async def force_health_check():
    """Force an immediate pipeline health check"""
    try:
        health_result = monitor.check_pipeline_health()
        return {
            "message": "Health check completed",
            "result": health_result.dict(),
            "timestamp": datetime.now()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@app.post("/pipeline/trigger-recovery")
async def trigger_recovery():
    """Manually trigger recovery process"""
    try:
        # Create a simulated failure event for testing recovery
        from src.models import PipelineEvent, FailureType
        import random
        
        failure_types = [FailureType.NETWORK, FailureType.VALIDATION_SERVICE, FailureType.DATABASE]
        simulated_failure = PipelineEvent(
            timestamp=datetime.now(),
            event_type="manual_recovery_trigger",
            details={"trigger": "manual", "components": "all"},
            status="failed",
            failure_type=random.choice(failure_types)
        )
        
        result = monitor.trigger_auto_recovery(simulated_failure)
        
        return {
            "message": "Recovery process triggered",
            "recovery_result": result.dict(),
            "timestamp": datetime.now()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recovery trigger failed: {str(e)}")

# NEW ENDPOINTS ADDED BELOW

@app.get("/pipeline/history")
async def get_pipeline_history(limit: int = 10):
    """Get recent pipeline events from database"""
    try:
        events = monitor.database.get_recent_events(limit)
        recoveries = monitor.database.get_recovery_attempts(limit)
        return {
            "events": events,
            "recovery_attempts": recoveries,
            "event_count": len(events),
            "recovery_count": len(recoveries),
            "timestamp": datetime.now()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching history: {str(e)}")

@app.get("/pipeline/analytics")
async def get_analytics():
    """Get pipeline analytics and statistics"""
    try:
        stats = monitor.get_system_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating analytics: {str(e)}")

@app.get("/pipeline/components")
async def get_components_status():
    """Get detailed status of all pipeline components"""
    try:
        health_result = monitor.check_pipeline_health()
        components_status = {}
        
        for component, data in health_result.components.items():
            components_status[component] = {
                "healthy": data.get('healthy', False),
                "status": "operational" if data.get('healthy', False) else "degraded",
                "metrics": {k: v for k, v in data.items() if k != 'healthy'},
                "last_checked": health_result.timestamp
            }
        
        return {
            "components": components_status,
            "overall_status": health_result.status.value,
            "timestamp": datetime.now()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching component status: {str(e)}")

@app.get("/pipeline/failures")
async def get_failure_history(limit: int = 20):
    """Get recent pipeline failures"""
    try:
        all_events = monitor.database.get_recent_events(limit * 2)  # Get more events to filter
        failures = [event for event in all_events if event['status'] == 'failed'][:limit]
        
        failure_summary = {}
        for failure in failures:
            failure_type = failure.get('failure_type', 'unknown')
            failure_summary[failure_type] = failure_summary.get(failure_type, 0) + 1
        
        return {
            "failures": failures,
            "failure_count": len(failures),
            "failure_summary": failure_summary,
            "timestamp": datetime.now()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching failure history: {str(e)}")

@app.post("/pipeline/reset-stats")
async def reset_statistics():
    """Reset pipeline statistics (for testing purposes)"""
    try:
        # Note: This only resets in-memory stats, not the database
        monitor.failure_history.clear()
        monitor.recovery_history.clear()
        monitor.current_status = "healthy"
        
        return {
            "message": "Pipeline statistics reset successfully",
            "timestamp": datetime.now()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resetting statistics: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )